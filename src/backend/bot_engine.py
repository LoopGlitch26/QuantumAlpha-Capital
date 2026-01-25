"""
QuantumAlpha Capital Engine - Core trading logic separated from UI
Advanced systematic alpha generation system
"""

import asyncio
import json
import logging
from collections import deque, OrderedDict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any

from src.backend.agent.decision_maker import QuantumDecisionEngine
from src.backend.analysts.market_scanner import MarketScanner
from src.backend.config_loader import CONFIG
from src.backend.indicators.taapi_client import TAAPIClient
from src.backend.models.trade_proposal import TradeProposal
from src.backend.trading.hyperliquid_api import HyperliquidAPI
from src.backend.utils.prompt_utils import json_default


@dataclass
class SystemState:
    """Comprehensive system state for real-time market operations"""
    active_status: bool = False
    account_balance: float = 0.0
    portfolio_value: float = 0.0
    performance_ratio: float = 0.0
    risk_metric: float = 0.0
    open_positions: List[Dict] = field(default_factory=list)
    managed_positions: List[Dict] = field(default_factory=list)
    pending_orders: List[Dict] = field(default_factory=list)
    execution_history: List[Dict] = field(default_factory=list)
    market_intelligence: List[Dict] = field(default_factory=list)  # Market data for dashboard
    awaiting_approval: List[Dict] = field(default_factory=list)  # Pending trade proposals (manual mode)
    neural_reasoning: Dict = field(default_factory=dict)
    multi_analyst_results: Dict = field(default_factory=dict)  # Multi-analyst system results
    last_sync: str = ""
    system_error: Optional[str] = None
    cycle_count: int = 0


