"""Centralized environment variable loading for the trading agent configuration."""

import json
import os
from typing import Union, Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()


def _get_env(name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """Fetch an environment variable with optional default and required validation."""
    value = os.getenv(name, default)
    if required and (value is None or value == ""):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _get_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: Optional[int] = None) -> Optional[int]:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError(f"Invalid integer for {name}: {raw}") from exc


def _get_json(name: str, default: Optional[dict] = None) -> Optional[dict]:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            raise RuntimeError(f"Environment variable {name} must be a JSON object")
        return parsed
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON for {name}: {raw}") from exc


def _get_list(name: str, default: Optional[List[str]] = None) -> Optional[List[str]]:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    raw = raw.strip()
    # Support JSON-style lists
    if raw.startswith("[") and raw.endswith("]"):
        try:
            parsed = json.loads(raw)
            if not isinstance(parsed, list):
                raise RuntimeError(f"Environment variable {name} must be a list if using JSON syntax")
            return [str(item).strip().strip('"\'') for item in parsed if str(item).strip()]
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON list for {name}: {raw}") from exc
    # Fallback: comma separated string
    values = []
    for item in raw.split(","):
        cleaned = item.strip().strip('"\'')
        if cleaned:
            values.append(cleaned)
    return values or default


CONFIG = {
    # API keys - not required during module import (checked when platform starts)
    "taapi_api_key": _get_env("TAAPI_API_KEY"),
    "hyperliquid_private_key": _get_env("HYPERLIQUID_PRIVATE_KEY") or _get_env("LIGHTER_PRIVATE_KEY"),
    "hyperliquid_account_address": _get_env("HYPERLIQUID_ACCOUNT_ADDRESS"),  # For API wallets
    "mnemonic": _get_env("MNEMONIC"),
    # Hyperliquid network/base URL overrides
    "hyperliquid_base_url": _get_env("HYPERLIQUID_BASE_URL"),
    "hyperliquid_network": _get_env("HYPERLIQUID_NETWORK", "mainnet"),
    # Neural Decision Engine via OpenRouter
    "openrouter_api_key": _get_env("OPENROUTER_API_KEY"),
    "openrouter_base_url": _get_env("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    "openrouter_referer": _get_env("OPENROUTER_REFERER"),
    "openrouter_app_title": _get_env("OPENROUTER_APP_TITLE", "quantumalpha-capital"),
    "llm_model": _get_env("AI_MODEL") or _get_env("LLM_MODEL", "deepseek/deepseek-chat-v3.1"),
    # Neural reasoning capabilities
    "reasoning_enabled": _get_bool("REASONING_ENABLED", False),
    "reasoning_effort": _get_env("REASONING_EFFORT", "high"),
    # Provider routing
    "provider_config": _get_json("PROVIDER_CONFIG"),
    "provider_quantizations": _get_list("PROVIDER_QUANTIZATIONS"),
    # Portfolio management controls
    "assets": _get_env("INSTRUMENTS") or _get_env("ASSETS"),  # e.g., "BTC ETH LTC" or "BTC,ETH,LTC"
    "interval": _get_env("ANALYSIS_TIMEFRAME") or _get_env("INTERVAL"),  # e.g., "5m", "1h"
    "trading_mode": _get_env("EXECUTION_MODE") or _get_env("TRADING_MODE", "systematic"),  # systematic or manual
    # Platform server
    "api_host": _get_env("API_HOST", "0.0.0.0"),
    "api_port": _get_env("APP_PORT") or _get_env("API_PORT") or "3000",
}
