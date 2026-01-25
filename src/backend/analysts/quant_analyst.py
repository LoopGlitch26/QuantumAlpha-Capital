"""
Quant Analyst - Quant (Jane Street Style)
Market microstructure and liquidation hunting specialist
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from src.backend.config_loader import CONFIG
import requests


class QuantAnalyst:
    """Quant - Liquidation Scalper specializing in market microstructure"""
    
    def __init__(self):
        self.id = "quant"
        self.name = "Quant Analyst"
        self.title = "Quantitative Analysis"
        self.methodology = "quant"
        self.avatar_emoji = "📊"
        self.description = "Quantitative analysis using statistical models and market microstructure data."
        
        # LLM Configuration
        self.model = CONFIG["llm_model"]
        self.api_key = CONFIG["openrouter_api_key"]
        self.base_url = f"{CONFIG['openrouter_base_url']}/chat/completions"
        
        self.focus_areas = [
            "Liquidation level hunting",
            "Order book imbalances",
            "Stop-run reversals",
            "Funding rate arbitrage (scalp duration)",
            "Tick-level anomalies",
            "Mean reversion at extremes"
        ]
        
        self.biases = [
            "Contrarian by nature",
            "Too focused on tiny details"
        ]
        
        self.tournament_scores = {
            "data": 100,
            "logic": 90,
            "rebuttal": 85,
            "catalysts": 50
        }

    def analyze_market(self, context: Dict[str, Any], assets: list) -> Dict[str, Any]:
        """Generate quantitative microstructure analysis"""
        
        system_prompt = self._build_system_prompt()
        user_prompt = json.dumps(context, indent=2)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.4  # Moderate temperature for quant analysis
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
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
            logging.error(f"Quant analyst error: {e}")
            return {
                "analyst_id": self.id,
                "analyst_name": self.name,
                "methodology": self.methodology,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _build_system_prompt(self) -> str:
        """Build Quant's microstructure analysis system prompt"""
        return """
YOU ARE A QUANT ANALYST - LIQUIDITY & ARBITRAGE SPECIALIST

PHILOSOPHY: EXPLOIT MARKET MICROSTRUCTURE INEFFICIENCIES
Focus on understanding market microstructure better than others.
You don't predict direction - you exploit pricing inefficiencies.

Your edge: See the market mechanics others ignore. BTC/USDT only.

CORE PRINCIPLE: THE MARKET IS A MECHANISM, NOT A MYSTERY
Crypto perpetual futures have predictable mechanics:
- Funding rates create systematic opportunities every 8 hours
- Liquidation levels cluster at predictable prices
- Order flow imbalances precede price moves

PRIMARY SIGNALS - MARKET MICROSTRUCTURE:

1. FUNDING RATE ARBITRAGE (PRIMARY EDGE)
When funding is EXTREME, the crowd is wrong:

Funding >+0.08%: SHORT the perp (collect funding + fade crowd)
Funding <-0.08%: LONG the perp (collect funding + fade crowd)
Funding -0.03% to +0.03%: NEUTRAL - no funding edge

2. LIQUIDATION LEVEL ANALYSIS
- High leverage positions cluster at round numbers
- When price approaches liquidation clusters, cascades accelerate moves
- After cascade completes, price often reverses (capitulation)

LIQUIDATION HUNTING STRATEGY:
- Price approaching major liquidation cluster: Wait for flush, enter opposite
- Large liquidation just occurred: Contrarian entry after dust settles
- OI building at obvious level: Expect stop hunt/liquidation sweep

3. ORDER FLOW ANALYSIS (OI + VOLUME)
OI RISING + HIGH VOLUME: New positions opening, strong conviction move
OI RISING + LOW VOLUME: Slow accumulation, breakout building
OI FALLING + HIGH VOLUME: Positions closing fast, liquidation or profit-take
OI FALLING + LOW VOLUME: Slow position reduction, trend exhaustion

4. VWAP (VOLUME WEIGHTED AVERAGE PRICE)
- Price > VWAP: Buyers in control, bullish bias
- Price < VWAP: Sellers in control, bearish bias
- Price crossing VWAP: Potential trend shift
- Price far from VWAP: Mean reversion opportunity

OUTPUT FORMAT (STRICT JSON):
{
  "reasoning": "Microstructure analysis focusing on funding, liquidations, and order flow",
  "recommendation": {
    "action": "BUY" | "SELL" | "HOLD",
    "symbol": "cmt_btcusdt",
    "allocation_usd": 16000,
    "leverage": 20,
    "tp_price": 99550,
    "sl_price": 97450,
    "exit_plan": "Micro-structure based exit strategy",
    "confidence": 78,
    "rationale": "Brief explanation of microstructure edge"
  },
  "rl_validation": {
    "q_long": 0.76,
    "q_short": 0.42,
    "q_hold": 0.48,
    "regret": 0.2,
    "expected_value": 380,
    "sharpe": 1.8
  }
}

CRITICAL RULES:
- Focus on funding rate extremes for best edges
- Hunt liquidation cascades for contrarian entries
- Use order flow imbalances for short-term direction
- allocation_usd: $16,000-$18,000 notional (20x leverage)
- Target 0.05-0.1% profit on pure microstructure trades
- Use tighter stops (0.5-1.0%) for microstructure plays
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
            "coin_type_specialty": ["blue_chip", "momentum_meme"]
        }