class QuantumMarketProcessor:
    """
    Advanced algorithmic market processing engine with neural decision integration.
    Operates independently from UI layer via sophisticated callback architecture.
    """

    def __init__(
        self,
        instruments: List[str],
        timeframe: str,
        on_system_update: Optional[Callable[[SystemState], None]] = None,
        on_execution_complete: Optional[Callable[[Dict], None]] = None,
        on_system_alert: Optional[Callable[[str], None]] = None,
    ):
        """
        Initialize quantum market processing engine.

        Args:
            instruments: List of tradeable instruments (e.g., ["BTC", "ETH"])
            timeframe: Processing interval (e.g., "5m", "1h")
            on_system_update: Callback for system state updates
            on_execution_complete: Callback when execution is completed
            on_system_alert: Callback for system alerts
        """
        self.instruments = instruments
        self.timeframe = timeframe
        self.on_system_update = on_system_update
        self.on_execution_complete = on_execution_complete
        self.on_system_alert = on_system_alert

        # Logging (initialize first!)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("quantumalpha.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Initialize market processing components
        self.taapi = TAAPIClient()
        self.hyperliquid = HyperliquidAPI()
        self.neural_engine = QuantumDecisionEngine()
        self.market_scanner = MarketScanner()  # Multi-analyst system

        # System state
        self.system_state = SystemState()
        self.processing_active = False
        self._execution_task: Optional[asyncio.Task] = None

        # Internal state tracking (from original main.py)
        self.initialization_time: Optional[datetime] = None
        self.cycle_count = 0
        self.performance_log: List[float] = []  # For Sharpe calculation
        self.managed_positions: List[Dict] = []  # Local tracking of open positions
        self.system_events: deque = deque(maxlen=200)
        self.baseline_portfolio_value: Optional[float] = None
        self.price_cache: Dict[str, deque] = {instrument: deque(maxlen=60) for instrument in instruments}
        self.active_trades: List[Dict] = []  # Track active trades
        self.invocation_count: int = 0  # Track AI invocations
        self.price_history: Dict[str, deque] = {instrument: deque(maxlen=100) for instrument in instruments}  # Price history for charts
        
        # Manual execution mode
        self.execution_mode = CONFIG.get("trading_mode", "auto").lower()
        self.awaiting_proposals: List[TradeProposal] = []
        self.logger.info(f"Execution mode: {self.execution_mode.upper()}")

        # File paths
        self.journal_path = Path("data/diary.jsonl")
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)

    async def initialize_processing(self):
        """Initialize the quantum market processor"""
        if self.processing_active:
            self.logger.warning("Processor already active")
            return

        self.processing_active = True
        self.system_state.active_status = True
        self.initialization_time = datetime.now(timezone.utc)
        self.cycle_count = 0

        # Get baseline portfolio value
        try:
            user_state = await self.hyperliquid.get_user_state()
            self.baseline_portfolio_value = user_state.get('total_value', 0.0)
            if self.baseline_portfolio_value == 0.0:
                self.baseline_portfolio_value = user_state.get('balance', 10000.0)
        except Exception as e:
            self.logger.error(f"Failed to get baseline portfolio value: {e}")
            self.baseline_portfolio_value = 10000.0

        self._execution_task = asyncio.create_task(self._quantum_processing_loop())
        self.logger.info(f"Processor initialized - Instruments: {self.instruments}, Timeframe: {self.timeframe}")
        
        # Send activity event for GUI
        if self.on_system_alert:
            self.on_system_alert(f"🚀 QuantumAlpha initialized - Trading {', '.join(self.instruments)} on {self.timeframe}")
            
        self._notify_system_update()

    async def terminate_processing(self):
        """Terminate the quantum market processor"""
        if not self.processing_active:
            return

        self.processing_active = False
        self.system_state.active_status = False

        if self._execution_task:
            self._execution_task.cancel()
            try:
                await self._execution_task
            except asyncio.CancelledError:
                pass

        self.logger.info("Processor terminated")
        self._notify_system_update()

    async def _quantum_processing_loop(self):
        """
        Quantum market processing loop with neural decision integration.
        Adapted from advanced algorithmic trading systems
        """
        try:
            while self.processing_active:
                self.cycle_count += 1
                self.system_state.cycle_count = self.cycle_count

                try:
                    # ===== PHASE 1: Fetch Portfolio State =====
                    self.invocation_count += 1
                    portfolio_state = await self.hyperliquid.get_user_state()
                    account_balance = portfolio_state['balance']
                    portfolio_value = portfolio_state['total_value']

                    # Calculate performance metrics
                    # Set baseline on first cycle
                    if self.baseline_portfolio_value is None:
                        self.baseline_portfolio_value = portfolio_value
                    
                    # Calculate return based on actual baseline
                    if self.baseline_portfolio_value > 0:
                        performance_ratio = ((portfolio_value - self.baseline_portfolio_value) / self.baseline_portfolio_value) * 100
                    else:
                        performance_ratio = 0.0

                    risk_metric = self._calculate_risk_metric(self.performance_log)
                    
                    self.logger.debug(f"  Balance: ${account_balance:,.2f} | Return: {performance_ratio:+.2f}% | Risk: {risk_metric:.2f}")

                    # Update system state
                    self.system_state.account_balance = account_balance
                    self.system_state.portfolio_value = portfolio_value
                    self.system_state.performance_ratio = performance_ratio
                    self.system_state.risk_metric = risk_metric

                    # ===== PHASE 2: Enrich Positions =====
                    enriched_positions = []
                    for pos in portfolio_state['positions']:
                        symbol = pos.get('coin')
                        try:
                            current_price = await self.hyperliquid.get_current_price(symbol)
                            enriched_positions.append({
                                'symbol': symbol,
                                'quantity': float(pos.get('szi', 0) or 0),
                                'entry_price': float(pos.get('entryPx', 0) or 0),
                                'current_price': current_price,
                                'liquidation_price': float(pos.get('liquidationPx', 0) or 0),
                                'unrealized_pnl': pos.get('pnl', 0.0),
                                'leverage': pos.get('leverage', {}).get('value', 1) if isinstance(pos.get('leverage'), dict) else pos.get('leverage', 1)
                            })
                        except Exception as e:
                            self.logger.error(f"Error enriching position for {symbol}: {e}")

                    self.system_state.open_positions = enriched_positions

                    # ===== PHASE 3: Load Recent Diary =====
                    recent_diary = self._load_recent_journal(limit=10)

                    # ===== PHASE 4: Fetch Open Orders =====
                    open_orders_raw = await self.hyperliquid.get_open_orders()
                    open_orders = []
                    for o in open_orders_raw:
                        order_type_obj = o.get('orderType', {})
                        trigger_price = None
                        order_type_str = 'limit'

                        if isinstance(order_type_obj, dict) and 'trigger' in order_type_obj:
                            order_type_str = 'trigger'
                            trigger_data = order_type_obj.get('trigger', {})
                            if 'triggerPx' in trigger_data:
                                trigger_price = float(trigger_data['triggerPx'])

                        open_orders.append({
                            'coin': o.get('coin'),
                            'oid': o.get('oid'),
                            'is_buy': o.get('side') == 'B',
                            'size': float(o.get('sz', 0)),
                            'price': float(o.get('limitPx', 0)),
                            'trigger_price': trigger_price,
                            'order_type': order_type_str
                        })

                    self.system_state.pending_orders = open_orders

                    # ===== PHASE 5: Reconcile Active Trades =====
                    await self._reconcile_active_trades(portfolio_state['positions'], open_orders_raw)

                    # ===== PHASE 6: Fetch Recent Fills =====
                    fills_raw = await self.hyperliquid.get_recent_fills(limit=50)
                    recent_fills = []
                    for fill in fills_raw[-20:]:
                        ts = fill.get('time')
                        if ts and ts > 1_000_000_000_000:
                            ts = ts / 1000
                        ts_str = datetime.fromtimestamp(ts, timezone.utc).isoformat() if ts else ""

                        recent_fills.append({
                            'timestamp': ts_str,
                            'coin': fill.get('coin'),
                            'is_buy': fill.get('side') == 'B',
                            'size': float(fill.get('sz', 0)),
                            'price': float(fill.get('px', 0))
                        })

                    self.system_state.execution_history = recent_fills

                    # ===== PHASE 7: Build Dashboard =====
                    # Calculate dashboard metrics
                    total_return_pct = performance_ratio
                    balance = account_balance
                    total_value = portfolio_value
                    sharpe_ratio = risk_metric
                    
                    dashboard = {
                        'total_return_pct': total_return_pct,
                        'balance': balance,
                        'account_value': total_value,
                        'sharpe_ratio': sharpe_ratio,
                        'positions': enriched_positions,
                        'active_trades': self.active_trades,
                        'open_orders': open_orders,
                        'recent_diary': recent_diary,
                        'recent_fills': recent_fills
                    }

                    # ===== PHASE 8: Gather Market Data =====
                    market_sections = []
                    for idx, instrument in enumerate(self.instruments):
                        try:
                            # Current price
                            current_price = await self.hyperliquid.get_current_price(instrument)

                            # Store price history
                            self.price_history[instrument].append({
                                't': datetime.now(timezone.utc).isoformat(),
                                'mid': current_price
                            })

                            # Open interest and funding
                            oi = await self.hyperliquid.get_open_interest(instrument)
                            funding = await self.hyperliquid.get_funding_rate(instrument)

                            # Fetch all indicators using bulk endpoint (2 requests instead of 10)
                            # Note: fetch_asset_indicators() already includes 15s delay between 5m and interval requests
                            # Uses caching to avoid redundant API calls
                            indicators = self.taapi.fetch_asset_indicators(instrument)
                            
                            # Add delay between assets to respect TAAPI rate limit (1 req/15s)
                            # Only wait if this is not the last instrument
                            if idx < len(self.instruments) - 1:
                                self.logger.info(f"Waiting 15s before fetching next asset (TAAPI rate limit)...")
                                await asyncio.sleep(15)
                            
                            # Extract 5m indicators - handle both single values and lists
                            ema20_5m_data = indicators["5m"].get("ema20", [])
                            ema20_5m_series = [ema20_5m_data] if isinstance(ema20_5m_data, (int, float)) else (ema20_5m_data if ema20_5m_data else [])
                            
                            macd_5m_data = indicators["5m"].get("macd", [])
                            # MACD can return dict or list of dicts - handle both cases
                            if isinstance(macd_5m_data, dict):
                                # Single dict - extract valueMACD
                                macd_5m_series = [macd_5m_data.get('valueMACD', macd_5m_data.get('value', 0))]
                            elif isinstance(macd_5m_data, list):
                                # List of dicts or values
                                macd_5m_series = [m.get('valueMACD', m.get('value', m)) if isinstance(m, dict) else m for m in macd_5m_data]
                            elif isinstance(macd_5m_data, (int, float)):
                                macd_5m_series = [macd_5m_data]
                            else:
                                macd_5m_series = []
                            
                            rsi7_5m_data = indicators["5m"].get("rsi7", [])
                            rsi7_5m_series = [rsi7_5m_data] if isinstance(rsi7_5m_data, (int, float)) else (rsi7_5m_data if rsi7_5m_data else [])
                            
                            rsi14_5m_data = indicators["5m"].get("rsi14", [])
                            rsi14_5m_series = [rsi14_5m_data] if isinstance(rsi14_5m_data, (int, float)) else (rsi14_5m_data if rsi14_5m_data else [])

                            # Extract long-term indicators (interval from config: 1h, 4h, etc.)
                            interval = CONFIG.get("interval", "1h")
                            lt_indicators = indicators.get(interval, {})
                            
                            # Handle single values or lists for all indicators
                            lt_ema20_data = lt_indicators.get("ema20")
                            lt_ema20 = lt_ema20_data if not isinstance(lt_ema20_data, list) else (lt_ema20_data[-1] if lt_ema20_data else None)
                            
                            lt_ema50_data = lt_indicators.get("ema50")
                            lt_ema50 = lt_ema50_data if not isinstance(lt_ema50_data, list) else (lt_ema50_data[-1] if lt_ema50_data else None)
                            
                            lt_atr3_data = lt_indicators.get("atr3")
                            lt_atr3 = lt_atr3_data if not isinstance(lt_atr3_data, list) else (lt_atr3_data[-1] if lt_atr3_data else None)
                            
                            lt_atr14_data = lt_indicators.get("atr14")
                            lt_atr14 = lt_atr14_data if not isinstance(lt_atr14_data, list) else (lt_atr14_data[-1] if lt_atr14_data else None)
                            
                            lt_macd_data = lt_indicators.get("macd", [])
                            # Handle MACD for long-term indicators too
                            if isinstance(lt_macd_data, dict):
                                lt_macd_series = [lt_macd_data.get('valueMACD', lt_macd_data.get('value', 0))]
                            elif isinstance(lt_macd_data, list):
                                lt_macd_series = [m.get('valueMACD', m.get('value', m)) if isinstance(m, dict) else m for m in lt_macd_data]
                            elif isinstance(lt_macd_data, (int, float)):
                                lt_macd_series = [lt_macd_data]
                            else:
                                lt_macd_series = []
                            
                            lt_rsi_data = lt_indicators.get("rsi14", [])
                            lt_rsi_series = [lt_rsi_data] if isinstance(lt_rsi_data, (int, float)) else (lt_rsi_data if lt_rsi_data else [])

                            # Build market data structure
                            market_sections.append({
                                "asset": instrument,
                                "current_price": current_price,
                                "intraday": {
                                    "ema20": ema20_5m_series[-1] if ema20_5m_series else None,
                                    "macd": macd_5m_series[-1] if macd_5m_series else None,
                                    "rsi7": rsi7_5m_series[-1] if rsi7_5m_series else None,
                                    "rsi14": rsi14_5m_series[-1] if rsi14_5m_series else None,
                                    "series": {
                                        "ema20": ema20_5m_series,
                                        "macd": macd_5m_series,
                                        "rsi7": rsi7_5m_series,
                                        "rsi14": rsi14_5m_series
                                    }
                                },
                                "long_term": {
                                    "ema20": lt_ema20,
                                    "ema50": lt_ema50,
                                    "atr3": lt_atr3,
                                    "atr14": lt_atr14,
                                    "macd_series": lt_macd_series,
                                    "rsi_series": lt_rsi_series
                                },
                                "open_interest": oi,
                                "funding_rate": funding,
                                "funding_annualized_pct": funding * 24 * 365 * 100 if funding else None,
                                "recent_mid_prices": [p['mid'] for p in list(self.price_history[instrument])[-10:]]
                            })

                        except Exception as e:
                            self.logger.error(f"Error gathering market data for {instrument}: {e}")
                            import traceback
                            self.logger.error(f"Traceback: {traceback.format_exc()}")

                    # ===== PHASE 9: Build LLM Context =====
                    context_payload = OrderedDict([
                        ("invocation", {
                            "count": self.invocation_count,
                            "current_time": datetime.now(timezone.utc).isoformat()
                        }),
                        ("account", dashboard),
                        ("market_data", market_sections),
                        ("instructions", {
                            "instruments": self.instruments,
                            "note": "Follow the system prompt guidelines strictly"
                        })
                    ])
                    context = json.dumps(context_payload, default=json_default, indent=2)

                    # Log prompt
                    with open("data/prompts.log", "a", encoding="utf-8") as f:
                        f.write(f"\n{'='*80}\n")
                        f.write(f"Invocation {self.invocation_count} - {datetime.now(timezone.utc).isoformat()}\n")
                        f.write(f"{'='*80}\n")
                        f.write(context + "\n")

                    # ===== PHASE 10: Get Neural Decision =====
                    # Option 1: Use multi-analyst system (new)
                    if CONFIG.get("use_multi_analyst", False):
                        self.logger.info("Using multi-analyst system for decision making...")
                        
                        # Send activity event for GUI
                        if self.on_system_alert:
                            self.on_system_alert("🧠 Multi-analyst system analyzing market...")
                        
                        decisions = await self.market_scanner.analyze_market(context_payload, self.instruments)
                        
                        # Extract final recommendation from judge
                        final_rec = decisions.get("final_recommendation")
                        if final_rec:
                            # Convert to original format for compatibility
                            decisions = {
                                "reasoning": decisions.get("judge_decision", {}).get("reasoning", "Multi-analyst decision"),
                                "trade_decisions": [final_rec]
                            }
                        else:
                            # No recommendation from judge, use HOLD
                            decisions = {
                                "reasoning": "Multi-analyst system recommends HOLD",
                                "trade_decisions": [{
                                    "asset": asset,
                                    "action": "hold",
                                    "allocation_usd": 0,
                                    "tp_price": None,
                                    "sl_price": None,
                                    "exit_plan": "",
                                    "rationale": "No consensus from analysts"
                                } for asset in self.instruments]
                            }
                        
                        # Store full multi-analyst results
                        self.system_state.neural_reasoning = decisions
                        # Store the full decisions object which contains analyst_results
                        self.system_state.multi_analyst_results = decisions
                        
                        # Extract trade decisions for processing
                        trade_decisions = decisions.get('trade_decisions', [])
                        
                    else:
                        # Option 2: Use original neural engine (default)
                        decisions = await asyncio.to_thread(
                            self.neural_engine.synthesize_market_decisions, self.instruments, context
                        )

                        # Validate and retry if needed
                        if not isinstance(decisions, dict) or 'trade_decisions' not in decisions:
                            self.logger.warning("Invalid decision format, retrying with strict prefix...")
                            strict_context = (
                                "Return ONLY the JSON object per the schema. "
                                "No markdown, no explanation.\n\n" + context
                            )
                            decisions = await asyncio.to_thread(
                                self.neural_engine.synthesize_market_decisions, self.instruments, strict_context
                            )

                        # Check for all-hold with parse errors
                        trade_decisions = decisions.get('trade_decisions', [])
                        if all(
                            d.get('action') == 'hold' and 'parse error' in d.get('rationale', '').lower()
                            for d in trade_decisions
                        ):
                            self.logger.warning("All holds with parse errors, retrying...")
                            decisions = await asyncio.to_thread(
                                self.neural_engine.synthesize_market_decisions, self.instruments, context
                            )
                            trade_decisions = decisions.get('trade_decisions', [])

                        self.system_state.neural_reasoning = decisions

                    # Extract reasoning
                    reasoning = decisions.get('reasoning', '')
                    if reasoning:
                        self.logger.info(f"Decision Reasoning: {reasoning[:200]}...")

                    # ===== PHASE 11: Execute Trades or Create Proposals =====
                    for decision in trade_decisions:
                        instrument = decision.get('asset')
                        if instrument not in self.instruments:
                            continue

                        action = decision.get('action')
                        rationale = decision.get('rationale', '')
                        allocation = float(decision.get('allocation_usd', 0))
                        tp_price = decision.get('tp_price')
                        sl_price = decision.get('sl_price')
                        exit_plan = decision.get('exit_plan', '')
                        confidence = decision.get('confidence', 75.0)

                        if action in ['buy', 'sell']:
                            # MANUAL MODE: Create proposal instead of executing
                            if self.execution_mode == "manual":
                                try:
                                    current_price = await self.hyperliquid.get_current_price(instrument)
                                    size = allocation / current_price if current_price > 0 else 0
                                    
                                    # Calculate risk/reward
                                    risk_reward = None
                                    if tp_price and sl_price and current_price:
                                        potential_gain = abs(tp_price - current_price) / current_price
                                        potential_loss = abs(sl_price - current_price) / current_price
                                        if potential_loss > 0:
                                            risk_reward = potential_gain / potential_loss
                                    
                                    proposal = TradeProposal(
                                        asset=instrument,
                                        action=action,
                                        confidence=confidence,
                                        risk_reward=risk_reward,
                                        entry_price=current_price,
                                        tp_price=tp_price,
                                        sl_price=sl_price,
                                        size=size,
                                        allocation=allocation,
                                        rationale=rationale,
                                        market_conditions={
                                            'current_price': current_price,
                                            'exit_plan': exit_plan
                                        }
                                    )
                                    
                                    self.awaiting_proposals.append(proposal)
                                    self.logger.info(f"[PROPOSAL] Created: {action.upper()} {asset} @ ${current_price:,.2f} (ID: {proposal.id[:8]})")
                                    
                                    # Update state with proposals
                                    self.system_state.awaiting_approval = [p.to_dict() for p in self.awaiting_proposals if p.is_pending]
                                    
                                except Exception as e:
                                    self.logger.error(f"Error creating proposal for {asset}: {e}")
                                    
                                continue  # Skip execution in manual mode
                            
                            # AUTO MODE: Execute immediately (original behavior)
                            try:
                                current_price = await self.hyperliquid.get_current_price(instrument)
                                amount = allocation / current_price if current_price > 0 else 0

                                if amount > 0:
                                    # Place market order
                                    if action == 'buy':
                                        order_result = await self.hyperliquid.place_buy_order(instrument, amount)
                                    else:
                                        order_result = await self.hyperliquid.place_sell_order(instrument, amount)

                                    self.logger.info(f"Executed {action} {instrument}: {amount:.6f} @ {current_price}")
                                    
                                    # Send activity event for GUI
                                    if self.on_system_alert:
                                        self.on_system_alert(f"Executed {action.upper()} {instrument}: {amount:.4f} @ ${current_price:,.2f}")

                                    # Wait and check fills
                                    await asyncio.sleep(1)
                                    recent_fills_check = await self.hyperliquid.get_recent_fills(limit=5)
                                    filled = any(
                                        f.get('coin') == instrument and
                                        abs(float(f.get('sz', 0)) - amount) < 0.0001
                                        for f in recent_fills_check
                                    )

                                    # Place TP/SL orders
                                    tp_oid = None
                                    sl_oid = None

                                    if tp_price:
                                        try:
                                            is_buy = (action == 'buy')
                                            tp_order = await self.hyperliquid.place_take_profit(
                                                instrument, is_buy, amount, tp_price
                                            )
                                            oids = self.hyperliquid.extract_oids(tp_order)
                                            tp_oid = oids[0] if oids else None
                                            self.logger.info(f"Placed TP order for {instrument} @ {tp_price}")
                                        except Exception as e:
                                            self.logger.error(f"Failed to place TP: {e}")

                                    if sl_price:
                                        try:
                                            is_buy = (action == 'buy')
                                            sl_order = await self.hyperliquid.place_stop_loss(
                                                instrument, is_buy, amount, sl_price
                                            )
                                            oids = self.hyperliquid.extract_oids(sl_order)
                                            sl_oid = oids[0] if oids else None
                                            self.logger.info(f"Placed SL order for {instrument} @ {sl_price}")
                                        except Exception as e:
                                            self.logger.error(f"Failed to place SL: {e}")

                                    # Update active trades
                                    self.active_trades = [
                                        t for t in self.active_trades if t['asset'] != instrument
                                    ]
                                    self.active_trades.append({
                                        'asset': instrument,
                                        'is_long': (action == 'buy'),
                                        'amount': amount,
                                        'entry_price': current_price,
                                        'tp_oid': tp_oid,
                                        'sl_oid': sl_oid,
                                        'exit_plan': exit_plan,
                                        'opened_at': datetime.now(timezone.utc).isoformat()
                                    })

                                    # Write to journal
                                    self._write_journal_entry({
                                        'timestamp': datetime.now(timezone.utc).isoformat(),
                                        'asset': instrument,
                                        'action': action,
                                        'allocation_usd': allocation,
                                        'amount': amount,
                                        'entry_price': current_price,
                                        'tp_price': tp_price,
                                        'tp_oid': tp_oid,
                                        'sl_price': sl_price,
                                        'sl_oid': sl_oid,
                                        'exit_plan': exit_plan,
                                        'rationale': rationale,
                                        'order_result': str(order_result),
                                        'opened_at': datetime.now(timezone.utc).isoformat(),
                                        'filled': filled
                                    })

                                    # Notify GUI of execution
                                    if self.on_execution_complete:
                                        self.on_execution_complete({
                                            'asset': instrument,
                                            'action': action,
                                            'amount': amount,
                                            'price': current_price,
                                            'timestamp': datetime.now(timezone.utc).isoformat()
                                        })

                                    # Track PnL for Sharpe
                                    # (Simplified - actual PnL tracked on position close)

                            except Exception as e:
                                self.logger.error(f"Error executing {action} for {asset}: {e}")
                                if self.on_system_alert:
                                    self.on_system_alert(f"Trade execution error: {e}")

                        elif action == 'hold':
                            self.logger.info(f"{instrument}: HOLD - {rationale}")
                            
                            # Send activity event for GUI
                            if self.on_system_alert:
                                self.on_system_alert(f"{instrument}: HOLD - {rationale[:50]}...")
                                
                            self._write_journal_entry({
                                'timestamp': datetime.now(timezone.utc).isoformat(),
                                'asset': instrument,
                                'action': 'hold',
                                'rationale': rationale
                            })

                    # Update market intelligence in state for dashboard
                    self.system_state.market_intelligence = market_sections
                    
                    # Update state timestamp
                    self.system_state.last_sync = datetime.now(timezone.utc).isoformat()
                    self._notify_system_update()

                except Exception as e:
                    self.logger.error(f"Error in main loop iteration: {e}", exc_info=True)
                    self.system_state.system_error = str(e)
                    if self.on_system_alert:
                        self.on_system_alert(str(e))

                # ===== PHASE 12: Sleep Until Next Interval =====
                await asyncio.sleep(self._get_interval_seconds())

        except asyncio.CancelledError:
            self.logger.info("Agent loop cancelled")
        except Exception as e:
            self.logger.error(f"Fatal error in agent loop: {e}", exc_info=True)
            self.system_state.system_error = str(e)
            if self.on_system_alert:
                self.on_system_alert(str(e))

    async def _reconcile_active_trades(self, positions: List[Dict], open_orders: List[Dict]):
        """
        Reconcile local active_trades with exchange state.
        Remove stale entries that no longer exist on exchange.
        """
        exchange_assets = {pos.get('coin') for pos in positions}
        order_assets = {o.get('coin') for o in open_orders}
        tracked_assets = exchange_assets | order_assets

        removed = []
        for trade in self.active_trades[:]:
            if trade['asset'] not in tracked_assets:
                self.active_trades.remove(trade)
                removed.append(trade['asset'])

        if removed:
            self.logger.info(f"Reconciled: removed stale trades for {removed}")
            self._write_journal_entry({
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'action': 'reconcile',
                'removed_assets': removed,
                'note': 'Position no longer exists on exchange'
            })

    def _calculate_risk_metric(self, returns: List[float]) -> float:
        """Calculate risk-adjusted performance metric from returns list"""
        if len(returns) < 2:
            return 0.0

        try:
            import statistics
            mean = statistics.mean(returns)
            stdev = statistics.stdev(returns)
            return mean / stdev if stdev > 0 else 0.0
        except Exception:
            return 0.0

    def _get_interval_seconds(self) -> int:
        """Convert interval string to seconds"""
        if self.timeframe.endswith('m'):
            return int(self.timeframe[:-1]) * 60
        elif self.timeframe.endswith('h'):
            return int(self.timeframe[:-1]) * 3600
        elif self.timeframe.endswith('d'):
            return int(self.timeframe[:-1]) * 86400
        return 300  # default 5 minutes

    def _notify_system_update(self):
        """Notify GUI of system state update via callback"""
        if self.on_system_update:
            try:
                self.on_system_update(self.system_state)
            except Exception as e:
                self.logger.error(f"Error in system update callback: {e}")

    def _write_journal_entry(self, entry: Dict):
        """Write entry to journal.jsonl"""
        try:
            with open(self.journal_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=json_default) + "\n")
        except Exception as e:
            self.logger.error(f"Failed to write journal entry: {e}")

    def _load_recent_journal(self, limit: int = 10) -> List[Dict]:
        """Load recent journal entries"""
        if not self.journal_path.exists():
            return []

        try:
            entries = []
            with open(self.journal_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
            return entries[-limit:]
        except Exception as e:
            self.logger.error(f"Failed to load journal: {e}")
            return []

    def get_system_state(self) -> SystemState:
        """Get current system state"""
        return self.system_state

    def get_assets(self) -> List[str]:
        """Get configured instruments"""
        return self.instruments

    def get_interval(self) -> str:
        """Get configured timeframe"""
        return self.timeframe

    async def close_position(self, asset: str) -> bool:
        """
        Manually close a position for given asset.

        Args:
            asset: Asset symbol to close

        Returns:
            True if successful, False otherwise
        """
        try:
            # Cancel all orders for this asset
            await self.hyperliquid.cancel_all_orders(asset)

            # Find position
            for pos in self.system_state.open_positions:
                if pos['symbol'] == asset:
                    quantity = abs(pos['quantity'])
                    if quantity > 0:
                        # Close position (reverse direction)
                        if pos['quantity'] > 0:  # Long position
                            await self.hyperliquid.place_sell_order(asset, quantity)
                        else:  # Short position
                            await self.hyperliquid.place_buy_order(asset, quantity)

                        # Remove from active trades
                        self.active_trades = [
                            t for t in self.active_trades if t['asset'] != asset
                        ]

                        self._write_journal_entry({
                            'timestamp': datetime.now(timezone.utc).isoformat(),
                            'asset': asset,
                            'action': 'manual_close',
                            'quantity': quantity,
                            'note': 'Position closed manually via GUI'
                        })

                        self.logger.info(f"Manually closed position: {asset}")
                        return True

            self.logger.warning(f"No position found to close: {asset}")
            return False

        except Exception as e:
            self.logger.error(f"Failed to close position {asset}: {e}")
            if self.on_system_alert:
                self.on_system_alert(f"Failed to close position: {e}")
            return False
    
    # ===== MANUAL TRADING MODE METHODS =====
    
    def get_pending_proposals(self) -> List[TradeProposal]:
        """Get list of pending trade proposals"""
        return [p for p in self.awaiting_proposals if p.is_pending]
    
    def approve_proposal(self, proposal_id: str) -> bool:
        """
        Approve and execute a trade proposal.
        
        Args:
            proposal_id: ID of the proposal to approve
            
        Returns:
            True if proposal found and approved, False otherwise
        """
        proposal = next((p for p in self.awaiting_proposals if p.id == proposal_id), None)
        
        if not proposal or not proposal.is_pending:
            self.logger.warning(f"Proposal {proposal_id} not found or not pending")
            return False
        
        # Mark as approved
        proposal.approve()
        self.logger.info(f"[APPROVED] Proposal: {proposal.action.upper()} {proposal.asset} (ID: {proposal_id[:8]})")
        
        # Execute asynchronously
        asyncio.create_task(self._execute_proposal(proposal))
        
        # Update state
        self.system_state.awaiting_approval = [p.to_dict() for p in self.awaiting_proposals if p.is_pending]
        self._notify_system_update()
        
        return True
    
    def reject_proposal(self, proposal_id: str, reason: Optional[str] = None) -> bool:
        """
        Reject a trade proposal.
        
        Args:
            proposal_id: ID of the proposal to reject
            reason: Optional reason for rejection
            
        Returns:
            True if proposal found and rejected, False otherwise
        """
        proposal = next((p for p in self.awaiting_proposals if p.id == proposal_id), None)
        
        if not proposal or not proposal.is_pending:
            self.logger.warning(f"Proposal {proposal_id} not found or not pending")
            return False
        
        # Mark as rejected
        proposal.reject(reason or "Rejected by user")
        self.logger.info(f"[REJECTED] Proposal: {proposal.action.upper()} {proposal.asset} (ID: {proposal_id[:8]})")
        
        # Write to journal
        self._write_journal_entry({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'asset': proposal.asset,
            'action': 'proposal_rejected',
            'proposal_id': proposal_id,
            'reason': reason,
            'rationale': proposal.rationale
        })
        
        # Update state
        self.system_state.awaiting_approval = [p.to_dict() for p in self.awaiting_proposals if p.is_pending]
        self._notify_system_update()
        
        return True
    
    async def _execute_proposal(self, proposal: TradeProposal):
        """
        Execute an approved trade proposal.
        
        Args:
            proposal: The approved proposal to execute
        """
        try:
            self.logger.info(f"Executing proposal: {proposal.action.upper()} {proposal.asset}")
            
            # Get fresh price
            current_price = await self.hyperliquid.get_current_price(proposal.asset)
            amount = proposal.size
            
            if amount <= 0:
                raise ValueError(f"Invalid amount: {amount}")
            
            # Place market order
            if proposal.action == 'buy':
                order_result = await self.hyperliquid.place_buy_order(proposal.asset, amount)
            elif proposal.action == 'sell':
                order_result = await self.hyperliquid.place_sell_order(proposal.asset, amount)
            else:
                raise ValueError(f"Invalid action: {proposal.action}")
            
            self.logger.info(f"Order placed: {proposal.action} {proposal.asset}: {amount:.6f} @ {current_price}")
            
            # Wait and check fills
            await asyncio.sleep(1)
            recent_fills = await self.hyperliquid.get_recent_fills(limit=5)
            filled = any(
                f.get('coin') == proposal.asset and
                abs(float(f.get('sz', 0)) - amount) < 0.0001
                for f in recent_fills
            )
            
            # Place TP/SL if specified
            tp_oid = None
            sl_oid = None
            
            if proposal.tp_price:
                try:
                    is_buy = (proposal.action == 'buy')
                    tp_order = await self.hyperliquid.place_take_profit(
                        proposal.asset, is_buy, amount, proposal.tp_price
                    )
                    oids = self.hyperliquid.extract_oids(tp_order)
                    tp_oid = oids[0] if oids else None
                    self.logger.info(f"Placed TP order @ {proposal.tp_price}")
                except Exception as e:
                    self.logger.error(f"Failed to place TP: {e}")
            
            if proposal.sl_price:
                try:
                    is_buy = (proposal.action == 'buy')
                    sl_order = await self.hyperliquid.place_stop_loss(
                        proposal.asset, is_buy, amount, proposal.sl_price
                    )
                    oids = self.hyperliquid.extract_oids(sl_order)
                    sl_oid = oids[0] if oids else None
                    self.logger.info(f"Placed SL order @ {proposal.sl_price}")
                except Exception as e:
                    self.logger.error(f"Failed to place SL: {e}")
            
            # Update active trades
            self.active_trades = [
                t for t in self.active_trades if t['asset'] != proposal.asset
            ]
            self.active_trades.append({
                'asset': proposal.asset,
                'is_long': (proposal.action == 'buy'),
                'amount': amount,
                'entry_price': current_price,
                'tp_oid': tp_oid,
                'sl_oid': sl_oid,
                'exit_plan': proposal.market_conditions.get('exit_plan', ''),
                'opened_at': datetime.now(timezone.utc).isoformat(),
                'from_proposal': proposal.id
            })
            
            # Mark proposal as executed
            proposal.mark_executed(current_price)
            
            # Write to journal
            self._write_journal_entry({
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'asset': proposal.asset,
                'action': proposal.action,
                'allocation_usd': proposal.allocation,
                'amount': amount,
                'entry_price': current_price,
                'tp_price': proposal.tp_price,
                'tp_oid': tp_oid,
                'sl_price': proposal.sl_price,
                'sl_oid': sl_oid,
                'rationale': proposal.rationale,
                'order_result': str(order_result),
                'filled': filled,
                'from_proposal': proposal.id,
                'approved_manually': True
            })
            
            # Notify GUI
            if self.on_execution_complete:
                self.on_execution_complete({
                    'asset': proposal.asset,
                    'action': proposal.action,
                    'amount': amount,
                    'price': current_price,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'from_proposal': True
                })
            
            self.logger.info(f"[SUCCESS] Proposal executed: {proposal.id[:8]}")
            
        except Exception as e:
            self.logger.error(f"Failed to execute proposal {proposal.id}: {e}")
            proposal.mark_failed(str(e))
            
            if self.on_system_alert:
                self.on_system_alert(f"Failed to execute trade: {e}")
        
        finally:
            # Update state
            self.system_state.awaiting_approval = [p.to_dict() for p in self.awaiting_proposals if p.is_pending]
            self._notify_system_update()
