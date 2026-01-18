"""
Advanced Portfolio Optimization Engine
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timezone
import logging


@dataclass
class PositionAllocation:
    """Optimized position allocation recommendation"""
    instrument: str
    action: str  # "buy", "sell", "hold"
    allocation_pct: float  # Percentage of portfolio
    allocation_usd: float  # USD amount
    leverage: float
    confidence: float
    risk_score: float
    expected_return: float
    stop_loss_pct: float
    take_profit_pct: float
    reasoning: str


class AdvancedPortfolioOptimizer:
    """
    Sophisticated portfolio optimization using modern portfolio theory
    and risk-adjusted return maximization
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.max_position_size = 0.5  # 50% max per position
        self.max_portfolio_risk = 0.15  # 15% max portfolio risk
        self.target_sharpe = 1.5  # Target Sharpe ratio
        
    def optimize_portfolio(
        self,
        signals: List[Dict],
        account_balance: float,
        current_positions: List[Dict],
        risk_tolerance: str = "aggressive"
    ) -> List[PositionAllocation]:
        """
        Optimize portfolio allocation based on signals and risk parameters
        
        Args:
            signals: List of market signals with confidence scores
            account_balance: Available account balance
            current_positions: Current open positions
            risk_tolerance: "conservative", "moderate", "aggressive"
            
        Returns:
            List of optimized position allocations
        """
        allocations = []
        
        # Risk adjustment based on tolerance
        risk_multiplier = self._get_risk_multiplier(risk_tolerance)
        
        # Calculate available capital (excluding current positions)
        available_capital = self._calculate_available_capital(
            account_balance, current_positions
        )
        
        # Process each signal
        for signal in signals:
            if signal.get("action") == "hold":
                continue
                
            allocation = self._calculate_optimal_allocation(
                signal, available_capital, risk_multiplier
            )
            
            if allocation and allocation.allocation_usd > 0:
                allocations.append(allocation)
        
        # Portfolio-level optimization
        allocations = self._optimize_portfolio_weights(allocations, available_capital)
        
        # Risk validation
        allocations = self._validate_portfolio_risk(allocations, account_balance)
        
        return allocations
    
    def _get_risk_multiplier(self, risk_tolerance: str) -> float:
        """Get risk multiplier based on tolerance level"""
        multipliers = {
            "conservative": 0.5,
            "moderate": 1.0,
            "aggressive": 1.5
        }
        return multipliers.get(risk_tolerance, 1.0)
    
    def _calculate_available_capital(
        self, 
        account_balance: float, 
        current_positions: List[Dict]
    ) -> float:
        """Calculate available capital for new positions"""
        # Reserve 20% for margin and unexpected moves
        reserved_capital = account_balance * 0.2
        
        # Calculate capital tied up in current positions
        used_capital = sum(
            abs(pos.get("quantity", 0)) * pos.get("entry_price", 0) 
            for pos in current_positions
        )
        
        available = account_balance - reserved_capital - used_capital
        return max(0, available)
    
    def _calculate_optimal_allocation(
        self,
        signal: Dict,
        available_capital: float,
        risk_multiplier: float
    ) -> Optional[PositionAllocation]:
        """Calculate optimal allocation for a single signal"""
        try:
            instrument = signal.get("asset", "")
            action = signal.get("action", "hold")
            confidence = float(signal.get("confidence", 0.5))
            
            if action == "hold" or confidence < 0.6:
                return None
            
            # Base allocation based on confidence
            base_allocation_pct = confidence * 0.3 * risk_multiplier  # Max 30% base
            
            # Adjust for signal strength and market conditions
            signal_strength = self._assess_signal_strength(signal)
            allocation_pct = base_allocation_pct * signal_strength
            
            # Cap at maximum position size
            allocation_pct = min(allocation_pct, self.max_position_size)
            
            # Calculate USD allocation
            allocation_usd = available_capital * allocation_pct
            
            # Determine optimal leverage
            leverage = self._calculate_optimal_leverage(confidence, signal_strength)
            
            # Risk metrics
            risk_score = self._calculate_position_risk(allocation_pct, leverage, confidence)
            expected_return = self._estimate_expected_return(signal, leverage)
            
            # Stop loss and take profit levels
            stop_loss_pct = self._calculate_stop_loss(signal, leverage)
            take_profit_pct = self._calculate_take_profit(signal, leverage)
            
            # Generate reasoning
            reasoning = self._generate_allocation_reasoning(
                signal, allocation_pct, leverage, confidence
            )
            
            return PositionAllocation(
                instrument=instrument,
                action=action,
                allocation_pct=allocation_pct,
                allocation_usd=allocation_usd,
                leverage=leverage,
                confidence=confidence,
                risk_score=risk_score,
                expected_return=expected_return,
                stop_loss_pct=stop_loss_pct,
                take_profit_pct=take_profit_pct,
                reasoning=reasoning
            )
            
        except Exception as e:
            self.logger.error(f"Error calculating allocation for {signal}: {e}")
            return None
    
    def _assess_signal_strength(self, signal: Dict) -> float:
        """Assess overall signal strength from multiple factors"""
        base_strength = 1.0
        
        # Technical indicator alignment
        rationale = signal.get("rationale", "").lower()
        
        # Boost for multiple confirming indicators
        if "ema" in rationale and "macd" in rationale:
            base_strength *= 1.2
        if "rsi" in rationale:
            base_strength *= 1.1
        if "volume" in rationale:
            base_strength *= 1.1
        if "breakout" in rationale:
            base_strength *= 1.3
        if "divergence" in rationale:
            base_strength *= 1.2
        
        # Reduce for uncertainty indicators
        if "uncertain" in rationale or "mixed" in rationale:
            base_strength *= 0.8
        
        return min(2.0, base_strength)  # Cap at 2x
    
    def _calculate_optimal_leverage(self, confidence: float, signal_strength: float) -> float:
        """Calculate optimal leverage based on confidence and signal strength"""
        # Base leverage from confidence
        base_leverage = 1.0 + (confidence - 0.5) * 10  # 1x to 6x range
        
        # Adjust for signal strength
        leverage = base_leverage * signal_strength
        
        # Apply safety caps
        leverage = max(1.0, min(10.0, leverage))
        
        return round(leverage, 1)
    
    def _calculate_position_risk(
        self, 
        allocation_pct: float, 
        leverage: float, 
        confidence: float
    ) -> float:
        """Calculate position risk score (0-1, higher = riskier)"""
        # Base risk from allocation size
        size_risk = allocation_pct / self.max_position_size
        
        # Leverage risk
        leverage_risk = (leverage - 1) / 9  # Normalize 1-10x to 0-1
        
        # Confidence risk (lower confidence = higher risk)
        confidence_risk = 1 - confidence
        
        # Combined risk score
        total_risk = (size_risk * 0.4 + leverage_risk * 0.4 + confidence_risk * 0.2)
        
        return min(1.0, total_risk)
    
    def _estimate_expected_return(self, signal: Dict, leverage: float) -> float:
        """Estimate expected return for the position"""
        # Base return estimate from signal confidence
        confidence = signal.get("confidence", 0.5)
        base_return = confidence * 0.05  # 5% max base return
        
        # Adjust for leverage
        leveraged_return = base_return * leverage
        
        # Adjust for market conditions and volatility
        # This is a simplified model - in practice would use more sophisticated methods
        market_adjustment = 1.0  # Could incorporate VIX, market regime, etc.
        
        return leveraged_return * market_adjustment
    
    def _calculate_stop_loss(self, signal: Dict, leverage: float) -> float:
        """Calculate appropriate stop loss percentage"""
        # Base stop loss inversely related to leverage
        base_stop = 0.02  # 2% base
        leveraged_stop = base_stop / leverage
        
        # Minimum and maximum bounds
        stop_loss = max(0.005, min(0.05, leveraged_stop))  # 0.5% to 5%
        
        return stop_loss
    
    def _calculate_take_profit(self, signal: Dict, leverage: float) -> float:
        """Calculate take profit target"""
        # Base take profit based on risk/reward ratio
        stop_loss = self._calculate_stop_loss(signal, leverage)
        risk_reward_ratio = 2.5  # Target 2.5:1 risk/reward
        
        take_profit = stop_loss * risk_reward_ratio
        
        return take_profit
    
    def _generate_allocation_reasoning(
        self,
        signal: Dict,
        allocation_pct: float,
        leverage: float,
        confidence: float
    ) -> str:
        """Generate human-readable reasoning for the allocation"""
        instrument = signal.get("asset", "")
        action = signal.get("action", "").upper()
        
        reasoning_parts = [
            f"{action} {instrument}: {allocation_pct:.1%} allocation",
            f"{leverage:.1f}x leverage based on {confidence:.1%} confidence"
        ]
        
        # Add signal-specific reasoning
        rationale = signal.get("rationale", "")
        if rationale:
            reasoning_parts.append(f"Signal: {rationale[:100]}...")
        
        return " | ".join(reasoning_parts)
    
    def _optimize_portfolio_weights(
        self,
        allocations: List[PositionAllocation],
        available_capital: float
    ) -> List[PositionAllocation]:
        """Optimize portfolio weights to maximize risk-adjusted returns"""
        if not allocations:
            return allocations
        
        # Calculate total requested allocation
        total_requested = sum(a.allocation_pct for a in allocations)
        
        # If over-allocated, scale down proportionally
        if total_requested > 1.0:
            scale_factor = 0.95 / total_requested  # Leave 5% buffer
            
            for allocation in allocations:
                allocation.allocation_pct *= scale_factor
                allocation.allocation_usd = available_capital * allocation.allocation_pct
        
        return allocations
    
    def _validate_portfolio_risk(
        self,
        allocations: List[PositionAllocation],
        account_balance: float
    ) -> List[PositionAllocation]:
        """Validate and adjust portfolio-level risk"""
        # Calculate portfolio risk
        portfolio_risk = sum(
            a.allocation_pct * a.risk_score for a in allocations
        )
        
        # If portfolio risk too high, scale down high-risk positions
        if portfolio_risk > self.max_portfolio_risk:
            risk_scale_factor = self.max_portfolio_risk / portfolio_risk
            
            for allocation in allocations:
                if allocation.risk_score > 0.7:  # High risk positions
                    allocation.allocation_pct *= risk_scale_factor
                    allocation.allocation_usd *= risk_scale_factor
                    allocation.leverage *= 0.9  # Slightly reduce leverage
        
        # Remove positions that are too small to be meaningful
        min_position_size = account_balance * 0.01  # 1% minimum
        allocations = [
            a for a in allocations 
            if a.allocation_usd >= min_position_size
        ]
        
        return allocations
    
    def calculate_portfolio_metrics(
        self,
        allocations: List[PositionAllocation]
    ) -> Dict[str, float]:
        """Calculate portfolio-level risk and return metrics"""
        if not allocations:
            return {
                "total_allocation": 0.0,
                "weighted_confidence": 0.0,
                "portfolio_risk": 0.0,
                "expected_return": 0.0,
                "estimated_sharpe": 0.0
            }
        
        total_allocation = sum(a.allocation_pct for a in allocations)
        
        # Weighted metrics
        weighted_confidence = sum(
            a.allocation_pct * a.confidence for a in allocations
        ) / total_allocation if total_allocation > 0 else 0
        
        portfolio_risk = sum(
            a.allocation_pct * a.risk_score for a in allocations
        )
        
        expected_return = sum(
            a.allocation_pct * a.expected_return for a in allocations
        )
        
        # Estimated Sharpe ratio (simplified)
        estimated_sharpe = expected_return / portfolio_risk if portfolio_risk > 0 else 0
        
        return {
            "total_allocation": total_allocation,
            "weighted_confidence": weighted_confidence,
            "portfolio_risk": portfolio_risk,
            "expected_return": expected_return,
            "estimated_sharpe": estimated_sharpe
        }