"""
QuantumAlpha Capital - Elite Trading Platform
Advanced systematic alpha generation interface
"""

from nicegui import ui
from src.gui.services.bot_service import AgentService
from src.gui.services.state_manager import StateManager
from src.gui.themes.quantumalpha_theme import apply_quantumalpha_theme

# Import comprehensive dashboard
from src.gui.pages.dashboard import create_dashboard

# Global services
agent_service = AgentService()
state_manager = StateManager()

# Connect services
agent_service.state_manager = state_manager


def create_app():
    """Initialize the QuantumAlpha Capital comprehensive trading platform"""

    # Apply elite theme
    apply_quantumalpha_theme()
    
    # Add professional fonts and custom styles
    ui.add_head_html('''
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <style>
            body { 
                font-family: 'Inter', sans-serif; 
                background: #030712;
                overflow-x: hidden;
            }
            .nicegui-content { 
                padding: 20px !important; 
                margin: 0 !important;
                max-width: 100% !important;
            }
            .q-page-container {
                padding: 0 !important;
            }
        </style>
    ''')

    # Comprehensive trading command center
    with ui.column().classes('w-full min-h-screen bg-gray-950 p-4'):
        create_dashboard(agent_service, state_manager)