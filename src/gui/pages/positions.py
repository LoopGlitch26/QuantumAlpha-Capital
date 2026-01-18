"""
QuantumAlpha Capital - Position Analytics Command Center
Elite-grade position management with advanced risk analytics and real-time monitoring
"""

from nicegui import ui
from src.gui.services.bot_service import AgentService
from src.gui.services.state_manager import StateManager


def create_positions(agent_service: AgentService, state_manager: StateManager):
    """Create elite position analytics command center with advanced monitoring"""
    
    # Elite header with neural branding
    with ui.row().classes('w-full items-center justify-between mb-6'):
        with ui.row().classes('items-center gap-4'):
            ui.icon('account_balance', size='48px').classes('text-cyan-400')
            with ui.column().classes('gap-1'):
                ui.label('Position Analytics').classes('text-4xl font-bold text-white')
                ui.label('Neural Risk Management & Performance Monitoring').classes('text-lg text-cyan-300')
    
    # Elite performance metrics dashboard
    with ui.row().classes('w-full gap-4 mb-6'):
        # Active Positions Counter
        with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-blue-900 to-blue-950 border border-blue-700'):
            with ui.row().classes('items-center gap-4'):
                ui.icon('trending_up', size='32px').classes('text-blue-400')
                with ui.column().classes('gap-1'):
                    positions_count = ui.label('0').classes('text-4xl font-bold text-white')
                    ui.label('Active Positions').classes('text-sm text-blue-300 font-medium')
        
        # Unrealized PnL with dynamic coloring
        with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-purple-900 to-purple-950 border border-purple-700'):
            with ui.row().classes('items-center gap-4'):
                ui.icon('analytics', size='32px').classes('text-purple-400')
                with ui.column().classes('gap-1'):
                    total_pnl = ui.label('$0.00').classes('text-4xl font-bold text-white')
                    ui.label('Unrealized PnL').classes('text-sm text-purple-300 font-medium')
        
        # Total Market Exposure
        with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-indigo-900 to-indigo-950 border border-indigo-700'):
            with ui.row().classes('items-center gap-4'):
                ui.icon('account_balance_wallet', size='32px').classes('text-indigo-400')
                with ui.column().classes('gap-1'):
                    total_exposure = ui.label('$0.00').classes('text-4xl font-bold text-white')
                    ui.label('Market Exposure').classes('text-sm text-indigo-300 font-medium')
        
        # Risk Score Indicator
        with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-orange-900 to-orange-950 border border-orange-700'):
            with ui.row().classes('items-center gap-4'):
                ui.icon('security', size='32px').classes('text-orange-400')
                with ui.column().classes('gap-1'):
                    risk_score = ui.label('0%').classes('text-4xl font-bold text-white')
                    ui.label('Portfolio Risk').classes('text-sm text-orange-300 font-medium')
    
    # Elite position management interface
    with ui.card().classes('w-full p-6 bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-700'):
        with ui.row().classes('w-full items-center justify-between mb-6'):
            with ui.row().classes('items-center gap-3'):
                ui.icon('table_chart', size='28px').classes('text-cyan-400')
                ui.label('Position Portfolio').classes('text-2xl font-bold text-white')
            
            # Action controls
            with ui.row().classes('gap-2'):
                ui.button('🔄 Refresh', on_click=lambda: None).classes('bg-blue-600 hover:bg-blue-700 px-4 py-2')
                ui.button('📊 Analytics', on_click=lambda: None).classes('bg-purple-600 hover:bg-purple-700 px-4 py-2')
                ui.button('⚠️ Close All', on_click=lambda: None).classes('bg-red-600 hover:bg-red-700 px-4 py-2')
        
        # Enhanced table columns with professional styling
        columns = [
            {'name': 'symbol', 'label': 'Instrument', 'field': 'symbol', 'align': 'left', 'sortable': True},
            {'name': 'side', 'label': 'Direction', 'field': 'side', 'align': 'center', 'sortable': True},
            {'name': 'quantity', 'label': 'Position Size', 'field': 'quantity', 'align': 'right', 'sortable': True},
            {'name': 'entry_price', 'label': 'Entry Price', 'field': 'entry_price', 'align': 'right', 'sortable': True},
            {'name': 'current_price', 'label': 'Mark Price', 'field': 'current_price', 'align': 'right', 'sortable': True},
            {'name': 'unrealized_pnl', 'label': 'Unrealized PnL', 'field': 'unrealized_pnl', 'align': 'right', 'sortable': True},
            {'name': 'pnl_pct', 'label': 'Return %', 'field': 'pnl_pct', 'align': 'right', 'sortable': True},
            {'name': 'leverage', 'label': 'Leverage', 'field': 'leverage', 'align': 'center', 'sortable': True},
            {'name': 'liquidation_price', 'label': 'Liquidation', 'field': 'liquidation_price', 'align': 'right', 'sortable': True},
            {'name': 'risk_level', 'label': 'Risk Level', 'field': 'risk_level', 'align': 'center', 'sortable': True},
            {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'align': 'center'},
        ]
        
        # Elite data table with enhanced styling
        table = ui.table(
            columns=columns,
            rows=[],
            row_key='symbol',
            pagination={'rowsPerPage': 15, 'sortBy': 'unrealized_pnl', 'descending': True}
        ).classes('w-full bg-gray-800 text-white')
        
        # Enhanced PnL cell with profit/loss indicators
        table.add_slot('body-cell-unrealized_pnl', '''
            <q-td :props="props">
                <div class="flex items-center gap-2">
                    <q-icon 
                        :name="props.row.unrealized_pnl >= 0 ? 'trending_up' : 'trending_down'" 
                        :color="props.row.unrealized_pnl >= 0 ? 'green' : 'red'" 
                        size="sm"
                    />
                    <span :class="props.row.unrealized_pnl >= 0 ? 'text-green-400' : 'text-red-400'" class="font-bold text-lg">
                        {{ props.row.unrealized_pnl >= 0 ? '+' : '' }}${{ Math.abs(props.row.unrealized_pnl).toFixed(2) }}
                    </span>
                </div>
            </q-td>
        ''')
        
        # Enhanced PnL percentage with color coding
        table.add_slot('body-cell-pnl_pct', '''
            <q-td :props="props">
                <q-badge 
                    :color="props.row.pnl_pct >= 0 ? 'green' : 'red'" 
                    :label="(props.row.pnl_pct >= 0 ? '+' : '') + props.row.pnl_pct.toFixed(2) + '%'"
                    class="text-sm font-bold px-3 py-1"
                />
            </q-td>
        ''')
        
        # Enhanced side indicator with directional icons
        table.add_slot('body-cell-side', '''
            <q-td :props="props">
                <q-badge 
                    :color="props.row.side === 'LONG' ? 'green' : 'red'" 
                    class="text-sm font-bold px-3 py-1"
                >
                    <q-icon 
                        :name="props.row.side === 'LONG' ? 'north' : 'south'" 
                        size="xs" 
                        class="mr-1"
                    />
                    {{ props.row.side }}
                </q-badge>
            </q-td>
        ''')
        
        # Risk level indicator
        table.add_slot('body-cell-risk_level', '''
            <q-td :props="props">
                <q-badge 
                    :color="props.row.risk_level === 'LOW' ? 'green' : props.row.risk_level === 'MEDIUM' ? 'orange' : 'red'"
                    :label="props.row.risk_level"
                    class="text-xs font-bold px-2 py-1"
                />
            </q-td>
        ''')
        
        # Enhanced action buttons with tooltips
        table.add_slot('body-cell-actions', '''
            <q-td :props="props">
                <div class="flex gap-1">
                    <q-btn 
                        flat dense round 
                        icon="show_chart" 
                        color="blue" 
                        size="sm" 
                        @click="$parent.$emit('chart', props.row)"
                        class="hover:bg-blue-900"
                    >
                        <q-tooltip>Technical Analysis</q-tooltip>
                    </q-btn>
                    <q-btn 
                        flat dense round 
                        icon="tune" 
                        color="purple" 
                        size="sm" 
                        @click="$parent.$emit('manage', props.row)"
                        class="hover:bg-purple-900"
                    >
                        <q-tooltip>Manage Position</q-tooltip>
                    </q-btn>
                    <q-btn 
                        flat dense round 
                        icon="close" 
                        color="red" 
                        size="sm" 
                        @click="$parent.$emit('close', props.row)"
                        class="hover:bg-red-900"
                    >
                        <q-tooltip>Close Position</q-tooltip>
                    </q-btn>
                </div>
            </q-td>
        ''')
        
        # Enhanced chart analysis dialog
        chart_dialog = ui.dialog()
        with chart_dialog, ui.card().classes('w-[800px] bg-gray-900 border border-cyan-500'):
            with ui.row().classes('w-full items-center justify-between mb-4'):
                dialog_title = ui.label('').classes('text-2xl font-bold text-white')
                ui.button('✕', on_click=chart_dialog.close).classes('bg-red-600 hover:bg-red-700 w-10 h-10 rounded-full')
            
            with ui.column().classes('w-full gap-4'):
                ui.label('📊 Technical Analysis Dashboard').classes('text-lg text-cyan-400 font-medium')
                dialog_content = ui.label('Advanced charting and technical indicators coming soon...').classes('text-gray-400 text-center py-8')
                
                # Placeholder for future chart integration
                with ui.card().classes('w-full h-64 bg-gray-800 border border-gray-600'):
                    ui.label('TradingView Chart Integration').classes('text-center text-gray-500 mt-24')
        
        # Enhanced position management dialog
        manage_dialog = ui.dialog()
        with manage_dialog, ui.card().classes('w-[600px] bg-gray-900 border border-purple-500'):
            with ui.row().classes('w-full items-center justify-between mb-4'):
                manage_title = ui.label('').classes('text-2xl font-bold text-white')
                ui.button('✕', on_click=manage_dialog.close).classes('bg-red-600 hover:bg-red-700 w-10 h-10 rounded-full')
            
            with ui.column().classes('w-full gap-4'):
                ui.label('⚙️ Position Management').classes('text-lg text-purple-400 font-medium')
                
                # Position adjustment controls
                with ui.row().classes('w-full gap-4'):
                    with ui.card().classes('flex-1 p-4 bg-gray-800'):
                        ui.label('Stop Loss').classes('text-sm text-gray-300 mb-2')
                        sl_input = ui.number(label='Price', value=0, format='%.2f').classes('w-full')
                    
                    with ui.card().classes('flex-1 p-4 bg-gray-800'):
                        ui.label('Take Profit').classes('text-sm text-gray-300 mb-2')
                        tp_input = ui.number(label='Price', value=0, format='%.2f').classes('w-full')
                
                with ui.row().classes('w-full justify-end gap-2 mt-4'):
                    ui.button('Cancel', on_click=manage_dialog.close).classes('bg-gray-600 hover:bg-gray-700 px-6 py-2')
                    ui.button('Update Position', on_click=lambda: None).classes('bg-purple-600 hover:bg-purple-700 px-6 py-2')
        
        # Enhanced close confirmation dialog
        close_dialog = ui.dialog()
        with close_dialog, ui.card().classes('w-[500px] bg-gray-900 border border-red-500'):
            with ui.row().classes('w-full items-center justify-between mb-4'):
                close_title = ui.label('').classes('text-2xl font-bold text-white')
                ui.button('✕', on_click=close_dialog.close).classes('bg-gray-600 hover:bg-gray-700 w-10 h-10 rounded-full')
            
            with ui.column().classes('w-full gap-4'):
                ui.icon('warning', size='48px').classes('text-red-400 mx-auto')
                close_message = ui.label('').classes('text-gray-300 text-center')
                
                with ui.row().classes('w-full justify-center gap-4 mt-6'):
                    ui.button('Cancel', on_click=close_dialog.close).classes('bg-gray-600 hover:bg-gray-700 px-8 py-3')
                    close_confirm_btn = ui.button('Close Position', on_click=lambda: None).classes('bg-red-600 hover:bg-red-700 px-8 py-3 font-bold')
        
        # Enhanced event handlers
        current_position = {'symbol': None}
        
        def show_chart(e):
            """Show enhanced chart analysis dialog"""
            position = e.args
            dialog_title.text = f"📊 {position['symbol']} Technical Analysis"
            chart_dialog.open()
        
        def show_manage_dialog(e):
            """Show position management dialog"""
            position = e.args
            current_position['symbol'] = position['symbol']
            manage_title.text = f"⚙️ Manage {position['symbol']} Position"
            
            # Pre-populate current values
            sl_input.value = position.get('liquidation_price', 0) * 0.95  # Conservative SL
            tp_input.value = position.get('current_price', 0) * 1.1  # 10% profit target
            
            manage_dialog.open()
        
        async def show_close_dialog(e):
            """Show enhanced close confirmation dialog"""
            position = e.args
            current_position['symbol'] = position['symbol']
            close_title.text = f"⚠️ Close {position['symbol']} Position"
            
            pnl_color = "text-green-400" if position['unrealized_pnl'] >= 0 else "text-red-400"
            pnl_sign = "+" if position['unrealized_pnl'] >= 0 else ""
            
            close_message.text = f"""
Are you sure you want to close your {position['side']} position in {position['symbol']}?

Current Performance:
• Unrealized PnL: {pnl_sign}${position['unrealized_pnl']:.2f} ({position['pnl_pct']:+.2f}%)
• Position Size: {position['quantity']:.6f} {position['symbol']}
• Entry Price: ${position['entry_price']:,.2f}
• Current Price: ${position['current_price']:,.2f}

This action cannot be undone.
            """.strip()
            
            close_dialog.open()
        
        async def confirm_close():
            """Execute position closure with enhanced feedback"""
            symbol = current_position['symbol']
            if symbol:
                try:
                    close_dialog.close()
                    ui.notify(f'🔄 Executing market close for {symbol}...', type='info', position='top')
                    
                    success = await agent_service.close_position(symbol)
                    
                    if success:
                        ui.notify(f'✅ {symbol} position closed successfully!', type='positive', position='top')
                    else:
                        ui.notify(f'❌ Failed to close {symbol} position - Check logs', type='negative', position='top')
                except Exception as e:
                    ui.notify(f'⚠️ Execution error: {str(e)}', type='negative', position='top')
        
        # Wire up enhanced event handlers
        table.on('chart', show_chart)
        table.on('manage', show_manage_dialog)
        table.on('close', show_close_dialog)
        close_confirm_btn.on('click', confirm_close)
    
    # Elite empty state with neural branding
    empty_message = ui.column().classes('w-full items-center py-16')
    with empty_message:
        ui.icon('account_balance', size='96px').classes('text-gray-600 mb-4')
        ui.label('No Active Positions').classes('text-3xl font-bold text-gray-400 mb-2')
        ui.label('Neural analysis will identify optimal entry points').classes('text-lg text-gray-500 mb-6')
        ui.button('🚀 Start Agent', on_click=lambda: None).classes('bg-cyan-600 hover:bg-cyan-700 px-8 py-3 text-lg font-bold')
    
    empty_message.visible = True
    
    # Enhanced update function with risk analytics
    async def update_positions():
        """Update positions with advanced analytics and risk assessment"""
        try:
            state = state_manager.get_state()
            positions = state.open_positions or []
            
            # Show/hide empty state
            empty_message.visible = len(positions) == 0
            table.visible = len(positions) > 0
            
            if positions:
                # Advanced portfolio analytics
                total_unrealized_pnl = sum(p.get('unrealized_pnl', 0) for p in positions)
                total_notional = sum(abs(p.get('quantity', 0) * p.get('current_price', 0)) for p in positions)
                
                # Risk assessment calculations
                portfolio_balance = state.balance or 1000  # Fallback to prevent division by zero
                exposure_ratio = (total_notional / portfolio_balance) if portfolio_balance > 0 else 0
                risk_percentage = min(exposure_ratio * 100, 100)
                
                # Update elite performance metrics
                positions_count.text = str(len(positions))
                
                # Dynamic PnL coloring
                total_pnl.text = f"${total_unrealized_pnl:+,.2f}"
                if total_unrealized_pnl >= 0:
                    total_pnl.classes(remove='text-red-400', add='text-green-400')
                else:
                    total_pnl.classes(remove='text-green-400', add='text-red-400')
                
                total_exposure.text = f"${total_notional:,.2f}"
                
                # Risk score with color coding
                risk_score.text = f"{risk_percentage:.1f}%"
                if risk_percentage < 30:
                    risk_score.classes(remove='text-red-400 text-yellow-400', add='text-green-400')
                elif risk_percentage < 70:
                    risk_score.classes(remove='text-red-400 text-green-400', add='text-yellow-400')
                else:
                    risk_score.classes(remove='text-green-400 text-yellow-400', add='text-red-400')
                
                # Enhanced position data formatting
                rows = []
                for pos in positions:
                    quantity = pos.get('quantity', 0)
                    entry_price = pos.get('entry_price', 0)
                    current_price = pos.get('current_price', 0)
                    unrealized_pnl = pos.get('unrealized_pnl', 0)
                    liquidation_price = pos.get('liquidation_price', 0)
                    
                    # Calculate advanced metrics
                    pnl_pct = 0
                    if entry_price > 0:
                        if quantity > 0:  # LONG
                            pnl_pct = ((current_price - entry_price) / entry_price) * 100
                        else:  # SHORT
                            pnl_pct = ((entry_price - current_price) / entry_price) * 100
                    
                    # Risk level assessment
                    if liquidation_price > 0 and current_price > 0:
                        distance_to_liq = abs(current_price - liquidation_price) / current_price
                        if distance_to_liq > 0.2:
                            risk_level = 'LOW'
                        elif distance_to_liq > 0.1:
                            risk_level = 'MEDIUM'
                        else:
                            risk_level = 'HIGH'
                    else:
                        risk_level = 'LOW'
                    
                    rows.append({
                        'symbol': pos.get('symbol', ''),
                        'side': 'LONG' if quantity > 0 else 'SHORT',
                        'quantity': abs(quantity),
                        'entry_price': entry_price,
                        'current_price': current_price,
                        'unrealized_pnl': unrealized_pnl,
                        'pnl_pct': pnl_pct,
                        'leverage': pos.get('leverage', 1),
                        'liquidation_price': liquidation_price,
                        'risk_level': risk_level,
                    })
                
                table.rows = rows
                table.update()
            else:
                # Reset metrics when no positions
                positions_count.text = '0'
                total_pnl.text = '$0.00'
                total_pnl.classes(remove='text-red-400 text-green-400', add='text-white')
                total_exposure.text = '$0.00'
                risk_score.text = '0%'
                risk_score.classes(remove='text-red-400 text-yellow-400', add='text-green-400')
        
        except Exception as e:
            ui.notify(f'⚠️ Position update error: {str(e)}', type='warning', position='top')
    
    # High-frequency refresh for real-time monitoring
    ui.timer(1.5, update_positions)
    
    # Initial update
    # Note: Can't await in sync context, timer will handle it
