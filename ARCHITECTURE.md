# QuantumAlpha Capital - System Architecture & Technical Documentation

This document provides a comprehensive technical overview of the QuantumAlpha Capital systematic trading platform architecture, including system design, data flow, and implementation details.

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    QuantumAlpha Capital System                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   GUI Layer     │  │  Backend Core   │  │  External APIs  │ │
│  │   (NiceGUI)     │  │   (AsyncIO)     │  │   (REST/WS)     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│           │                     │                     │         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ State Manager   │  │ Trading Engine  │  │ Market Data     │ │
│  │ (Real-time)     │  │ (Decision Loop) │  │ (TAAPI/HL)      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│           │                     │                     │         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Database      │  │   AI Agent      │  │   Risk Mgmt     │ │
│  │  (SQLAlchemy)   │  │  (LLM Client)   │  │  (Position)     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Core Components

### 1. **Trading Engine** (`src/backend/bot_engine.py`)

The heart of the system, responsible for:
- **Main Trading Loop**: 5-minute interval execution cycle
- **State Management**: Account, positions, and market data tracking
- **Order Execution**: Market orders with stop-loss/take-profit
- **Performance Tracking**: Real-time P&L and analytics

#### Key Classes & Methods

```python
class QuantumMarketProcessor:
    async def initialize_processing()    # Initialize and start processing loop
    async def terminate_processing()     # Graceful shutdown
    async def _quantum_processing_loop() # Core market analysis cycle
    async def close_position()           # Manual position management
    
    # Manual execution mode
    def approve_proposal()               # Execute pending execution
    def reject_proposal()                # Reject execution proposal
```

#### Trading Loop Flow

```
1. Fetch Account State (balance, positions, orders)
   ↓
2. Gather Market Data (prices, indicators, funding)
   ↓  
3. Build AI Context (structured data for LLM)
   ↓
4. Get AI Decision (trade recommendations)
   ↓
5. Execute Trades (market orders + risk management)
   ↓
6. Update State (positions, performance, logs)
   ↓
7. Sleep Until Next Interval (5 minutes default)
```

### 2. **AI Decision Maker** (`src/backend/agent/decision_maker.py`)

Interfaces with large language models for trading decisions:
- **LLM Integration**: OpenRouter API with multiple model support
- **Structured Output**: JSON schema enforcement for reliable parsing
- **Tool Calling**: Dynamic indicator fetching during analysis
- **Retry Logic**: Robust error handling and fallback mechanisms

#### Key Features

```python
class QuantumDecisionEngine:
    def synthesize_market_decisions()    # Main decision entry point
    def _process_neural_analysis()       # Core LLM interaction
    def _sanitize_output()               # Output validation and cleanup
    def _build_schema()                  # JSON schema generation
```

#### AI System Prompt Structure

```
1. Role Definition: "Elite quantitative portfolio strategist and systems engineer"
2. Profit Optimization: "SYSTEMATIC PROFIT EXTRACTION via algorithmic alpha generation"
3. Strategy Guidelines: Bidirectional momentum, systematic scalping, swing optimization
4. Risk Management: Leverage scaling, systematic position sizing, risk termination
5. Output Contract: Strict JSON format with neural reasoning + systematic decisions
```

### 3. **Exchange Integration** (`src/backend/trading/hyperliquid_api.py`)

Hyperliquid API wrapper with enterprise-grade reliability:
- **SDK Wrapper**: High-level interface over Hyperliquid SDK
- **Retry Logic**: Exponential backoff for network failures
- **Order Management**: Market, limit, stop-loss, take-profit orders
- **Account State**: Real-time balance and position tracking

#### Key Methods

```python
class HyperliquidAPI:
    # Order Management
    async def place_buy_order()     # Market buy with slippage
    async def place_sell_order()    # Market sell with slippage
    async def place_take_profit()   # TP trigger order
    async def place_stop_loss()     # SL trigger order
    
    # Account & Market Data
    async def get_user_state()      # Account balance & positions
    async def get_current_price()   # Real-time asset prices
    async def get_open_interest()   # Market OI data
    async def get_funding_rate()    # Funding rates
```

### 4. **GUI Application** (`src/gui/`)

Modern desktop interface built with NiceGUI:
- **Real-time Dashboard**: Live performance and market data
- **Manual Trading**: Trade proposal approval system
- **Settings Management**: Configuration and API key management
- **Analytics**: Performance charts and trade history

#### Component Structure

```
src/gui/
├── app.py              # Main application and routing
├── components/         # Reusable UI components
│   ├── header.py      # Navigation and status
│   ├── charts.py      # Performance visualizations
│   └── tables.py      # Data tables and grids
├── pages/             # Application pages
│   ├── dashboard.py   # Main trading dashboard
│   ├── settings.py    # Configuration management
│   ├── reasoning.py   # AI decision analysis
│   └── manual.py      # Manual trading interface
└── services/          # Business logic services
    ├── agent_service.py # Trading agent interface
    └── state_manager.py # UI state management
```

