"""
QuantumAlpha Capital - Comprehensive Trading Command Center
Professional agentic trading platform with advanced analytics
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from nicegui import ui
from datetime import datetime, timezone
from src.gui.services.bot_service import AgentService
from src.gui.services.state_manager import StateManager

# Import modular components - using try/except for graceful fallback
try:
    from src.gui.components.charts_widget import (
        create_equity_chart,
        create_allocation_chart, 
        create_technical_chart, 
        update_portfolio_charts, 
        update_technical_chart
    )
    from src.gui.components.positions_widget import (
        create_positions_table, 
        update_positions_table
    )
    from src.gui.components.proposals_widget import (
        create_proposals_widget, 
        update_proposals_widget
    )
    MODULAR_COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import modular components: {e}")
    MODULAR_COMPONENTS_AVAILABLE = False


def create_dashboard(agent_service: AgentService, state_manager: StateManager):
    """Create comprehensive trading command center using modular components"""

    # Professional header
    with ui.row().classes('w-full items-center justify-between mb-6'):
        with ui.row().classes('items-center gap-4'):
            ui.icon('dashboard', size='48px').classes('text-cyan-400')
            with ui.column().classes('gap-1'):
                ui.label('QuantumAlpha Capital').classes('text-4xl font-bold text-white')
                ui.label('Onchain Agentic Trading Platform').classes('text-lg text-cyan-300')
        
        # System status indicator
        system_status = ui.label('STANDBY').classes('text-xl font-bold text-gray-400')

    # Top Metrics Row (Original 4 metrics)
    with ui.grid(columns=4).classes('w-full gap-4 mb-6'):
        # Portfolio Balance
        with ui.card().classes('p-4 bg-gradient-to-br from-blue-900 to-blue-950 border border-blue-700'):
            balance_value = ui.label('$0.00').classes('text-3xl font-bold text-white')
            ui.label('Total Balance').classes('text-sm text-blue-200 mt-1')

        # Total Return
        with ui.card().classes('p-4 bg-gradient-to-br from-green-900 to-green-950 border border-green-700'):
            return_value = ui.label('+0.00%').classes('text-3xl font-bold text-white')
            ui.label('Total Return').classes('text-sm text-green-200 mt-1')

        # Sharpe Ratio (restored from original)
        with ui.card().classes('p-4 bg-gradient-to-br from-purple-900 to-purple-950 border border-purple-700'):
            sharpe_value = ui.label('0.00').classes('text-3xl font-bold text-white')
            ui.label('Sharpe Ratio').classes('text-sm text-purple-200 mt-1')

        # Active Positions
        with ui.card().classes('p-4 bg-gradient-to-br from-orange-900 to-orange-950 border border-orange-700'):
            positions_count = ui.label('0').classes('text-3xl font-bold text-white')
            ui.label('Active Positions').classes('text-sm text-orange-200 mt-1')

    # Main Content Grid
    with ui.row().classes('w-full gap-4 mb-6'):
        # LEFT COLUMN - Charts (60% width)
        with ui.column().classes('flex-[3] gap-4'):
            # Portfolio Charts Row using modular components or fallback
            with ui.row().classes('w-full gap-4 mb-4'):
                # Portfolio Value Chart (left half)
                with ui.card().classes('flex-1 p-4'):
                    ui.label('Portfolio Value').classes('text-xl font-bold text-white mb-2')
                    
                    if MODULAR_COMPONENTS_AVAILABLE:
                        equity_chart = create_equity_chart()
                    else:
                        # Fallback implementation
                        equity_chart = ui.plotly(go.Figure(
                            data=[go.Scatter(
                                x=[],
                                y=[],
                                mode='lines',
                                name='Value',
                                line=dict(color='#667eea', width=3)
                            )],
                            layout=go.Layout(
                                template='plotly_dark',
                                height=300,
                                margin=dict(l=50, r=20, t=20, b=40),
                                xaxis=dict(title='Time', showgrid=True, gridcolor='#374151'),
                                yaxis=dict(title='Value ($)', showgrid=True, gridcolor='#374151'),
                                paper_bgcolor='#1f2937',
                                plot_bgcolor='#1f2937',
                                font=dict(color='#e5e7eb')
                            )
                        )).classes('w-full')

                # Asset Allocation Pie Chart (right half)
                with ui.card().classes('flex-1 p-4'):
                    ui.label('Asset Allocation').classes('text-xl font-bold text-white mb-2')
                    
                    if MODULAR_COMPONENTS_AVAILABLE:
                        allocation_chart = create_allocation_chart()
                    else:
                        # Fallback implementation
                        allocation_chart = ui.plotly(go.Figure(
                            data=[go.Pie(
                                labels=[],
                                values=[],
                                hole=0.4,
                                marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#4facfe'])
                            )],
                            layout=go.Layout(
                                template='plotly_dark',
                                height=300,
                                margin=dict(l=20, r=20, t=20, b=20),
                                paper_bgcolor='#1f2937',
                                plot_bgcolor='#1f2937',
                                font=dict(color='#e5e7eb'),
                                showlegend=True,
                                legend=dict(orientation='v', x=1, y=0.5)
                            )
                        )).classes('w-full')

            # Market Intelligence Grid
            with ui.card().classes('w-full p-4'):
                ui.label('Market Intelligence').classes('text-xl font-bold text-white mb-4')
                
                market_data_container = ui.row().classes('w-full gap-4')
                with market_data_container:
                    ui.label('Loading market data...').classes('text-gray-400 text-center py-4')

        # RIGHT COLUMN - Positions & Activity (40% width)
        with ui.column().classes('flex-[2] gap-4'):
            # Active Positions Section using modular component
            with ui.card().classes('w-full p-4'):
                with ui.row().classes('w-full items-center justify-between mb-4'):
                    ui.label('Active Positions').classes('text-xl font-bold text-white')
                    ui.button('Refresh', on_click=lambda: None).classes('bg-blue-600 hover:bg-blue-700 px-3 py-1 text-sm')

                # Use modular positions table or fallback
                if MODULAR_COMPONENTS_AVAILABLE:
                    positions_table, positions_empty = create_positions_table(agent_service, state_manager)
                else:
                    # Fallback implementation
                    positions_columns = [
                        {'name': 'symbol', 'label': 'Asset', 'field': 'symbol', 'align': 'left'},
                        {'name': 'side', 'label': 'Side', 'field': 'side', 'align': 'center'},
                        {'name': 'size', 'label': 'Size', 'field': 'size', 'align': 'right'},
                        {'name': 'pnl', 'label': 'PnL', 'field': 'pnl', 'align': 'right'},
                        {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'align': 'center'},
                    ]
                    
                    positions_table = ui.table(
                        columns=positions_columns,
                        rows=[],
                        row_key='symbol',
                        pagination={'rowsPerPage': 5}
                    ).classes('w-full bg-gray-800 text-white')

                    # Enhanced PnL cell styling
                    positions_table.add_slot('body-cell-pnl', '''
                        <q-td :props="props">
                            <span :class="props.row.pnl >= 0 ? 'text-green-400' : 'text-red-400'" class="font-bold">
                                {{ props.row.pnl >= 0 ? '+' : '' }}${{ Math.abs(props.row.pnl).toFixed(2) }}
                            </span>
                        </q-td>
                    ''')

                    # Side indicator styling
                    positions_table.add_slot('body-cell-side', '''
                        <q-td :props="props">
                            <q-badge 
                                :color="props.row.side === 'LONG' ? 'green' : 'red'" 
                                :label="props.row.side"
                                class="text-xs font-bold"
                            />
                        </q-td>
                    ''')

                    # Action buttons
                    positions_table.add_slot('body-cell-actions', '''
                        <q-td :props="props">
                            <q-btn 
                                flat dense round 
                                icon="close" 
                                color="red" 
                                size="sm" 
                                @click="$parent.$emit('close', props.row)"
                            />
                        </q-td>
                    ''')

                    # Empty state for positions
                    positions_empty = ui.column().classes('w-full items-center py-8')
                    with positions_empty:
                        ui.icon('account_balance', size='48px').classes('text-gray-600 mb-2')
                        ui.label('No Active Positions').classes('text-lg text-gray-400')
                        ui.label('Neural analysis will identify optimal entries').classes('text-sm text-gray-500')

            # Agent Controls & Activity Feed
            with ui.card().classes('w-full p-4'):
                ui.label('Agent Controls').classes('text-xl font-bold text-white mb-4')

                with ui.row().classes('gap-4 items-center mb-4'):
                    # Start/Stop buttons
                    start_btn = ui.button('Start Agent', on_click=lambda: start_agent())
                    start_btn.classes('bg-green-600 hover:bg-green-700 text-white px-6 py-3')

                    stop_btn = ui.button('Stop Agent', on_click=lambda: stop_agent())
                    stop_btn.classes('bg-red-600 hover:bg-red-700 text-white px-6 py-3')
                    stop_btn.props('disable')

                    # Refresh data button
                    refresh_btn = ui.button('Refresh Data', on_click=lambda: refresh_market_data())
                    refresh_btn.classes('bg-blue-600 hover:bg-blue-700 text-white px-4 py-3')

                # Status indicators
                with ui.row().classes('gap-4 items-center mb-4'):
                    status_indicator = ui.label('Stopped').classes('text-lg font-bold')
                    last_refresh_label = ui.label('Last refresh: Never').classes('text-sm text-gray-400')

                # Activity Feed
                ui.label('Activity Feed').classes('text-lg font-bold text-white mb-2')
                activity_log = ui.log(max_lines=6).classes('w-full h-24 bg-gray-900 text-gray-300 p-4 rounded')
                activity_log.push('QuantumAlpha Capital initialized. Ready for neural analysis...')

    # Bottom Row - Technical Analysis & Neural Proposals
    with ui.row().classes('w-full gap-4 mb-6'):
        # Technical Analysis Chart (Left - 60%) using modular component
        with ui.card().classes('flex-[3] p-4'):
            ui.label('Technical Analysis').classes('text-xl font-bold text-white mb-2')
            
            # Asset selector for technical chart
            with ui.row().classes('items-center gap-4 mb-4'):
                ui.label('Asset:').classes('text-white')
                asset_select = ui.select(
                    options=['BTC', 'ETH', 'LTC'],
                    value='BTC'
                ).classes('w-32')
                
                ui.label('Timeframe:').classes('text-white ml-4')
                timeframe_select = ui.select(
                    options=['5m', '15m', '1h', '4h', '1d'],
                    value='5m'
                ).classes('w-24')

            # Use modular technical chart or fallback
            if MODULAR_COMPONENTS_AVAILABLE:
                technical_chart = create_technical_chart()
            else:
                # Fallback implementation
                technical_chart = ui.plotly(go.Figure()).classes('w-full')
                
                # Initialize with proper dark theme
                technical_chart.figure = make_subplots(
                    rows=3, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.05,
                    subplot_titles=('Price & EMAs', 'RSI', 'MACD'),
                    row_heights=[0.6, 0.2, 0.2]
                )

                # Apply dark theme immediately
                technical_chart.figure.update_layout(
                    template='plotly_dark',
                    height=400,
                    margin=dict(l=50, r=20, t=60, b=40),
                    paper_bgcolor='#1f2937',
                    plot_bgcolor='#1f2937',
                    font=dict(color='#e5e7eb', size=12),
                    showlegend=True,
                    legend=dict(
                        x=0, y=1, 
                        bgcolor='rgba(31, 41, 55, 0.9)',
                        bordercolor='#374151',
                        borderwidth=1,
                        font=dict(color='#e5e7eb')
                    )
                )

                # Force dark background on all subplots
                for i in range(1, 4):
                    technical_chart.figure.update_xaxes(
                        gridcolor='#374151',
                        zerolinecolor='#4b5563',
                        tickcolor='#6b7280',
                        linecolor='#4b5563',
                        tickfont=dict(color='#e5e7eb'),
                        row=i, col=1
                    )
                    technical_chart.figure.update_yaxes(
                        gridcolor='#374151',
                        zerolinecolor='#4b5563',
                        tickcolor='#6b7280',
                        linecolor='#4b5563',
                        tickfont=dict(color='#e5e7eb'),
                        row=i, col=1
                    )
                
                # Add sample data
                import datetime
                now = datetime.datetime.now()
                sample_times = [(now - datetime.timedelta(minutes=i*5)).strftime('%H:%M') for i in range(12, 0, -1)]
                sample_prices = [50000 + i*100 + (i%3)*200 for i in range(12)]
                sample_rsi = [50 + (i%6)*5 for i in range(12)]
                sample_macd = [(i%4 - 2)*0.1 for i in range(12)]
                
                # Add sample price data
                technical_chart.figure.add_trace(
                    go.Scatter(
                        x=sample_times, y=sample_prices,
                        mode='lines',
                        name='BTC Price',
                        line=dict(color='#3b82f6', width=2)
                    ),
                    row=1, col=1
                )
                
                # Add sample RSI data
                technical_chart.figure.add_trace(
                    go.Scatter(
                        x=sample_times, y=sample_rsi,
                        mode='lines',
                        name='RSI',
                        line=dict(color='#ef4444', width=2)
                    ),
                    row=2, col=1
                )
                
                # Add RSI levels
                technical_chart.figure.add_hline(y=70, line_dash="dash", line_color="#ef4444", opacity=0.5, row=2, col=1)
                technical_chart.figure.add_hline(y=30, line_dash="dash", line_color="#10b981", opacity=0.5, row=2, col=1)
                
                # Add sample MACD data
                technical_chart.figure.add_trace(
                    go.Scatter(
                        x=sample_times, y=sample_macd,
                        mode='lines',
                        name='MACD',
                        line=dict(color='#8b5cf6', width=2)
                    ),
                    row=3, col=1
                )
                
                # Add MACD zero line
                technical_chart.figure.add_hline(y=0, line_dash="dash", line_color="#6b7280", opacity=0.5, row=3, col=1)

        # Neural Proposals Section (Right - 40%) using modular component
        with ui.card().classes('flex-[2] p-4'):
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label('Neural Proposals').classes('text-xl font-bold text-white')
                proposals_count_badge = ui.badge('0', color='purple').classes('text-sm')

            # Use modular proposals widget or fallback
            if MODULAR_COMPONENTS_AVAILABLE:
                proposals_container, proposals_empty, create_proposal_card = create_proposals_widget(agent_service, state_manager)
            else:
                # Fallback implementation
                proposals_container = ui.column().classes('w-full gap-3')
                
                # Empty state for proposals
                proposals_empty = ui.column().classes('w-full items-center py-8')
                with proposals_empty:
                    ui.icon('lightbulb_outline', size='48px').classes('text-gray-600 mb-2')
                    ui.label('No Proposals').classes('text-lg text-gray-400')
                    ui.label('AI will generate recommendations').classes('text-sm text-gray-500')

                def create_proposal_card(proposal: dict):
                    """Create a compact proposal card for the sidebar"""
                    asset = proposal.get('asset', 'N/A')
                    action = proposal.get('action', 'hold')
                    confidence = proposal.get('confidence', 0)
                    entry_price = proposal.get('entry_price', 0)
                    proposal_id = proposal.get('id', '')

                    # Action styling
                    if action == 'buy':
                        action_color = 'bg-green-600'
                    elif action == 'sell':
                        action_color = 'bg-red-600'
                    else:
                        action_color = 'bg-gray-600'

                    with ui.card().classes(f'w-full p-3 bg-gradient-to-r from-gray-800 to-gray-900 border border-gray-600'):
                        # Header
                        with ui.row().classes('w-full items-center justify-between mb-2'):
                            ui.label(asset).classes('text-lg font-bold text-white')
                            
                            with ui.badge().classes(f'{action_color} text-white text-xs px-2 py-1'):
                                ui.label(action.upper()).classes('font-bold')

                        # Details
                        with ui.row().classes('w-full justify-between items-center mb-2'):
                            ui.label(f'${entry_price:,.2f}').classes('text-sm text-gray-300')
                            ui.label(f'{confidence:.0f}%').classes('text-sm text-cyan-400 font-bold')

                        # Actions
                        with ui.row().classes('w-full gap-2'):
                            ui.button('Reject', on_click=lambda pid=proposal_id: reject_proposal(pid)).classes('bg-red-600 hover:bg-red-700 flex-1 py-1 text-xs')
                            ui.button('Approve', on_click=lambda pid=proposal_id: approve_proposal(pid)).classes('bg-green-600 hover:bg-green-700 flex-1 py-1 text-xs')

    # Technical Indicators Panel
    with ui.card().classes('w-full p-4'):
        ui.label('Technical Analysis Dashboard').classes('text-xl font-bold text-white mb-4')
        
        with ui.row().classes('w-full gap-4'):
            # Trend Analysis
            with ui.card().classes('flex-1 p-4 bg-gradient-to-br from-gray-800 to-gray-900'):
                ui.label('Trend Analysis').classes('text-lg font-bold text-blue-400 mb-3')
                
                with ui.column().classes('gap-2 w-full'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label('EMA 20 (5m)').classes('text-gray-300')
                        ema20_5m_label = ui.label('$0.00').classes('text-white font-semibold')

                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label('EMA 20 (4h)').classes('text-gray-300')
                        ema20_4h_label = ui.label('$0.00').classes('text-white font-semibold')

                    ui.separator()
                    trend_signal_label = ui.label('NEUTRAL').classes('text-xl font-bold text-gray-400')

            # Momentum Analysis
            with ui.card().classes('flex-1 p-4 bg-gradient-to-br from-gray-800 to-gray-900'):
                ui.label('Momentum Analysis').classes('text-lg font-bold text-yellow-400 mb-3')
                
                with ui.column().classes('gap-2 w-full'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label('RSI 14').classes('text-gray-300')
                        rsi14_label = ui.label('50.00').classes('text-white font-semibold')

                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label('MACD').classes('text-gray-300')
                        macd_label = ui.label('0.00').classes('text-white font-semibold')

                    ui.separator()
                    momentum_signal_label = ui.label('NEUTRAL').classes('text-xl font-bold text-gray-400')

            # Neural Sentiment
            with ui.card().classes('flex-1 p-4 bg-gradient-to-br from-gray-800 to-gray-900'):
                ui.label('Neural Sentiment').classes('text-lg font-bold text-purple-400 mb-3')
                
                with ui.column().classes('gap-2 w-full'):
                    sentiment_label = ui.label('ANALYZING').classes('text-2xl font-bold text-gray-400')
                    sentiment_desc = ui.label('Neural analysis in progress...').classes('text-sm text-gray-400')
                    
                    ui.separator()
                    confidence_progress = ui.linear_progress(value=0.5, show_value=False).classes('w-full')

    # Control Functions

    async def approve_proposal(proposal_id: str):
        """Approve a trade proposal"""
        try:
            success = agent_service.approve_proposal(proposal_id)
            if success:
                activity_log.push(f'Proposal {proposal_id[:8]} approved')
                ui.notify('Trade Approved!', type='positive')
            else:
                ui.notify('Approval Failed', type='negative')
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')

    async def reject_proposal(proposal_id: str):
        """Reject a trade proposal"""
        try:
            success = agent_service.reject_proposal(proposal_id, "Rejected via dashboard")
            if success:
                activity_log.push(f'Proposal {proposal_id[:8]} rejected')
                ui.notify('Proposal Rejected', type='warning')
            else:
                ui.notify('Rejection Failed', type='negative')
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')

    async def close_position_handler(e):
        """Handle position closure from table"""
        position = e.args
        symbol = position['symbol']
        
        try:
            activity_log.push(f'Closing {symbol} position...')
            success = await agent_service.close_position(symbol)
            
            if success:
                activity_log.push(f'{symbol} position closed successfully!')
                ui.notify(f'{symbol} Position Closed!', type='positive')
            else:
                activity_log.push(f'Failed to close {symbol} position')
                ui.notify(f'Failed to close {symbol}', type='negative')
        except Exception as e:
            activity_log.push(f'Close error: {str(e)}')
            ui.notify(f'Error: {str(e)}', type='negative')

    async def start_agent():
        """Start the trading agent"""
        try:
            system_status.text = 'STARTING...'
            system_status.classes(remove='text-green-400 text-gray-400 text-red-400', add='text-yellow-400')
            activity_log.push('Starting QuantumAlpha neural engine...')

            await agent_service.start()

            system_status.text = 'ACTIVE'
            system_status.classes(remove='text-yellow-400 text-gray-400 text-red-400', add='text-green-400')
            status_indicator.text = 'Running'
            status_indicator.classes(remove='text-gray-400 text-red-500', add='text-green-500')
            start_btn.props('disable')
            stop_btn.props(remove='disable')

            activity_log.push('Neural engine activated successfully!')
            ui.notify('QuantumAlpha Agent Started!', type='positive')

        except Exception as e:
            system_status.text = 'ERROR'
            system_status.classes(remove='text-green-400 text-yellow-400 text-gray-400', add='text-red-400')
            status_indicator.text = 'Error'
            status_indicator.classes(remove='text-green-500 text-gray-400', add='text-red-500')
            activity_log.push(f'Startup error: {str(e)}')
            ui.notify(f'Failed to start: {str(e)}', type='negative')

    async def stop_agent():
        """Stop the trading agent"""
        try:
            system_status.text = 'STOPPING...'
            system_status.classes(remove='text-green-400 text-gray-400 text-red-400', add='text-yellow-400')
            activity_log.push('Stopping neural engine...')

            await agent_service.stop()

            system_status.text = 'STANDBY'
            system_status.classes(remove='text-yellow-400 text-green-400 text-red-400', add='text-gray-400')
            status_indicator.text = 'Stopped'
            status_indicator.classes(remove='text-green-500 text-red-500', add='text-gray-400')
            start_btn.props(remove='disable')
            stop_btn.props('disable')

            activity_log.push('Neural engine stopped successfully!')
            ui.notify('Agent Stopped', type='info')

        except Exception as e:
            activity_log.push(f'Stop error: {str(e)}')
            ui.notify(f'Failed to stop: {str(e)}', type='negative')

    async def refresh_market_data():
        """Refresh market data from Hyperliquid"""
        try:
            refresh_btn.enabled = False
            activity_log.push('Refreshing market intelligence...')

            success = await agent_service.refresh_market_data()

            if success:
                last_refresh_label.text = f'Last refresh: {datetime.now().strftime("%H:%M:%S")}'
                activity_log.push('Market data refreshed successfully!')
                ui.notify('Market Data Updated!', type='positive')
                await update_dashboard()
            else:
                activity_log.push('Failed to refresh market data')
                ui.notify('Refresh Failed', type='negative')

        except Exception as e:
            activity_log.push(f'Refresh error: {str(e)}')
            ui.notify(f'Error: {str(e)}', type='negative')
        finally:
            refresh_btn.enabled = True

    async def update_dashboard():
        """Update all dashboard components using modular functions"""
        try:
            state = state_manager.get_state()

            # Update top metrics - restored original 4 metrics
            balance_value.text = f'${state.account_balance:,.2f}'

            # Return with color coding
            return_pct = state.performance_ratio
            return_value.text = f'{return_pct:+.2f}%'
            if return_pct >= 0:
                return_value.classes(remove='text-red-400', add='text-green-400')
            else:
                return_value.classes(remove='text-green-400', add='text-red-400')

            # Sharpe Ratio (restored from original)
            sharpe_value.text = f'{state.risk_metric:.2f}'

            # Positions data
            positions = state.open_positions or []
            positions_count.text = str(len(positions))

            # Update portfolio charts using modular function or fallback
            equity_history = agent_service.get_equity_history()
            if MODULAR_COMPONENTS_AVAILABLE:
                update_portfolio_charts(equity_chart, allocation_chart, equity_history, positions, state.account_balance)
            else:
                # Fallback implementation
                if equity_history and len(equity_history) > 0:
                    times = [d['time'] for d in equity_history]
                    values = [d['value'] for d in equity_history]
                    equity_chart.figure.data[0].x = times
                    equity_chart.figure.data[0].y = values
                    equity_chart.update()
                else:
                    # Show sample data
                    import datetime
                    now = datetime.datetime.now()
                    sample_times = [(now - datetime.timedelta(hours=i)).strftime('%H:%M') for i in range(24, 0, -1)]
                    base_value = state.account_balance or 1000
                    sample_values = []
                    for i in range(24):
                        growth = base_value * (1 + (i * 0.002))
                        volatility = base_value * 0.01 * (0.5 - (i % 7) / 14)
                        sample_values.append(growth + volatility)
                    
                    equity_chart.figure.data[0].x = sample_times
                    equity_chart.figure.data[0].y = sample_values
                    equity_chart.update()

                # Update allocation chart
                if positions and len(positions) > 0:
                    labels = []
                    values = []
                    for pos in positions:
                        symbol = pos.get('symbol', '')
                        quantity = abs(pos.get('quantity', 0))
                        current_price = pos.get('current_price', 0)
                        position_value = quantity * current_price
                        
                        if position_value > 0:
                            labels.append(symbol)
                            values.append(position_value)

                    total_position_value = sum(values)
                    cash_allocation = max(0, state.account_balance - total_position_value)
                    if cash_allocation > 0:
                        labels.append('Cash')
                        values.append(cash_allocation)

                    allocation_chart.figure.data[0].labels = labels
                    allocation_chart.figure.data[0].values = values
                    allocation_chart.update()
                else:
                    base_balance = state.account_balance or 1000
                    allocation_chart.figure.data[0].labels = ['BTC', 'ETH', 'Cash']
                    allocation_chart.figure.data[0].values = [base_balance * 0.4, base_balance * 0.3, base_balance * 0.3]
                    allocation_chart.update()

            # Update positions table using modular function or fallback
            if MODULAR_COMPONENTS_AVAILABLE:
                update_positions_table(positions_table, positions_empty, positions)
            else:
                # Fallback implementation
                positions_empty.visible = len(positions) == 0
                positions_table.visible = len(positions) > 0
                
                if positions:
                    rows = []
                    for pos in positions:
                        quantity = pos.get('quantity', 0)
                        rows.append({
                            'symbol': pos.get('symbol', ''),
                            'side': 'LONG' if quantity > 0 else 'SHORT',
                            'size': f'{abs(quantity):.4f}',
                            'pnl': pos.get('unrealized_pnl', 0),
                        })
                    positions_table.rows = rows
                    positions_table.update()

            # Update proposals using modular function or fallback
            proposals = state.awaiting_approval or []
            proposals_count_badge.text = str(len(proposals))
            if MODULAR_COMPONENTS_AVAILABLE:
                update_proposals_widget(proposals_container, proposals_empty, proposals, create_proposal_card)
            else:
                # Fallback implementation
                proposals_empty.visible = len(proposals) == 0
                
                proposals_container.clear()
                if proposals:
                    with proposals_container:
                        for proposal in proposals[:3]:  # Show max 3 in sidebar
                            create_proposal_card(proposal)

            # Update market intelligence
            await update_market_intelligence(state)

            # Update technical indicators
            await update_technical_indicators(state)

            # Update system status
            if state.active_status:
                system_status.text = 'ACTIVE'
                system_status.classes(remove='text-yellow-400 text-gray-400 text-red-400', add='text-green-400')
            else:
                system_status.text = 'STANDBY'
                system_status.classes(remove='text-yellow-400 text-green-400 text-red-400', add='text-gray-400')

        except Exception as e:
            activity_log.push(f'Dashboard update error: {str(e)}')
            print(f"Dashboard update error: {e}")

    async def update_market_intelligence(state):
        """Update market intelligence section"""
        try:
            market_data = state.market_intelligence if hasattr(state, 'market_intelligence') else []
            
            market_data_container.clear()
            
            if market_data and isinstance(market_data, list) and len(market_data) > 0:
                with market_data_container:
                    for asset_data in market_data[:3]:  # Show max 3 assets
                        asset = asset_data.get('asset', 'N/A')
                        price = asset_data.get('current_price', 0)
                        
                        with ui.card().classes('flex-1 p-3 bg-gradient-to-br from-gray-700 to-gray-800 border border-gray-600'):
                            ui.label(asset).classes('text-lg font-bold text-white mb-1')
                            ui.label(f'${price:,.2f}').classes('text-xl text-green-400 mb-2')
                            
                            # Quick indicators
                            intraday = asset_data.get('intraday', {})
                            rsi = intraday.get('rsi14', 0)
                            if rsi:
                                rsi_color = 'text-red-400' if rsi > 70 else 'text-green-400' if rsi < 30 else 'text-gray-400'
                                ui.label(f'RSI: {rsi:.1f}').classes(f'text-sm {rsi_color}')
            else:
                with market_data_container:
                    ui.label('No market data available').classes('text-gray-400 text-center py-4')

        except Exception as e:
            print(f"Error updating market intelligence: {e}")

    async def update_technical_indicators(state):
        """Update technical indicators panel"""
        try:
            # Get market data for selected asset
            selected_asset = asset_select.value
            market_data = None
            
            if hasattr(state, 'market_intelligence') and state.market_intelligence:
                market_data = next((m for m in state.market_intelligence if m.get('asset') == selected_asset), None)

            if market_data:
                # Update EMA values
                intraday = market_data.get('intraday', {})
                long_term = market_data.get('long_term', {})
                
                ema20_5m = intraday.get('ema20')
                ema20_4h = long_term.get('ema20')
                
                if ema20_5m:
                    ema20_5m_label.text = f'${ema20_5m:,.2f}'
                else:
                    ema20_5m_label.text = '--'
                    
                if ema20_4h:
                    ema20_4h_label.text = f'${ema20_4h:,.2f}'
                else:
                    ema20_4h_label.text = '--'

                # Update RSI and MACD
                rsi14 = intraday.get('rsi14')
                macd = intraday.get('macd')
                
                if rsi14:
                    rsi14_label.text = f'{rsi14:.1f}'
                    if rsi14 > 70:
                        rsi14_label.classes('text-red-400 font-semibold')
                    elif rsi14 < 30:
                        rsi14_label.classes('text-green-400 font-semibold')
                    else:
                        rsi14_label.classes('text-white font-semibold')
                else:
                    rsi14_label.text = '--'

                if macd:
                    macd_label.text = f'{macd:.4f}'
                    if macd > 0:
                        macd_label.classes('text-green-400 font-semibold')
                    else:
                        macd_label.classes('text-red-400 font-semibold')
                else:
                    macd_label.text = '--'

                # Update sentiment analysis
                await update_sentiment_analysis(market_data)

                # Update technical analysis chart using modular function or fallback
                if MODULAR_COMPONENTS_AVAILABLE:
                    update_technical_chart(technical_chart, market_data)
                else:
                    # Enhanced fallback implementation with RSI and MACD
                    try:
                        recent_prices = market_data.get('recent_mid_prices', [])
                        intraday = market_data.get('intraday', {})
                        
                        if recent_prices and len(recent_prices) > 1:
                            max_points = min(12, len(recent_prices))
                            recent_prices = recent_prices[-max_points:]
                            
                            times = [f"T-{len(recent_prices)-i}" for i in range(len(recent_prices))]
                            
                            # Clear existing data and rebuild
                            technical_chart.figure.data = []
                            
                            # Add price data (subplot 1)
                            technical_chart.figure.add_trace(
                                go.Scatter(
                                    x=times, y=recent_prices,
                                    mode='lines',
                                    name='Price',
                                    line=dict(color='#3b82f6', width=2)
                                ),
                                row=1, col=1
                            )
                            
                            # Add EMA if available
                            ema20_series = intraday.get('series', {}).get('ema20', [])
                            if ema20_series and len(ema20_series) >= max_points:
                                ema20_data = ema20_series[-max_points:]
                                technical_chart.figure.add_trace(
                                    go.Scatter(
                                        x=times, y=ema20_data,
                                        mode='lines',
                                        name='EMA20',
                                        line=dict(color='#f59e0b', width=2)
                                    ),
                                    row=1, col=1
                                )
                            
                            # Add RSI data (subplot 2)
                            rsi_series = intraday.get('series', {}).get('rsi14', [])
                            if rsi_series and len(rsi_series) >= max_points:
                                rsi_data = rsi_series[-max_points:]
                                # Ensure RSI values are valid (0-100 range)
                                rsi_data = [max(0, min(100, val)) for val in rsi_data if isinstance(val, (int, float))]
                                if rsi_data:
                                    technical_chart.figure.add_trace(
                                        go.Scatter(
                                            x=times[:len(rsi_data)], y=rsi_data,
                                            mode='lines',
                                            name='RSI',
                                            line=dict(color='#ef4444', width=2)
                                        ),
                                        row=2, col=1
                                    )
                                    
                                    # Add RSI reference lines
                                    technical_chart.figure.add_hline(y=70, line_dash="dash", line_color="#ef4444", opacity=0.5, row=2, col=1)
                                    technical_chart.figure.add_hline(y=30, line_dash="dash", line_color="#10b981", opacity=0.5, row=2, col=1)
                            
                            # Add MACD data (subplot 3)
                            macd_series = intraday.get('series', {}).get('macd', [])
                            if macd_series and len(macd_series) >= max_points:
                                macd_data = macd_series[-max_points:]
                                # Filter out invalid MACD values
                                macd_data = [val for val in macd_data if isinstance(val, (int, float)) and not (val != val)]  # Remove NaN
                                if macd_data:
                                    technical_chart.figure.add_trace(
                                        go.Scatter(
                                            x=times[:len(macd_data)], y=macd_data,
                                            mode='lines',
                                            name='MACD',
                                            line=dict(color='#8b5cf6', width=2)
                                        ),
                                        row=3, col=1
                                    )
                                    
                                    # Add MACD zero line
                                    technical_chart.figure.add_hline(y=0, line_dash="dash", line_color="#6b7280", opacity=0.5, row=3, col=1)
                            
                            # Update the chart
                            technical_chart.update()
                            
                    except Exception as e:
                        print(f"Error updating technical chart: {e}")
                        import traceback
                        traceback.print_exc()

        except Exception as e:
            print(f"Error updating technical indicators: {e}")

    # Cache for technical chart data to avoid unnecessary updates
    _last_technical_update = None
    _technical_cache = {}

    async def update_technical_chart_optimized(market_data):
        """OPTIMIZED: Update technical analysis chart with faster performance"""
        nonlocal _last_technical_update, _technical_cache
        
        try:
            # PERFORMANCE: Check if we need to update (throttle updates)
            import time
            current_time = time.time()
            if _last_technical_update and (current_time - _last_technical_update) < 3.0:
                return  # Skip update if less than 3 seconds since last update
            
            recent_prices = market_data.get('recent_mid_prices', [])
            if recent_prices and len(recent_prices) > 1:
                # PERFORMANCE: Limit data points to last 12 for speed
                max_points = 12
                if len(recent_prices) > max_points:
                    recent_prices = recent_prices[-max_points:]
                
                times = [f"T-{len(recent_prices)-i}" for i in range(len(recent_prices))]
                
                # PERFORMANCE: Update existing traces instead of recreating
                if len(technical_chart.figure.data) >= 3:
                    technical_chart.figure.data[0].x = times
                    technical_chart.figure.data[0].y = recent_prices

                    # Add EMA if available - OPTIMIZED
                    intraday = market_data.get('intraday', {})
                    ema20_series = intraday.get('series', {}).get('ema20', [])
                    if ema20_series and len(ema20_series) >= len(recent_prices):
                        ema20_data = ema20_series[-len(recent_prices):]
                        if len(technical_chart.figure.data) > 1:
                            # Add EMA trace if not exists
                            if len(technical_chart.figure.data) == 3:  # Only price, RSI, MACD
                                technical_chart.figure.add_trace(
                                    go.Scatter(
                                        x=times, y=ema20_data,
                                        mode='lines',
                                        name='EMA20',
                                        line=dict(color='#f59e0b', width=2)
                                    ),
                                    row=1, col=1
                                )

                    # RSI subplot - OPTIMIZED (index 1)
                    rsi_series = intraday.get('series', {}).get('rsi14', [])
                    if rsi_series and len(rsi_series) >= len(recent_prices):
                        rsi_data = rsi_series[-len(recent_prices):]
                        technical_chart.figure.data[1].x = times
                        technical_chart.figure.data[1].y = rsi_data

                    # MACD subplot - OPTIMIZED (index 2)
                    macd_series = intraday.get('series', {}).get('macd', [])
                    if macd_series and len(macd_series) >= len(recent_prices):
                        macd_data = macd_series[-len(recent_prices):]
                        technical_chart.figure.data[2].x = times
                        technical_chart.figure.data[2].y = macd_data

            # PERFORMANCE: Batch update with minimal layout changes
            technical_chart.figure.update_layout(uirevision='constant')  # Prevent full redraw
            technical_chart.update()
            _last_technical_update = current_time

        except Exception as e:
            print(f"Error updating technical chart: {e}")

    async def update_sentiment_analysis(market_data):
        """Update neural sentiment analysis"""
        try:
            current_price = market_data.get('current_price', 0)
            intraday = market_data.get('intraday', {})
            long_term = market_data.get('long_term', {})
            
            ema20_5m = intraday.get('ema20')
            ema20_4h = long_term.get('ema20')
            rsi14 = intraday.get('rsi14')
            macd = intraday.get('macd')

            # Calculate trend signal
            if current_price and ema20_5m and ema20_4h:
                if current_price > ema20_5m > ema20_4h:
                    trend_signal_label.text = 'BULLISH'
                    trend_signal_label.classes('text-xl font-bold text-green-400')
                elif current_price < ema20_5m < ema20_4h:
                    trend_signal_label.text = 'BEARISH'
                    trend_signal_label.classes('text-xl font-bold text-red-400')
                else:
                    trend_signal_label.text = 'MIXED'
                    trend_signal_label.classes('text-xl font-bold text-yellow-400')

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

            if 'STRONG' in momentum_signals or 'POSITIVE' in momentum_signals:
                momentum_signal_label.text = 'STRONG'
                momentum_signal_label.classes('text-xl font-bold text-green-400')
            elif 'WEAK' in momentum_signals or 'NEGATIVE' in momentum_signals:
                momentum_signal_label.text = 'WEAK'
                momentum_signal_label.classes('text-xl font-bold text-red-400')
            else:
                momentum_signal_label.text = 'NEUTRAL'
                momentum_signal_label.classes('text-xl font-bold text-gray-400')

            # Overall sentiment
            bullish_signals = (trend_signal_label.text == 'BULLISH') + (momentum_signal_label.text == 'STRONG')
            bearish_signals = (trend_signal_label.text == 'BEARISH') + (momentum_signal_label.text == 'WEAK')

            if bullish_signals > bearish_signals:
                sentiment_label.text = 'BULLISH'
                sentiment_label.classes('text-2xl font-bold text-green-400')
                sentiment_desc.text = 'Neural analysis indicates upward momentum'
                confidence_progress.value = 0.7
            elif bearish_signals > bullish_signals:
                sentiment_label.text = 'BEARISH'
                sentiment_label.classes('text-2xl font-bold text-red-400')
                sentiment_desc.text = 'Neural analysis indicates downward pressure'
                confidence_progress.value = 0.7
            else:
                sentiment_label.text = 'NEUTRAL'
                sentiment_label.classes('text-2xl font-bold text-gray-400')
                sentiment_desc.text = 'Mixed signals, awaiting clearer direction'
                confidence_progress.value = 0.5

        except Exception as e:
            print(f"Error in sentiment analysis: {e}")

    # Event Handlers
    
    # Wire up position table events (only if not using modular components)
    if not MODULAR_COMPONENTS_AVAILABLE:
        positions_table.on('close', close_position_handler)

    # Asset/timeframe change handlers
    asset_select.on('update:model-value', lambda: update_dashboard())
    timeframe_select.on('update:model-value', lambda: update_dashboard())

    # OPTIMIZED Auto-refresh Timers
    
    # FAST update for technical analysis only (every 1 second)
    async def fast_technical_update():
        """Fast update for technical analysis chart only"""
        try:
            state = state_manager.get_state()
            if hasattr(state, 'market_intelligence') and state.market_intelligence:
                selected_asset = asset_select.value
                market_data = next((m for m in state.market_intelligence if m.get('asset') == selected_asset), None)
                if market_data:
                    if MODULAR_COMPONENTS_AVAILABLE:
                        update_technical_chart(technical_chart, market_data)
                    else:
                        # Enhanced fallback - update with RSI and MACD
                        try:
                            recent_prices = market_data.get('recent_mid_prices', [])
                            intraday = market_data.get('intraday', {})
                            
                            if recent_prices and len(recent_prices) > 1:
                                max_points = 12
                                if len(recent_prices) > max_points:
                                    recent_prices = recent_prices[-max_points:]
                                
                                times = [f"T-{len(recent_prices)-i}" for i in range(len(recent_prices))]
                                
                                # Update existing traces if they exist
                                if len(technical_chart.figure.data) >= 1:
                                    # Update price data
                                    technical_chart.figure.data[0].x = times
                                    technical_chart.figure.data[0].y = recent_prices
                                    
                                    # Update RSI if available and trace exists
                                    rsi_series = intraday.get('series', {}).get('rsi14', [])
                                    if rsi_series and len(rsi_series) >= len(recent_prices) and len(technical_chart.figure.data) >= 2:
                                        rsi_data = rsi_series[-len(recent_prices):]
                                        # Find RSI trace (should be index 1 or 2 depending on EMA)
                                        for i, trace in enumerate(technical_chart.figure.data):
                                            if trace.name == 'RSI':
                                                technical_chart.figure.data[i].x = times
                                                technical_chart.figure.data[i].y = rsi_data
                                                break
                                    
                                    # Update MACD if available and trace exists
                                    macd_series = intraday.get('series', {}).get('macd', [])
                                    if macd_series and len(macd_series) >= len(recent_prices):
                                        macd_data = macd_series[-len(recent_prices):]
                                        # Find MACD trace
                                        for i, trace in enumerate(technical_chart.figure.data):
                                            if trace.name == 'MACD':
                                                technical_chart.figure.data[i].x = times
                                                technical_chart.figure.data[i].y = macd_data
                                                break
                                    
                                    technical_chart.update()
                        except:
                            pass
        except Exception as e:
            pass  # Silent fail for performance
    
    # MEDIUM update for main dashboard (every 3 seconds)
    ui.timer(3.0, update_dashboard)
    
    # FAST update for technical analysis (every 1 second)
    ui.timer(1.0, fast_technical_update)

    # Initial update
    ui.timer(0.5, update_dashboard)
