"""
Market Scanner - Multi-Analyst Orchestrator
Coordinates all analysts and implements debate/judge system
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from src.backend.config_loader import CONFIG
from .technical_analyst import TechnicalAnalyst
from .ml_analyst import MLAnalyst
from .risk_analyst import RiskAnalyst
from .quant_analyst import QuantAnalyst
import requests


class MarketScanner:
    """Orchestrates multi-analyst system with debate and judge mechanisms"""
    
    def __init__(self):
        self.analysts = {
            "technical": TechnicalAnalyst(),
            "ml": MLAnalyst(),
            "risk": RiskAnalyst(),
            "quant": QuantAnalyst()
        }
        
        # Judge configuration
        self.model = CONFIG["llm_model"]
        self.api_key = CONFIG["openrouter_api_key"]
        self.base_url = f"{CONFIG['openrouter_base_url']}/chat/completions"
        
        self.logger = logging.getLogger(__name__)

    async def analyze_market(self, context: Dict[str, Any], assets: list) -> Dict[str, Any]:
        """Run full multi-analyst analysis with judge decision"""
        
        try:
            # Step 1: Get all analyst recommendations
            analyst_results = {}
            
            for analyst_id, analyst in self.analysts.items():
                try:
                    result = analyst.analyze_market(context, assets)
                    analyst_results[analyst_id] = result
                    self.logger.info(f"Analyst {analyst_id} completed analysis")
                except Exception as e:
                    self.logger.error(f"Analyst {analyst_id} failed: {e}")
                    analyst_results[analyst_id] = {
                        "analyst_id": analyst_id,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Step 2: Run judge evaluation
            judge_decision = await self._run_judge(context, analyst_results)
            
            # Step 3: Compile final result
            return {
                "timestamp": datetime.now().isoformat(),
                "context_summary": {
                    "assets": assets,
                    "account_balance": context.get("account", {}).get("balance", 0),
                    "active_positions": len(context.get("account", {}).get("positions", []))
                },
                "analyst_results": analyst_results,
                "judge_decision": judge_decision,
                "final_recommendation": judge_decision.get("final_recommendation"),
                "warnings": judge_decision.get("warnings", [])
            }
            
        except Exception as e:
            self.logger.error(f"Market scanner error: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "analyst_results": analyst_results if 'analyst_results' in locals() else {},
                "judge_decision": None,
                "final_recommendation": None
            }

    async def _run_judge(self, context: Dict[str, Any], analyst_results: Dict[str, Any]) -> Dict[str, Any]:
        """Run AI judge to evaluate analyst recommendations"""
        
        system_prompt = self._build_judge_prompt()
        
        # Build user message with context and analyst outputs
        user_message = self._build_judge_user_message(context, analyst_results)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.3  # Lower temperature for judge decisions
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            try:
                judge_decision = json.loads(content)
                return judge_decision
            except json.JSONDecodeError:
                return {
                    "winner": "NONE",
                    "reasoning": "Judge response parsing failed",
                    "final_action": "HOLD",
                    "final_recommendation": None,
                    "warnings": ["Judge parsing error"],
                    "raw_content": content
                }
                
        except Exception as e:
            self.logger.error(f"Judge evaluation error: {e}")
            return {
                "winner": "NONE",
                "reasoning": f"Judge evaluation failed: {str(e)}",
                "final_action": "HOLD",
                "final_recommendation": None,
                "warnings": [f"Judge error: {str(e)}"]
            }

    def _build_judge_prompt(self) -> str:
        """Build judge system prompt"""
        return """
You are the JUDGE in a TRADING COMPETITION.

COMPETITION CONTEXT (CONVICTION TRADING v5.6.0)
- 4 AI analysts competing for best recommendation
- Limited time window to maximize profit
- Winners used strict TP/SL, 20x leverage, and quick scalps

WHAT WINNERS DID:
- SNIPER MODE: Big positions, tight stops, quick profits
- BIG MARGIN: ~80-90% of account per trade (~$800 margin)
- HIGH leverage: 20x FIXED
- QUICK SCALPS: Take 0.8-1.5% price movement profit (16-30% ROE)
- TIGHT STOPS: 1% max SL
- FOCUSED: BTC/USDT only
- NO HEDGING: Directional bets only

YOUR JOB: SNIPER EXECUTION — BIG SIZE, QUICK WINS

You will receive recommendations from 4 analysts:
1. TECHNICAL ANALYST - Price action, indicators, chart patterns
2. ML ANALYST - Machine learning and AI-based analysis
3. RISK ANALYST - Risk management and portfolio optimization
4. QUANT ANALYST - Statistical models and market microstructure

