"""
Proposals Widget - Reusable neural proposals component
"""

from nicegui import ui
from src.gui.services.bot_service import AgentService
from src.gui.services.state_manager import StateManager


def create_proposals_widget(agent_service: AgentService, state_manager: StateManager):
    """Create neural proposals widget that can be reused"""
    
    proposals_container = ui.column().classes('w-full gap-3')
    
    # Empty state for proposals
    proposals_empty = ui.column().classes('w-full items-center py-8')
    with proposals_empty:
        ui.icon('lightbulb_outline', size='48px').classes('text-gray-600 mb-2')
        ui.label('No Proposals').classes('text-lg text-gray-400')
        ui.label('AI will generate recommendations').classes('text-sm text-gray-500')

    def create_proposal_card(proposal: dict):
        """Create a compact proposal card"""
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

    async def approve_proposal(proposal_id: str):
        """Approve a trade proposal"""
        try:
            success = agent_service.approve_proposal(proposal_id)
            if success:
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
                ui.notify('Proposal Rejected', type='warning')
            else:
                ui.notify('Rejection Failed', type='negative')
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')

    return proposals_container, proposals_empty, create_proposal_card


def update_proposals_widget(proposals_container, proposals_empty, proposals, create_proposal_card):
    """Update proposals widget with new data"""
    proposals_empty.visible = len(proposals) == 0
    
    proposals_container.clear()
    if proposals:
        with proposals_container:
            for proposal in proposals[:3]:  # Show max 3 in sidebar
                create_proposal_card(proposal)