# Setup Guide - QuantumAlpha Capital

This guide will walk you through setting up and configuring QuantumAlpha Capital for automated systematic alpha generation on Hyperliquid.

---

## 📋 Prerequisites

### System Requirements
- **Python 3.9+** (with pip)
- **4GB+ RAM** (for GUI and data processing)
- **Stable Internet Connection** (for API reliability)
- **Operating System**: Windows 10+, macOS 10.14+, or Linux

### Required Accounts & API Keys

1. **Hyperliquid Account**
   - Create account at [hyperliquid.xyz](https://hyperliquid.xyz)
   - Generate API wallet or use existing wallet private key
   - Fund account with USDC for trading

2. **OpenRouter Account** 
   - Sign up at [openrouter.ai](https://openrouter.ai)
   - Add credits to your account ($10+ recommended)
   - Generate API key for model access

3. **TAAPI Account**
   - Register at [taapi.io](https://taapi.io)
   - Free plan supports BTC, ETH, XRP, LTC, XMR
   - Get your API key from dashboard

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone <your-repository-url>
cd quantumalpha-capital
```

### 2. Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python test_installation.py
```

### 3. Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit configuration file
nano .env  # or use your preferred editor
```

---

## ⚙️ Configuration

### Environment Variables (.env)

#### Required Settings

```env
# Hyperliquid API Configuration
HYPERLIQUID_PRIVATE_KEY=0x1234567890abcdef...              # Your wallet private key
HYPERLIQUID_ACCOUNT_ADDRESS=0x5678...          # Your main account address

# AI Model Access  
OPENROUTER_API_KEY=sk-or-v1-your-key-here               # OpenRouter API key

# Technical Analysis
TAAPI_API_KEY=eyJhbGci...your-jwt-token-here                     # TAAPI.io API key
```

#### Trading Settings

```env
# Assets to trade (space-separated)
ASSETS=BTC ETH LTC

# Trading interval
INTERVAL=5m                    # 5m, 15m, 1h, 4h

# Execution mode
TRADING_MODE=auto              # auto or manual

# AI model selection
LLM_MODEL=deepseek/deepseek-chat-v3.1
```

### API Key Setup Guide

#### 1. Hyperliquid Setup

**Option A: Use Existing Wallet**
```bash
# Export private key from MetaMask/wallet
HYPERLIQUID_PRIVATE_KEY=0x1234567890abcdef...
HYPERLIQUID_ACCOUNT_ADDRESS=0x9876543210fedcba...
```

**Option B: Generate New API Wallet**
```bash
# Create dedicated trading wallet
# Fund with small amount for testing
HYPERLIQUID_PRIVATE_KEY=0xnew_wallet_key...
HYPERLIQUID_ACCOUNT_ADDRESS=0xmain_account...
```

#### 2. OpenRouter Setup

```bash
# 1. Visit https://openrouter.ai
# 2. Sign up and verify email
# 3. Add credits ($10+ recommended)
# 4. Generate API key in dashboard
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

**Recommended Models:**
- `deepseek/deepseek-chat-v3.1` (Best performance, $0.14/1M tokens)
- `openai/gpt-4o-mini` (Fast and cheap, $0.15/1M tokens)
- `anthropic/claude-3-haiku` (Good reasoning, $0.25/1M tokens)

#### 3. TAAPI Setup

```bash
# 1. Register at https://taapi.io
# 2. Verify email and login
# 3. Copy API key from dashboard
TAAPI_API_KEY=eyJhbGci...your-jwt-token-here
```

**Free Plan Limitations:**
- 1 request per 15 seconds
- Supports: BTC, ETH, XRP, LTC, XMR only
- 500 requests per month

---

## 🎯 Initial Setup & Testing

### 1. Test Installation

```bash
# Run installation test
python test_installation.py

# Expected output:
# ✅ Python version: 3.9+
# ✅ All dependencies installed
# ✅ Configuration file found
# ✅ API keys configured
```

### 2. Validate API Connections

```bash
# Start agent in test mode
python main.py

# Check logs for connection status:
# ✅ Hyperliquid connection established
# ✅ OpenRouter API accessible  
# ✅ TAAPI indicators loading
```

### 3. Paper Trading Test

```bash
# Set to manual mode for testing
TRADING_MODE=manual

# Start agent and observe:
# - Market data loading
# - AI generating trade proposals
# - Manual approval interface working
```

---

## 🛡️ Security Best Practices

### Wallet Security

```bash
# 1. Use dedicated trading wallet
# 2. Limit funds to acceptable loss amount
# 3. Never share private keys
# 4. Use hardware wallet for main funds
# 5. Regular security audits
```

### API Key Protection

```bash
# 1. Store keys in .env file only
# 2. Never commit .env to version control
# 3. Use environment variables in production
# 4. Rotate keys regularly
# 5. Monitor API usage
```

### Risk Management

```bash
# Set conservative limits initially
MAX_POSITION_SIZE=0.2          # 20% max per trade
MAX_LEVERAGE=5                 # 5x max leverage
STOP_LOSS_PCT=0.01            # 1% max risk per trade
```

---

## 🚀 Running the Agent

### Development Mode

```bash
# Start with full logging
python main.py

# Monitor logs in separate terminal
tail -f quantumalpha.log
```

### Production Mode

```bash
# Run as background service (Linux/macOS)
nohup python main.py > output.log 2>&1 &

# Or use screen/tmux
screen -S trading-bot
python main.py
# Ctrl+A, D to detach
```

### Windows Service

```bash
# Install as Windows service (optional)
pip install pywin32
python -m win32serviceutil InstallService trading_bot_service.py
```

---

## 📊 Monitoring & Maintenance

### Real-Time Monitoring

1. **GUI Dashboard**: Real-time performance and positions
2. **Log Files**: `quantumalpha.log` for system events
3. **Trade Journal**: `data/diary.jsonl` for trade history
4. **Performance Metrics**: Sharpe ratio, drawdown, win rate

### Daily Maintenance

```bash
# Check system status
ps aux | grep python              # Verify agent running
tail -n 50 quantumalpha.log               # Recent log entries
df -h                            # Disk space
free -m                          # Memory usage
```

### Weekly Reviews

1. **Performance Analysis**: Review P&L and metrics
2. **Strategy Adjustment**: Modify parameters if needed
3. **Risk Assessment**: Ensure position sizes appropriate
4. **System Updates**: Update dependencies if needed

---

## 🔧 Troubleshooting

### Common Issues

#### 1. API Connection Errors

```bash
# Error: "Invalid API key"
# Solution: Verify API keys in .env file
# Check: Key format, expiration, account status

# Error: "Rate limit exceeded"  
# Solution: Reduce trading frequency
# Check: TAAPI free plan limits (1 req/15s)
```

#### 2. Trading Execution Issues

```bash
# Error: "Insufficient balance"
# Solution: Fund Hyperliquid account
# Check: USDC balance in Perps wallet

# Error: "Position size too large"
# Solution: Reduce MAX_POSITION_SIZE
# Check: Risk management settings
```

#### 3. GUI Problems

```bash
# Error: "Port already in use"
# Solution: Kill existing process
# Command: pkill -f "python main.py"

# Error: "Display not found"
# Solution: Enable X11 forwarding (Linux)
# Command: export DISPLAY=:0
```

### Debug Mode

```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG
python main.py

# Check specific components
python -c "from src.backend.trading.hyperliquid_api import HyperliquidAPI; api = HyperliquidAPI()"
```

### Log Analysis

```bash
# Search for errors
grep -i error quantumalpha.log

# Monitor real-time
tail -f quantumalpha.log | grep -i "trade\|error\|warning"

# Performance metrics
grep -i "sharpe\|return\|drawdown" quantumalpha.log
```

---

## 📈 Performance Optimization

### System Optimization

```bash
# Increase file descriptor limits
ulimit -n 4096

# Optimize Python performance
export PYTHONOPTIMIZE=1

# Use faster JSON library (optional)
pip install orjson
```

### Trading Optimization

```bash
# Reduce API calls
INTERVAL=15m                   # Longer intervals

# Optimize position sizing
MAX_POSITION_SIZE=0.3          # Larger positions, fewer trades

# Use faster models
LLM_MODEL=openai/gpt-4o-mini   # Faster response times
```

---

## 🔄 Updates & Maintenance

### Updating the Agent

```bash
# Backup current configuration
cp .env .env.backup
cp -r data data.backup

# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restore configuration
cp .env.backup .env
```

### Database Maintenance

```bash
# Backup database
cp data/quantumalpha.db data/quantumalpha.db.backup

# Migrate to new schema (if needed)
python scripts/migrate_to_database.py

# Vacuum database (monthly)
sqlite3 data/quantumalpha.db "VACUUM;"
```

---

## 📞 Support & Resources

### Documentation
- [README.md](README.md) - Project overview
- [TRADING_STRATEGIES.md](TRADING_STRATEGIES.md) - Strategy details
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture

### Community
- GitHub Issues - Bug reports and feature requests
- Discussions - Strategy sharing and questions

### External Resources
- [Hyperliquid Docs](https://hyperliquid.gitbook.io/) - Exchange API documentation
- [OpenRouter Models](https://openrouter.ai/models) - Available AI models
- [TAAPI Indicators](https://taapi.io/indicators/) - Technical indicator reference

---

## ⚠️ Important Disclaimers

### Risk Warning
- **Cryptocurrency trading involves substantial risk**
- **Past performance does not guarantee future results**
- **Only trade with funds you can afford to lose**
- **Start with small amounts and paper trading**

### Liability
- This software is provided "as is" without warranty
- Users are responsible for their own trading decisions
- Developers are not liable for any financial losses
- Always understand the risks before automated trading

---

*Setup complete! Your QuantumAlpha Capital systematic trading platform is ready to analyze markets and execute trades. Start with manual mode and small positions to familiarize yourself with the system.*