---

## 📊 Data Flow Architecture

### 1. **Market Data Pipeline**

```
External APIs → Data Aggregation → Indicator Calculation → AI Analysis
     ↓               ↓                    ↓                  ↓
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Hyperliquid │ │   TAAPI     │ │ Local Cache │ │ LLM Context │
│   (Price)   │ │(Indicators) │ │ (History)   │ │ (Decision)  │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

#### Data Sources

- **Hyperliquid API**: Real-time prices, positions, orders, funding
- **TAAPI.io**: Technical indicators (EMA, MACD, RSI, ATR)
- **Local Cache**: Price history, performance metrics, trade logs

### 2. **Decision Flow**

```
Market Data → AI Context → LLM Analysis → Trade Decision → Order Execution
     ↓            ↓           ↓             ↓              ↓
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Structured  │ │   JSON      │ │ Reasoning   │ │ Validated   │ │ Exchange    │
│    Data     │ │  Payload    │ │ + Actions   │ │ Parameters  │ │   Orders    │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

### 3. **State Management**

```python
@dataclass
class SystemState:
    # Core Status
    active_status: bool = False
    account_balance: float = 0.0
    portfolio_value: float = 0.0
    performance_ratio: float = 0.0
    
    # Market Operations
    open_positions: List[Dict] = field(default_factory=list)
    managed_positions: List[Dict] = field(default_factory=list)
    pending_orders: List[Dict] = field(default_factory=list)
    
    # Intelligence
    market_intelligence: List[Dict] = field(default_factory=list)
    neural_reasoning: Dict = field(default_factory=dict)
    
    # Manual Mode
    awaiting_approval: List[Dict] = field(default_factory=list)
```

---

## 🔄 Async Architecture

### Event Loop Design

The system uses Python's `asyncio` for concurrent operations:

```python
# Main Components Running Concurrently
async def main():
    # 1. Trading Engine (main loop)
    trading_task = asyncio.create_task(bot_engine.start())
    
    # 2. GUI Application (user interface)  
    gui_task = asyncio.create_task(ui.run())
    
    # 3. Market Data Streams (real-time updates)
    data_task = asyncio.create_task(market_data_stream())
    
    # Wait for all components
    await asyncio.gather(trading_task, gui_task, data_task)
```

### Concurrency Patterns

1. **Producer-Consumer**: Market data → Trading decisions
2. **Observer Pattern**: State changes → GUI updates
3. **Request-Response**: User actions → Agent responses
4. **Background Tasks**: Periodic data fetching and cleanup

---

## 🗄️ Database Architecture

### SQLAlchemy Models

```python
# Core Trading Entities
class Trade(Base):
    id: int
    asset: str
    action: str  # buy/sell/hold
    entry_price: float
    exit_price: Optional[float]
    quantity: float
    pnl: Optional[float]
    timestamp: datetime

class Position(Base):
    id: int
    asset: str
    quantity: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    
class MarketData(Base):
    id: int
    asset: str
    price: float
    volume: float
    timestamp: datetime
```

### Migration System

```bash
# Database operations
python scripts/migrate_to_database.py  # JSONL → SQLite migration
```

---

## 🔐 Security Architecture

### API Key Management

```python
# Environment-based configuration
CONFIG = {
    "hyperliquid_private_key": os.getenv("HYPERLIQUID_PRIVATE_KEY"),
    "openrouter_api_key": os.getenv("OPENROUTER_API_KEY"),
    "taapi_api_key": os.getenv("TAAPI_API_KEY")
}

# Validation and encryption
def validate_credentials():
    if not all([private_key, api_key]):
        raise ValueError("Missing required credentials")
```

### Risk Controls

```python
# Position size limits
MAX_POSITION_SIZE = 0.5  # 50% of account
MAX_LEVERAGE = 10
MAX_DAILY_LOSS = 0.1     # 10% daily loss limit

# Order validation
def validate_order(asset, size, price):
    if size > MAX_POSITION_SIZE * account_balance:
        raise ValueError("Position size exceeds limit")
```

---

## 📈 Performance Optimization

### Caching Strategy

```python
# Market data caching
@lru_cache(maxsize=1000)
def get_indicator_data(asset, timeframe, indicator):
    return taapi_client.fetch(asset, timeframe, indicator)

# Price history buffering
price_history = {
    asset: deque(maxlen=1000) for asset in ASSETS
}
```

### Rate Limiting

```python
# TAAPI rate limits (1 req/15s on free plan)
async def fetch_with_rate_limit():
    await asyncio.sleep(15)  # Respect rate limits
    return await api_call()
```

### Memory Management

- **Circular Buffers**: Limited history storage with `deque(maxlen=N)`
- **Lazy Loading**: Load data only when needed
- **Garbage Collection**: Periodic cleanup of old data
- **Connection Pooling**: Reuse HTTP connections

---

