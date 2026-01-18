"""
Header Component - Top navigation bar with quick metrics
"""

from nicegui import ui
from src.gui.services.state_manager import StateManager


def create_header(state_manager: StateManager):
    """
    Create header component with logo, quick metrics, and status.

    Args:
        state_manager: Global state manager instance
    """
    with ui.row().classes('w-full bg-gray-900 px-6 py-3 shadow-lg items-center'):
        with ui.row().classes('w-full items-center justify-between'):
            # Logo and title
            with ui.row().classes('items-center gap-3'):
                ui.label('⚡').classes('text-4xl')
                with ui.column().classes('gap-0'):
                    ui.label('QuantumAlpha').classes('text-2xl font-bold text-white leading-none')
                    ui.label('CAPITAL').classes('text-sm font-light text-blue-400 tracking-widest leading-none')

            # Elite metrics dashboard
            with ui.row().classes('gap-8'):
                # Portfolio Value
                with ui.column().classes('text-center'):
                    balance_label = ui.label('$0.00').classes('text-xl font-bold text-white')
                    ui.label('Portfolio Value').classes('text-xs text-gray-400')

                # Alpha Generation
                with ui.column().classes('text-center'):
                    pnl_label = ui.label('+0.00%').classes('text-xl font-bold text-green-500')
                    ui.label('Alpha Generated').classes('text-xs text-gray-400')

                # Risk Metric
                with ui.column().classes('text-center'):
                    sharpe_label = ui.label('0.00').classes('text-xl font-bold text-white')
                    ui.label('Risk Metric').classes('text-xs text-gray-400')

                # System Status
                with ui.column().classes('text-center'):
                    status_label = ui.label('⚫ Inactive').classes('text-sm font-bold')

            # Auto-refresh elite metrics
            async def update_header():
                state = state_manager.get_state()

                # Update portfolio value
                balance_label.text = f"${state.account_balance:,.2f}"

                # Update alpha generation with color coding
                performance_ratio = state.performance_ratio
                pnl_label.text = f"{performance_ratio:+.2f}%"
                if performance_ratio >= 0:
                    pnl_label.classes(remove='text-red-500', add='text-green-500')
                else:
                    pnl_label.classes(remove='text-green-500', add='text-red-500')

                # Update risk metric
                sharpe_label.text = f"{state.risk_metric:.2f}"

                # Update system status
                if state.active_status:
                    status_label.text = '🟢 Active'
                    status_label.classes(remove='text-gray-400', add='text-green-500')
                else:
                    status_label.text = '⚫ Inactive'
                    status_label.classes(remove='text-green-500', add='text-gray-400')

                # Error indicator
                if state.system_error:
                    status_label.text = '🔴 Alert'
                    status_label.classes(remove='text-green-500 text-gray-400', add='text-red-500')

            # Refresh every second
            ui.timer(1.0, update_header)
