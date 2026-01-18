"""Decision-making agent that orchestrates LLM prompts and indicator lookups."""

import requests
from src.backend.config_loader import CONFIG
from src.backend.indicators.taapi_client import TAAPIClient
import json
import logging
from datetime import datetime

class QuantumDecisionEngine:
    """Advanced AI-powered market analysis and decision synthesis system."""

    def __init__(self):
        """Initialize neural network configuration, API endpoints, and market data processors."""
        self.model = CONFIG["llm_model"]
        self.api_key = CONFIG["openrouter_api_key"]
        base = CONFIG["openrouter_base_url"]
        self.base_url = f"{base}/chat/completions"
        self.referer = CONFIG.get("openrouter_referer")
        self.app_title = CONFIG.get("openrouter_app_title")
        self.taapi = TAAPIClient()
        # Fast/cheap sanitizer model to normalize outputs on parse failures
        self.sanitize_model = CONFIG.get("sanitize_model") or "openai/gpt-5"

        # Warn if using a model that may not support tools
        if ":free" in self.model.lower() or "deepseek" in self.model.lower():
            logging.info(f"[INFO] Using model {self.model} - dynamic tool use may not be available. Agent will work with pre-fetched indicators only.")

    def synthesize_market_decisions(self, assets, context):
        """Synthesize optimal market positions across multiple asset classes.

        Args:
            assets: Portfolio of tradeable instruments for analysis.
            context: Comprehensive market intelligence and account metrics.

        Returns:
            Structured decision matrix with risk-adjusted position recommendations.
        """
        return self._process_neural_analysis(context, assets=assets)

    def _process_neural_analysis(self, context, assets):
        """Execute advanced neural processing pipeline for market intelligence synthesis."""
        system_prompt = (
            "You are an elite QUANTITATIVE PORTFOLIO STRATEGIST and advanced MATHEMATICAL SYSTEMS ENGINEER specializing in algorithmic alpha generation through multi-dimensional market analysis.\n"
            "Your mission: Execute SYSTEMATIC PROFIT EXTRACTION via sophisticated quantitative models across perpetual futures markets.\n"
            f"- target_instruments = {json.dumps(assets)}\n"
            "- multi_timeframe_analytics (5m precision entries, 4h macro trend validation)\n"
            "- active_position_management with dynamic exit protocols\n"
            "- historical_performance_metrics and risk-adjusted returns\n\n"
            "Utilize the 'current_timestamp' from user context for all temporal calculations including cooldown periods and exit schedule evaluations.\n\n"
            "SYSTEMATIC ALPHA GENERATION FRAMEWORK:\n"
            "Execute AGGRESSIVE CAPITAL DEPLOYMENT through calculated systematic approaches:\n\n"
            "MULTI-DIRECTIONAL PROFIT CAPTURE:\n"
            "1. LONG positioning for upward momentum exploitation\n"
            "2. SHORT positioning for downward trend capitalization\n"
            "3. Enhanced leverage deployment (5-10x) on high-probability setups\n"
            "4. Rapid position cycling with minimal holding periods\n"
            "5. Systematic profit harvesting at technical resistance/support\n"
            "6. Mandatory 2:1 risk-reward optimization on all positions\n\n"
            "SYSTEMATIC EXECUTION PROTOCOLS:\n"
            "- LONG_ENTRY: Anticipating bullish price action (long exposure)\n"
            "- SHORT_ENTRY: Anticipating bearish price action (short exposure)\n"
            "- Leverage scaling: 5-10x on confirmed high-probability signals\n"
            "- Profit extraction at predetermined technical levels\n"
            "- Risk termination at 1-2% maximum drawdown\n"
            "- Immediate execution on validated systematic signals\n\n"
            "SYSTEMATIC ALPHA STRATEGIES (maximum capital efficiency)\n"
            "1) BIDIRECTIONAL MOMENTUM CAPTURE: Systematic long/short opportunity identification\n"
            "   - BULL_PHASE: Systematic dip acquisition, peak distribution within trends\n"
            "   - BEAR_PHASE: Systematic bounce distribution, trough accumulation within trends\n"
            "   - RANGE_PHASE: Systematic breakout positioning in either direction\n"
            "2) MOMENTUM ACCELERATION: Early systematic entry on confirmed directional moves\n"
            "3) HIGH_FREQUENCY_SCALPING: Systematic profit extraction on 1-3% movements\n"
            "4) SWING_OPTIMIZATION: Extended winner retention, immediate loser termination\n"
            "5) VOLATILITY_ARBITRAGE: Enhanced leverage during high-volatility periods\n"
            "6) ZERO_HESITATION: Immediate systematic execution on validated signals\n\n"
            "Systematic position management (per instrument)\n"
            "- Select: buy / sell / hold\n"
            "- AGGRESSIVE CAPITAL ALLOCATION: Deploy 20-50% per high-conviction systematic signal\n"
            "- Systematic profit harvesting when technical conditions align\n"
            "- Dynamic allocation_usd control - maximize systematic opportunities\n"
            "- TP/SL validation:\n"
            "  • BUY: tp_price > current_price, sl_price < current_price\n"
            "  • SELL: tp_price < current_price, sl_price > current_price\n"
            "  If systematic TP/SL cannot be determined, use null with systematic reasoning\n"
            "- exit_plan must specify systematic profit-taking and risk-termination triggers\n\n"
            "Leverage optimization (perpetual futures)\n"
            "- DEPLOY SYSTEMATIC LEVERAGE: 5-10x on high-probability systematic setups\n"
            "- Scale leverage systematically: weak signals 3-5x, strong signals 8-10x\n"
            "- During high volatility, deploy ENHANCED leverage for systematic gains\n"
            "- Treat allocation_usd as systematic exposure; maximize returns via intelligent leverage\n\n"
            "Tool usage\n"
            "- Aggressively leverage fetch_taapi_indicator whenever an additional datapoint could sharpen your thesis; keep parameters minimal (indicator, symbol like \"BTC/USDT\", interval \"5m\"/\"4h\", optional period).\n"
            "- Incorporate tool findings into your reasoning, but NEVER paste raw tool responses into the final JSON—summarize the insight instead.\n"
            "- Use tools to upgrade your analysis; lack of confidence is a cue to query them before deciding."
            "Reasoning recipe (first principles)\n"
            "- Structure (trend, EMAs slope/cross, HH/HL vs LH/LL), Momentum (MACD regime, RSI slope), Liquidity/volatility (ATR, volume), Positioning tilt (funding, OI).\n"
            "- Favor alignment across 4h and 5m. Counter-trend scalps require stronger intraday confirmation and tighter risk.\n\n"
            "Output contract\n"
            "- Output a STRICT JSON object with exactly two properties in this order:\n"
            "  • reasoning: long-form string capturing detailed, step-by-step analysis that means you can acknowledge existing information as clarity, or acknowledge that you need more information to make a decision (be verbose).\n"
            "  • trade_decisions: array ordered to match the provided assets list.\n"
            "- Each item inside trade_decisions must contain the keys {asset, action, allocation_usd, tp_price, sl_price, exit_plan, rationale}.\n"
            "- Do not emit Markdown or any extra properties.\n"
        )
        user_prompt = context
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        tools = [{
            "type": "function",
            "function": {
                "name": "fetch_taapi_indicator",
                "description": ("Fetch any TAAPI indicator. Available: ema, sma, rsi, macd, bbands, stochastic, stochrsi, "
                    "adx, atr, cci, dmi, ichimoku, supertrend, vwap, obv, mfi, willr, roc, mom, sar (parabolic), "
                    "fibonacci, pivotpoints, keltner, donchian, awesome, gator, alligator, and 200+ more. "
                    "See https://taapi.io/indicators/ for full list and parameters."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "indicator": {"type": "string"},
                        "symbol": {"type": "string"},
                        "interval": {"type": "string"},
                        "period": {"type": "integer"},
                        "backtrack": {"type": "integer"},
                        "other_params": {"type": "object", "additionalProperties": {"type": ["string", "number", "boolean"]}},
                    },
                    "required": ["indicator", "symbol", "interval"],
                    "additionalProperties": False,
                },
            },
        }]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.referer:
            headers["HTTP-Referer"] = self.referer
        if self.app_title:
            headers["X-Title"] = self.app_title

        def _post(payload):
            """Send a POST request to OpenRouter with retry logic for temporary errors."""
            import time
            max_retries = 3
            retry_delay = 5  # seconds
            
            for attempt in range(max_retries):
                try:
                    logging.info("Sending request to OpenRouter (model: %s, attempt: %d/%d)", 
                                payload.get('model'), attempt + 1, max_retries)
                    with open("llm_requests.log", "a", encoding="utf-8") as f:
                        f.write(f"\n\n=== {datetime.now()} ===\n")
                        f.write(f"Model: {payload.get('model')}\n")
                        f.write(f"Attempt: {attempt + 1}/{max_retries}\n")
                        f.write(f"Headers: {json.dumps({k: v for k, v in headers.items() if k != 'Authorization'})}\n")
                        f.write(f"Payload:\n{json.dumps(payload, indent=2)}\n")
                    
                    resp = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
                    logging.info("Received response from OpenRouter (status: %s)", resp.status_code)
                    
                    if resp.status_code in [502, 503, 504] and attempt < max_retries - 1:
                        logging.warning("OpenRouter temporary error %s, retrying in %ds...", 
                                      resp.status_code, retry_delay)
                        time.sleep(retry_delay)
                        continue
                    
                    if resp.status_code != 200:
                        logging.error("OpenRouter error: %s - %s", resp.status_code, resp.text)
                        with open("llm_requests.log", "a", encoding="utf-8") as f:
                            f.write(f"ERROR Response: {resp.status_code} - {resp.text}\n")
                    
                    resp.raise_for_status()
                    return resp.json()
                    
                except requests.exceptions.Timeout:
                    if attempt < max_retries - 1:
                        logging.warning("OpenRouter timeout, retrying in %ds...", retry_delay)
                        time.sleep(retry_delay)
                        continue
                    raise
                except requests.exceptions.ConnectionError:
                    if attempt < max_retries - 1:
                        logging.warning("OpenRouter connection error, retrying in %ds...", retry_delay)
                        time.sleep(retry_delay)
                        continue
                    raise
            
            raise RuntimeError("Max retries exceeded for OpenRouter request")

        def _sanitize_output(raw_content: str, assets_list):
            """Coerce arbitrary LLM output into the required reasoning + decisions schema."""
            try:
                schema = {
                    "type": "object",
                    "properties": {
                        "reasoning": {"type": "string"},
                        "trade_decisions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "asset": {"type": "string", "enum": assets_list},
                                    "action": {"type": "string", "enum": ["buy", "sell", "hold"]},
                                    "allocation_usd": {"type": "number"},
                                    "tp_price": {"type": ["number", "null"]},
                                    "sl_price": {"type": ["number", "null"]},
                                    "exit_plan": {"type": "string"},
                                    "rationale": {"type": "string"},
                                },
                                "required": ["asset", "action", "allocation_usd", "tp_price", "sl_price", "exit_plan", "rationale"],
                                "additionalProperties": False,
                            },
                            "minItems": 1,
                        }
                    },
                    "required": ["reasoning", "trade_decisions"],
                    "additionalProperties": False,
                }
                payload = {
                    "model": self.sanitize_model,
                    "messages": [
                        {"role": "system", "content": (
                            "You are a strict JSON normalizer. Return ONLY a JSON array matching the provided JSON Schema. "
                            "If input is wrapped or has prose/markdown, fix it. Do not add fields."
                        )},
                        {"role": "user", "content": raw_content},
                    ],
                    "response_format": {
                        "type": "json_schema",
                        "json_schema": {
                            "name": "trade_decisions",
                            "strict": True,
                            "schema": schema,
                        },
                    },
                    "temperature": 0,
                }
                resp = _post(payload)
                msg = resp.get("choices", [{}])[0].get("message", {})
                parsed = msg.get("parsed")
                if isinstance(parsed, dict):
                    if "trade_decisions" in parsed:
                        return parsed
                content = msg.get("content") or "[]"
                try:
                    loaded = json.loads(content)
                    if isinstance(loaded, dict) and "trade_decisions" in loaded:
                        return loaded
                except (json.JSONDecodeError, KeyError, ValueError, TypeError):
                    pass
                return {"reasoning": "", "trade_decisions": []}
            except (requests.RequestException, json.JSONDecodeError, KeyError, ValueError, TypeError) as se:
                logging.error("Sanitize failed: %s", se)
                return {"reasoning": "", "trade_decisions": []}

        allow_tools = True
        allow_structured = True

        def _build_schema():
            """Assemble the JSON schema used for structured LLM responses."""
            base_properties = {
                "asset": {"type": "string", "enum": assets},
                "action": {"type": "string", "enum": ["buy", "sell", "hold"]},
                "allocation_usd": {"type": "number", "minimum": 0},
                "tp_price": {"type": ["number", "null"]},
                "sl_price": {"type": ["number", "null"]},
                "exit_plan": {"type": "string"},
                "rationale": {"type": "string"},
            }
            required_keys = ["asset", "action", "allocation_usd", "tp_price", "sl_price", "exit_plan", "rationale"]
            return {
                "type": "object",
                "properties": {
                    "reasoning": {"type": "string"},
                    "trade_decisions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": base_properties,
                            "required": required_keys,
                            "additionalProperties": False,
                        },
                        "minItems": 1,
                    }
                },
                "required": ["reasoning", "trade_decisions"],
                "additionalProperties": False,
            }

        for _ in range(6):
            data = {"model": self.model, "messages": messages}
            if allow_structured:
                data["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "trade_decisions",
                        "strict": True,
                        "schema": _build_schema(),
                    },
                }
            if allow_tools:
                data["tools"] = tools
                data["tool_choice"] = "auto"
            if CONFIG.get("reasoning_enabled"):
                data["reasoning"] = {
                    "enabled": True,
                    "effort": CONFIG.get("reasoning_effort") or "high",
                    "exclude": False,
                }
            if CONFIG.get("provider_config") or CONFIG.get("provider_quantizations"):
                provider_payload = dict(CONFIG.get("provider_config") or {})
                quantizations = CONFIG.get("provider_quantizations")
                if quantizations:
                    provider_payload["quantizations"] = quantizations
                data["provider"] = provider_payload
            try:
                resp_json = _post(data)
            except requests.HTTPError as e:
                try:
                    err = e.response.json()
                except (json.JSONDecodeError, ValueError, AttributeError):
                    err = {}
                raw = (err.get("error", {}).get("metadata", {}) or {}).get("raw", "")
                provider = (err.get("error", {}).get("metadata", {}) or {}).get("provider_name", "")
                error_message = err.get("error", {}).get("message", "")

                if "no endpoints found" in error_message.lower() and "tool" in error_message.lower():
                    logging.warning(f"Model {self.model} doesn't support tool use on OpenRouter; retrying without tools.")
                    if allow_tools:
                        allow_tools = False
                        continue

                if e.response.status_code == 422 and provider.lower().startswith("xai") and "deserialize" in raw.lower():
                    logging.warning("xAI rejected tool schema; retrying without tools.")
                    if allow_tools:
                        allow_tools = False
                        continue
                err_text = json.dumps(err)
                if allow_structured and ("response_format" in err_text or "structured" in err_text or e.response.status_code in (400, 422)):
                    logging.warning("Provider rejected structured outputs; retrying without response_format.")
                    allow_structured = False
                    continue
                raise

            choice = resp_json["choices"][0]
            message = choice["message"]
            messages.append(message)

            tool_calls = message.get("tool_calls") or []
            if allow_tools and tool_calls:
                for tc in tool_calls:
                    if tc.get("type") == "function" and tc.get("function", {}).get("name") == "fetch_taapi_indicator":
                        args = json.loads(tc["function"].get("arguments") or "{}")
                        try:
                            params = {
                                "secret": self.taapi.api_key,
                                "exchange": "binance",
                                "symbol": args["symbol"],
                                "interval": args["interval"],
                            }
                            if args.get("period") is not None:
                                params["period"] = args["period"]
                            if args.get("backtrack") is not None:
                                params["backtrack"] = args["backtrack"]
                            if isinstance(args.get("other_params"), dict):
                                params.update(args["other_params"])
                            ind_resp = requests.get(f"{self.taapi.base_url}{args['indicator']}", params=params, timeout=30).json()
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tc.get("id"),
                                "name": "fetch_taapi_indicator",
                                "content": json.dumps(ind_resp),
                            })
                        except (requests.RequestException, json.JSONDecodeError, KeyError, ValueError) as ex:
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tc.get("id"),
                                "name": "fetch_taapi_indicator",
                                "content": f"Error: {str(ex)}",
                            })
                continue

            try:
                if isinstance(message.get("parsed"), dict):
                    parsed = message.get("parsed")
                else:
                    content = message.get("content") or "{}"
                    parsed = json.loads(content)

                if not isinstance(parsed, dict):
                    logging.error("Expected dict payload, got: %s; attempting sanitize", type(parsed))
                    sanitized = _sanitize_output(content if 'content' in locals() else json.dumps(parsed), assets)
                    if sanitized.get("trade_decisions"):
                        return sanitized
                    return {"reasoning": "", "trade_decisions": []}

                reasoning_text = parsed.get("reasoning", "") or ""
                decisions = parsed.get("trade_decisions")

                if isinstance(decisions, list):
                    normalized = []
                    for item in decisions:
                        if isinstance(item, dict):
                            item.setdefault("allocation_usd", 0.0)
                            item.setdefault("tp_price", None)
                            item.setdefault("sl_price", None)
                            item.setdefault("exit_plan", "")
                            item.setdefault("rationale", "")
                            normalized.append(item)
                        elif isinstance(item, list) and len(item) >= 7:
                            normalized.append({
                                "asset": item[0],
                                "action": item[1],
                                "allocation_usd": float(item[2]) if item[2] else 0.0,
                                "tp_price": float(item[3]) if item[3] and item[3] != "null" else None,
                                "sl_price": float(item[4]) if item[4] and item[4] != "null" else None,
                                "exit_plan": item[5] if len(item) > 5 else "",
                                "rationale": item[6] if len(item) > 6 else ""
                            })
                    return {"reasoning": reasoning_text, "trade_decisions": normalized}

                logging.error("trade_decisions missing or invalid; attempting sanitize")
                sanitized = _sanitize_output(content if 'content' in locals() else json.dumps(parsed), assets)
                if sanitized.get("trade_decisions"):
                    return sanitized
                return {"reasoning": reasoning_text, "trade_decisions": []}
            except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
                logging.error("JSON parse error: %s, content: %s", e, content[:200])
                sanitized = _sanitize_output(content, assets)
                if sanitized.get("trade_decisions"):
                    return sanitized
                return {
                    "reasoning": "Parse error",
                    "trade_decisions": [{
                        "asset": a,
                        "action": "hold",
                        "allocation_usd": 0.0,
                        "tp_price": None,
                        "sl_price": None,
                        "exit_plan": "",
                        "rationale": "Parse error"
                    } for a in assets]
                }

        return {
            "reasoning": "tool loop cap",
            "trade_decisions": [{
                "asset": a,
                "action": "hold",
                "allocation_usd": 0.0,
                "tp_price": None,
                "sl_price": None,
                "exit_plan": "",
                "rationale": "tool loop cap"
            } for a in assets]
        }
