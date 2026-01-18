"""
Market Intelligence Page - Live market data and neural analysis
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from nicegui import ui
from datetime import datetime, timezone
from src.gui.services.bot_service import AgentService
from src.gui.services.state_manager import StateManager


def create_market(agent_service: AgentService, state_manager: StateManager):
    """Create market intelligence page with live data and advanced analytics"""

    ui.label('🌐 Market Intelligence').classes('text-3xl font-bold mb-4 text-white')

    # ===== ASSET SELECTOR & CONTROLS =====
    with ui.row().classes('w-full items-center gap-4 mb-6'):
        ui.label('Neural Analysis Target:').classes('text-lg font-semibold text-white')

        # Get assets from agent config
        state = state_manager.get_state()
        configured_assets = agent_service.get_assets() if agent_service.is_running() else ['BTC', 'ETH', 'LTC']
        available_assets = configured_assets if configured_assets else ['BTC', 'ETH', 'LTC']

        asset_select = ui.select(
            label='Asset',
            options=available_assets,
            value=available_assets[0] if available_assets else 'BTC'
        ).classes('w-48')

        interval_select = ui.select(
            label='Timeframe',
            options=['5m', '15m', '1h', '4h', '1d'],
            value='5m'
        ).classes('w-32')

        # Refresh button
        refresh_btn = ui.button('🔄 Refresh', on_click=lambda: update_market_data())
        refresh_btn.classes('bg-blue-600 hover:bg-blue-700 text-white px-4 py-2')

        # Last update indicator
        last_update_label = ui.label('Last update: --').classes('text-sm text-gray-400 ml-auto')

    # ===== PRICE METRICS CARDS =====
    with ui.grid(columns=4).classes('w-full gap-4 mb-6'):
        # Current Price Card
        with ui.card().classes('metric-card bg-gradient-to-br from-blue-800 to-blue-900'):
            current_price_label = ui.label('$0.00').classes('text-4xl font-bold text-white')
            ui.label('Current Price').classes('text-sm text-blue-200 mt-2')
            price_change_label = ui.label('').classes('text-sm mt-1')

        # Open Interest Card
        with ui.card().classes('metric-card bg-gradient-to-br from-purple-800 to-purple-900'):
            open_interest_label = ui.label('$0.00M').classes('text-4xl font-bold text-white')
            ui.label('Open Interest').classes('text-sm text-purple-200 mt-2')

        # Funding Rate Card
        with ui.card().classes('metric-card bg-gradient-to-br from-green-800 to-green-900'):
            funding_rate_label = ui.label('0.00%').classes('text-4xl font-bold text-white')
            ui.label('Funding Rate').classes('text-sm text-green-200 mt-2')
            funding_annual_label = ui.label('').classes('text-sm mt-1')

        # Neural Confidence Card
        with ui.card().classes('metric-card bg-gradient-to-br from-orange-800 to-orange-900'):
            confidence_label = ui.label('--').classes('text-4xl font-bold text-white')
            ui.label('Neural Confidence').classes('text-sm text-orange-200 mt-2')

    # ===== PRICE CHART WITH INDICATORS =====
    with ui.card().classes('w-full p-4 mb-6'):
        ui.label('📈 Price Action & Technical Analysis').classes('text-xl font-bold text-white mb-2')

        # Advanced price chart with indicators
        price_chart = ui.plotly(make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('Price & EMAs', 'RSI', 'MACD'),
            row_heights=[0.6, 0.2, 0.2]
        )).classes('w-full')

        # Configure chart layout
        price_chart.figure.update_layout(
            template='plotly_dark',
            height=600,
            margin=dict(l=50, r=20, t=60, b=40),
            paper_bgcolor='#1f2937',
            plot_bgcolor='#1f2937',
            font=dict(color='#e5e7eb'),
            showlegend=True,
            legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0.5)')
        )

    # ===== TECHNICAL INDICATORS GRID =====
    with ui.row().classes('w-full gap-4 mb-6'):
        # Left column - Trend Analysis
        with ui.card().classes('flex-1 p-4 bg-gradient-to-br from-gray-800 to-gray-900'):
            ui.label('🔍 Trend Analysis').classes('text-xl font-bold text-white mb-4')

            with ui.column().classes('gap-3 w-full'):
                # EMA Analysis
                ui.label('Exponential Moving Averages').classes('text-lg font-semibold text-blue-400')
                
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('EMA 20 (5m)').classes('text-gray-300')
                    ema20_5m_label = ui.label('$0.00').classes('text-white font-semibold')

                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('EMA 20 (4h)').classes('text-gray-300')
                    ema20_4h_label = ui.label('$0.00').classes('text-white font-semibold')

                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('EMA 50 (4h)').classes('text-gray-300')
                    ema50_label = ui.label('$0.00').classes('text-white font-semibold')

                ui.separator()

                # Trend Signal
                ui.label('Trend Signal').classes('text-lg font-semibold text-green-400')
                trend_signal_label = ui.label('NEUTRAL').classes('text-2xl font-bold text-gray-400')
                trend_desc_label = ui.label('Analyzing trend direction...').classes('text-sm text-gray-400')

        # Right column - Momentum Analysis
        with ui.card().classes('flex-1 p-4 bg-gradient-to-br from-gray-800 to-gray-900'):
            ui.label('⚡ Momentum Analysis').classes('text-xl font-bold text-white mb-4')

            with ui.column().classes('gap-3 w-full'):
                # RSI Analysis
                ui.label('Relative Strength Index').classes('text-lg font-semibold text-yellow-400')
                
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('RSI 7 (5m)').classes('text-gray-300')
                    rsi7_label = ui.label('50.00').classes('text-white font-semibold')

                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('RSI 14 (5m)').classes('text-gray-300')
                    rsi14_label = ui.label('50.00').classes('text-white font-semibold')

                # RSI Visual Indicator
                rsi_progress = ui.linear_progress(value=0.5, show_value=False).classes('w-full mt-2')

                ui.separator()

                # MACD Analysis
                ui.label('MACD Momentum').classes('text-lg font-semibold text-purple-400')
                
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('MACD Line').classes('text-gray-300')
                    macd_line_label = ui.label('0.00').classes('text-white font-semibold')

                # Momentum Signal
                momentum_signal_label = ui.label('NEUTRAL').classes('text-2xl font-bold text-gray-400 mt-2')
                momentum_desc_label = ui.label('Analyzing momentum...').classes('text-sm text-gray-400')

    # ===== MARKET SENTIMENT & NEURAL ANALYSIS =====
    with ui.card().classes('w-full p-4 mb-6'):
        ui.label('🧠 Neural Market Sentiment').classes('text-xl font-bold text-white mb-4')

        with ui.row().classes('w-full gap-6 items-center'):
            # Overall Sentiment
            with ui.column().classes('flex-1'):
                ui.label('Overall Sentiment').classes('text-lg font-semibold text-gray-300 mb-2')
                sentiment_label = ui.label('ANALYZING').classes('text-4xl font-bold text-gray-400')
                sentiment_desc = ui.label('Neural analysis in progress...').classes('text-sm text-gray-400 mt-2')

            # Signal Strength Indicators
            with ui.column().classes('flex-1'):
                ui.label('Signal Strength').classes('text-lg font-semibold text-gray-300 mb-2')
                
                with ui.row().classes('items-center gap-2 mb-2'):
                    trend_strength_icon = ui.label('○').classes('text-2xl text-gray-400')
                    ui.label('Trend Strength').classes('text-gray-300')
                    trend_strength_label = ui.label('--').classes('text-white font-semibold ml-auto')

                with ui.row().classes('items-center gap-2 mb-2'):
                    momentum_strength_icon = ui.label('○').classes('text-2xl text-gray-400')
                    ui.label('Momentum Strength').classes('text-gray-300')
                    momentum_strength_label = ui.label('--').classes('text-white font-semibold ml-auto')

                with ui.row().classes('items-center gap-2'):
                    volatility_icon = ui.label('○').classes('text-2xl text-gray-400')
                    ui.label('Volatility Level').classes('text-gray-300')
                    volatility_label = ui.label('--').classes('text-white font-semibold ml-auto')

            # Risk Assessment
            with ui.column().classes('flex-1'):
                ui.label('Risk Assessment').classes('text-lg font-semibold text-gray-300 mb-2')
                risk_gauge = ui.linear_progress(value=0.5, show_value=False).classes('mb-2 w-full')
                risk_level_label = ui.label('MODERATE').classes('text-xl font-bold text-orange-400')
                risk_desc_label = ui.label('Standard market conditions').classes('text-sm text-gray-400')

    # ===== DATA STATUS & CONTROLS =====
    with ui.card().classes('w-full p-4'):
        ui.label('📊 Data Status & Controls').classes('text-xl font-bold text-white mb-4')

        with ui.row().classes('w-full items-center gap-4'):
            # Data freshness indicators
            with ui.column().classes('flex-1'):
                ui.label('Data Freshness').classes('text-sm font-semibold text-gray-300')
                data_status_label = ui.label('⚫ No Data').classes('text-lg font-bold')
                data_age_label = ui.label('Waiting for market data...').classes('text-sm text-gray-400')

            # Agent status
            with ui.column().classes('flex-1'):
                ui.label('Agent Status').classes('text-sm font-semibold text-gray-300')
                agent_status_label = ui.label('⚫ Inactive').classes('text-lg font-bold')
                agent_cycle_label = ui.label('Cycle: --').classes('text-sm text-gray-400')

            # Manual refresh controls
            with ui.column().classes('flex-1'):
                ui.label('Manual Controls').classes('text-sm font-semibold text-gray-300')
                with ui.row().classes('gap-2'):
                    ui.button('🔄 Force Refresh', on_click=lambda: force_refresh_data()).classes('bg-blue-600 text-white px-3 py-1 text-sm')
                    ui.button('📊 Export Data', on_click=lambda: export_market_data()).classes('bg-green-600 text-white px-3 py-1 text-sm')

    # ===== UPDATE FUNCTIONS =====
    async def update_market_data():
        """Update market intelligence with latest data from agent"""
        try:
            state = state_manager.get_state()
            selected_asset = asset_select.value

            # Update last refresh time
            current_time = datetime.now(timezone.utc)
            last_update_label.text = f'Last update: {current_time.strftime("%H:%M:%S")}'

            # Update agent status
            if state.active_status:
                agent_status_label.text = '🟢 Active'
                agent_status_label.classes('text-lg font-bold text-green-400')
                agent_cycle_label.text = f'Cycle: {state.cycle_count}'
            else:
                agent_status_label.text = '⚫ Inactive'
                agent_status_label.classes('text-lg font-bold text-gray-400')
                agent_cycle_label.text = 'Cycle: --'

            # Find market data for selected asset
            market_data = None
            if state.market_intelligence and isinstance(state.market_intelligence, list):
                market_data = next((m for m in state.market_intelligence if m.get('asset') == selected_asset), None)

            if not market_data:
                # No data available
                data_status_label.text = '🔴 No Data'
                data_status_label.classes('text-lg font-bold text-red-400')
                data_age_label.text = f'No data for {selected_asset}'
                
                # Reset all displays to default
                current_price_label.text = 'Loading...'
                open_interest_label.text = '--'
                funding_rate_label.text = '--'
                confidence_label.text = '--'
                sentiment_label.text = 'NO DATA'
                sentiment_label.classes('text-4xl font-bold text-gray-500')
                sentiment_desc.text = f'Waiting for {selected_asset} market data from agent...'
                return

            # Data is available
            data_status_label.text = '🟢 Live Data'
            data_status_label.classes('text-lg font-bold text-green-400')
            data_age_label.text = 'Real-time from agent'

            # Update price information
            current_price = market_data.get('current_price', 0)
            if current_price:
                current_price_label.text = f'${current_price:,.2f}'
                
                # Calculate price change from recent prices if available
                recent_prices = market_data.get('recent_mid_prices', [])
                if len(recent_prices) >= 2:
                    price_change = ((current_price - recent_prices[0]) / recent_prices[0]) * 100
                    price_change_label.text = f'{price_change:+.2f}% from start'
                    if price_change >= 0:
                        price_change_label.classes('text-green-400 text-sm mt-1')
                    else:
                        price_change_label.classes('text-red-400 text-sm mt-1')
                else:
                    price_change_label.text = ''
            else:
                current_price_label.text = '--'

            # Update open interest
            open_interest = market_data.get('open_interest', 0)
            if open_interest:
                if open_interest > 1e9:
                    open_interest_label.text = f'${open_interest/1e9:.1f}B'
                elif open_interest > 1e6:
                    open_interest_label.text = f'${open_interest/1e6:.1f}M'
                else:
                    open_interest_label.text = f'${open_interest:,.0f}'
            else:
                open_interest_label.text = '--'

            # Update funding rate
            funding_rate = market_data.get('funding_rate', 0)
            if funding_rate is not None:
                funding_rate_pct = funding_rate * 100
                funding_rate_label.text = f'{funding_rate_pct:+.4f}%'
                
                # Color code funding rate
                if funding_rate_pct > 0.01:
                    funding_rate_label.classes('text-4xl font-bold text-red-400')
                elif funding_rate_pct < -0.01:
                    funding_rate_label.classes('text-4xl font-bold text-green-400')
                else:
                    funding_rate_label.classes('text-4xl font-bold text-white')
                
                # Annual funding rate
                annual_funding = market_data.get('funding_annualized_pct', 0)
                if annual_funding:
                    funding_annual_label.text = f'{annual_funding:+.1f}% annual'
                    funding_annual_label.classes('text-sm mt-1 text-gray-300')
            else:
                funding_rate_label.text = '--'

            # Update technical indicators
            intraday = market_data.get('intraday', {})
            long_term = market_data.get('long_term', {})

            # EMA values
            ema20_5m = intraday.get('ema20')
            ema20_4h = long_term.get('ema20')
            ema50_4h = long_term.get('ema50')

            if ema20_5m:
                ema20_5m_label.text = f'${ema20_5m:,.2f}'
            else:
                ema20_5m_label.text = '--'

            if ema20_4h:
                ema20_4h_label.text = f'${ema20_4h:,.2f}'
            else:
                ema20_4h_label.text = '--'

            if ema50_4h:
                ema50_label.text = f'${ema50_4h:,.2f}'
            else:
                ema50_label.text = '--'

            # RSI values
            rsi7_val = intraday.get('rsi7')
            rsi14_val = intraday.get('rsi14')

            if rsi7_val:
                rsi7_label.text = f'{rsi7_val:.1f}'
            else:
                rsi7_label.text = '--'

            if rsi14_val:
                rsi14_label.text = f'{rsi14_val:.1f}'
                rsi_progress.value = rsi14_val / 100
                
                # Color code RSI
                if rsi14_val > 70:
                    rsi14_label.classes('text-red-400 font-semibold')
                elif rsi14_val < 30:
                    rsi14_label.classes('text-green-400 font-semibold')
                else:
                    rsi14_label.classes('text-white font-semibold')
            else:
                rsi14_label.text = '--'
                rsi_progress.value = 0.5

            # MACD
            macd_val = intraday.get('macd')
            if macd_val:
                macd_line_label.text = f'{macd_val:.4f}'
                if macd_val > 0:
                    macd_line_label.classes('text-green-400 font-semibold')
                else:
                    macd_line_label.classes('text-red-400 font-semibold')
            else:
                macd_line_label.text = '--'

            # Update sentiment analysis
            await update_sentiment_analysis(current_price, ema20_5m, ema20_4h, rsi14_val, macd_val)

            # Update charts
            await update_charts(market_data)

        except Exception as e:
            ui.notify(f'Error updating market data: {str(e)}', type='negative')
            data_status_label.text = '🔴 Error'
            data_status_label.classes('text-lg font-bold text-red-400')

    async def update_sentiment_analysis(current_price, ema20_5m, ema20_4h, rsi14, macd):
        """Update neural sentiment analysis based on indicators"""
        try:
            # Calculate trend signal
            trend_signals = []
            if current_price and ema20_5m and ema20_4h:
                if current_price > ema20_5m > ema20_4h:
                    trend_signals.append('BULLISH')
                elif current_price < ema20_5m < ema20_4h:
                    trend_signals.append('BEARISH')
                else:
                    trend_signals.append('MIXED')

            # Calculate momentum signal
            momentum_signals = []
            if rsi14:
                if rsi14 > 60:
                    momentum_signals.append('STRONG')
                elif rsi14 < 40:
                    momentum_signals.append('WEAK')
                else:
                    momentum_signals.append('NEUTRAL')

            if macd:
                if macd > 0:
                    momentum_signals.append('POSITIVE')
                else:
                    momentum_signals.append('NEGATIVE')

            # Overall sentiment
            bullish_count = trend_signals.count('BULLISH') + momentum_signals.count('STRONG') + momentum_signals.count('POSITIVE')
            bearish_count = trend_signals.count('BEARISH') + momentum_signals.count('WEAK') + momentum_signals.count('NEGATIVE')

            if bullish_count > bearish_count:
                sentiment_label.text = 'BULLISH'
                sentiment_label.classes('text-4xl font-bold text-green-400')
                sentiment_desc.text = 'Neural analysis indicates upward momentum'
                confidence_label.text = f'{min(85, 50 + bullish_count * 10)}%'
            elif bearish_count > bullish_count:
                sentiment_label.text = 'BEARISH'
                sentiment_label.classes('text-4xl font-bold text-red-400')
                sentiment_desc.text = 'Neural analysis indicates downward pressure'
                confidence_label.text = f'{min(85, 50 + bearish_count * 10)}%'
            else:
                sentiment_label.text = 'NEUTRAL'
                sentiment_label.classes('text-4xl font-bold text-gray-400')
                sentiment_desc.text = 'Mixed signals, awaiting clearer direction'
                confidence_label.text = '50%'

            # Update trend signal
            if trend_signals:
                trend_signal = trend_signals[0]
                trend_signal_label.text = trend_signal
                if trend_signal == 'BULLISH':
                    trend_signal_label.classes('text-2xl font-bold text-green-400')
                    trend_desc_label.text = 'Price above key EMAs'
                elif trend_signal == 'BEARISH':
                    trend_signal_label.classes('text-2xl font-bold text-red-400')
                    trend_desc_label.text = 'Price below key EMAs'
                else:
                    trend_signal_label.classes('text-2xl font-bold text-yellow-400')
                    trend_desc_label.text = 'Mixed EMA signals'

            # Update momentum signal
            if momentum_signals:
                if 'STRONG' in momentum_signals or 'POSITIVE' in momentum_signals:
                    momentum_signal_label.text = 'STRONG'
                    momentum_signal_label.classes('text-2xl font-bold text-green-400')
                    momentum_desc_label.text = 'Positive momentum indicators'
                elif 'WEAK' in momentum_signals or 'NEGATIVE' in momentum_signals:
                    momentum_signal_label.text = 'WEAK'
                    momentum_signal_label.classes('text-2xl font-bold text-red-400')
                    momentum_desc_label.text = 'Negative momentum indicators'
                else:
                    momentum_signal_label.text = 'NEUTRAL'
                    momentum_signal_label.classes('text-2xl font-bold text-gray-400')
                    momentum_desc_label.text = 'Balanced momentum'

        except Exception as e:
            print(f"Error in sentiment analysis: {e}")

    async def update_charts(market_data):
        """Update price and indicator charts"""
        try:
            intraday = market_data.get('intraday', {})
            recent_prices = market_data.get('recent_mid_prices', [])
            current_price = market_data.get('current_price', 0)

            if recent_prices and len(recent_prices) > 1:
                # Create time series for recent prices
                times = [f"T-{len(recent_prices)-i}" for i in range(len(recent_prices))]
                
                # Update price chart (main subplot)
                price_chart.figure.data = []
                
                # Price line
                price_chart.figure.add_trace(
                    go.Scatter(
                        x=times, y=recent_prices,
                        mode='lines+markers',
                        name='Price',
                        line=dict(color='#3b82f6', width=3),
                        marker=dict(size=6)
                    ),
                    row=1, col=1
                )

                # EMA lines if available
                ema20_series = intraday.get('series', {}).get('ema20', [])
                if ema20_series and len(ema20_series) == len(recent_prices):
                    price_chart.figure.add_trace(
                        go.Scatter(
                            x=times, y=ema20_series,
                            mode='lines',
                            name='EMA20',
                            line=dict(color='#f59e0b', width=2)
                        ),
                        row=1, col=1
                    )

                # RSI chart
                rsi_series = intraday.get('series', {}).get('rsi14', [])
                if rsi_series and len(rsi_series) == len(recent_prices):
                    price_chart.figure.add_trace(
                        go.Scatter(
                            x=times, y=rsi_series,
                            mode='lines',
                            name='RSI',
                            line=dict(color='#ef4444', width=2)
                        ),
                        row=2, col=1
                    )
                    
                    # RSI overbought/oversold lines
                    price_chart.figure.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=2, col=1)
                    price_chart.figure.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=2, col=1)

                # MACD chart
                macd_series = intraday.get('series', {}).get('macd', [])
                if macd_series and len(macd_series) == len(recent_prices):
                    price_chart.figure.add_trace(
                        go.Scatter(
                            x=times, y=macd_series,
                            mode='lines',
                            name='MACD',
                            line=dict(color='#8b5cf6', width=2)
                        ),
                        row=3, col=1
                    )
                    
                    # MACD zero line
                    price_chart.figure.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, row=3, col=1)

                price_chart.update()

        except Exception as e:
            print(f"Error updating charts: {e}")

    async def force_refresh_data():
        """Force refresh market data from agent service"""
        try:
            ui.notify('Forcing data refresh...', type='info')
            success = await agent_service.refresh_market_data()
            if success:
                await update_market_data()
                ui.notify('Market data refreshed successfully!', type='positive')
            else:
                ui.notify('Failed to refresh market data', type='negative')
        except Exception as e:
            ui.notify(f'Refresh error: {str(e)}', type='negative')

    async def export_market_data():
        """Export current market data to JSON"""
        try:
            state = state_manager.get_state()
            if state.market_intelligence:
                import json
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'market_data_{timestamp}.json'
                
                data = {
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'market_intelligence': state.market_intelligence,
                    'agent_status': {
                        'active': state.active_status,
                        'cycle_count': state.cycle_count,
                        'last_sync': state.last_sync
                    }
                }
                
                json_str = json.dumps(data, indent=2, default=str)
                ui.download(json_str, filename)
                ui.notify(f'Exported {filename}', type='positive')
            else:
                ui.notify('No market data to export', type='warning')
        except Exception as e:
            ui.notify(f'Export error: {str(e)}', type='negative')

    # ===== AUTO-REFRESH & EVENT HANDLERS =====
    
    # Auto-refresh every 3 seconds
    ui.timer(3.0, update_market_data)

    # Refresh on asset/interval change
    asset_select.on('update:model-value', lambda: update_market_data())
    interval_select.on('update:model-value', lambda: update_market_data())

    # Initial update
    ui.timer(0.5, update_market_data)  # Slight delay for initialization
