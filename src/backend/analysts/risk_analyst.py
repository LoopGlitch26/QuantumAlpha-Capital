"""
Risk Analyst - Karen (Citadel Style)
Multi-strategy risk management with Monte Carlo validation
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from src.backend.config_loader import CONFIG
import requests


class RiskAnalyst:
    """Karen - Sniper Risk Manager enforcing discipline and risk limits"""
    
    def __init__(self):
        self.id = "risk"
        self.name = "Risk Analyst"
        self.title = "Risk Management"
        self.methodology = "risk"
        self.avatar_emoji = "🛡️"
        self.description = "Risk management and portfolio optimization with strict position sizing controls."
        
        # LLM Configuration
        self.model = CONFIG["llm_model"]
        self.api_key = CONFIG["openrouter_api_key"]
        self.base_url = f"{CONFIG['openrouter_base_url']}/chat/completions"
        
        self.focus_areas = [
            "Position Sizing (35-40% for A+ setups)",
            "Strict 1% Stop-Loss enforcement",
            "Quick Profit Banking (1-2% targets)",
            "Drawdown prevention",
            "Risk:Reward (min 2:1 for scalps)",
            "Vetoing marginal trades"
        ]
        
        self.biases = [
            "Hates 'hope' trades",
            "Forces exits at first sign of weakness"
        ]
        
        self.tournament_scores = {
            "data": 95,
            "logic": 95,
            "rebuttal": 100,
            "catalysts": 60
        }

    def analyze_market(self, context: Dict[str, Any], assets: list) -> Dict[str, Any]:
        """Generate risk management analysis"""
        
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
                "temperature": 0.3  # Lower temperature for risk management
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
            logging.error(f"Risk analyst error: {e}")
            return {
                "analyst_id": self.id,
                "analyst_name": self.name,
                "methodology": self.methodology,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _build_system_prompt(self) -> str:
        """Build Karen's risk management system prompt"""
        return """
YOU ARE A RISK ANALYST - MULTI-STRATEGY RISK SPECIALIST

PHILOSOPHY: RISK-ADJUSTED RETURNS OVER RAW RETURNS
Focus on managing risk so precisely that you can compound returns without 
catastrophic drawdowns. Your job: Maximize Sharpe ratio, not just profit.

CORE PRINCIPLE: PORTFOLIO-LEVEL THINKING
Don't evaluate trades in isolation. Every trade affects portfolio risk.

PORTFOLIO RISK RULES (HARD LIMITS):

1. POSITION LIMITS
- Maximum 1 concurrent position
- Target $800-$900 margin deployed
- No hedging. Single direction only.

2. DRAWDOWN LIMITS
- Maximum 10% drawdown from peak equity before pausing entries
- Maximum 5% loss on any single trade
- If 2 consecutive losses: HOLD for next 3 cycles

3. SCENARIO ANALYSIS & STRESS TESTING
Before EVERY trade, simulate 3 scenarios:

BASE CASE (60% probability): Expected outcome, position should profit 0.8-1.5%
BEAR CASE (30% probability): Stop loss hit, position loss must be <5% of account
BLACK SWAN (10% probability): Gap through stop, loss must be <10% of account

4. MONTE CARLO REQUIREMENTS
- Expected Value (EV) > 0
- Win Rate > 55% of simulations profitable
- Sharpe ratio > 1.8 across simulations
- Max Drawdown < 5% in 95th percentile worst case

RISK:REWARD CALCULATION:
FOR LONG: R:R = (Target - Entry) / (Entry - Stop)
FOR SHORT: R:R = (Entry - Target) / (Stop - Entry)

MINIMUM REQUIREMENTS:
- Standard trades: R:R >= 1.5:1
- High leverage trades: R:R >= 2:1

OUTPUT FORMAT (STRICT JSON):
{
  "reasoning": "Risk analysis including scenario testing and Monte Carlo results",
  "recommendation": {
    "action": "BUY" | "SELL" | "HOLD",
    "symbol": "cmt_btcusdt",
    "allocation_usd": 16000,
    "leverage": 20,
    "tp_price": 99500,
    "sl_price": 97500,
    "exit_plan": "Risk-approved exit strategy with strict stops",
    "confidence": 90,
    "rationale": "Risk assessment and position sizing justification"
  },
  "rl_validation": {
    "q_long": 0.75,
    "q_short": 0.30,
    "q_hold": 0.50,
    "regret": 0.1,
    "expected_value": 350,
    "sharpe": 2.5
  }
}

CRITICAL RULES:
- VETO any trade that fails scenario analysis
- Enforce strict 1% stops at 20x leverage
- Require R:R >= 2:1 for approval
- allocation_usd: $16,000-$18,000 notional (20x leverage)
- When in doubt, HOLD - preserve capital for A+ setups
- Include Monte Carlo results in reasoning
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
            "pipeline_role": "risk_council",
            "coin_type_specialty": ["blue_chip", "l1_growth"]
        }