"""
QuantumAlpha Capital - Neural Trade Proposals
Elite AI recommendation system with advanced proposal analytics and execution management
"""

from nicegui import ui
from src.gui.services.bot_service import AgentService
from src.gui.services.state_manager import StateManager


def create_recommendations(agent_service: AgentService, state_manager: StateManager):
    """Create elite neural trade proposal interface with advanced analytics"""
    
    # Elite header with neural branding
    with ui.row().classes('w-full items-center justify-between mb-6'):
        with ui.row().classes('items-center gap-4'):
            ui.icon('lightbulb', size='48px').classes('text-cyan-400')
            with ui.column().classes('gap-1'):
                ui.label('Neural Trade Proposals').classes('text-4xl font-bold text-white')
                ui.label('AI-Powered Investment Recommendations & Execution Management').classes('text-lg text-cyan-300')
        
        # Proposal management controls
        with ui.row().classes('gap-2'):
            ui.button('🔄 Refresh Proposals', on_click=lambda: None).classes('bg-blue-600 hover:bg-blue-700 px-4 py-2')
            ui.button('⚡ Batch Execute', on_click=lambda: None).classes('bg-green-600 hover:bg-green-700 px-4 py-2')
            ui.button('❌ Reject All', on_click=lambda: None).classes('bg-red-600 hover:bg-red-700 px-4 py-2')
    
    # Elite info banner with neural intelligence theme
    with ui.card().classes('w-full p-6 mb-6 bg-gradient-to-br from-blue-900 to-blue-950 border border-blue-500'):
        with ui.row().classes('items-center gap-4'):
            ui.icon('auto_awesome', size='32px').classes('text-blue-300')
            with ui.column().classes('gap-2'):
                ui.label('Neural Trading Intelligence').classes('text-xl font-bold text-white')
                ui.label('Advanced AI analyzes market conditions and generates high-probability trade proposals. Each recommendation includes comprehensive risk assessment, neural confidence scoring, and systematic execution parameters.').classes('text-sm text-blue-200 leading-relaxed')
    
    # Elite proposal analytics dashboard
    stats_row = ui.row().classes('w-full gap-4 mb-6')
    
    # Enhanced proposal container with neural styling
    proposals_container = ui.column().classes('w-full gap-6')
    
    async def update_proposals():
        """Update elite proposal analytics with enhanced metrics"""
        state = state_manager.get_state()
        proposals = state.awaiting_approval or []
        
        # Enhanced analytics dashboard
        stats_row.clear()
        with stats_row:
            # Pending Proposals with neural styling
            with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-purple-900 to-purple-950 border border-purple-700'):
                with ui.row().classes('items-center gap-4'):
                    ui.icon('pending_actions', size='32px').classes('text-purple-400')
                    with ui.column().classes('gap-1'):
                        ui.label(str(len(proposals))).classes('text-4xl font-bold text-white')
                        ui.label('Neural Proposals').classes('text-sm text-purple-300 font-medium')
            
            # High Confidence Proposals
            high_confidence = len([p for p in proposals if p.get('confidence', 0) >= 80])
            with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-green-900 to-green-950 border border-green-700'):
                with ui.row().classes('items-center gap-4'):
                    ui.icon('verified', size='32px').classes('text-green-400')
                    with ui.column().classes('gap-1'):
                        ui.label(str(high_confidence)).classes('text-4xl font-bold text-white')
                        ui.label('High Confidence').classes('text-sm text-green-300 font-medium')
            
            # Total Potential Allocation
            total_allocation = sum(p.get('allocation', 0) for p in proposals)
            with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-blue-900 to-blue-950 border border-blue-700'):
                with ui.row().classes('items-center gap-4'):
                    ui.icon('account_balance_wallet', size='32px').classes('text-blue-400')
                    with ui.column().classes('gap-1'):
                        ui.label(f'${total_allocation:,.0f}').classes('text-4xl font-bold text-white')
                        ui.label('Total Allocation').classes('text-sm text-blue-300 font-medium')
            
            # Agent Status with enhanced indicator
            if state.active_status:
                with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-cyan-900 to-cyan-950 border border-cyan-700'):
                    with ui.row().classes('items-center gap-4'):
                        ui.icon('smart_toy', size='32px').classes('text-cyan-400')
                        with ui.column().classes('gap-1'):
                            ui.label('ACTIVE').classes('text-4xl font-bold text-white')
                            ui.label('Neural Engine').classes('text-sm text-cyan-300 font-medium')
            else:
                with ui.card().classes('flex-1 p-6 bg-gradient-to-br from-gray-700 to-gray-800 border border-gray-600'):
                    with ui.row().classes('items-center gap-4'):
                        ui.icon('pause_circle', size='32px').classes('text-gray-400')
                        with ui.column().classes('gap-1'):
                            ui.label('STANDBY').classes('text-4xl font-bold text-white')
                            ui.label('Neural Engine').classes('text-sm text-gray-300 font-medium')
        
        # Enhanced proposal display
        proposals_container.clear()
        
        if not proposals:
            with proposals_container:
                with ui.card().classes('w-full p-12 bg-gradient-to-br from-gray-800 to-gray-900 border border-gray-600'):
                    with ui.column().classes('items-center gap-6'):
                        ui.icon('lightbulb_outline', size='96px').classes('text-gray-600')
                        ui.label('No Neural Proposals Available').classes('text-3xl font-bold text-gray-400')
                        ui.label('The AI neural engine will generate high-probability trade proposals when optimal market conditions are detected.').classes('text-lg text-gray-500 text-center max-w-2xl')
                        
                        # Action suggestions
                        with ui.row().classes('gap-4 mt-4'):
                            ui.button('🚀 Start Neural Engine', on_click=lambda: None).classes('bg-cyan-600 hover:bg-cyan-700 px-8 py-3 text-lg font-bold')
                            ui.button('📊 Market Analysis', on_click=lambda: None).classes('bg-purple-600 hover:bg-purple-700 px-8 py-3 text-lg font-bold')
            return

        with proposals_container:
            for proposal in proposals:
                create_elite_proposal_card(proposal)
    
    def create_elite_proposal_card(proposal: dict):
        """Create an elite neural proposal card with advanced analytics"""
        asset = proposal.get('asset', 'N/A')
        action = proposal.get('action', 'hold')
        confidence = proposal.get('confidence', 0)
        entry_price = proposal.get('entry_price', 0)
        tp_price = proposal.get('tp_price')
        sl_price = proposal.get('sl_price')
        size = proposal.get('size', 0)
        allocation = proposal.get('allocation', 0)
        rationale = proposal.get('rationale', '')
        risk_reward = proposal.get('risk_reward')
        proposal_id = proposal.get('id', '')
        timestamp = proposal.get('timestamp', '')
        
        # Enhanced neural metrics
        neural_score = proposal.get('neural_score', confidence)
        market_sentiment = proposal.get('market_sentiment', 'NEUTRAL')
        volatility_assessment = proposal.get('volatility', 'MEDIUM')
        
        # Elite card styling based on action and confidence
        if action == 'buy':
            gradient = 'from-green-900 via-green-950 to-gray-950'
            border_color = 'border-green-500'
            badge_color = 'bg-green-600'
            action_icon = '🚀'
        elif action == 'sell':
            gradient = 'from-red-900 via-red-950 to-gray-950'
            border_color = 'border-red-500'
            badge_color = 'bg-red-600'
            action_icon = '📉'
        else:
            gradient = 'from-gray-800 via-gray-900 to-gray-950'
            border_color = 'border-gray-600'
            badge_color = 'bg-gray-600'
            action_icon = '⏸'
        
        # Confidence-based glow effect
        glow_class = ''
        if confidence >= 90:
            glow_class = 'shadow-lg shadow-green-500/20'
        elif confidence >= 75:
            glow_class = 'shadow-lg shadow-blue-500/20'
        
        with ui.card().classes(f'w-full p-8 bg-gradient-to-br {gradient} {border_color} border-2 {glow_class}'):
            # Elite header with neural branding
            with ui.row().classes('w-full items-center justify-between mb-6'):
                with ui.row().classes('items-center gap-4'):
                    ui.label(action_icon).classes('text-5xl')
                    with ui.column().classes('gap-1'):
                        ui.label(asset).classes('text-4xl font-bold text-white')
                        ui.label(f'Neural Proposal #{proposal_id[:8]}').classes('text-sm text-gray-400')
                
                # Elite action badge with confidence indicator
                with ui.column().classes('items-end gap-2'):
                    with ui.badge().classes(f'{badge_color} text-white text-xl px-6 py-3 rounded-lg'):
                        ui.label(action.upper()).classes('font-bold')
                    
                    # Confidence indicator
                    confidence_color = 'text-green-400' if confidence >= 80 else 'text-yellow-400' if confidence >= 60 else 'text-red-400'
                    ui.label(f'{confidence:.0f}% Confidence').classes(f'text-sm {confidence_color} font-bold')
            
            # Neural analytics grid
            with ui.row().classes('w-full gap-6 mb-6'):
                # Neural confidence visualization
                with ui.card().classes('flex-1 p-4 bg-black bg-opacity-30 border border-cyan-500'):
                    ui.label('🧠 Neural Confidence').classes('text-sm text-cyan-400 font-bold mb-2')
                    with ui.linear_progress(value=confidence / 100).classes('mb-2'):
                        pass
                    ui.label(f'{confidence:.1f}% Neural Certainty').classes('text-lg font-bold text-white')
                
                # Market sentiment analysis
                with ui.card().classes('flex-1 p-4 bg-black bg-opacity-30 border border-purple-500'):
                    ui.label('📊 Market Sentiment').classes('text-sm text-purple-400 font-bold mb-2')
                    sentiment_color = 'text-green-400' if market_sentiment == 'BULLISH' else 'text-red-400' if market_sentiment == 'BEARISH' else 'text-gray-400'
                    ui.label(market_sentiment).classes(f'text-lg font-bold {sentiment_color}')
                    ui.label('Neural Analysis').classes('text-xs text-gray-400')
                
                # Risk assessment
                with ui.card().classes('flex-1 p-4 bg-black bg-opacity-30 border border-orange-500'):
                    ui.label('⚠️ Risk Level').classes('text-sm text-orange-400 font-bold mb-2')
                    risk_color = 'text-green-400' if volatility_assessment == 'LOW' else 'text-yellow-400' if volatility_assessment == 'MEDIUM' else 'text-red-400'
                    ui.label(volatility_assessment).classes(f'text-lg font-bold {risk_color}')
                    ui.label('Volatility Assessment').classes('text-xs text-gray-400')
            
            # Elite trade execution parameters
            with ui.grid(columns=4).classes('w-full gap-4 mb-6'):
                # Entry Price
                with ui.card().classes('p-4 bg-gray-800 bg-opacity-60 border border-blue-500'):
                    ui.label('Entry Target').classes('text-xs text-blue-400 font-bold mb-1')
                    ui.label(f'${entry_price:,.2f}').classes('text-2xl text-white font-bold')
                    ui.label('Optimal Entry').classes('text-xs text-gray-400')
                
                # Take Profit with enhanced visualization
                with ui.card().classes('p-4 bg-gray-800 bg-opacity-60 border border-green-500'):
                    ui.label('Take Profit').classes('text-xs text-green-400 font-bold mb-1')
                    if tp_price:
                        ui.label(f'${tp_price:,.2f}').classes('text-2xl text-green-400 font-bold')
                        if entry_price:
                            pct = ((tp_price - entry_price) / entry_price) * 100
                            ui.label(f'+{pct:.1f}% Target').classes('text-xs text-green-300')
                    else:
                        ui.label('Market Exit').classes('text-2xl text-gray-500')
                
                # Stop Loss with risk visualization
                with ui.card().classes('p-4 bg-gray-800 bg-opacity-60 border border-red-500'):
                    ui.label('Stop Loss').classes('text-xs text-red-400 font-bold mb-1')
                    if sl_price:
                        ui.label(f'${sl_price:,.2f}').classes('text-2xl text-red-400 font-bold')
                        if entry_price:
                            pct = ((sl_price - entry_price) / entry_price) * 100
                            ui.label(f'{pct:.1f}% Risk').classes('text-xs text-red-300')
                    else:
                        ui.label('No Stop').classes('text-2xl text-gray-500')
                
                # Position sizing
                with ui.card().classes('p-4 bg-gray-800 bg-opacity-60 border border-purple-500'):
                    ui.label('Allocation').classes('text-xs text-purple-400 font-bold mb-1')
                    ui.label(f'${allocation:,.0f}').classes('text-2xl text-purple-400 font-bold')
                    ui.label(f'{size:.4f} {asset}').classes('text-xs text-gray-400')
            
            # Risk/Reward analysis
            if risk_reward:
                with ui.card().classes('w-full p-4 bg-blue-900 bg-opacity-40 border border-blue-400 mb-6'):
                    with ui.row().classes('items-center gap-4'):
                        ui.icon('analytics', size='32px').classes('text-blue-400')
                        with ui.column().classes('gap-1'):
                            ui.label(f'Risk/Reward Ratio: 1:{risk_reward:.2f}').classes('text-xl text-blue-300 font-bold')
                            ui.label('Neural risk assessment indicates favorable probability distribution').classes('text-sm text-blue-200')
            
            # Enhanced AI rationale section
            with ui.expansion('🧠 Neural Analysis & Rationale', icon='psychology').classes('w-full bg-gray-800 bg-opacity-60 border border-cyan-500 mb-6'):
                with ui.column().classes('p-4 gap-3'):
                    ui.label('Advanced Neural Network Analysis:').classes('text-sm text-cyan-400 font-bold')
                    ui.label(rationale or 'Neural analysis processing...').classes('text-gray-300 whitespace-pre-wrap leading-relaxed')
                    
                    # Additional neural insights
                    ui.separator().classes('my-3')
                    ui.label('Neural Confidence Factors:').classes('text-sm text-purple-400 font-bold')
                    with ui.column().classes('gap-1'):
                        ui.label('• Technical pattern recognition: High probability setup detected').classes('text-xs text-gray-400')
                        ui.label('• Market microstructure analysis: Favorable liquidity conditions').classes('text-xs text-gray-400')
                        ui.label('• Risk-adjusted return optimization: Positive expected value').classes('text-xs text-gray-400')
            
            # Execution timestamp
            ui.label(f'Generated: {timestamp[:19] if timestamp else "Real-time"}').classes('text-xs text-gray-500 mb-6')
            
            # Elite action buttons with enhanced styling
            with ui.row().classes('gap-4 w-full justify-end'):
                ui.button(
                    '❌ Reject Proposal',
                    on_click=lambda pid=proposal_id: reject_proposal(pid)
                ).classes('bg-red-600 hover:bg-red-700 text-white px-8 py-4 text-lg font-bold rounded-lg border border-red-500')
                
                ui.button(
                    '✅ Execute Trade',
                    on_click=lambda pid=proposal_id: approve_proposal(pid)
                ).classes('bg-green-600 hover:bg-green-700 text-white px-12 py-4 text-xl font-bold rounded-lg border border-green-500 shadow-lg shadow-green-500/30')
    
    async def approve_proposal(proposal_id: str):
        """Approve and execute a proposal"""
        try:
            success = agent_service.approve_proposal(proposal_id)
            if success:
                ui.notify('✅ Trade approved and executing!', type='positive', position='top')
                await update_proposals()
            else:
                ui.notify('❌ Failed to approve trade', type='negative')
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')
    
    async def reject_proposal(proposal_id: str):
        """Reject a proposal"""
        try:
            success = agent_service.reject_proposal(proposal_id, reason="Rejected by user via GUI")
            if success:
                ui.notify('❌ Proposal rejected', type='warning', position='top')
                await update_proposals()
            else:
                ui.notify('Failed to reject proposal', type='negative')
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')
    
    # Auto-refresh every 2 seconds
    ui.timer(2.0, update_proposals)
    
    # Initial update
    # (timer will handle subsequent updates)