## 🔧 Configuration Management

### Environment Variables

```bash
# Trading Configuration
ASSETS=BTC ETH LTC                    # Space-separated assets
INTERVAL=5m                           # Trading interval
TRADING_MODE=auto                     # auto/manual mode
LLM_MODEL=deepseek/deepseek-chat-v3.1 # AI model

# API Keys
HYPERLIQUID_PRIVATE_KEY=0x1234567890abcdef...         # Trading wallet
OPENROUTER_API_KEY=sk-or-v1-your-key-here       # AI model access
TAAPI_API_KEY=eyJhbGci...your-jwt-token-here             # Technical indicators

# Risk Management
MAX_POSITION_SIZE=0.5                 # 50% max allocation
MAX_LEVERAGE=10                       # Maximum leverage
STOP_LOSS_PCT=0.02                    # 2% max risk per trade
```

### Dynamic Configuration

```python
# Runtime configuration updates
def update_config(key, value):
    CONFIG[key] = value
    save_config()  # Persist changes
    notify_components()  # Update running components
```

---

## 🚀 Deployment Architecture

### Local Development

```bash
# Development setup
git clone <repository>
cd quantumalpha-capital
pip install -r requirements.txt
cp .env.example .env  # Configure API keys
python main.py        # Start application
```

### Production Deployment

```bash
# Production considerations
- Dedicated server/VPS for 24/7 operation
- Process monitoring (systemd, supervisor)
- Log rotation and monitoring
- Backup strategies for database
- Network redundancy for API access
```

### Docker Containerization

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

---

## 📊 Monitoring & Observability

### Logging Architecture

```python
# Multi-level logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("quantumalpha.log"),      # File logging
        logging.StreamHandler()              # Console output
    ]
)

# Specialized logs
- quantumalpha.log: General application logs
- llm_requests.log: AI model interactions
- data/prompts.log: Trading decision context
- data/diary.jsonl: Trade execution history
```

### Performance Metrics

```python
# Real-time metrics
class PerformanceTracker:
    def track_trade(self, trade):
        self.total_trades += 1
        self.total_pnl += trade.pnl
        self.update_sharpe_ratio()
        self.update_drawdown()
        
    def get_metrics(self):
        return {
            "total_return": self.total_pnl,
            "sharpe_ratio": self.sharpe_ratio,
            "max_drawdown": self.max_drawdown,
            "win_rate": self.wins / self.total_trades
        }
```

---

## 🔮 Extensibility & Future Architecture

### Plugin System

```python
# Strategy plugin interface
class TradingStrategy:
    def analyze(self, market_data) -> Signal:
        raise NotImplementedError
        
    def risk_management(self, signal) -> Position:
        raise NotImplementedError

# Plugin registration
strategy_registry = {
    "momentum": MomentumStrategy(),
    "scalping": ScalpingStrategy(),
    "swing": SwingStrategy()
}
```

### Multi-Exchange Support

```python
# Exchange abstraction
class ExchangeInterface:
    async def place_order(self, order) -> OrderResult:
        raise NotImplementedError
        
    async def get_balance(self) -> Balance:
        raise NotImplementedError

# Exchange implementations
exchanges = {
    "hyperliquid": HyperliquidAPI(),
    "binance": BinanceAPI(),      # Future
    "bybit": BybitAPI()           # Future
}
```

### Microservices Architecture (Future)

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Trading   │  │   Market    │  │     AI      │
│   Service   │  │    Data     │  │   Service   │
│             │  │   Service   │  │             │
└─────────────┘  └─────────────┘  └─────────────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
              ┌─────────────┐
              │   Message   │
              │    Queue    │
              │  (Redis)    │
              └─────────────┘
```

---

## 📚 Technical Dependencies

### Core Libraries

```python
# Trading & Market Data
hyperliquid-python-sdk==0.1.9    # Exchange integration
requests==2.31.0                 # HTTP client
aiohttp==3.9.1                   # Async HTTP

# AI & ML
openai==1.3.0                    # LLM integration (via OpenRouter)
numpy==1.24.3                    # Numerical computing
pandas==2.0.3                    # Data analysis

# GUI & Interface  
nicegui==1.4.21                  # Desktop GUI framework
plotly==5.17.0                   # Interactive charts

# Database & Storage
sqlalchemy==2.0.23               # ORM
alembic==1.13.1                  # Database migrations

# Utilities
python-dotenv==1.0.0             # Environment management
eth-account==0.9.0               # Ethereum wallet utilities
```

### System Requirements

- **Python**: 3.9+ (async/await, type hints)
- **Memory**: 512MB+ (GUI + data caching)
- **Storage**: 1GB+ (logs, database, history)
- **Network**: Stable internet (API reliability)
- **OS**: Windows/macOS/Linux (cross-platform)

---

*This architecture is designed for scalability, reliability, and maintainability. The modular design allows for easy extension and customization while maintaining robust error handling and performance optimization.*