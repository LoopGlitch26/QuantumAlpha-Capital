"""
QuantumAlpha Capital - System Configuration
Elite configuration management with advanced security and neural optimization settings
"""

import asyncio
import json
import os
from pathlib import Path
from nicegui import ui
from src.gui.services.bot_service import AgentService
from src.gui.services.state_manager import StateManager
from src.backend.config_loader import CONFIG


def create_settings(agent_service: AgentService, state_manager: StateManager):
    """Create elite system configuration interface with advanced management capabilities"""

    # Elite header with neural branding
    with ui.row().classes('w-full items-center justify-between mb-6'):
        with ui.row().classes('items-center gap-4'):
            ui.icon('settings', size='48px').classes('text-cyan-400')
            with ui.column().classes('gap-1'):
                ui.label('System Configuration').classes('text-4xl font-bold text-white')
                ui.label('Neural Engine & Risk Management Configuration').classes('text-lg text-cyan-300')
        
        # Configuration status indicator
        with ui.row().classes('items-center gap-3'):
            config_status = ui.icon('circle', size='16px').classes('text-green-400')
            ui.label('Configuration Active').classes('text-sm text-green-300 font-medium')

    # Configuration file path
    config_file = Path('data/config.json')

    # Load configuration from file or use defaults
    def load_config():
        """Load configuration from file"""
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                ui.notify(f'Failed to load config: {e}', type='warning')

        # Return defaults from environment
        return {
            'strategy': {
                'assets': CONFIG.get('assets') or 'BTC ETH',
                'interval': CONFIG.get('interval') or '5m',
                'llm_model': CONFIG.get('llm_model') or 'x-ai/grok-4',
                'reasoning_enabled': CONFIG.get('reasoning_enabled', False),
                'reasoning_effort': CONFIG.get('reasoning_effort') or 'high'
            },
            'api_keys': {
                'taapi_api_key': CONFIG.get('taapi_api_key') or '',
                'hyperliquid_private_key': CONFIG.get('hyperliquid_private_key') or '',
                'hyperliquid_network': CONFIG.get('hyperliquid_network') or 'mainnet',
                'openrouter_api_key': CONFIG.get('openrouter_api_key') or ''
            },
            'risk_management': {
                'max_position_size': 1000,
                'max_leverage': 3,
                'stop_loss_pct': 5,
                'take_profit_pct': 10,
                'max_open_positions': 5
            },
            'notifications': {
                'desktop_enabled': True,
                'telegram_enabled': False,
                'telegram_token': '',
                'telegram_chat_id': ''
            }
        }

    def save_config(config_data):
        """Save configuration to file"""
        try:
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            return True
        except Exception as e:
            ui.notify(f'Failed to save config: {e}', type='negative')
            return False

    # Load initial configuration
    config_data = load_config()

    # Elite configuration management
    with ui.card().classes('w-full p-6 bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-700'):
        with ui.tabs().classes('w-full') as tabs:
            tab_strategy = ui.tab('🧠 Neural Strategy', icon='psychology')
            tab_api = ui.tab('🔑 API Security', icon='security')
            tab_risk = ui.tab('⚡ Risk Engine', icon='shield')
            tab_notifications = ui.tab('📡 Alerts', icon='notifications')
            tab_advanced = ui.tab('⚙️ Advanced', icon='tune')

        with ui.tab_panels(tabs, value=tab_strategy).classes('w-full'):
            # ===== TAB 1: NEURAL STRATEGY CONFIGURATION =====
            with ui.tab_panel(tab_strategy):
                with ui.row().classes('w-full items-center justify-between mb-6'):
                    ui.label('Neural Strategy Configuration').classes('text-3xl font-bold text-white')
                    ui.button('🔄 Reset to Defaults', on_click=lambda: None).classes('bg-gray-600 hover:bg-gray-700 px-4 py-2')

                with ui.column().classes('gap-6 w-full max-w-4xl'):
                    # Trading instruments with enhanced selection
                    with ui.card().classes('p-6 bg-gray-800 border border-blue-500'):
                        ui.label('🎯 Trading Instruments').classes('text-xl font-bold text-blue-400 mb-4')
                        
                        assets_input = ui.textarea(
                            label='Instruments (space or comma separated)',
                            placeholder='BTC ETH SOL AVAX MATIC',
                            value=config_data['strategy']['assets']
                        ).classes('w-full')
                        
                        with ui.row().classes('gap-2 mt-2'):
                            ui.button('BTC ETH', on_click=lambda: assets_input.set_value('BTC ETH')).classes('bg-blue-600 hover:bg-blue-700 px-3 py-1 text-sm')
                            ui.button('Top 5', on_click=lambda: assets_input.set_value('BTC ETH SOL AVAX MATIC')).classes('bg-purple-600 hover:bg-purple-700 px-3 py-1 text-sm')
                            ui.button('DeFi Focus', on_click=lambda: assets_input.set_value('ETH UNI AAVE COMP')).classes('bg-green-600 hover:bg-green-700 px-3 py-1 text-sm')
                        
                        ui.label('Select high-liquidity instruments for optimal neural analysis').classes('text-sm text-gray-400 mt-2')

                    # Neural engine configuration
                    with ui.card().classes('p-6 bg-gray-800 border border-purple-500'):
                        ui.label('🧠 Neural Engine Settings').classes('text-xl font-bold text-purple-400 mb-4')
                        
                        with ui.row().classes('w-full gap-6'):
                            # Timeframe selection
                            with ui.column().classes('flex-1'):
                                ui.label('Analysis Timeframe').classes('text-lg font-semibold text-white mb-2')
                                interval_select = ui.select(
                                    label='Timeframe',
                                    options={
                                        '1m': '1 Minute (Ultra High Frequency)',
                                        '5m': '5 Minutes (High Frequency)', 
                                        '15m': '15 Minutes (Medium Frequency)',
                                        '1h': '1 Hour (Low Frequency)',
                                        '4h': '4 Hours (Position Trading)'
                                    },
                                    value=config_data['strategy']['interval']
                                ).classes('w-full')
                            
                            # LLM Model selection with enhanced options
                            with ui.column().classes('flex-1'):
                                ui.label('Neural Model').classes('text-lg font-semibold text-white mb-2')
                                llm_model_select = ui.select(
                                    label='AI Model',
                                    options={
                                        'deepseek/deepseek-chat-v3.1': 'DeepSeek V3.1 (Recommended)',
                                        'x-ai/grok-4': 'Grok-4 (High Performance)',
                                        'qwen/qwq-32b-preview': 'QwQ-32B (Reasoning)',
                                        'anthropic/claude-3.5-sonnet': 'Claude 3.5 Sonnet',
                                        'openai/gpt-4o': 'GPT-4o (Premium)',
                                        'google/gemini-2.0-flash-exp': 'Gemini 2.0 Flash',
                                        'qwen/qwen-2.5-72b-instruct': 'Qwen 2.5 72B'
                                    },
                                    value=config_data['strategy']['llm_model']
                                ).classes('w-full')
                        
                        # Advanced reasoning configuration
                        ui.separator().classes('my-4')
                        
                        with ui.row().classes('w-full items-center gap-6'):
                            reasoning_enabled = ui.checkbox(
                                'Enable Advanced Reasoning',
                                value=config_data['strategy']['reasoning_enabled']
                            ).classes('text-lg')
                            
                            reasoning_effort = ui.select(
                                label='Reasoning Depth',
                                options={
                                    'low': 'Low (Fast)',
                                    'medium': 'Medium (Balanced)', 
                                    'high': 'High (Thorough)'
                                },
                                value=config_data['strategy']['reasoning_effort']
                            ).classes('flex-1')
                        
                        ui.label('Advanced reasoning improves decision quality but increases processing time').classes('text-sm text-gray-400 mt-2')

                    
                    # Performance optimization settings
                    with ui.card().classes('p-6 bg-gray-800 border border-green-500'):
                        ui.label('⚡ Performance Optimization').classes('text-xl font-bold text-green-400 mb-4')
                        
                        with ui.row().classes('w-full gap-6'):
                            # Analysis frequency
                            with ui.column().classes('flex-1'):
                                ui.label('Analysis Frequency').classes('text-lg font-semibold text-white mb-2')
                                analysis_freq = ui.slider(
                                    min=30,
                                    max=300,
                                    value=60,
                                    step=30
                                ).classes('w-full')
                                analysis_freq_label = ui.label('60 seconds').classes('text-sm text-gray-400')
                                analysis_freq.on('update:model-value', lambda e: analysis_freq_label.set_text(f'{e.args} seconds'))
                            
                            # Batch processing
                            with ui.column().classes('flex-1'):
                                ui.label('Processing Mode').classes('text-lg font-semibold text-white mb-2')
                                batch_processing = ui.checkbox('Enable Batch Processing', value=True)
                                ui.label('Process multiple instruments simultaneously').classes('text-sm text-gray-400')

                    ui.separator().classes('my-6')

                    # Enhanced save and load functionality
                    async def save_strategy_config():
                        try:
                            # Update config data with enhanced validation
                            assets_text = assets_input.value.strip()
                            if not assets_text:
                                ui.notify('❌ Please specify at least one trading instrument', type='negative')
                                return
                            
                            # Parse and validate assets
                            assets_list = [a.strip().upper() for a in assets_text.replace(',', ' ').split() if a.strip()]
                            if not assets_list:
                                ui.notify('❌ Invalid instrument format', type='negative')
                                return
                            
                            config_data['strategy']['assets'] = ' '.join(assets_list)
                            config_data['strategy']['interval'] = interval_select.value
                            config_data['strategy']['llm_model'] = llm_model_select.value
                            config_data['strategy']['reasoning_enabled'] = reasoning_enabled.value
                            config_data['strategy']['reasoning_effort'] = reasoning_effort.value

                            # Save to file
                            if save_config(config_data):
                                # Update agent service config
                                agent_service.update_config({
                                    'assets': assets_list,
                                    'interval': config_data['strategy']['interval'],
                                    'model': config_data['strategy']['llm_model']
                                })
                                ui.notify('✅ Neural strategy configuration saved successfully!', type='positive', position='top')
                                config_status.classes(remove='text-red-400', add='text-green-400')
                            else:
                                ui.notify('❌ Failed to save configuration', type='negative')
                                config_status.classes(remove='text-green-400', add='text-red-400')
                        except Exception as e:
                            ui.notify(f'⚠️ Configuration error: {str(e)}', type='negative')

                    with ui.row().classes('gap-4 justify-center'):
                        ui.button('💾 Save Neural Configuration', on_click=save_strategy_config, icon='save').classes('bg-blue-600 hover:bg-blue-700 px-8 py-3 text-lg font-bold')
                        ui.button('🔄 Load Defaults', on_click=lambda: None, icon='refresh').classes('bg-gray-600 hover:bg-gray-700 px-8 py-3 text-lg font-bold')
                        ui.button('🧪 Test Configuration', on_click=lambda: None, icon='science').classes('bg-purple-600 hover:bg-purple-700 px-8 py-3 text-lg font-bold')

            # ===== TAB 2: API KEYS =====
            with ui.tab_panel(tab_api):
                ui.label('API Keys Configuration').classes('text-2xl font-bold mb-4 text-white')

                with ui.column().classes('gap-4 w-full max-w-2xl'):
                    # Connection status indicators
                    ui.label('Connection Status').classes('text-lg font-semibold text-white')
                    with ui.row().classes('gap-4 items-center'):
                        taapi_status = ui.label('TAAPI: 🔴 Not Connected').classes('text-sm')
                        hyperliquid_status = ui.label('Hyperliquid: 🔴 Not Connected').classes('text-sm')
                        openrouter_status = ui.label('OpenRouter: 🔴 Not Connected').classes('text-sm')

                    ui.separator()

                    # TAAPI Key
                    ui.label('TAAPI.io API Key').classes('text-lg font-semibold text-white')
                    taapi_input = ui.input(
                        label='TAAPI API Key',
                        placeholder='eyJhbGci...your-jwt-token-here',
                        value=config_data['api_keys']['taapi_api_key'],
                        password=True,
                        password_toggle_button=True
                    ).classes('w-full')
                    ui.label('Get your API key from https://taapi.io').classes('text-xs text-gray-400')

                    ui.separator()

                    # Hyperliquid Key
                    ui.label('Hyperliquid Private Key').classes('text-lg font-semibold text-white')
                    hyperliquid_input = ui.input(
                        label='Private Key',
                        placeholder='0x...',
                        value=config_data['api_keys']['hyperliquid_private_key'],
                        password=True,
                        password_toggle_button=True
                    ).classes('w-full')
                    ui.label('Your wallet private key for trading').classes('text-xs text-gray-400')

                    # Network selection
                    hyperliquid_network = ui.select(
                        label='Network',
                        options=['mainnet', 'testnet'],
                        value=config_data['api_keys']['hyperliquid_network']
                    ).classes('w-full')

                    ui.separator()

                    # OpenRouter Key
                    ui.label('OpenRouter API Key').classes('text-lg font-semibold text-white')
                    openrouter_input = ui.input(
                        label='OpenRouter API Key',
                        placeholder='sk-or-v1-your-key-here',
                        value=config_data['api_keys']['openrouter_api_key'],
                        password=True,
                        password_toggle_button=True
                    ).classes('w-full')
                    ui.label('Get your API key from https://openrouter.ai').classes('text-xs text-gray-400')

                    ui.separator()

                    # Test connections button
                    async def test_api_connections():
                        """Test all API connections"""
                        try:
                            ui.notify('Testing API connections...', type='info')

                            # Update environment variables temporarily for testing
                            if taapi_input.value:
                                os.environ['TAAPI_API_KEY'] = taapi_input.value
                            if hyperliquid_input.value:
                                os.environ['HYPERLIQUID_PRIVATE_KEY'] = hyperliquid_input.value
                            if openrouter_input.value:
                                os.environ['OPENROUTER_API_KEY'] = openrouter_input.value

                            # Test connections via agent service
                            results = await agent_service.test_api_connections()

                            # Update status indicators
                            taapi_status.text = f"TAAPI: {'🟢 Connected' if results.get('TAAPI', False) else '🔴 Failed'}"
                            hyperliquid_status.text = f"Hyperliquid: {'🟢 Connected' if results.get('Hyperliquid', False) else '🔴 Failed'}"
                            openrouter_status.text = f"OpenRouter: {'🟢 Connected' if results.get('OpenRouter', False) else '🔴 Failed'}"

                            # Show summary notification
                            connected_count = sum(1 for v in results.values() if v)
                            total_count = len(results)

                            if connected_count == total_count:
                                ui.notify(f'All APIs connected successfully! ({connected_count}/{total_count})', type='positive')
                            elif connected_count > 0:
                                ui.notify(f'Partially connected: {connected_count}/{total_count} APIs', type='warning')
                            else:
                                ui.notify('All connections failed. Check your API keys.', type='negative')

                        except Exception as e:
                            ui.notify(f'Error testing connections: {str(e)}', type='negative')

                    async def save_api_keys():
                        """Save API keys to configuration"""
                        try:
                            # Update config data
                            config_data['api_keys']['taapi_api_key'] = taapi_input.value
                            config_data['api_keys']['hyperliquid_private_key'] = hyperliquid_input.value
                            config_data['api_keys']['hyperliquid_network'] = hyperliquid_network.value
                            config_data['api_keys']['openrouter_api_key'] = openrouter_input.value

                            # Save to file
                            if save_config(config_data):
                                # Update environment variables
                                if taapi_input.value:
                                    os.environ['TAAPI_API_KEY'] = taapi_input.value
                                if hyperliquid_input.value:
                                    os.environ['HYPERLIQUID_PRIVATE_KEY'] = hyperliquid_input.value
                                if openrouter_input.value:
                                    os.environ['OPENROUTER_API_KEY'] = openrouter_input.value

                                ui.notify('API keys saved successfully!', type='positive')
                                ui.notify('Note: Restart the agent for changes to take effect', type='info')
                            else:
                                ui.notify('Failed to save API keys', type='negative')
                        except Exception as e:
                            ui.notify(f'Error saving API keys: {str(e)}', type='negative')

                    with ui.row().classes('gap-2'):
                        ui.button('Save API Keys', on_click=save_api_keys, icon='save').props('color=primary')
                        ui.button('Test Connections', on_click=test_api_connections, icon='network_check').props('color=secondary')

                    ui.separator()

                    # Warning
                    with ui.card().classes('bg-orange-900 p-4'):
                        ui.label('⚠️ Security Warning').classes('text-lg font-bold text-white mb-2')
                        ui.label('Never share your private keys. Keys are stored in data/config.json - keep this file secure!').classes('text-sm text-gray-200')

            # ===== TAB 3: RISK MANAGEMENT =====
            with ui.tab_panel(tab_risk):
                ui.label('Risk Management').classes('text-2xl font-bold mb-4 text-white')

                with ui.column().classes('gap-6 w-full max-w-2xl'):
                    # Max Position Size
                    ui.label('Maximum Position Size').classes('text-lg font-semibold text-white')
                    with ui.row().classes('items-center w-full gap-4'):
                        max_position_slider = ui.slider(
                            min=100,
                            max=10000,
                            value=config_data['risk_management']['max_position_size'],
                            step=100
                        ).classes('flex-grow')
                        max_position_label = ui.label(f"${config_data['risk_management']['max_position_size']:,.0f}").classes('text-white font-bold min-w-[100px]')
                        max_position_slider.on('update:model-value', lambda e: max_position_label.set_text(f'${e.args:,.0f}'))
                    ui.label('Maximum USD allocation per position').classes('text-xs text-gray-400')

                    ui.separator()

                    # Max Leverage
                    ui.label('Maximum Leverage').classes('text-lg font-semibold text-white')
                    with ui.row().classes('items-center w-full gap-4'):
                        max_leverage_slider = ui.slider(
                            min=1,
                            max=20,
                            value=config_data['risk_management']['max_leverage'],
                            step=0.5
                        ).classes('flex-grow')
                        max_leverage_label = ui.label(f"{config_data['risk_management']['max_leverage']:.1f}x").classes('text-white font-bold min-w-[100px]')
                        max_leverage_slider.on('update:model-value', lambda e: max_leverage_label.set_text(f'{e.args:.1f}x'))
                    ui.label('Maximum leverage for perpetual futures (1x-20x)').classes('text-xs text-gray-400')

                    ui.separator()

                    # Stop Loss %
                    ui.label('Default Stop Loss').classes('text-lg font-semibold text-white')
                    with ui.row().classes('items-center w-full gap-4'):
                        stop_loss_slider = ui.slider(
                            min=1,
                            max=20,
                            value=config_data['risk_management']['stop_loss_pct'],
                            step=0.5
                        ).classes('flex-grow')
                        stop_loss_label = ui.label(f"{config_data['risk_management']['stop_loss_pct']:.1f}%").classes('text-white font-bold min-w-[100px]')
                        stop_loss_slider.on('update:model-value', lambda e: stop_loss_label.set_text(f'{e.args:.1f}%'))
                    ui.label('Default stop loss percentage from entry').classes('text-xs text-gray-400')

                    ui.separator()

                    # Take Profit %
                    ui.label('Default Take Profit').classes('text-lg font-semibold text-white')
                    with ui.row().classes('items-center w-full gap-4'):
                        take_profit_slider = ui.slider(
                            min=2,
                            max=50,
                            value=config_data['risk_management']['take_profit_pct'],
                            step=1
                        ).classes('flex-grow')
                        take_profit_label = ui.label(f"{config_data['risk_management']['take_profit_pct']:.0f}%").classes('text-white font-bold min-w-[100px]')
                        take_profit_slider.on('update:model-value', lambda e: take_profit_label.set_text(f'{e.args:.0f}%'))
                    ui.label('Default take profit percentage from entry').classes('text-xs text-gray-400')

                    ui.separator()

                    # Max Open Positions
                    ui.label('Maximum Open Positions').classes('text-lg font-semibold text-white')
                    max_positions_input = ui.number(
                        label='Max Positions',
                        value=config_data['risk_management']['max_open_positions'],
                        min=1,
                        max=20
                    ).classes('w-full')
                    ui.label('Maximum number of concurrent open positions').classes('text-xs text-gray-400')

                    ui.separator()

                    # Save button
                    async def save_risk_config():
                        try:
                            # Update config data
                            config_data['risk_management']['max_position_size'] = int(max_position_slider.value)
                            config_data['risk_management']['max_leverage'] = float(max_leverage_slider.value)
                            config_data['risk_management']['stop_loss_pct'] = float(stop_loss_slider.value)
                            config_data['risk_management']['take_profit_pct'] = float(take_profit_slider.value)
                            config_data['risk_management']['max_open_positions'] = int(max_positions_input.value)

                            # Save to file
                            if save_config(config_data):
                                ui.notify('Risk management settings saved successfully!', type='positive')
                            else:
                                ui.notify('Failed to save risk settings', type='negative')
                        except Exception as e:
                            ui.notify(f'Error saving risk config: {str(e)}', type='negative')

                    ui.button('Save Risk Settings', on_click=save_risk_config, icon='save').props('color=primary')

                    ui.separator()

                    # Warning about leverage
                    with ui.card().classes('bg-red-900 p-4'):
                        ui.label('⚠️ Risk Warning').classes('text-lg font-bold text-white mb-2')
                        ui.label('High leverage increases both potential profits and losses. Use with caution!').classes('text-sm text-gray-200')

            # ===== TAB 4: NOTIFICATIONS =====
            with ui.tab_panel(tab_notifications):
                ui.label('Notifications').classes('text-2xl font-bold mb-4 text-white')

                with ui.column().classes('gap-4 w-full max-w-2xl'):
                    # Desktop Notifications
                    ui.label('Desktop Notifications').classes('text-lg font-semibold text-white')
                    desktop_enabled_checkbox = ui.checkbox(
                        'Enable Desktop Notifications',
                        value=config_data['notifications']['desktop_enabled']
                    )
                    ui.label('Show system notifications for important events').classes('text-xs text-gray-400')

                    ui.separator()

                    # Telegram Agent
                    ui.label('Telegram Notifications').classes('text-lg font-semibold text-white')
                    telegram_enabled_checkbox = ui.checkbox(
                        'Enable Telegram Notifications',
                        value=config_data['notifications']['telegram_enabled']
                    )

                    # Telegram token and chat ID (shown when enabled)
                    telegram_token_input = ui.input(
                        label='Telegram Agent Token',
                        placeholder='123456:ABC-DEF...',
                        value=config_data['notifications']['telegram_token'],
                        password=True,
                        password_toggle_button=True
                    ).classes('w-full')
                    telegram_token_input.visible = telegram_enabled_checkbox.value

                    telegram_chat_input = ui.input(
                        label='Telegram Chat ID',
                        placeholder='123456789',
                        value=config_data['notifications']['telegram_chat_id']
                    ).classes('w-full')
                    telegram_chat_input.visible = telegram_enabled_checkbox.value

                    # Toggle visibility when checkbox changes
                    def toggle_telegram_inputs(e):
                        telegram_token_input.visible = e.value
                        telegram_chat_input.visible = e.value

                    telegram_enabled_checkbox.on('update:model-value', toggle_telegram_inputs)

                    ui.label('Get your agent token from @BotFather on Telegram').classes('text-xs text-gray-400')

                    ui.separator()

                    # Test Notification button
                    async def test_notification():
                        try:
                            if desktop_enabled_checkbox.value:
                                ui.notify('Test notification sent! This is how trade alerts will look.', type='info')
                            else:
                                ui.notify('Desktop notifications are disabled', type='warning')

                            if telegram_enabled_checkbox.value and telegram_token_input.value:
                                ui.notify('Telegram test notification would be sent here', type='info')
                                # TODO: Implement actual Telegram notification

                        except Exception as e:
                            ui.notify(f'Error sending test notification: {str(e)}', type='negative')

                    # Save button
                    async def save_notification_config():
                        try:
                            # Update config data
                            config_data['notifications']['desktop_enabled'] = desktop_enabled_checkbox.value
                            config_data['notifications']['telegram_enabled'] = telegram_enabled_checkbox.value
                            config_data['notifications']['telegram_token'] = telegram_token_input.value
                            config_data['notifications']['telegram_chat_id'] = telegram_chat_input.value

                            # Save to file
                            if save_config(config_data):
                                ui.notify('Notification settings saved successfully!', type='positive')
                            else:
                                ui.notify('Failed to save notification settings', type='negative')
                        except Exception as e:
                            ui.notify(f'Error saving notification config: {str(e)}', type='negative')

                    with ui.row().classes('gap-2'):
                        ui.button('Save Notification Settings', on_click=save_notification_config, icon='save').props('color=primary')
                        ui.button('Test Notification', on_click=test_notification, icon='notifications_active').props('color=secondary')

                    ui.separator()

                    # Info box
                    with ui.card().classes('bg-blue-900 p-4'):
                        ui.label('ℹ️ Notification Features').classes('text-lg font-bold text-white mb-2')
                        ui.label('Configure notifications for trade executions, errors, and daily summaries.').classes('text-sm text-gray-200')

            # ===== TAB 5: ADVANCED CONFIGURATION =====
            with ui.tab_panel(ui.tab('⚙️ Advanced', icon='tune')):
                with ui.row().classes('w-full items-center justify-between mb-6'):
                    ui.label('Advanced System Configuration').classes('text-3xl font-bold text-white')
                    ui.button('⚠️ Factory Reset', on_click=lambda: None).classes('bg-red-600 hover:bg-red-700 px-4 py-2')

                with ui.column().classes('gap-6 w-full max-w-4xl'):
                    # Neural engine tuning
                    with ui.card().classes('p-6 bg-gray-800 border border-cyan-500'):
                        ui.label('🧠 Neural Engine Tuning').classes('text-xl font-bold text-cyan-400 mb-4')
                        
                        with ui.row().classes('w-full gap-6'):
                            # Temperature control
                            with ui.column().classes('flex-1'):
                                ui.label('Decision Temperature').classes('text-lg font-semibold text-white mb-2')
                                temp_slider = ui.slider(min=0.1, max=2.0, value=0.7, step=0.1).classes('w-full')
                                temp_label = ui.label('0.7 (Balanced)').classes('text-sm text-gray-400')
                                temp_slider.on('update:model-value', lambda e: temp_label.set_text(f'{e.args:.1f} {"(Conservative)" if e.args < 0.5 else "(Aggressive)" if e.args > 1.2 else "(Balanced)"}'))
                            
                            # Confidence threshold
                            with ui.column().classes('flex-1'):
                                ui.label('Minimum Confidence').classes('text-lg font-semibold text-white mb-2')
                                conf_slider = ui.slider(min=50, max=95, value=75, step=5).classes('w-full')
                                conf_label = ui.label('75% (Recommended)').classes('text-sm text-gray-400')
                                conf_slider.on('update:model-value', lambda e: conf_label.set_text(f'{e.args}% {"(Conservative)" if e.args > 85 else "(Aggressive)" if e.args < 65 else "(Recommended)"}'))
                    
                    # Performance monitoring
                    with ui.card().classes('p-6 bg-gray-800 border border-orange-500'):
                        ui.label('📊 Performance Monitoring').classes('text-xl font-bold text-orange-400 mb-4')
                        
                        with ui.row().classes('w-full gap-4'):
                            enable_logging = ui.checkbox('Detailed Logging', value=True)
                            enable_metrics = ui.checkbox('Performance Metrics', value=True)
                            enable_backtesting = ui.checkbox('Backtesting Mode', value=False)
                        
                        ui.label('Enhanced monitoring for system optimization and debugging').classes('text-sm text-gray-400 mt-2')
                    
                    # Database and storage
                    with ui.card().classes('p-6 bg-gray-800 border border-purple-500'):
                        ui.label('💾 Data Management').classes('text-xl font-bold text-purple-400 mb-4')
                        
                        with ui.row().classes('w-full gap-4'):
                            # Database cleanup
                            with ui.column().classes('flex-1'):
                                ui.label('Data Retention').classes('text-lg font-semibold text-white mb-2')
                                retention_select = ui.select(
                                    label='Keep Data For',
                                    options={
                                        '7': '7 Days',
                                        '30': '30 Days', 
                                        '90': '90 Days',
                                        '365': '1 Year',
                                        '0': 'Forever'
                                    },
                                    value='90'
                                ).classes('w-full')
                            
                            # Export options
                            with ui.column().classes('flex-1'):
                                ui.label('Data Export').classes('text-lg font-semibold text-white mb-2')
                                with ui.row().classes('gap-2'):
                                    ui.button('📥 Export Trades', on_click=lambda: None).classes('bg-blue-600 hover:bg-blue-700 px-4 py-2')
                                    ui.button('🗄️ Backup Config', on_click=lambda: None).classes('bg-green-600 hover:bg-green-700 px-4 py-2')
                    
                    # System diagnostics
                    with ui.card().classes('p-6 bg-gray-800 border border-red-500'):
                        ui.label('🔧 System Diagnostics').classes('text-xl font-bold text-red-400 mb-4')
                        
                        with ui.row().classes('w-full gap-4'):
                            ui.button('🧪 Run Diagnostics', on_click=lambda: None).classes('bg-blue-600 hover:bg-blue-700 px-6 py-3')
                            ui.button('📋 System Report', on_click=lambda: None).classes('bg-purple-600 hover:bg-purple-700 px-6 py-3')
                            ui.button('🔄 Restart Services', on_click=lambda: None).classes('bg-orange-600 hover:bg-orange-700 px-6 py-3')
                            ui.button('⚠️ Emergency Stop', on_click=lambda: None).classes('bg-red-600 hover:bg-red-700 px-6 py-3')
                    
                    # Developer options
                    with ui.card().classes('p-6 bg-gray-800 border border-yellow-500'):
                        ui.label('👨‍💻 Developer Options').classes('text-xl font-bold text-yellow-400 mb-4')
                        
                        with ui.column().classes('gap-3'):
                            debug_mode = ui.checkbox('Debug Mode', value=False)
                            api_logging = ui.checkbox('API Request Logging', value=False)
                            neural_tracing = ui.checkbox('Neural Decision Tracing', value=False)
                            
                            ui.label('⚠️ Warning: Debug options may impact performance').classes('text-sm text-yellow-300 mt-2')
                    
                    ui.separator().classes('my-6')
                    
                    # Advanced save functionality
                    async def save_advanced_config():
                        try:
                            # Save advanced configuration
                            advanced_config = {
                                'neural_tuning': {
                                    'temperature': temp_slider.value,
                                    'min_confidence': conf_slider.value
                                },
                                'monitoring': {
                                    'detailed_logging': enable_logging.value,
                                    'performance_metrics': enable_metrics.value,
                                    'backtesting_mode': enable_backtesting.value
                                },
                                'data_management': {
                                    'retention_days': int(retention_select.value)
                                },
                                'developer': {
                                    'debug_mode': debug_mode.value,
                                    'api_logging': api_logging.value,
                                    'neural_tracing': neural_tracing.value
                                }
                            }
                            
                            # Save to advanced config file
                            advanced_config_file = Path('data/advanced_config.json')
                            advanced_config_file.parent.mkdir(parents=True, exist_ok=True)
                            with open(advanced_config_file, 'w') as f:
                                json.dump(advanced_config, f, indent=2)
                            
                            ui.notify('✅ Advanced configuration saved successfully!', type='positive', position='top')
                        except Exception as e:
                            ui.notify(f'⚠️ Error saving advanced config: {str(e)}', type='negative')
                    
                    with ui.row().classes('gap-4 justify-center'):
                        ui.button('💾 Save Advanced Settings', on_click=save_advanced_config).classes('bg-cyan-600 hover:bg-cyan-700 px-8 py-3 text-lg font-bold')
                        ui.button('🔄 Reset to Defaults', on_click=lambda: None).classes('bg-gray-600 hover:bg-gray-700 px-8 py-3 text-lg font-bold')
                    
                    # Warning section
                    with ui.card().classes('bg-red-900 p-6 border border-red-500'):
                        ui.label('⚠️ Advanced Configuration Warning').classes('text-xl font-bold text-white mb-3')
                        ui.label('These settings directly affect neural engine performance and system behavior. Modify only if you understand the implications. Incorrect settings may impact trading performance or system stability.').classes('text-sm text-red-200 leading-relaxed')

    # Load current configuration on page load
    async def load_initial_config():
        """Load current agent configuration on page initialization"""
        try:
            current_config = await agent_service.get_current_config() if hasattr(agent_service, 'get_current_config') else None
            if current_config:
                # Update UI with current config
                pass
        except Exception as e:
            pass  # Fail silently on initial load

    # Schedule initial config load
    asyncio.create_task(load_initial_config())
