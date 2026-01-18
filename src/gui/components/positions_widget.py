"""
Positions Widget - Reusable positions table component
"""

from nicegui import ui
from src.gui.services.bot_service import AgentService
from src.gui.services.state_manager import StateManager


def create_positions_table(agent_service: AgentService, state_manager: StateManager):
    """Create positions table widget that can be reused"""
    
    # Positions table
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

    async def close_position_handler(e):
        """Handle position closure from table"""
        position = e.args
        symbol = position['symbol']
        
        try:
            success = await agent_service.close_position(symbol)
            
            if success:
                ui.notify(f'{symbol} Position Closed!', type='positive')
            else:
                ui.notify(f'Failed to close {symbol}', type='negative')
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')

    # Wire up events
    positions_table.on('close', close_position_handler)

    return positions_table, positions_empty


def update_positions_table(positions_table, positions_empty, positions):
    """Update positions table with new data"""
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