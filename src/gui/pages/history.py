"""
QuantumAlpha Capital - Trade History Analytics
Professional trade analysis with advanced filtering and performance metrics
"""

import csv
from datetime import datetime
from nicegui import ui
from src.gui.services.bot_service import AgentService
from src.gui.services.state_manager import StateManager


def create_history(agent_service: AgentService, state_manager: StateManager):
    """Create elite trade history analytics with advanced filtering and insights"""

    # Elite header with neural branding
    with ui.row().classes('w-full items-center justify-between mb-6'):
        with ui.row().classes('items-center gap-4'):
            ui.icon('history', size='48px').classes('text-cyan-400')
            with ui.column().classes('gap-1'):
                ui.label('Trade History Analytics').classes('text-4xl font-bold text-white')
                ui.label('Neural Performance Analysis & Trade Intelligence').classes('text-lg text-cyan-300')
        
        # Quick action buttons
        with ui.row().classes('gap-2'):
            ui.button('📊 Performance Report', on_click=lambda: None).classes('bg-purple-600 hover:bg-purple-700 px-4 py-2')
            ui.button('📈 Analytics Dashboard', on_click=lambda: None).classes('bg-blue-600 hover:bg-blue-700 px-4 py-2')

        # Elite filtering and control center
        with ui.card().classes('w-full p-6 mb-6 bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-700'):
            with ui.row().classes('w-full items-center justify-between mb-4'):
                with ui.row().classes('items-center gap-3'):
                    ui.icon('filter_list', size='28px').classes('text-cyan-400')
                    ui.label('Trade Analysis Filters').classes('text-xl font-bold text-white')
                
                # Export controls
                with ui.row().classes('gap-2'):
                    export_btn = ui.button('📥 Export CSV', on_click=lambda: None).classes('bg-green-600 hover:bg-green-700 px-4 py-2')
                    ui.button('📋 Copy Data', on_click=lambda: None).classes('bg-blue-600 hover:bg-blue-700 px-4 py-2')

            with ui.row().classes('w-full gap-4 items-end'):
                # Enhanced filter controls
                asset_filter = ui.select(
                    label='Instrument',
                    options=['All'] + agent_service.get_assets(),
                    value='All'
                ).classes('flex-1')

                action_filter = ui.select(
                    label='Trade Type',
                    options=['All', 'buy', 'sell', 'hold'],
                    value='All'
                ).classes('flex-1')
                
                # Performance filter
                performance_filter = ui.select(
                    label='Performance',
                    options=['All', 'Profitable', 'Loss', 'Breakeven'],
                    value='All'
                ).classes('flex-1')

                limit_filter = ui.number(
                    label='Max Results',
                    value=100,
                    min=10,
                    max=1000,
                    step=10
                ).classes('flex-1')

                # Apply filters button
                apply_btn = ui.button('🔍 Apply Filters', on_click=lambda: None).classes('bg-cyan-600 hover:bg-cyan-700 px-6 py-3 font-bold')

        # Elite performance metrics dashboard
        with ui.row().classes('w-full gap-4 mb-6'):
            # Total Trades
            with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-cyan-900 to-cyan-950 border border-cyan-700'):
                with ui.row().classes('items-center gap-4'):
                    ui.icon('swap_horiz', size='32px').classes('text-cyan-400')
                    with ui.column().classes('gap-1'):
                        total_trades = ui.label('0').classes('text-4xl font-bold text-white')
                        ui.label('Total Executions').classes('text-sm text-cyan-300 font-medium')

            # Win Rate with performance indicator
            with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-green-900 to-green-950 border border-green-700'):
                with ui.row().classes('items-center gap-4'):
                    ui.icon('trending_up', size='32px').classes('text-green-400')
                    with ui.column().classes('gap-1'):
                        win_rate = ui.label('0%').classes('text-4xl font-bold text-white')
                        ui.label('Success Rate').classes('text-sm text-green-300 font-medium')

            # Total PnL with dynamic coloring
            with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-purple-900 to-purple-950 border border-purple-700'):
                with ui.row().classes('items-center gap-4'):
                    ui.icon('account_balance', size='32px').classes('text-purple-400')
                    with ui.column().classes('gap-1'):
                        total_pnl_label = ui.label('$0.00').classes('text-4xl font-bold text-white')
                        ui.label('Net Profit/Loss').classes('text-sm text-purple-300 font-medium')
            
            # Average Trade Performance
            with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-orange-900 to-orange-950 border border-orange-700'):
                with ui.row().classes('items-center gap-4'):
                    ui.icon('analytics', size='32px').classes('text-orange-400')
                    with ui.column().classes('gap-1'):
                        avg_trade = ui.label('$0.00').classes('text-4xl font-bold text-white')
                        ui.label('Avg Per Trade').classes('text-sm text-orange-300 font-medium')

        # Elite trade analytics table
        with ui.card().classes('w-full p-6 bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-700'):
            with ui.row().classes('w-full items-center justify-between mb-6'):
                with ui.row().classes('items-center gap-3'):
                    ui.icon('table_chart', size='28px').classes('text-cyan-400')
                    ui.label('Trade Execution Log').classes('text-2xl font-bold text-white')
                
                # Table controls
                with ui.row().classes('gap-2'):
                    ui.button('🔄 Refresh', on_click=lambda: None).classes('bg-blue-600 hover:bg-blue-700 px-4 py-2')
                    ui.button('📊 Analyze', on_click=lambda: None).classes('bg-purple-600 hover:bg-purple-700 px-4 py-2')

            # Enhanced table columns with professional styling
            columns = [
                {'name': 'timestamp', 'label': 'Execution Time', 'field': 'timestamp', 'align': 'left', 'sortable': True},
                {'name': 'asset', 'label': 'Instrument', 'field': 'asset', 'align': 'center', 'sortable': True},
                {'name': 'action', 'label': 'Direction', 'field': 'action', 'align': 'center', 'sortable': True},
                {'name': 'entry_price', 'label': 'Entry Price', 'field': 'entry_price', 'align': 'right', 'sortable': True},
                {'name': 'exit_price', 'label': 'Exit Price', 'field': 'exit_price', 'align': 'right', 'sortable': True},
                {'name': 'size', 'label': 'Position Size', 'field': 'size', 'align': 'right', 'sortable': True},
                {'name': 'pnl', 'label': 'Realized PnL', 'field': 'pnl', 'align': 'right', 'sortable': True},
                {'name': 'pnl_pct', 'label': 'Return %', 'field': 'pnl_pct', 'align': 'right', 'sortable': True},
                {'name': 'duration', 'label': 'Hold Time', 'field': 'duration', 'align': 'center', 'sortable': True},
                {'name': 'rationale', 'label': 'AI Rationale', 'field': 'rationale', 'align': 'left'},
            ]

            # Elite data table with enhanced styling
            table = ui.table(
                columns=columns,
                rows=[],
                row_key='timestamp',
                pagination={'rowsPerPage': 25, 'sortBy': 'timestamp', 'descending': True}
            ).classes('w-full bg-gray-800 text-white')

            # Enhanced action cell with directional indicators
            table.add_slot('body-cell-action', '''
                <q-td :props="props">
                    <q-badge
                        :color="props.row.action === 'buy' ? 'green' : props.row.action === 'sell' ? 'red' : 'grey'"
                        class="text-sm font-bold px-3 py-1"
                    >
                        <q-icon 
                            :name="props.row.action === 'buy' ? 'north' : props.row.action === 'sell' ? 'south' : 'pause'" 
                            size="xs" 
                            class="mr-1"
                        />
                        {{ props.row.action.toUpperCase() }}
                    </q-badge>
                </q-td>
            ''')

            # Enhanced PnL cell with performance indicators
            table.add_slot('body-cell-pnl', '''
                <q-td :props="props">
                    <div v-if="props.row.pnl !== null" class="flex items-center gap-2">
                        <q-icon 
                            :name="props.row.pnl >= 0 ? 'trending_up' : 'trending_down'" 
                            :color="props.row.pnl >= 0 ? 'green' : 'red'" 
                            size="sm"
                        />
                        <span :class="props.row.pnl >= 0 ? 'text-green-400' : 'text-red-400'" class="font-bold text-lg">
                            {{ props.row.pnl >= 0 ? '+' : '' }}${{ Math.abs(props.row.pnl).toFixed(2) }}
                        </span>
                    </div>
                    <span v-else class="text-gray-500">-</span>
                </q-td>
            ''')

            # Enhanced PnL percentage with badges
            table.add_slot('body-cell-pnl_pct', '''
                <q-td :props="props">
                    <q-badge 
                        v-if="props.row.pnl_pct !== null" 
                        :color="props.row.pnl_pct >= 0 ? 'green' : 'red'" 
                        :label="(props.row.pnl_pct >= 0 ? '+' : '') + props.row.pnl_pct.toFixed(2) + '%'"
                        class="text-sm font-bold px-3 py-1"
                    />
                    <span v-else class="text-gray-500">-</span>
                </q-td>
            ''')

            # Enhanced rationale cell with expandable content
            table.add_slot('body-cell-rationale', '''
                <q-td :props="props">
                    <div class="flex items-center gap-2">
                        <div class="text-sm text-gray-400 truncate max-w-xs cursor-pointer" @click="$parent.$emit('detail', props.row)">
                            {{ props.row.rationale ? props.row.rationale.substring(0, 60) + '...' : 'No analysis available' }}
                        </div>
                        <q-btn 
                            v-if="props.row.rationale" 
                            flat dense round 
                            icon="visibility" 
                            color="blue" 
                            size="xs" 
                            @click="$parent.$emit('detail', props.row)"
                        >
                            <q-tooltip>View Full Analysis</q-tooltip>
                        </q-btn>
                    </div>
                </q-td>
            ''')

            # Enhanced trade analysis dialog
            detail_dialog = ui.dialog()
            with detail_dialog, ui.card().classes('w-[800px] bg-gray-900 border border-cyan-500'):
                with ui.row().classes('w-full items-center justify-between mb-6'):
                    detail_title = ui.label('').classes('text-2xl font-bold text-white')
                    ui.button('✕', on_click=detail_dialog.close).classes('bg-red-600 hover:bg-red-700 w-10 h-10 rounded-full')
                
                with ui.column().classes('w-full gap-6'):
                    # Trade summary section
                    with ui.card().classes('w-full p-4 bg-gray-800 border border-gray-600'):
                        ui.label('📊 Trade Summary').classes('text-lg text-cyan-400 font-bold mb-3')
                        with ui.grid(columns=3).classes('gap-4'):
                            detail_asset = ui.label('').classes('text-gray-300')
                            detail_action = ui.label('').classes('text-gray-300')
                            detail_prices = ui.label('').classes('text-gray-300')
                        detail_pnl = ui.label('').classes('text-lg font-bold mt-2')
                    
                    # AI analysis section
                    with ui.card().classes('w-full p-4 bg-gray-800 border border-gray-600'):
                        ui.label('🧠 Neural Analysis').classes('text-lg text-purple-400 font-bold mb-3')
                        detail_rationale = ui.label('').classes('text-gray-300 whitespace-pre-wrap leading-relaxed')
                    
                    # Performance metrics
                    with ui.card().classes('w-full p-4 bg-gray-800 border border-gray-600'):
                        ui.label('📈 Performance Metrics').classes('text-lg text-green-400 font-bold mb-3')
                        detail_metrics = ui.column().classes('gap-2')

            def show_detail(e):
                """Show enhanced trade analysis dialog"""
                trade = e.args
                detail_title.text = f"🔍 Trade Analysis - {trade['asset']}"
                
                # Trade summary
                detail_asset.text = f"Instrument: {trade['asset']}"
                detail_action.text = f"Direction: {trade['action'].upper()}"
                
                # Handle None values for prices
                entry_str = f"${trade['entry_price']:.2f}" if trade.get('entry_price') else 'N/A'
                exit_str = f"${trade['exit_price']:.2f}" if trade.get('exit_price') else 'N/A'
                detail_prices.text = f"Entry: {entry_str} | Exit: {exit_str}"

                # PnL with enhanced formatting
                if trade.get('pnl') is not None:
                    pnl_value = trade['pnl']
                    pnl_pct = trade.get('pnl_pct', 0)
                    pnl_color = "text-green-400" if pnl_value >= 0 else "text-red-400"
                    pnl_sign = "+" if pnl_value >= 0 else ""
                    detail_pnl.text = f"Realized PnL: {pnl_sign}${pnl_value:.2f} ({pnl_pct:+.2f}%)"
                    detail_pnl.classes(remove='text-red-400 text-green-400', add=pnl_color)
                else:
                    detail_pnl.text = "Realized PnL: Pending"
                    detail_pnl.classes(remove='text-red-400 text-green-400', add='text-gray-400')

                # AI rationale
                rationale_text = trade.get('rationale') or 'No neural analysis available for this trade.'
                detail_rationale.text = rationale_text
                
                # Performance metrics
                detail_metrics.clear()
                with detail_metrics:
                    if trade.get('size'):
                        ui.label(f"Position Size: {trade['size']:.6f} {trade['asset']}").classes('text-gray-300')
                    if trade.get('duration'):
                        ui.label(f"Hold Duration: {trade['duration']}").classes('text-gray-300')
                    else:
                        ui.label("Hold Duration: Not available").classes('text-gray-400')
                    
                    # Risk metrics (if available)
                    ui.label("Risk Assessment: Neural risk analysis").classes('text-gray-300')
                    ui.label("Confidence Level: High probability execution").classes('text-gray-300')
                
                detail_dialog.open()

            table.on('detail', show_detail)

        # Elite empty state
        empty_message = ui.column().classes('w-full items-center py-16')
        with empty_message:
            ui.icon('history', size='96px').classes('text-gray-600 mb-4')
            ui.label('No Trade History').classes('text-3xl font-bold text-gray-400 mb-2')
            ui.label('Neural trading decisions will appear here once the agent executes trades').classes('text-lg text-gray-500 mb-6')
            ui.button('🚀 Start Trading Agent', on_click=lambda: None).classes('bg-cyan-600 hover:bg-cyan-700 px-8 py-3 text-lg font-bold')
        
        empty_message.visible = True

    # Enhanced filter state management
    current_filters = {
        'asset': 'All',
        'action': 'All',
        'performance': 'All',
        'limit': 100
    }

    # Update function
    async def update_history():
        """Update trade history table"""
        try:
            # Get filtered trade history
            asset = None if current_filters['asset'] == 'All' else current_filters['asset']
            action = None if current_filters['action'] == 'All' else current_filters['action']
            limit = int(current_filters['limit'])

            trades = agent_service.get_trade_history(asset=asset, action=action, limit=limit)

            # Show/hide empty message
            empty_message.visible = len(trades) == 0
            table.visible = len(trades) > 0

            if trades:
                # Calculate statistics
                total_count = len(trades)
                profitable_trades = sum(1 for t in trades if t.get('pnl', 0) > 0)
                win_rate_pct = (profitable_trades / total_count * 100) if total_count > 0 else 0
                total_pnl_value = sum(t.get('pnl', 0) for t in trades if t.get('pnl') is not None)

                # Update statistics cards
                total_trades.text = str(total_count)
                win_rate.text = f"{win_rate_pct:.1f}%"
                total_pnl_label.text = f"${total_pnl_value:+,.2f}"
                if total_pnl_value >= 0:
                    total_pnl_label.classes(remove='text-red-500', add='text-green-500')
                else:
                    total_pnl_label.classes(remove='text-green-500', add='text-red-500')

                # Format trades for table
                rows = []
                for trade in trades:
                    # Parse timestamp
                    timestamp = trade.get('timestamp', '')
                    if timestamp:
                        try:
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            timestamp_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                        except:
                            timestamp_str = timestamp
                    else:
                        timestamp_str = 'N/A'

                    rows.append({
                        'timestamp': timestamp_str,
                        'asset': trade.get('asset', 'N/A'),
                        'action': trade.get('action', 'N/A'),
                        'entry_price': trade.get('entry_price', 0),
                        'exit_price': trade.get('exit_price'),
                        'size': trade.get('size', 0),
                        'pnl': trade.get('pnl'),
                        'pnl_pct': trade.get('pnl_pct'),
                        'rationale': trade.get('rationale', ''),
                    })

                table.rows = rows
                table.update()
            else:
                # Clear statistics when no trades
                total_trades.text = '0'
                win_rate.text = '0%'
                total_pnl_label.text = '$0.00'

        except Exception as e:
            ui.notify(f'Error updating history: {str(e)}', type='warning')

    # Apply filters handler
    async def apply_filters():
        """Apply selected filters"""
        current_filters['asset'] = asset_filter.value
        current_filters['action'] = action_filter.value
        current_filters['limit'] = limit_filter.value
        await update_history()
        ui.notify('Filters applied', type='info')

    # Export CSV handler
    async def export_csv():
        """Export trade history to CSV"""
        try:
            # Get current filtered data
            asset = None if current_filters['asset'] == 'All' else current_filters['asset']
            action = None if current_filters['action'] == 'All' else current_filters['action']
            limit = int(current_filters['limit'])

            trades = agent_service.get_trade_history(asset=asset, action=action, limit=limit)

            if not trades:
                ui.notify('No trades to export', type='warning')
                return

            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'trade_history_{timestamp}.csv'

            # Write CSV
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['timestamp', 'asset', 'action', 'entry_price', 'exit_price', 'size', 'pnl', 'pnl_pct', 'rationale']
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                writer.writeheader()
                for trade in trades:
                    writer.writerow({
                        'timestamp': trade.get('timestamp', ''),
                        'asset': trade.get('asset', ''),
                        'action': trade.get('action', ''),
                        'entry_price': trade.get('entry_price', 0),
                        'exit_price': trade.get('exit_price', ''),
                        'size': trade.get('size', 0),
                        'pnl': trade.get('pnl', ''),
                        'pnl_pct': trade.get('pnl_pct', ''),
                        'rationale': trade.get('rationale', ''),
                    })

            ui.notify(f'Exported {len(trades)} trades to {filename}', type='positive')

        except Exception as e:
            ui.notify(f'Error exporting CSV: {str(e)}', type='negative')

    # Wire up button handlers
    apply_btn.on('click', apply_filters)
    export_btn.on('click', export_csv)

    # Auto-refresh every 5 seconds
    ui.timer(5.0, update_history)

    # Initial update
    # Note: Can't await in sync context, timer will handle it
