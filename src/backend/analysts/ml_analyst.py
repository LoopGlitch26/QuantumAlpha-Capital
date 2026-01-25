"""
ML Analyst - Ray (Two Sigma Style)
Volatility expansion specialist using ML and derivatives data
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from src.backend.config_loader import CONFIG
import requests


class MLAnalyst:
    """Ray - Volatility Hunter specializing in derivatives and sentiment analysis"""
    
    def __init__(self):
        self.id = "ml"
        self.name = "ML Analyst"
        self.title = "Machine Learning Analysis"
        self.methodology = "ml"
        self.avatar_emoji = "🤖"
        self.description = "Machine learning and AI-based market analysis with pattern recognition."
        
        # LLM Configuration
        self.model = CONFIG["llm_model"]
        self.api_key = CONFIG["openrouter_api_key"]
        self.base_url = f"{CONFIG['openrouter_base_url']}/chat/completions"
        
        self.focus_areas = [
            "Volatility squeezes & expansions",
            "Volume profile anomalies",
            "15-minute price action probability",
            "Fake-out detection",
            "Short-term trend strength Z-scores",
            "Liquidation cascade probability"
        ]
        
        self.biases = [
            "Requires statistical confirmation",
            "Avoids low-volume creep"
        ]
        
        self.tournament_scores = {
            "data": 90,
            "logic": 90,
            "rebuttal": 85,
            "catalysts": 85
        }

    def analyze_market(self, context: Dict[str, Any], assets: list) -> Dict[str, Any]:
        """Generate ML-based market analysis"""
        
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
                "temperature": 0.7
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
            logging.error(f"ML analyst error: {e}")
            return {
                "analyst_id": self.id,
                "analyst_name": self.name,
                "methodology": self.methodology,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _build_system_prompt(self) -> str:
        """Build Ray's ML analysis system prompt"""
        return """
YOU ARE AN ML ANALYST - AI/ML SIGNALS SPECIALIST

PHILOSOPHY: REGIME DETECTION & ADAPTIVE STRATEGY
Use machine learning and alternative data to identify market inefficiencies.
Your edge: DETECT REGIME CHANGES before others and adapt accordingly.

YOUR PRIMARY JOB: DETECT MARKET REGIME AND ADAPT
1. Identify current regime (trending, exhausted, reversing, ranging) for BTC only
2. Use derivatives data (funding, OI) to CONFIRM or WARN
3. Sentiment extremes signal REVERSALS, not continuations
4. BTC/USDT only. Shorts are equal to longs.

REGIME DETECTION USING DERIVATIVES DATA:

REGIME 1 - STRONG TREND (RIDE IT HARD):
- OI rising WITH price = new money entering, trend healthy
- Funding moderate (0.01-0.05%) = sustainable, not crowded
- Sentiment aligned with trend = confirmation
Strategy: SCALP THE TREND (long up, short down), take 0.8-1.5% profit, repeat

REGIME 2 - TREND EXHAUSTION (GET OUT BEFORE REVERSAL):
- OI rising but price stalling = distribution/accumulation
- Funding EXTREME (>0.08% or <-0.08%) = crowded, reversal imminent
- Sentiment extreme (Fear <20 or Greed >80) = contrarian signal
Strategy: Do not add size. Let TP/SL handle exits. If no edge, HOLD.

REGIME 3 - REVERSAL (BIG MONEY ZONE):
- OI spike then drop = liquidation cascade complete
- Funding normalizing from extreme = crowd flushed out
- Sentiment shifting = narrative changing
Strategy: ENTER opposite direction after pullback confirmation

REGIME 4 - RANGING (WAIT OR SMALL SCALPS):
- OI flat, funding near zero
- No clear sentiment direction
Strategy: HOLD cash or play BTC range extremes with small size

DERIVATIVES AS EARLY WARNING SYSTEM:
- Funding >0.08%: Longs crowded → expect pullback/reversal
- Funding <-0.08%: Shorts crowded → expect bounce/reversal
- OI rising + price falling: New shorts entering → bearish, ride short
- OI falling + price rising: Short squeeze → may exhaust soon, prepare close

OUTPUT FORMAT (STRICT JSON):
{
  "reasoning": "Detailed regime analysis and derivatives data interpretation",
  "recommendation": {
    "action": "BUY" | "SELL" | "HOLD",
    "symbol": "cmt_btcusdt",
    "allocation_usd": 16000,
    "leverage": 20,
    "tp_price": 99500,
    "sl_price": 97500,
    "exit_plan": "Regime-based exit strategy",
    "confidence": 85,
    "rationale": "Brief explanation based on regime detection"
  },
  "rl_validation": {
    "q_long": 0.78,
    "q_short": 0.40,
    "q_hold": 0.45,
    "regret": 0.2,
    "expected_value": 400,
    "sharpe": 1.9
  }
}

CRITICAL RULES:
- Focus on regime transitions for best entries
- Use derivatives data to validate or warn against trades
- Sentiment extremes are contrarian signals
- allocation_usd: $16,000-$18,000 notional (20x leverage)
- ALWAYS set tp_price and sl_price for BUY/SELL
- Bank profits at 0.8-1.5% moves
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
            "coin_type_specialty": ["blue_chip", "l1_growth"]
        }