"""
QuantumAlpha Capital Elite Theme
Professional dark theme with quantum-inspired design elements
"""

from nicegui import ui


def apply_quantumalpha_theme():
    """Apply the elite QuantumAlpha Capital theme"""
    
    # Elite color palette
    colors = {
        'primary': '#0066FF',      # Quantum Blue
        'secondary': '#00FFFF',    # Cyan Accent
        'success': '#00FF88',      # Alpha Green
        'warning': '#FFB800',      # Warning Amber
        'error': '#FF4444',        # Alert Red
        'dark': '#0A0A0F',         # Deep Space
        'surface': '#1A1A2E',      # Surface Dark
        'card': '#16213E',         # Card Background
        'border': '#2A3F5F',       # Border Color
    }
    
    # Apply custom CSS for elite appearance
    ui.add_head_html(f'''
    <style>
        :root {{
            --q-primary: {colors['primary']};
            --q-secondary: {colors['secondary']};
            --q-accent: {colors['secondary']};
            --q-positive: {colors['success']};
            --q-negative: {colors['error']};
            --q-warning: {colors['warning']};
            --q-dark: {colors['dark']};
        }}
        
        /* Elite Background */
        body {{
            background: linear-gradient(135deg, {colors['dark']} 0%, {colors['surface']} 100%);
            font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        }}
        
        /* Quantum Glow Effects */
        .quantum-glow {{
            box-shadow: 0 0 20px rgba(0, 102, 255, 0.3);
            border: 1px solid rgba(0, 102, 255, 0.5);
        }}
        
        .alpha-card {{
            background: linear-gradient(145deg, {colors['card']}, {colors['surface']});
            border: 1px solid {colors['border']};
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }}
        
        /* Elite Metrics */
        .metric-positive {{
            color: {colors['success']};
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }}
        
        .metric-negative {{
            color: {colors['error']};
            text-shadow: 0 0 10px rgba(255, 68, 68, 0.5);
        }}
        
        .metric-neutral {{
            color: {colors['secondary']};
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
        }}
        
        /* Professional Buttons */
        .elite-button {{
            background: linear-gradient(45deg, {colors['primary']}, {colors['secondary']});
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
        }}
        
        .elite-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 102, 255, 0.4);
        }}
        
        /* Status Indicators */
        .status-active {{
            color: {colors['success']};
            animation: pulse-green 2s infinite;
        }}
        
        .status-inactive {{
            color: #666;
        }}
        
        .status-alert {{
            color: {colors['error']};
            animation: pulse-red 1s infinite;
        }}
        
        @keyframes pulse-green {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}
        
        @keyframes pulse-red {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
        }}
        
        /* Elite Tables */
        .elite-table {{
            background: {colors['card']};
            border-radius: 8px;
            border: 1px solid {colors['border']};
        }}
        
        .elite-table th {{
            background: {colors['surface']};
            color: {colors['secondary']};
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.75rem;
        }}
        
        /* Quantum Navigation */
        .quantum-nav {{
            background: rgba(26, 26, 46, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid {colors['border']};
        }}
        
        /* Elite Charts */
        .chart-container {{
            background: {colors['card']};
            border-radius: 12px;
            border: 1px solid {colors['border']};
            padding: 20px;
        }}
        
        /* Professional Inputs */
        .elite-input {{
            background: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 6px;
            color: white;
        }}
        
        .elite-input:focus {{
            border-color: {colors['primary']};
            box-shadow: 0 0 0 2px rgba(0, 102, 255, 0.2);
        }}
        
        /* Loading Animations */
        .quantum-loading {{
            background: linear-gradient(90deg, 
                transparent, 
                rgba(0, 102, 255, 0.2), 
                transparent
            );
            animation: quantum-shimmer 1.5s infinite;
        }}
        
        @keyframes quantum-shimmer {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        
        /* Elite Scrollbars */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {colors['surface']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {colors['primary']};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {colors['secondary']};
        }}
    </style>
    ''')


def create_elite_card(title: str = "", classes: str = ""):
    """Create an elite-styled card component"""
    return ui.card().classes(f'alpha-card {classes}')


def create_metric_display(value: str, label: str, trend: str = "neutral"):
    """Create a professional metric display"""
    trend_class = f"metric-{trend}"
    
    with ui.column().classes('text-center'):
        ui.label(value).classes(f'text-2xl font-bold {trend_class}')
        ui.label(label).classes('text-xs text-gray-400 uppercase tracking-wide')


def create_elite_button(text: str, on_click=None, classes: str = ""):
    """Create an elite-styled button"""
    return ui.button(text, on_click=on_click).classes(f'elite-button {classes}')


def create_status_indicator(status: str, text: str):
    """Create a professional status indicator"""
    status_class = f"status-{status}"
    return ui.label(text).classes(f'font-bold {status_class}')