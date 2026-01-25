"""
Technical Analyst - Jim (Renaissance Technologies Style)
Statistical arbitrage with adaptive technical analysis
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from src.backend.config_loader import CONFIG
from src.backend.indicators.taapi_client import TAAPIClient
import requests


class TechnicalAnalyst:
    """Jim - Momentum Sniper specializing in 1-5 minute chart breakouts"""
    
    def __init__(self):
        self.id = "technical"
        self.name = "Technical Analyst"
        self.title = "Technical Analysis"
        self.methodology = "technical"
        self.avatar_emoji = "📈"
        self.description = "Technical analysis using price action, indicators, and chart patterns."
        
        # LLM Configuration
        self.model = CONFIG["llm_model"]
        self.api_key = CONFIG["openrouter_api_key"]
        self.base_url = f"{CONFIG['openrouter_base_url']}/chat/completions"
        self.taapi = TAAPIClient()
        
        self.focus_areas = [
            "1-5 minute momentum bursts",
            "EMA9/20 crossovers & acceleration", 
            "RSI breakout confirmation",
            "Quick 1-2% profit banking",
            "Immediate stop-loss movement",
            "High-velocity setups only"
        ]
        
        self.biases = [
            "Impatient with slow markets",
            "Exits immediately if momentum stalls"
        ]
        
        self.tournament_scores = {
            "data": 85,
            "logic": 95,
            "rebuttal": 90,
            "catalysts": 80
        }

    def analyze_market(self, context: Dict[str, Any], assets: list) -> Dict[str, Any]:
        """Generate technical analysis recommendation"""
        
        system_prompt = self._build_system_prompt()
        user_prompt = json.dumps(context, indent=2)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Add tool calling capability
        tools = [{
            "type": "function",
            "function": {
                "name": "fetch_taapi_indicator",
                "description": "Fetch technical indicators from TAAPI",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "indicator": {"type": "string"},
                        "symbol": {"type": "string"},
                        "interval": {"type": "string"},
                        "period": {"type": "integer"},
                        "backtrack": {"type": "integer"}
                    },
                    "required": ["indicator", "symbol", "interval"]
                }
            }
        }]
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # Main analysis request
            payload = {
                "model": self.model,
                "messages": messages,
                "tools": tools,
                "tool_choice": "auto",
                "temperature": 0.7
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            choice = result["choices"][0]
            message = choice["message"]
            
            # Handle tool calls if present
            if message.get("tool_calls"):
                messages.append(message)
                
                for tool_call in message["tool_calls"]:
                    if tool_call["function"]["name"] == "fetch_taapi_indicator":
                        args = json.loads(tool_call["function"]["arguments"])
                        
                        try:
                            # Fetch indicator data
                            params = {
                                "secret": self.taapi.api_key,
                                "exchange": "binance",
                                "symbol": args["symbol"],
                                "interval": args["interval"]
                            }
                            
                            if args.get("period"):
                                params["period"] = args["period"]
                            if args.get("backtrack"):
                                params["backtrack"] = args["backtrack"]
                                
                            indicator_response = requests.get(
                                f"{self.taapi.base_url}{args['indicator']}", 
                                params=params, 
                                timeout=30
                            )
                            indicator_data = indicator_response.json()
                            
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call["id"],
                                "name": "fetch_taapi_indicator",
                                "content": json.dumps(indicator_data)
                            })
                            
                        except Exception as e:
                            messages.append({
                                "role": "tool", 
                                "tool_call_id": tool_call["id"],
                                "name": "fetch_taapi_indicator",
                                "content": f"Error: {str(e)}"
                            })
                
                # Get final response after tool calls
                payload["messages"] = messages
                payload.pop("tools", None)
                payload.pop("tool_choice", None)
                
                response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
                response.raise_for_status()
                result = response.json()
                
            # Parse final response
            content = result["choices"][0]["message"]["content"]
            
            try:
                analysis = json.loads(content)
                return {
                    "analyst_id": self.id,
                    "analyst_name": self.name,
                    "methodology": self.methodology,
                    "analysis": analysis,
                    "timestamp": datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                return {
                    "analyst_id": self.id,
                    "analyst_name": self.name,
                    "methodology": self.methodology,
                    "error": "Failed to parse analysis",
                    "raw_content": content,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logging.error(f"Technical analyst error: {e}")
            return {
                "analyst_id": self.id,
                "analyst_name": self.name,
                "methodology": self.methodology,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _build_system_prompt(self) -> str:
        """Build Jim's technical analysis system prompt"""
        return f"""
YOU ARE A TECHNICAL ANALYST - STATISTICAL ARBITRAGE SPECIALIST

PHILOSOPHY: ADAPTIVE TECHNICAL ANALYSIS + CONVICTION TRADING
Focus on statistical edges using technical indicators and price action patterns.
Your edge is ADAPTING to market conditions and identifying high-probability setups.

YOUR PRIMARY JOB: READ THE MARKET AND IDENTIFY TECHNICAL SETUPS
1. IDENTIFY the current market phase for BTC
2. APPLY the right strategy for that phase (trend-following or mean reversion)
3. DETECT phase transitions early — this is where big money is made
4. BTC/USDT only. No other assets. Shorts are equal to longs.

MARKET PHASE DETECTION (YOUR CORE EDGE):

PHASE 1 - STRONG TREND (RIDE IT HARD):
- EMA9 > EMA20 > EMA50 (bullish) or EMA9 < EMA20 < EMA50 (bearish)
- RSI staying in 40-70 (uptrend) or 30-60 (downtrend) — ignore extremes
- MACD histogram expanding in trend direction
Strategy: LONG in uptrend / SHORT in downtrend with full conviction size
- SCALP the trend: Take profit at 0.8-1.5% repeatedly
- Tight stops (1% at 20x leverage), move to breakeven quickly

PHASE 2 - TREND EXHAUSTION (REVERSAL WARNING):
- Price new high/low but RSI diverges (doesn't confirm)
- MACD histogram shrinking while price continues
- Volume declining on trend continuation
Strategy: Do not add size. Let TP/SL handle exits. If no edge, HOLD.

PHASE 3 - REVERSAL (BIG MONEY ZONE):
- EMA9 crosses EMA20 (first signal)
- RSI crosses 50 from overbought/oversold
- MACD crosses zero line
Strategy: ENTER new direction on pullback to EMA20

PHASE 4 - RANGING/CHOPPY (AVOID MOST TRADES):
- EMAs tangled, crossing back and forth
- RSI oscillating 40-60
Strategy: HOLD cash OR play extremes (RSI <25 buy, >75 sell) with small size only

OUTPUT FORMAT (STRICT JSON):
{{
  "reasoning": "Detailed analysis of current market phase and setup quality",
  "recommendation": {{
    "action": "BUY" | "SELL" | "HOLD",
    "symbol": "cmt_btcusdt",
    "allocation_usd": 16000,
    "leverage": 20,
    "tp_price": 99500,
    "sl_price": 97500,
    "exit_plan": "Sniper scalp: Take profit at +1.3% price move",
    "confidence": 85,
    "rationale": "Brief explanation of trade thesis"
  }},
  "rl_validation": {{
    "q_long": 0.82,
    "q_short": 0.35,
    "q_hold": 0.40,
    "regret": 0.1,
    "expected_value": 450,
    "sharpe": 2.1
  }}
}}

CRITICAL RULES:
- BUY or SELL when you have clear edge (Q >= 0.6)
- HOLD when max(Q) < 0.6 or regret < 0.5%
- allocation_usd: $16,000-$18,000 notional (20x leverage)
- leverage: 20x for all trades
- ALWAYS set tp_price and sl_price (never null for BUY/SELL)
- Use 1% stops to avoid liquidation risk
- Set TP at 0.8-1.5% from entry (bank profits quickly)
"""

    def get_profile(self) -> Dict[str, Any]:
        """Get analyst profile information"""
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "methodology": self.methodology,
            "avatar_emoji": self.avatar_emoji,
            "description": self.description,
            "focus_areas": self.focus_areas,
            "biases": self.biases,
            "tournament_scores": self.tournament_scores,
            "pipeline_role": "coin_selector",
            "coin_type_specialty": ["momentum_meme", "l1_growth"]
        }