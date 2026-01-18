"""
QuantumAlpha Capital - Neural Decision Intelligence
Advanced AI reasoning visualization with decision analytics and neural pathway analysis
"""

import json
import asyncio
from datetime import datetime
from nicegui import ui
from src.gui.services.bot_service import AgentService
from src.gui.services.state_manager import StateManager


def create_reasoning(agent_service: AgentService, state_manager: StateManager):
    """Create elite neural reasoning interface with advanced AI decision visualization"""

    # Elite header with neural intelligence branding
    with ui.row().classes('w-full items-center justify-between mb-6'):
        with ui.row().classes('items-center gap-4'):
            ui.icon('psychology', size='48px').classes('text-cyan-400')
            with ui.column().classes('gap-1'):
                ui.label('Neural Decision Intelligence').classes('text-4xl font-bold text-white')
                ui.label('Advanced AI Reasoning & Decision Analytics').classes('text-lg text-cyan-300')
        
        # Neural status indicator
        with ui.row().classes('items-center gap-3'):
            neural_status = ui.icon('circle', size='16px').classes('text-green-400')
            ui.label('Neural Engine Active').classes('text-sm text-green-300 font-medium')

    # Elite neural data interface
    with ui.card().classes('w-full p-6 mb-6 bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-700'):
        with ui.row().classes('w-full justify-between items-center mb-4'):
            with ui.row().classes('items-center gap-3'):
                ui.icon('code', size='28px').classes('text-cyan-400')
                ui.label('Neural Network Output').classes('text-2xl font-bold text-white')
            
            with ui.row().classes('gap-2'):
                # Enhanced control buttons
                async def copy_json():
                    state = state_manager.get_state()
                    reasoning_data = state.neural_reasoning or {}
                    json_str = json.dumps(reasoning_data, indent=2)
                    ui.clipboard.write(json_str)
                    ui.notify('🧠 Neural data copied to clipboard!', type='positive', position='top')

                async def export_json():
                    state = state_manager.get_state()
                    reasoning_data = state.neural_reasoning or {}
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f'neural_analysis_{timestamp}.json'
                    json_str = json.dumps(reasoning_data, indent=2)
                    ui.download(json_str, filename)
                    ui.notify(f'📥 Exporting {filename}...', type='info', position='top')

                ui.button('📋 Copy Neural Data', on_click=copy_json).classes('bg-blue-600 hover:bg-blue-700 px-4 py-2')
                ui.button('⬇️ Export Analysis', on_click=export_json).classes('bg-purple-600 hover:bg-purple-700 px-4 py-2')
                ui.button('🔄 Refresh', on_click=lambda: None).classes('bg-green-600 hover:bg-green-700 px-4 py-2')

        # Enhanced JSON editor with neural styling
        json_editor = ui.json_editor({
            'content': {'json': {}},
            'mode': 'tree',
            'mainMenuBar': False,
            'navigationBar': False,
            'readOnly': True,
            'theme': 'dark'
        }).classes('w-full h-96 border border-gray-600 rounded-lg')

    # Elite decision analytics dashboard
    with ui.card().classes('w-full p-6 mb-6 bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-700'):
        with ui.row().classes('w-full items-center justify-between mb-4'):
            with ui.row().classes('items-center gap-3'):
                ui.icon('analytics', size='28px').classes('text-cyan-400')
                ui.label('Decision Analytics').classes('text-2xl font-bold text-white')
            
            # Enhanced filter controls
            with ui.row().classes('items-center gap-4'):
                ui.label('Filter Decisions:').classes('text-sm font-bold text-cyan-300')
                action_filter = ui.select(
                    label='',
                    value='all',
                    options={'all': 'All Actions', 'buy': 'Buy Signals', 'sell': 'Sell Signals', 'hold': 'Hold Decisions'}
                ).classes('w-40')
                
                # Real-time stats display
                stats_row = ui.row().classes('gap-6 items-center')
        
        # Decision confidence metrics
        with ui.row().classes('w-full gap-4 mb-4'):
            # Decision Count
            with ui.card().classes('flex-1 p-4 bg-gradient-to-br from-blue-900 to-blue-950 border border-blue-700'):
                with ui.row().classes('items-center gap-3'):
                    ui.icon('psychology', size='24px').classes('text-blue-400')
                    with ui.column().classes('gap-1'):
                        decision_count = ui.label('0').classes('text-2xl font-bold text-white')
                        ui.label('Neural Decisions').classes('text-xs text-blue-300')
            
            # Average Confidence
            with ui.card().classes('flex-1 p-4 bg-gradient-to-br from-purple-900 to-purple-950 border border-purple-700'):
                with ui.row().classes('items-center gap-3'):
                    ui.icon('trending_up', size='24px').classes('text-purple-400')
                    with ui.column().classes('gap-1'):
                        avg_confidence = ui.label('0%').classes('text-2xl font-bold text-white')
                        ui.label('Avg Confidence').classes('text-xs text-purple-300')
            
            # Processing Speed
            with ui.card().classes('flex-1 p-4 bg-gradient-to-br from-green-900 to-green-950 border border-green-700'):
                with ui.row().classes('items-center gap-3'):
                    ui.icon('speed', size='24px').classes('text-green-400')
                    with ui.column().classes('gap-1'):
                        processing_speed = ui.label('0ms').classes('text-2xl font-bold text-white')
                        ui.label('Processing Time').classes('text-xs text-green-300')

    # Elite neural decision timeline
    with ui.card().classes('w-full p-6 bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-700'):
        with ui.row().classes('w-full items-center justify-between mb-6'):
            with ui.row().classes('items-center gap-3'):
                ui.icon('timeline', size='28px').classes('text-cyan-400')
                ui.label('Neural Decision Timeline').classes('text-2xl font-bold text-white')
            
            # Timeline controls
            with ui.row().classes('gap-2'):
                ui.button('🔄 Refresh', on_click=lambda: None).classes('bg-blue-600 hover:bg-blue-700 px-4 py-2')
                ui.button('📊 Analyze Patterns', on_click=lambda: None).classes('bg-purple-600 hover:bg-purple-700 px-4 py-2')
                ui.button('🧠 Neural Insights', on_click=lambda: None).classes('bg-green-600 hover:bg-green-700 px-4 py-2')

        # Enhanced timeline container
        timeline_container = ui.column().classes('w-full')

    # Historical decisions storage
    historical_decisions = []

    # ===== AUTO-REFRESH LOGIC =====
    async def update_reasoning():
        """Update JSON editor and timeline with latest reasoning data"""
        state = state_manager.get_state()

        # Update JSON editor
        reasoning_data = state.neural_reasoning
        if reasoning_data and (reasoning_data.get('reasoning') or reasoning_data.get('trade_decisions')):
            json_editor.content = {'json': reasoning_data}
            json_editor.update()

            # Update timeline with filtering
            timeline_container.clear()
            with timeline_container:
                trade_decisions = reasoning_data.get('trade_decisions', [])

                # Add new decisions to history (avoiding duplicates)
                for decision in trade_decisions:
                    decision_id = f"{decision.get('asset')}_{decision.get('action')}_{decision.get('entry_price')}"
                    if not any(d.get('_id') == decision_id for d in historical_decisions):
                        decision['_id'] = decision_id
                        decision['timestamp'] = datetime.now().isoformat()
                        historical_decisions.insert(0, decision)  # Add to front of list
                        # Keep only last 20 decisions
                        if len(historical_decisions) > 20:
                            historical_decisions.pop()

                if trade_decisions:
                    # Apply filter
                    selected_filter = action_filter.value.upper()
                    filtered_decisions = [
                        d for d in trade_decisions
                        if selected_filter == 'ALL' or d.get('action', 'HOLD').upper() == selected_filter
                    ]

                    # Update stats
                    stats_row.clear()
                    with stats_row:
                        buy_count = len([d for d in trade_decisions if d.get('action', '').upper() == 'BUY'])
                        sell_count = len([d for d in trade_decisions if d.get('action', '').upper() == 'SELL'])
                        hold_count = len([d for d in trade_decisions if d.get('action', '').upper() == 'HOLD'])

                        ui.label(f'🟢 Buys: {buy_count}').classes('text-xs text-green-400 font-bold')
                        ui.label(f'🔴 Sells: {sell_count}').classes('text-xs text-red-400 font-bold')
                        ui.label(f'⚫ Holds: {hold_count}').classes('text-xs text-gray-400 font-bold')

                    if filtered_decisions:
                        # Create timeline with enhanced entries
                        with ui.timeline(side='right').classes('w-full'):
                            for decision in filtered_decisions:
                                asset = decision.get('asset', 'Unknown')
                                action = decision.get('action', 'hold').upper()
                                rationale = decision.get('rationale', 'No rationale provided')
                                allocation = decision.get('allocation_usd', 0)
                                tp_price = decision.get('tp_price')
                                sl_price = decision.get('sl_price')
                                exit_plan = decision.get('exit_plan', 'No exit plan')
                                entry_price = decision.get('entry_price', 'N/A')
                                confidence = decision.get('confidence', 0)

                                # Determine color based on action
                                if action == 'BUY':
                                    color = 'green'
                                    icon = '📈'
                                elif action == 'SELL':
                                    color = 'red'
                                    icon = '📉'
                                else:  # HOLD
                                    color = 'grey'
                                    icon = '⏸️'

                                # Timeline entry with enhanced details
                                with ui.timeline_entry(
                                    f'{icon} {asset} - {action}',
                                    color=color,
                                    icon='science'
                                ):
                                    # Confidence indicator
                                    if confidence:
                                        confidence_pct = int(confidence * 100) if confidence <= 1 else int(confidence)
                                        with ui.row().classes('items-center gap-2 mb-2'):
                                            ui.linear_progress(value=confidence).classes('flex-grow')
                                            ui.label(f'{confidence_pct}%').classes('text-xs text-gray-400 w-12')

                                    # Rationale
                                    ui.label(rationale).classes('text-sm text-gray-300 mb-2')

                                    # Details in grid
                                    with ui.grid(columns=2).classes('gap-2 text-xs text-gray-400'):
                                        ui.label(f'Entry: {entry_price}')
                                        ui.label(f'Allocation: ${allocation:,.2f}')
                                        ui.label(f'TP: {tp_price if tp_price else "N/A"}')
                                        ui.label(f'SL: {sl_price if sl_price else "N/A"}')
                                    with ui.row().classes('col-span-2'):
                                        ui.label(f'Exit Plan: {exit_plan[:50]}...' if len(str(exit_plan)) > 50 else f'Exit Plan: {exit_plan}')
                    else:
                        ui.label(f'No {action_filter.value} decisions in current batch').classes('text-gray-400 text-center py-4')
                else:
                    ui.label('No trade decisions yet').classes('text-gray-400 text-center py-4')
        else:
            # Empty state
            json_editor.content = {'json': {}}
            json_editor.update()
            timeline_container.clear()

            # Update stats in empty state
            stats_row.clear()
            with stats_row:
                ui.label('🟢 Buys: 0').classes('text-xs text-green-400 font-bold')
                ui.label('🔴 Sells: 0').classes('text-xs text-red-400 font-bold')
                ui.label('⚫ Holds: 0').classes('text-xs text-gray-400 font-bold')

            with timeline_container:
                with ui.column().classes('items-center py-8'):
                    ui.label('🧠').classes('text-6xl mb-4')
                    ui.label('No reasoning data available').classes('text-xl text-gray-400 mb-2')
                    ui.label('Start the agent from the Dashboard to see AI decisions').classes('text-sm text-gray-500')

    # Action filter change handler
    def on_filter_change(value):
        """Handle filter change"""
        asyncio.create_task(update_reasoning())

    action_filter.on('update:model-value', on_filter_change)

    # Auto-refresh every 3 seconds
    ui.timer(3.0, update_reasoning)

    # Initial update
    asyncio.create_task(update_reasoning())