DECISION FRAMEWORK:

STEP 1: IDENTIFY MARKET PHASE
- STRONG TREND: EMA9 > EMA20 > EMA50 (or vice versa)
- TREND EXHAUSTION: RSI divergence, funding extreme
- REVERSAL: EMA cross confirmed, RSI crossing 50
- RANGING/CHOPPY: EMAs tangled, no clear direction

STEP 2: PICK THE BEST RECOMMENDATION
- BTC/USDT only. Ignore all other assets.
- In TREND phase: Pick trades aligned with trend
- In EXHAUSTION phase: Prefer HOLD unless clear reversal
- In REVERSAL phase: Pick trades in NEW direction
- In RANGING phase: Pick HOLD or very small positions

STEP 3: POSITION MANAGEMENT
- Position size: $16,000-$18,000 notional at 20x
- Leverage: 20x FIXED
- Stop loss: 1% from entry (Tight!)
- Take profit: 0.8-1.5% price move (16-30% ROE)

OUTPUT FORMAT (STRICT JSON):
{
  "winner": "technical" | "ml" | "risk" | "quant" | "NONE",
  "reasoning": "Concise explanation (max 2 sentences)",
  "adjustments": null,
  "warnings": [],
  "final_action": "BUY" | "SELL" | "HOLD",
  "final_recommendation": {
    "action": "BUY" | "SELL",
    "symbol": "cmt_btcusdt",
    "allocation_usd": 16000,
    "leverage": 20,
    "tp_price": 99500,
    "sl_price": 97500,
    "exit_plan": "Sniper scalp: Take profit at 0.8-1.5% price move.",
    "confidence": 85
  }
}

CRITICAL RULES:
- If winner="NONE", then final_action MUST be "HOLD"
- If final_action="HOLD", then final_recommendation MUST be null
- If final_action is BUY/SELL, final_recommendation MUST be present
- Ensure all numeric fields are actual numbers, not strings
"""

    def _build_judge_user_message(self, context: Dict[str, Any], analyst_results: Dict[str, Any]) -> str:
        """Build judge user message with context and analyst outputs"""
        
        # Extract analyst outputs
        technical_output = self._extract_analyst_output(analyst_results.get("technical"))
        ml_output = self._extract_analyst_output(analyst_results.get("ml"))
        risk_output = self._extract_analyst_output(analyst_results.get("risk"))
        quant_output = self._extract_analyst_output(analyst_results.get("quant"))
        
        # Count valid analysts
        valid_outputs = [technical_output, ml_output, risk_output, quant_output]
        valid_count = sum(1 for output in valid_outputs if output and output != "FAILED")
        failed_count = 4 - valid_count
        
        return f"""=== MARKET CONTEXT ===
CONTEXT INCLUDES:
- account: Balance, positions, active trades
- market_data[]: Technical indicators (EMA, RSI, MACD, ATR, funding)
- sentiment: Fear & Greed, news sentiment, contrarian signals

=== ANALYST RECOMMENDATIONS ===
({valid_count} analysts responded, {failed_count} failed)

--- TECHNICAL ANALYST (Statistical Arbitrage + RL Validation) ---
{technical_output or 'FAILED'}

--- ML ANALYST (AI/ML Signals + Derivatives) ---
{ml_output or 'FAILED'}

--- RISK ANALYST (Multi-Strategy Risk + Monte Carlo) ---
{risk_output or 'FAILED'}

--- QUANT ANALYST (Liquidity & Arbitrage) ---
{quant_output or 'FAILED'}

=== YOUR TASK ===
Evaluate each analyst's recommendation for QUALITY, not just existence.
- Check rl_validation object for Q-values and regret calculations
- Pick the BEST trade if it has good risk/reward (confidence >= 70%, clear TP/SL)
- Use HIGH LEVERAGE (20x FIXED) for good setups - this is a competition!
- No long bias. If BTC trend is down, prefer shorts
- Output winner="NONE" if no entry trade meets quality threshold
- HOLD is a valid decision - don't force bad trades

MARKET DATA (CONTEXT JSON):
{json.dumps(context, indent=2)}

Output valid JSON only."""

    def _extract_analyst_output(self, analyst_result: Optional[Dict[str, Any]]) -> Optional[str]:
        """Extract analyst output for judge evaluation"""
        if not analyst_result:
            return None
            
        if "error" in analyst_result:
            return "FAILED"
            
        if "analysis" in analyst_result:
            return json.dumps(analyst_result["analysis"], indent=2)
            
        return None

    def get_analyst_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Get all analyst profiles"""
        return {
            analyst_id: analyst.get_profile() 
            for analyst_id, analyst in self.analysts.items()
        }