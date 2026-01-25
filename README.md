# QuantumAlpha Capital

A Python-based algorithmic multi-analyst trading platform for cryptocurrency perpetual futures on Hyperliquid exchange. Features AI-powered market analysis, real-time technical indicators, and automated trade execution with risk management.

<img width="1512" height="982" alt="Screenshot 2026-01-19 at 7 20 01 AM" src="https://github.com/user-attachments/assets/09a6b381-292f-4f55-98e7-3634783d3b95" />
<img width="1512" height="982" alt="Screenshot 2026-01-19 at 7 20 08 AM" src="https://github.com/user-attachments/assets/a4778bd8-bb18-4abc-b86f-6c27dd036eeb" />

---

## Features

- **Automated Trading**: Systematic trade execution on Hyperliquid perpetual futures
- **Multi-Analyst AI System**: 4-specialist ensemble (Technical, ML, Risk, Quant) with judge consensus
- **AI Integration**: Multiple LLM providers (OpenRouter) for market analysis and decision making
- **Technical Analysis**: Real-time RSI, MACD, EMA indicators via TAAPI.io
- **Risk Management**: Position sizing, stop-loss, take-profit automation
- **GUI Dashboard**: Real-time portfolio monitoring with live charts and analyst insights
- **Multi-Asset Support**: BTC, ETH, LTC perpetual futures trading

## Architecture

### Core Components

- **Market Processor** (`src/backend/bot_engine.py`): Main trading loop with 5-minute cycles
- **Multi-Analyst System** (`src/backend/analysts/`): 4-specialist ensemble with judge consensus
- **Decision Engine** (`src/backend/agent/decision_maker.py`): AI-powered trade signal generation
- **Exchange API** (`src/backend/trading/hyperliquid_api.py`): Hyperliquid integration
- **GUI Interface** (`src/gui/`): NiceGUI-based dashboard with real-time updates
- **Technical Analysis** (`src/backend/indicators/`): TAAPI.io client with caching

### Data Flow

```
TAAPI.io → Technical Indicators → Multi-Analyst System → Judge Consensus → Trade Signals → Hyperliquid Execution
    ↓              ↓                       ↓                    ↓              ↓              ↓
Market Data → Portfolio State → Analyst Insights → GUI Dashboard → User Interface → Trade Management
```

### Multi-Analyst System

The platform features a sophisticated 4-analyst ensemble system:

- **Technical Analyst**: Price action, chart patterns, technical indicators
- **ML Analyst**: Machine learning models and AI-based predictions  
- **Risk Analyst**: Risk management, position sizing, portfolio optimization
- **Quant Analyst**: Statistical models, market microstructure analysis

Each analyst provides independent recommendations which are evaluated by a **Judge** system that determines the final consensus decision based on confidence levels and market conditions.

## Installation

### Requirements

- Python 3.9+
- Hyperliquid account with API access
- OpenRouter API key for AI models
- TAAPI.io subscription for technical indicators

### Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/LoopGlitch26/QuantumAlpha-Capital.git
   cd QuantumAlpha-Capital
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run Application**
   ```bash
   python main.py
   ```

## Configuration

### Environment Variables

```env
# Trading Configuration
INSTRUMENTS=BTC ETH LTC                    # Assets to trade
ANALYSIS_TIMEFRAME=5m                      # Analysis frequency
EXECUTION_MODE=systematic                  # systematic/manual
AI_MODEL=deepseek/deepseek-chat-v3.1      # AI model selection
USE_MULTI_ANALYST=true                     # Enable 4-analyst ensemble system

# API Keys
HYPERLIQUID_PRIVATE_KEY=your_key          # Trading wallet private key
OPENROUTER_API_KEY=your_key               # AI model access
TAAPI_API_KEY=your_key                    # Technical analysis data

# Network
HYPERLIQUID_NETWORK=mainnet               # mainnet/testnet
```

### Trading Parameters

- **Position Sizing**: Configurable allocation per asset
- **Leverage**: 1-10x leverage on perpetual futures
- **Risk Management**: Stop-loss and take-profit automation
- **Execution Modes**: Systematic (auto) or manual approval

## Technical Specifications

### AI Models Supported

- DeepSeek Chat V3.1 (recommended)
- OpenAI GPT-4/GPT-4o
- Anthropic Claude 3.5
- Google Gemini Pro
- Meta Llama models

### Technical Indicators

- **Trend**: EMA 20/50 (5m and 4h timeframes)
- **Momentum**: RSI 7/14, MACD
- **Volatility**: ATR 3/14
- **Volume**: Real-time volume analysis

### Exchange Features

- **Hyperliquid Perpetuals**: BTC-USD, ETH-USD, LTC-USD
- **Order Types**: Market, limit orders
- **Position Management**: Long/short positions
- **Real-time Data**: WebSocket price feeds

## GUI Dashboard

### Components

- **Portfolio Metrics**: Balance, PnL, Sharpe ratio, active positions
- **Multi-Analyst Intelligence**: Real-time insights from 4 specialist analysts with judge consensus
- **Technical Charts**: Price, RSI, MACD with real-time updates
- **Position Management**: Open positions with risk metrics
- **Trade Proposals**: AI-generated recommendations with approval workflow
- **Market Intelligence**: Multi-asset price and indicator data

### Update Frequencies

- **Main Dashboard**: 3-second refresh cycle
- **Technical Charts**: 1-second updates
- **Market Data**: 5-minute collection cycle

## Development

### Project Structure

```
src/
├── backend/
│   ├── agent/           # AI decision making
│   ├── analysts/        # Multi-analyst ensemble system
│   ├── core/            # Portfolio optimization
│   ├── indicators/      # Technical analysis
│   ├── trading/         # Exchange integration
│   └── utils/           # Helper functions
├── gui/
│   ├── components/      # Reusable UI widgets
│   ├── pages/           # Dashboard pages
│   ├── services/        # Data services
│   └── themes/          # UI styling
└── database/            # Data persistence
```

### Key Dependencies

- **NiceGUI**: Web-based GUI framework
- **aiohttp**: Async HTTP client for APIs
- **plotly**: Interactive charting
- **sqlite3**: Local data storage
- **cryptography**: Wallet operations

## Risk Warnings

- **Financial Risk**: Cryptocurrency trading involves substantial risk of loss
- **API Security**: Protect your private keys and API credentials
- **Testing**: Use testnet for initial testing and development
- **Capital**: Only trade with funds you can afford to lose

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Documentation

- [SETUP.md](SETUP.md) - Detailed installation guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [TRADING_STRATEGIES.md](TRADING_STRATEGIES.md) - Strategy documentation
- [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) - Security guidelines

