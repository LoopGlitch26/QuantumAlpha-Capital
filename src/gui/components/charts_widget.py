"""
Charts Widget - Reusable chart components
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from nicegui import ui
import datetime


def create_equity_chart():
    """Create just the equity chart"""
    return ui.plotly(go.Figure(
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


def create_allocation_chart():
    """Create just the allocation chart"""
    return ui.plotly(go.Figure(
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


def create_portfolio_charts():
    """Create portfolio value and allocation charts"""
    
    # Portfolio Value Chart
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

    # Asset Allocation Pie Chart
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

    return equity_chart, allocation_chart


def create_technical_chart():
    """Create technical analysis chart with dark theme"""
    
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
    
    # Add sample data immediately
    now = datetime.datetime.now()
    sample_times = [(now - datetime.timedelta(minutes=i*5)).strftime('%H:%M') for i in range(20, 0, -1)]
    sample_prices = [50000 + i*100 + (i%3)*200 for i in range(20)]
    sample_rsi = [50 + (i%10)*3 for i in range(20)]
    sample_macd = [(i%5 - 2.5)*0.1 for i in range(20)]
    
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

    return technical_chart


def update_portfolio_charts(equity_chart, allocation_chart, equity_history, positions, account_balance):
    """Update portfolio charts with new data"""
    
    # Update equity chart
    if equity_history and len(equity_history) > 0:
        times = [d['time'] for d in equity_history]
        values = [d['value'] for d in equity_history]
        equity_chart.figure.data[0].x = times
        equity_chart.figure.data[0].y = values
        equity_chart.update()
    else:
        # Show sample data
        now = datetime.datetime.now()
        sample_times = [(now - datetime.timedelta(hours=i)).strftime('%H:%M') for i in range(24, 0, -1)]
        base_value = account_balance or 1000
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
        cash_allocation = max(0, account_balance - total_position_value)
        if cash_allocation > 0:
            labels.append('Cash')
            values.append(cash_allocation)

        allocation_chart.figure.data[0].labels = labels
        allocation_chart.figure.data[0].values = values
        allocation_chart.update()
    else:
        # Show sample allocation
        base_balance = account_balance or 1000
        allocation_chart.figure.data[0].labels = ['BTC', 'ETH', 'Cash']
        allocation_chart.figure.data[0].values = [base_balance * 0.4, base_balance * 0.3, base_balance * 0.3]
        allocation_chart.update()


def update_technical_chart(technical_chart, market_data):
    """Update technical analysis chart with market data"""
    
    try:
        # Clear existing data
        technical_chart.figure.data = []
        
        recent_prices = market_data.get('recent_mid_prices', []) if market_data else []
        if recent_prices and len(recent_prices) > 1:
            times = [f"T-{len(recent_prices)-i}" for i in range(len(recent_prices))]
            
            # Add price line
            technical_chart.figure.add_trace(
                go.Scatter(
                    x=times, y=recent_prices,
                    mode='lines+markers',
                    name='Price',
                    line=dict(color='#3b82f6', width=3),
                    marker=dict(size=4, color='#3b82f6')
                ),
                row=1, col=1
            )

            # Add indicators if available
            intraday = market_data.get('intraday', {})
            ema20_series = intraday.get('series', {}).get('ema20', [])
            if ema20_series and len(ema20_series) == len(recent_prices):
                technical_chart.figure.add_trace(
                    go.Scatter(
                        x=times, y=ema20_series,
                        mode='lines',
                        name='EMA20',
                        line=dict(color='#f59e0b', width=2)
                    ),
                    row=1, col=1
                )

            # RSI subplot
            rsi_series = intraday.get('series', {}).get('rsi14', [])
            if rsi_series and len(rsi_series) == len(recent_prices):
                technical_chart.figure.add_trace(
                    go.Scatter(
                        x=times, y=rsi_series,
                        mode='lines',
                        name='RSI',
                        line=dict(color='#ef4444', width=2)
                    ),
                    row=2, col=1
                )
                
                technical_chart.figure.add_hline(y=70, line_dash="dash", line_color="#ef4444", opacity=0.5, row=2, col=1)
                technical_chart.figure.add_hline(y=30, line_dash="dash", line_color="#10b981", opacity=0.5, row=2, col=1)

            # MACD subplot
            macd_series = intraday.get('series', {}).get('macd', [])
            if macd_series and len(macd_series) == len(recent_prices):
                technical_chart.figure.add_trace(
                    go.Scatter(
                        x=times, y=macd_series,
                        mode='lines',
                        name='MACD',
                        line=dict(color='#8b5cf6', width=2)
                    ),
                    row=3, col=1
                )
                
                technical_chart.figure.add_hline(y=0, line_dash="dash", line_color="#6b7280", opacity=0.5, row=3, col=1)

        else:
            # Show sample data when no real data available
            now = datetime.datetime.now()
            sample_times = [(now - datetime.timedelta(minutes=i*5)).strftime('%H:%M') for i in range(20, 0, -1)]
            
            base_price = 50000
            sample_prices = [base_price + i*50 + (i%4)*100 for i in range(20)]
            sample_rsi = [45 + (i%8)*5 for i in range(20)]
            sample_macd = [(i%6 - 3)*0.05 for i in range(20)]
            
            # Add sample data
            technical_chart.figure.add_trace(
                go.Scatter(x=sample_times, y=sample_prices, mode='lines', name='BTC Price', line=dict(color='#3b82f6', width=2)),
                row=1, col=1
            )
            technical_chart.figure.add_trace(
                go.Scatter(x=sample_times, y=sample_rsi, mode='lines', name='RSI', line=dict(color='#ef4444', width=2)),
                row=2, col=1
            )
            technical_chart.figure.add_trace(
                go.Scatter(x=sample_times, y=sample_macd, mode='lines', name='MACD', line=dict(color='#8b5cf6', width=2)),
                row=3, col=1
            )
            
            # Add reference lines
            technical_chart.figure.add_hline(y=70, line_dash="dash", line_color="#ef4444", opacity=0.5, row=2, col=1)
            technical_chart.figure.add_hline(y=30, line_dash="dash", line_color="#10b981", opacity=0.5, row=2, col=1)
            technical_chart.figure.add_hline(y=0, line_dash="dash", line_color="#6b7280", opacity=0.5, row=3, col=1)

        # Force update with dark theme
        technical_chart.figure.update_layout(
            template='plotly_dark',
            paper_bgcolor='#1f2937',
            plot_bgcolor='#1f2937',
            font=dict(color='#e5e7eb')
        )
        
        technical_chart.update()

    except Exception as e:
        print(f"Error updating technical chart: {e}")