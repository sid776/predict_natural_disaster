import plotly.graph_objects as go

def create_quantum_circuit_visualization():
    fig = go.Figure(go.Scatter(
        x=[0, 1, 2, 3],
        y=[0, 1, 0, 1],
        mode='lines+markers',
        name='Quantum Circuit',
        line={'color': '#9B59B6'},
        marker={'color': '#FF9800'}
    ))
    fig.update_layout(
        title='Quantum Circuit Visualization',
        plot_bgcolor='#F5EEF8',
        paper_bgcolor='#F5EEF8',
        font={'color': '#2C3E50', 'family': 'Poppins'}
    )
    return fig 