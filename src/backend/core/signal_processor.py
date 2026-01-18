"""
Advanced Signal Processing Engine for Market Intelligence
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class SignalStrength(Enum):
    """Signal strength classification"""
    WEAK = "weak"
    MODERATE = "moderate" 
    STRONG = "strong"
    CRITICAL = "critical"


@dataclass
class MarketSignal:
    """Structured market signal with confidence metrics"""
    instrument: str
    signal_type: str
    strength: SignalStrength
    confidence: float
    direction: str  # "bullish", "bearish", "neutral"
    timeframe: str
    indicators: Dict[str, float]
    timestamp: str
    
    
class QuantumSignalProcessor:
    """Advanced signal processing with quantum-inspired algorithms"""
    
    def __init__(self):
        self.signal_history: Dict[str, List[MarketSignal]] = {}
        self.confidence_threshold = 0.75
        
    def process_technical_signals(
        self, 
        instrument: str, 
        indicators: Dict[str, any],
        timeframe: str = "5m"
    ) -> List[MarketSignal]:
        """
        Process technical indicators into actionable market signals
        
        Args:
            instrument: Trading instrument symbol
            indicators: Dictionary of technical indicator values
            timeframe: Analysis timeframe
            
        Returns:
            List of processed market signals
        """
        signals = []
        
        # EMA Crossover Signal
        if self._has_ema_data(indicators):
            ema_signal = self._analyze_ema_crossover(instrument, indicators, timeframe)
            if ema_signal:
                signals.append(ema_signal)
        
        # MACD Momentum Signal  
        if self._has_macd_data(indicators):
            macd_signal = self._analyze_macd_momentum(instrument, indicators, timeframe)
            if macd_signal:
                signals.append(macd_signal)
                
        # RSI Divergence Signal
        if self._has_rsi_data(indicators):
            rsi_signal = self._analyze_rsi_divergence(instrument, indicators, timeframe)
            if rsi_signal:
                signals.append(rsi_signal)
                
        # Volatility Breakout Signal
        if self._has_atr_data(indicators):
            vol_signal = self._analyze_volatility_breakout(instrument, indicators, timeframe)
            if vol_signal:
                signals.append(vol_signal)
        
        # Store signal history
        if instrument not in self.signal_history:
            self.signal_history[instrument] = []
        self.signal_history[instrument].extend(signals)
        
        # Keep only recent signals (last 100)
        self.signal_history[instrument] = self.signal_history[instrument][-100:]
        
        return signals
    
    def _has_ema_data(self, indicators: Dict) -> bool:
        """Check if EMA data is available"""
        return "ema20" in indicators and "ema50" in indicators
    
    def _has_macd_data(self, indicators: Dict) -> bool:
        """Check if MACD data is available"""
        return "macd" in indicators
    
    def _has_rsi_data(self, indicators: Dict) -> bool:
        """Check if RSI data is available"""
        return "rsi14" in indicators or "rsi7" in indicators
        
    def _has_atr_data(self, indicators: Dict) -> bool:
        """Check if ATR data is available"""
        return "atr14" in indicators or "atr3" in indicators
    
    def _analyze_ema_crossover(
        self, 
        instrument: str, 
        indicators: Dict, 
        timeframe: str
    ) -> Optional[MarketSignal]:
        """Analyze EMA crossover patterns"""
        try:
            ema20 = float(indicators.get("ema20", 0))
            ema50 = float(indicators.get("ema50", 0))
            current_price = float(indicators.get("current_price", 0))
            
            if not all([ema20, ema50, current_price]):
                return None
            
            # Determine signal direction and strength
            ema_diff = (ema20 - ema50) / ema50 * 100
            price_above_ema20 = current_price > ema20
            
            if abs(ema_diff) < 0.5:
                return None  # Too close, no clear signal
            
            direction = "bullish" if ema20 > ema50 else "bearish"
            strength = SignalStrength.STRONG if abs(ema_diff) > 2.0 else SignalStrength.MODERATE
            confidence = min(0.95, 0.6 + abs(ema_diff) * 0.1)
            
            return MarketSignal(
                instrument=instrument,
                signal_type="ema_crossover",
                strength=strength,
                confidence=confidence,
                direction=direction,
                timeframe=timeframe,
                indicators={
                    "ema20": ema20,
                    "ema50": ema50,
                    "ema_diff_pct": ema_diff,
                    "price_above_ema20": price_above_ema20
                },
                timestamp=""
            )
            
        except (ValueError, TypeError):
            return None
    
    def _analyze_macd_momentum(
        self, 
        instrument: str, 
        indicators: Dict, 
        timeframe: str
    ) -> Optional[MarketSignal]:
        """Analyze MACD momentum signals"""
        try:
            macd_value = indicators.get("macd")
            if isinstance(macd_value, dict):
                macd = float(macd_value.get("valueMACD", 0))
                signal_line = float(macd_value.get("valueSignal", 0))
                histogram = float(macd_value.get("valueHistogram", 0))
            else:
                macd = float(macd_value or 0)
                signal_line = 0
                histogram = 0
            
            if not macd:
                return None
            
            # Analyze MACD signals
            macd_above_signal = macd > signal_line if signal_line else macd > 0
            histogram_increasing = histogram > 0
            
            direction = "bullish" if macd_above_signal else "bearish"
            strength = SignalStrength.STRONG if histogram_increasing else SignalStrength.MODERATE
            confidence = 0.7 + abs(histogram) * 0.1 if histogram else 0.6
            confidence = min(0.95, confidence)
            
            return MarketSignal(
                instrument=instrument,
                signal_type="macd_momentum",
                strength=strength,
                confidence=confidence,
                direction=direction,
                timeframe=timeframe,
                indicators={
                    "macd": macd,
                    "signal_line": signal_line,
                    "histogram": histogram,
                    "macd_above_signal": macd_above_signal
                },
                timestamp=""
            )
            
        except (ValueError, TypeError):
            return None
    
    def _analyze_rsi_divergence(
        self, 
        instrument: str, 
        indicators: Dict, 
        timeframe: str
    ) -> Optional[MarketSignal]:
        """Analyze RSI divergence and overbought/oversold conditions"""
        try:
            rsi14 = float(indicators.get("rsi14", 0))
            rsi7 = float(indicators.get("rsi7", 0))
            
            if not rsi14:
                return None
            
            # RSI signal analysis
            if rsi14 > 70:
                direction = "bearish"
                strength = SignalStrength.STRONG if rsi14 > 80 else SignalStrength.MODERATE
            elif rsi14 < 30:
                direction = "bullish" 
                strength = SignalStrength.STRONG if rsi14 < 20 else SignalStrength.MODERATE
            else:
                return None  # Neutral zone
            
            # Confidence based on RSI extremes
            if rsi14 > 70:
                confidence = 0.6 + (rsi14 - 70) * 0.01
            else:
                confidence = 0.6 + (30 - rsi14) * 0.01
            confidence = min(0.95, confidence)
            
            return MarketSignal(
                instrument=instrument,
                signal_type="rsi_divergence",
                strength=strength,
                confidence=confidence,
                direction=direction,
                timeframe=timeframe,
                indicators={
                    "rsi14": rsi14,
                    "rsi7": rsi7,
                    "overbought": rsi14 > 70,
                    "oversold": rsi14 < 30
                },
                timestamp=""
            )
            
        except (ValueError, TypeError):
            return None
    
    def _analyze_volatility_breakout(
        self, 
        instrument: str, 
        indicators: Dict, 
        timeframe: str
    ) -> Optional[MarketSignal]:
        """Analyze volatility breakout patterns"""
        try:
            atr14 = float(indicators.get("atr14", 0))
            atr3 = float(indicators.get("atr3", 0))
            current_price = float(indicators.get("current_price", 0))
            
            if not all([atr14, current_price]):
                return None
            
            # Volatility analysis
            volatility_ratio = atr3 / atr14 if atr14 > 0 else 1.0
            high_volatility = volatility_ratio > 1.5
            
            if not high_volatility:
                return None
            
            direction = "neutral"  # Volatility breakout can go either way
            strength = SignalStrength.STRONG if volatility_ratio > 2.0 else SignalStrength.MODERATE
            confidence = 0.6 + min(0.3, (volatility_ratio - 1.0) * 0.2)
            
            return MarketSignal(
                instrument=instrument,
                signal_type="volatility_breakout",
                strength=strength,
                confidence=confidence,
                direction=direction,
                timeframe=timeframe,
                indicators={
                    "atr14": atr14,
                    "atr3": atr3,
                    "volatility_ratio": volatility_ratio,
                    "high_volatility": high_volatility
                },
                timestamp=""
            )
            
        except (ValueError, TypeError):
            return None
    
    def get_signal_consensus(self, instrument: str, lookback: int = 5) -> Dict:
        """
        Get consensus signal from recent history
        
        Args:
            instrument: Trading instrument
            lookback: Number of recent signals to analyze
            
        Returns:
            Dictionary with consensus analysis
        """
        if instrument not in self.signal_history:
            return {"consensus": "neutral", "confidence": 0.0, "signals": []}
        
        recent_signals = self.signal_history[instrument][-lookback:]
        if not recent_signals:
            return {"consensus": "neutral", "confidence": 0.0, "signals": []}
        
        # Analyze signal consensus
        bullish_signals = [s for s in recent_signals if s.direction == "bullish"]
        bearish_signals = [s for s in recent_signals if s.direction == "bearish"]
        
        bullish_weight = sum(s.confidence for s in bullish_signals)
        bearish_weight = sum(s.confidence for s in bearish_signals)
        
        if bullish_weight > bearish_weight * 1.2:
            consensus = "bullish"
            confidence = bullish_weight / len(recent_signals)
        elif bearish_weight > bullish_weight * 1.2:
            consensus = "bearish"
            confidence = bearish_weight / len(recent_signals)
        else:
            consensus = "neutral"
            confidence = 0.5
        
        return {
            "consensus": consensus,
            "confidence": min(0.95, confidence),
            "signals": len(recent_signals),
            "bullish_weight": bullish_weight,
            "bearish_weight": bearish_weight
        }