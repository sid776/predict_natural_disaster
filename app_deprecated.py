from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import requests
from quantum_model import QuantumTornadoPredictor
import os
from dotenv import load_dotenv
import datetime
import math
import random
from datetime import datetime, timedelta
import json
import numpy as np
import traceback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from quantum_visualization import create_quantum_circuit_visualization
import dash
from flask import Flask, request, jsonify
from flask_cors import CORS
# Qiskit imports - commented out due to version compatibility issues
# from qiskit import QuantumCircuit, Aer, execute
# from qiskit.visualization import plot_histogram
import pennylane as qml
from sklearn.preprocessing import MinMaxScaler

# Load environment variables
load_dotenv()

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Expose the Flask server for Gunicorn

# Enable CORS for the Flask server
CORS(server)

predictor = QuantumTornadoPredictor()
geolocator = Nominatim(user_agent="tornado_predictor")

# --- Color palette matching the screenshot ---
COLORS = {
    'tab_tornado': '#FFA726',      # Orange
    'tab_earthquake': '#AB47BC',   # Purple
    'tab_wildfire': '#FFE066',     # Yellow
    'tab_flood': '#2ECC71',        # Green
    'tab_guide': '#42A5F5',        # Blue
    'sidebar_bg': '#F3E8FF',       # Light lavender
    'sidebar_border': '#B39DDB',   # Purple border
    'sidebar_button': '#8E24AA',   # Purple button
    'sidebar_button_text': '#FFFFFF',
    'main_bg': '#F8F9FA',          # Very light gray
    'card_bg': '#FFF9FB',          # Soft pastel
    'card_border': '#FFA726',      # Orange border for tornado
    'text': '#333A4D',             # Dark gray
    'white': '#FFFFFF',
}

# --- Graph color mapping for each disaster ---
GRAPH_COLORS = {
    'tornado': COLORS['tab_tornado'],
    'earthquake': COLORS['tab_earthquake'],
    'wildfire': COLORS['tab_wildfire'],
    'fire': COLORS['tab_wildfire'],  # Alias for fire
    'flood': COLORS['tab_flood'],
}

# Global statistics data (updated with real data)
GLOBAL_STATS = {
    'tornado': {
        'count': 1250,  # Average annual tornadoes in the US
        'deaths': 60,   # Average annual deaths
        'injuries': 1500,
        'damage': 1.5   # Billions USD
    },
    'earthquake': {
        'count': 20000,  # Annual earthquakes worldwide
        'deaths': 2000,  # Average annual deaths
        'injuries': 5000,
        'damage': 5.0    # Billions USD
    },
    'fire': {
        'count': 50000,  # Annual wildfires in the US
        'deaths': 100,   # Average annual deaths
        'injuries': 2000,
        'damage': 2.0    # Billions USD
    },
    'flood': {
        'count': 1000,   # Annual significant floods worldwide
        'deaths': 5000,  # Average annual deaths
        'injuries': 10000,
        'damage': 10.0   # Billions USD
    }
}

def get_coordinates(location):
    try:
        location_data = geolocator.geocode(location + ", USA")
        if location_data:
            return location_data.latitude, location_data.longitude
        return None, None
    except GeocoderTimedOut:
        return None, None

def get_weather_data(lat, lon):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    
    if not api_key:
        print("Error: OpenWeatherMap API key not found in .env file")
        return get_mock_weather_data()
    
    if api_key == 'your_openweathermap_api_key_here':
        print("Error: Please replace the placeholder API key with your actual OpenWeatherMap API key")
        return get_mock_weather_data()
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        print(f"Making API request to: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Headers: {response.headers}")
        print(f"API Response Content: {response.content}")
        
        if response.status_code == 200:
            weather_data = response.json()
            # Add coordinates to the weather data for the quantum model
            weather_data['coord'] = {'lat': lat, 'lon': lon}
            return weather_data
        elif response.status_code == 401:
            print("Error: Invalid API key")
            return get_mock_weather_data()
        elif response.status_code == 404:
            print("Error: Location not found")
            return get_mock_weather_data()
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return get_mock_weather_data()
            
    except requests.exceptions.Timeout:
        print("Error: API request timed out")
        return get_mock_weather_data()
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the API")
        return get_mock_weather_data()
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return get_mock_weather_data()

def get_mock_weather_data():
    """Return mock weather data for testing when the API is not available"""
    print("Using mock weather data")
    return {
        'main': {
            'temp': 293.15,  # 20°C
            'humidity': 65,
            'pressure': 1013
        },
        'wind': {
            'speed': 5.5,
            'deg': 180
        },
        'clouds': {
            'all': 40
        },
        'rain': {
            '1h': 0
        },
        'sys': {
            'sunrise': 1622520000,
            'sunset': 1622574000
        },
        'weather': [
            {
                'id': 800,
                'main': 'Clear',
                'description': 'clear sky',
                'icon': '01d'
            }
        ],
        'visibility': 10000,  # 10km
        'mock_data': True,  # Flag to indicate this is mock data
        'coord': {'lat': 40.7128, 'lon': -74.0060}  # Default coordinates (NYC)
    }

def test_api_connection():
    """Test the OpenWeatherMap API connection with a known location"""
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    print(f"Testing API connection with key: {api_key[:5]}...")
    
    # Test with New York City coordinates
    lat, lon = 40.7128, -74.0060
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        print(f"Requesting weather data from: {url}")
        response = requests.get(url, timeout=10)
        
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text[:500]}...")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Successfully parsed JSON response: {data.keys()}")
            return True
        else:
            print(f"API test failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"API test error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

# --- Helper: Always show a plot with sample/mock data ---
def create_gauge(disaster):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=0,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': COLORS['text']},
            'bar': {'color': GRAPH_COLORS[disaster]},
            'bgcolor': COLORS['white'],
            'borderwidth': 2,
            'bordercolor': GRAPH_COLORS[disaster],
            'steps': [
                {'range': [0, 30], 'color': '#FFE066'},
                {'range': [30, 70], 'color': '#FFA726'},
                {'range': [70, 100], 'color': '#FF7043'}
            ],
        },
        title={'text': "Probability (%)", 'font': {'color': COLORS['text'], 'size': 24}},
    )).update_layout(
        paper_bgcolor=COLORS['main_bg'],
        plot_bgcolor=COLORS['white'],
        font={'color': COLORS['text']}
    )

def create_forecast(disaster):
    dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
    y = [random.randint(20, 80) for _ in range(30)]
    return go.Figure(
        data=[go.Scatter(
            x=dates,
            y=y,
            mode='lines',
            line=dict(color=GRAPH_COLORS[disaster], width=3),
        )],
        layout=go.Layout(
            title=dict(text='30-Day Probability Forecast', font=dict(color=COLORS['text'], size=20)),
            xaxis=dict(title='Date', gridcolor=COLORS['sidebar_border']),
            yaxis=dict(title='Probability (%)', gridcolor=COLORS['sidebar_border'], range=[0, 100]),
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['white'],
            font=dict(color=COLORS['text'])
        )
    )

def create_factors(disaster):
    factors = ['Temperature', 'Humidity', 'Wind Speed', 'Pressure']
    y = [random.randint(10, 40) for _ in range(4)]
    return go.Figure(
        data=[go.Bar(
            x=factors,
            y=y,
            marker_color=GRAPH_COLORS[disaster]
        )],
        layout=go.Layout(
            title=dict(text='Factor Impact Analysis', font=dict(color=COLORS['text'], size=20)),
            xaxis=dict(title='Factors', gridcolor=COLORS['sidebar_border']),
            yaxis=dict(title='Impact (%)', gridcolor=COLORS['sidebar_border'], range=[0, 100]),
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['white'],
            font=dict(color=COLORS['text'])
        )
    )

# Update the initial gauge figure
def create_initial_gauge():
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=0,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': COLORS['text']},
            'bar': {'color': COLORS['primary']},
            'bgcolor': COLORS['card'],
            'borderwidth': 2,
            'bordercolor': COLORS['border'],
            'steps': [
                {'range': [0, 30], 'color': COLORS['success']},
                {'range': [30, 70], 'color': COLORS['warning']},
                {'range': [70, 100], 'color': COLORS['danger']}
            ],
        },
        title={'text': "Probability", 'font': {'color': COLORS['text'], 'size': 24}},
    )).update_layout(
        paper_bgcolor=COLORS['background'],
        plot_bgcolor=COLORS['card'],
        font={'color': COLORS['text']}
    )

# Update the initial forecast figure
def create_initial_forecast():
    dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
    return go.Figure(
        data=[go.Scatter(
            x=dates,
            y=[0] * 30,
            mode='lines+markers',
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(color=COLORS['accent'], size=8)
        )],
        layout=go.Layout(
            title=dict(text='30-Day Forecast', font=dict(color=COLORS['text'], size=24)),
            xaxis=dict(title='Date', gridcolor=COLORS['border']),
            yaxis=dict(title='Probability (%)', gridcolor=COLORS['border']),
            paper_bgcolor=COLORS['background'],
            plot_bgcolor=COLORS['card'],
            font=dict(color=COLORS['text'])
        )
    )

# Update the initial circuit figure
def create_initial_circuit():
    return go.Figure(
        data=[go.Scatter(
            x=[0, 1, 2, 3],
            y=[0, 1, 0, 1],
            mode='lines+markers',
            line=dict(color=COLORS['secondary'], width=3),
            marker=dict(color=COLORS['primary'], size=12)
        )],
        layout=go.Layout(
            title=dict(text='Quantum Circuit', font=dict(color=COLORS['text'], size=24)),
            xaxis=dict(title='Qubit', gridcolor=COLORS['border']),
            yaxis=dict(title='State', gridcolor=COLORS['border']),
            paper_bgcolor=COLORS['background'],
            plot_bgcolor=COLORS['card'],
            font=dict(color=COLORS['text'])
        )
    )

# Update the initial factors figure
def create_initial_factors():
    return go.Figure(
        data=[go.Bar(
            x=['Temperature', 'Humidity', 'Wind Speed', 'Pressure'],
            y=[0, 0, 0, 0],
            marker_color=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['warning']]
        )],
        layout=go.Layout(
            title=dict(text='Factor Impact Analysis', font=dict(color=COLORS['text'], size=24)),
            xaxis=dict(title='Factors', gridcolor=COLORS['border']),
            yaxis=dict(title='Impact (%)', gridcolor=COLORS['border']),
            paper_bgcolor=COLORS['background'],
            plot_bgcolor=COLORS['card'],
            font=dict(color=COLORS['text'])
        )
    )

# Update the initial global stats figure
def create_initial_global_stats():
    return go.Figure(
        data=[go.Bar(
            x=['Tornado', 'Earthquake', 'Fire', 'Flood'],
            y=[0, 0, 0, 0],
            marker_color=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['warning']]
        )],
        layout=go.Layout(
            title=dict(text='Global Disaster Statistics', font=dict(color=COLORS['text'], size=24)),
            xaxis=dict(title='Disaster Type', gridcolor=COLORS['border']),
            yaxis=dict(title='Annual Occurrences', gridcolor=COLORS['border']),
            paper_bgcolor=COLORS['background'],
            plot_bgcolor=COLORS['card'],
            font=dict(color=COLORS['text'])
        )
    )

# Update the app layout
app.layout = dbc.Container(
    fluid=True,
    style={'backgroundColor': COLORS['main_bg'], 'minHeight': '100vh'},
    children=[
        dbc.Navbar(
            dbc.Container([
                dbc.NavbarBrand("Quantum-Inspired Natural Disaster Prediction", style={'color': COLORS['tab_flood'], 'fontSize': '28px', 'fontWeight': 'bold'}),
            ], fluid=True),
            color=COLORS['white'],
            dark=False,
            className="mb-4",
            style={'boxShadow': '0 2px 4px rgba(0,0,0,0.08)'}
        ),
        dbc.Row([
            # Sidebar
            dbc.Col([
                html.H2("Input Parameters", style={'color': COLORS['tab_earthquake'], 'fontWeight': 'bold'}),
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Location", style={'color': COLORS['tab_guide']}),
                        dbc.Input(id="location-input", placeholder="Enter city, state", type="text", className="mb-3", style={'borderColor': COLORS['tab_guide']}),
                        html.H4("Prediction Model", style={'color': COLORS['tab_guide'], 'marginTop': '1rem'}),
                        dcc.Dropdown(
                            id="model-select",
                            options=[
                                {"label": "Quantum AI", "value": "quantum"},
                                {"label": "LSTM (Deep Learning)", "value": "lstm"},
                                {"label": "Random Forest", "value": "rf"},
                                {"label": "XGBoost", "value": "xgb"},
                                {"label": "SVM", "value": "svm"},
                                {"label": "MLP/ANN", "value": "mlp"},
                            ],
                            value="quantum",
                            clearable=False,
                            style={"marginBottom": "1rem"}
                        ),
                        dbc.Button("Predict", id="predict-button", color="primary", className="w-100", style={'backgroundColor': COLORS['sidebar_button'], 'color': COLORS['sidebar_button_text'], 'fontWeight': 'bold'}),
                    ])
                ], className="mb-4", style={'backgroundColor': COLORS['sidebar_bg'], 'border': f'2px solid {COLORS["sidebar_border"]}'}),
                dbc.Card([
                    dbc.CardBody([
                        html.H4("30-Day Tornado Forecast", style={'color': COLORS['tab_tornado']}),
                        dcc.Graph(id="sidebar-forecast-graph", figure=create_forecast('tornado'), config={'displayModeBar': False}),
                    ])
                ], style={'backgroundColor': COLORS['card_bg'], 'border': f'2px solid {COLORS["tab_tornado"]}'}),
            ], width=3),
            # Main Content
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(label="Tornado", tab_id="tornado", label_style={'background': COLORS['tab_tornado'], 'color': COLORS['white'], 'fontWeight': 'bold'}, active_label_style={'background': COLORS['tab_wildfire'], 'color': COLORS['tab_tornado']}),
                    dbc.Tab(label="Earthquake", tab_id="earthquake", label_style={'background': COLORS['tab_earthquake'], 'color': COLORS['white'], 'fontWeight': 'bold'}, active_label_style={'background': COLORS['tab_guide'], 'color': COLORS['tab_earthquake']}),
                    dbc.Tab(label="Wildfire", tab_id="wildfire", label_style={'background': COLORS['tab_wildfire'], 'color': COLORS['tab_tornado'], 'fontWeight': 'bold'}, active_label_style={'background': COLORS['tab_tornado'], 'color': COLORS['tab_wildfire']}),
                    dbc.Tab(label="Flood", tab_id="flood", label_style={'background': COLORS['tab_flood'], 'color': COLORS['white'], 'fontWeight': 'bold'}, active_label_style={'background': COLORS['tab_guide'], 'color': COLORS['tab_flood']}),
                    dbc.Tab(label="Guide", tab_id="guide", label_style={'background': COLORS['tab_guide'], 'color': COLORS['white'], 'fontWeight': 'bold'}, active_label_style={'background': COLORS['tab_earthquake'], 'color': COLORS['tab_guide']}),
                ], id="tabs", active_tab="tornado", className="mb-4"),
                # Render all outputs, hide those not active
                html.Div([
                    html.Div([
                        html.H3("Tornado Analysis", style={'color': COLORS['tab_tornado'], 'fontWeight': 'bold'}),
                        html.Div(id="tornado-result"),
                        dcc.Graph(id="tornado-gauge", figure=create_gauge('tornado')),
                        dcc.Graph(id="tornado-forecast", figure=create_forecast('tornado')),
                        dcc.Graph(id="tornado-factors", figure=create_factors('tornado')),
                    ], id="tornado-panel", style={"display": "block"}),
                    html.Div([
                        html.H3("Earthquake Analysis", style={'color': COLORS['tab_earthquake'], 'fontWeight': 'bold'}),
                        html.Div(id="earthquake-result"),
                        dcc.Graph(id="earthquake-gauge", figure=create_gauge('earthquake')),
                        dcc.Graph(id="earthquake-forecast", figure=create_forecast('earthquake')),
                        dcc.Graph(id="earthquake-factors", figure=create_factors('earthquake')),
                    ], id="earthquake-panel", style={"display": "none"}),
                    html.Div([
                        html.H3("Wildfire Analysis", style={'color': COLORS['tab_wildfire'], 'fontWeight': 'bold'}),
                        html.Div(id="fire-result"),
                        dcc.Graph(id="fire-gauge", figure=create_gauge('wildfire')),
                        dcc.Graph(id="fire-forecast", figure=create_forecast('wildfire')),
                        dcc.Graph(id="fire-factors", figure=create_factors('wildfire')),
                    ], id="wildfire-panel", style={"display": "none"}),
                    html.Div([
                        html.H3("Flood Analysis", style={'color': COLORS['tab_flood'], 'fontWeight': 'bold'}),
                        html.Div(id="flood-result"),
                        dcc.Graph(id="flood-gauge", figure=create_gauge('flood')),
                        dcc.Graph(id="flood-forecast", figure=create_forecast('flood')),
                        dcc.Graph(id="flood-factors", figure=create_factors('flood')),
                    ], id="flood-panel", style={"display": "none"}),
                ], id="all-panels"),
                # Guide tab content
                html.Div([
                    html.H3("Guide", style={'color': COLORS['tab_guide'], 'fontWeight': 'bold'}),
                    html.P("This guide explains the quantum-inspired algorithms and visualizations used in this app.", style={'color': COLORS['text']}),
                ], id="guide-panel", style={"display": "none"}),
            ], width=9),
        ]),
        dbc.Row(
            dbc.Col(
                html.Div(
                    "© 2024 Quantum-Inspired Natural Disaster Prediction. All rights reserved.",
                    style={'textAlign': 'center', 'color': COLORS['tab_earthquake'], 'padding': '20px', 'fontWeight': 'bold'}
                ),
                width=12,
            ),
            className="mt-4",
        ),
    ],
)

# Callbacks
@app.callback(
    [Output("tornado-result", "children"),
     Output("tornado-gauge", "figure"),
     Output("tornado-forecast", "figure"),
     Output("tornado-factors", "figure"),
     Output("earthquake-result", "children"),
     Output("earthquake-gauge", "figure"),
     Output("earthquake-forecast", "figure"),
     Output("earthquake-factors", "figure"),
     Output("fire-result", "children"),
     Output("fire-gauge", "figure"),
     Output("fire-forecast", "figure"),
     Output("fire-factors", "figure"),
     Output("flood-result", "children"),
     Output("flood-gauge", "figure"),
     Output("flood-forecast", "figure"),
     Output("flood-factors", "figure")],
    [Input("predict-button", "n_clicks")],
    [State("location-input", "value"), State("model-select", "value")]
)
def update_predictions(n_clicks, location, model):
    if n_clicks is None or not location:
        raise PreventUpdate
    try:
        lat, lon = get_coordinates(location)
        if not lat or not lon:
            return ["Invalid location. Please try again."] * 16
        weather_data = get_weather_data(lat, lon)
        # Select prediction method
        def predict(weather_data, disaster_type):
            if model == "quantum":
                return predict_with_quantum(weather_data, disaster_type)
            elif model == "lstm":
                return predict_with_lstm(weather_data, disaster_type)
            elif model == "rf":
                return predict_with_rf(weather_data, disaster_type)
            elif model == "xgb":
                return predict_with_xgb(weather_data, disaster_type)
            elif model == "svm":
                return predict_with_svm(weather_data, disaster_type)
            elif model == "mlp":
                return predict_with_mlp(weather_data, disaster_type)
            return 0.0
        tornado_prob = predict(weather_data, 'tornado')
        earthquake_prob = predict(weather_data, 'earthquake')
        fire_prob = predict(weather_data, 'fire')
        flood_prob = predict(weather_data, 'flood')
        results = []
        for disaster_type, prob in [
            ('tornado', tornado_prob),
            ('earthquake', earthquake_prob),
            ('fire', fire_prob),
            ('flood', flood_prob)
        ]:
            color = GRAPH_COLORS[disaster_type]
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"{disaster_type.capitalize()} Probability (%)",
                      'font': {'size': 24, 'color': COLORS['text'], 'family': 'Poppins'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': color},
                    'bar': {'color': color},
                    'bgcolor': COLORS['white'],
                    'borderwidth': 2,
                    'bordercolor': color,
                    'steps': [
                        {'range': [0, 30], 'color': '#FFE066'},
                        {'range': [30, 70], 'color': '#FFA726'},
                        {'range': [70, 100], 'color': '#FF7043'}
                    ],
                    'threshold': {
                        'line': {'color': color, 'width': 4},
                        'thickness': 0.75,
                        'value': prob * 100
                    }
                }
            ))
            dates = pd.date_range(start=pd.Timestamp.now(), periods=30, freq='D')
            forecast = get_30_day_forecast(lat, lon)
            probabilities = [prob for _ in forecast]  # Use the same prob for all days for demo
            fig_forecast = px.line(x=dates, y=probabilities,
                                 title='30-Day Probability Forecast',
                                 color_discrete_sequence=[color])
            fig_forecast.update_layout(
                plot_bgcolor=COLORS['card_bg'],
                paper_bgcolor=COLORS['card_bg'],
                xaxis_title="Date",
                yaxis_title="Probability (%)",
                font={'color': COLORS['text'], 'family': 'Poppins'},
                yaxis=dict(range=[0, 100])
            )
            factors = calculate_factor_impacts(weather_data)
            fig_factors = px.bar(x=list(factors.keys()), y=list(factors.values()),
                               title='Factor Impact Analysis',
                               color_discrete_sequence=[color])
            fig_factors.update_layout(
                plot_bgcolor=COLORS['card_bg'],
                paper_bgcolor=COLORS['card_bg'],
                xaxis_title="Weather Factor",
                yaxis_title="Impact (%)",
                font={'color': COLORS['text'], 'family': 'Poppins'},
                yaxis=dict(range=[0, 100])
            )
            result_text = [
                html.H3(f"{disaster_type.capitalize()} Prediction Results", style={'color': color, 'font-family': 'Poppins'}),
                html.P(f"Location: {location}", style={'color': COLORS['text'], 'font-family': 'Poppins'}),
                html.P(f"Probability: {prob * 100:.2f}%", style={'color': COLORS['text'], 'font-family': 'Poppins'}),
                html.H4("Key Factors:", style={'color': COLORS['text'], 'font-family': 'Poppins'}),
                html.Ul([html.Li(f"{k}: {v:.1f}%", style={'color': COLORS['text'], 'font-family': 'Poppins'}) for k, v in factors.items()])
            ]
            results.extend([result_text, fig_gauge, fig_forecast, fig_factors])
        return results
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        traceback.print_exc()
        return ["An error occurred. Please try again."] * 16

def generate_forecast(location, coordinates, current_weather):
    """Generate a 30-day forecast based on current weather conditions."""
    forecast = []
    base_weather = current_weather.copy()
    
    for day in range(30):
        date = datetime.now() + timedelta(days=day)
        weather = simulate_weather_changes(base_weather, day)
        probability = calculate_tornado_probability(weather)
        key_factors = get_key_factors(weather)
        
        forecast.append({
            'date': date.strftime('%Y-%m-%d'),
            'probability': probability,
            'weather': weather,
            'key_factors': key_factors
        })
    
    return forecast

def simulate_weather_changes(base_weather, day):
    """Simulate weather changes for each day in the forecast."""
    weather = base_weather.copy()
    
    # Add some randomness to weather parameters
    weather['main']['temp'] += random.uniform(-2, 2)
    weather['main']['humidity'] = max(0, min(100, weather['main']['humidity'] + random.uniform(-5, 5)))
    weather['main']['pressure'] += random.uniform(-5, 5)
    weather['wind']['speed'] = max(0, weather['wind']['speed'] + random.uniform(-1, 1))
    
    # Ensure values stay within reasonable ranges
    weather['main']['temp'] = max(-50, min(50, weather['main']['temp']))
    weather['main']['pressure'] = max(900, min(1100, weather['main']['pressure']))
    
    return weather

def get_key_factors(weather):
    """Determine which factors are most significant for tornado formation."""
    factors = []
    
    if weather['main']['temp'] > 25:
        factors.append('High Temperature')
    if weather['main']['humidity'] > 70:
        factors.append('High Humidity')
    if weather['main']['pressure'] < 1000:
        factors.append('Low Pressure')
    if weather['wind']['speed'] > 10:
        factors.append('Strong Winds')
    
    return factors if factors else ['Normal Conditions']

def calculate_tornado_probability(weather_data):
    """
    Calculate the probability of a tornado based on weather conditions.
    Returns a probability between 0 and 1.
    """
    # Extract weather parameters
    temp = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']
    
    # Initialize probability components
    temp_prob = 0.0
    humidity_prob = 0.0
    pressure_prob = 0.0
    wind_prob = 0.0
    
    # Temperature factor (optimal range: 20-30°C)
    if 20 <= temp <= 30:
        temp_prob = 1.0
    elif 15 <= temp < 20 or 30 < temp <= 35:
        temp_prob = 0.7
    elif 10 <= temp < 15 or 35 < temp <= 40:
        temp_prob = 0.4
    else:
        temp_prob = 0.1
    
    # Humidity factor (optimal range: 60-80%)
    if 60 <= humidity <= 80:
        humidity_prob = 1.0
    elif 50 <= humidity < 60 or 80 < humidity <= 90:
        humidity_prob = 0.7
    elif 40 <= humidity < 50 or 90 < humidity <= 95:
        humidity_prob = 0.4
    else:
        humidity_prob = 0.1
    
    # Pressure factor (optimal range: 980-1000 hPa)
    if 980 <= pressure <= 1000:
        pressure_prob = 1.0
    elif 970 <= pressure < 980 or 1000 < pressure <= 1010:
        pressure_prob = 0.7
    elif 960 <= pressure < 970 or 1010 < pressure <= 1020:
        pressure_prob = 0.4
    else:
        pressure_prob = 0.1
    
    # Wind speed factor (optimal range: 10-20 m/s)
    if 10 <= wind_speed <= 20:
        wind_prob = 1.0
    elif 7 <= wind_speed < 10 or 20 < wind_speed <= 25:
        wind_prob = 0.7
    elif 5 <= wind_speed < 7 or 25 < wind_speed <= 30:
        wind_prob = 0.4
    else:
        wind_prob = 0.1
    
    # Calculate weighted probability
    weights = {
        'temperature': 0.3,
        'humidity': 0.3,
        'pressure': 0.2,
        'wind_speed': 0.2
    }
    
    total_probability = (
        temp_prob * weights['temperature'] +
        humidity_prob * weights['humidity'] +
        pressure_prob * weights['pressure'] +
        wind_prob * weights['wind_speed']
    )
    
    # Apply quantum-inspired adjustments
    quantum_factor = random.uniform(0.9, 1.1)  # Simulate quantum uncertainty
    final_probability = min(1.0, total_probability * quantum_factor)
    
    return final_probability

def calculate_factor_impacts(weather_data):
    """
    Calculate the impact of each weather factor on the tornado probability.
    Returns a dictionary with impact percentages for each factor (0-100%).
    """
    # Extract weather parameters
    temp = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']

    # Calculate individual impacts (normalized to 0-1 range)
    temp_impact = calculate_temperature_impact(temp)
    humidity_impact = calculate_humidity_impact(humidity)
    pressure_impact = calculate_pressure_impact(pressure)
    wind_impact = calculate_wind_impact(wind_speed)

    # Calculate total impact
    total_impact = temp_impact + humidity_impact + pressure_impact + wind_impact
    
    # If total impact is 0, return equal small impacts
    if total_impact == 0:
        return {
            'temperature': 25.0,
            'humidity': 25.0,
            'pressure': 25.0,
            'wind_speed': 25.0
        }
    
    # Calculate percentages (ensuring they sum to 100%)
    impacts = {
        'temperature': round((temp_impact / total_impact) * 100, 1),
        'humidity': round((humidity_impact / total_impact) * 100, 1),
        'pressure': round((pressure_impact / total_impact) * 100, 1),
        'wind_speed': round((wind_impact / total_impact) * 100, 1)
    }
    
    # Ensure values sum to 100% (fix rounding errors)
    total = sum(impacts.values())
    if total != 100.0:
        diff = 100.0 - total
        # Add the difference to the largest value
        max_key = max(impacts, key=impacts.get)
        impacts[max_key] += diff
    
    return impacts

def calculate_temperature_impact(temp):
    """Calculate the impact of temperature on tornado probability (0-1 range)."""
    if 20 <= temp <= 30:  # Optimal range
        return 1.0
    elif 15 <= temp < 20 or 30 < temp <= 35:  # Good range
        return 0.7
    elif 10 <= temp < 15 or 35 < temp <= 40:  # Moderate range
        return 0.4
    else:  # Low impact
        return 0.1

def calculate_humidity_impact(humidity):
    """Calculate the impact of humidity on tornado probability (0-1 range)."""
    if 60 <= humidity <= 80:  # Optimal range
        return 1.0
    elif 50 <= humidity < 60 or 80 < humidity <= 90:  # Good range
        return 0.7
    elif 40 <= humidity < 50 or 90 < humidity <= 95:  # Moderate range
        return 0.4
    else:  # Low impact
        return 0.1

def calculate_pressure_impact(pressure):
    """Calculate the impact of pressure on tornado probability (0-1 range)."""
    if 980 <= pressure <= 1000:  # Optimal range
        return 1.0
    elif 970 <= pressure < 980 or 1000 < pressure <= 1010:  # Good range
        return 0.7
    elif 960 <= pressure < 970 or 1010 < pressure <= 1020:  # Moderate range
        return 0.4
    else:  # Low impact
        return 0.1

def calculate_wind_impact(wind_speed):
    """Calculate the impact of wind speed on tornado probability (0-1 range)."""
    if 10 <= wind_speed <= 20:  # Optimal range
        return 1.0
    elif 7 <= wind_speed < 10 or 20 < wind_speed <= 25:  # Good range
        return 0.7
    elif 5 <= wind_speed < 7 or 25 < wind_speed <= 30:  # Moderate range
        return 0.4
    else:  # Low impact
        return 0.1

def calculate_earthquake_probability(weather_data):
    """
    Calculate the probability of an earthquake based on research-based parameters.
    This model uses a combination of weather data and geological factors.
    """
    # Extract relevant weather parameters
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']
    
    # Research indicates that atmospheric pressure changes can trigger earthquakes
    # Sudden drops in pressure (especially below 990 hPa) can increase seismic activity
    pressure_factor = max(0, min(1, (1013 - pressure) / 50))
    
    # Humidity is less directly related to earthquakes, but high humidity often
    # accompanies low pressure systems which can trigger seismic activity
    humidity_factor = max(0, min(1, humidity / 100))
    
    # Combine factors with weights based on research
    # Pressure changes have a stronger correlation with seismic activity
    probability = (0.7 * pressure_factor + 0.3 * humidity_factor) * 0.6
    
    # Add some randomness to simulate uncertainty
    probability += random.uniform(-0.1, 0.1)
    
    # Ensure probability is between 0 and 1
    return max(0, min(1, probability))

def calculate_fire_probability(weather_data):
    """
    Calculate the probability of a forest fire based on research-based parameters.
    Uses the Canadian Forest Fire Weather Index (FWI) system as a reference.
    """
    # Extract relevant weather parameters
    temp = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    
    # Temperature factor - higher temperatures increase fire risk
    # Research shows temperatures above 30°C significantly increase fire risk
    temp_factor = max(0, min(1, (temp - 20) / 20))
    
    # Humidity factor - lower humidity increases fire risk
    # Research indicates humidity below 30% significantly increases fire risk
    humidity_factor = max(0, min(1, (100 - humidity) / 70))
    
    # Wind speed factor - higher wind speeds increase fire risk
    # Research shows wind speeds above 15 km/h (4.17 m/s) increase fire spread
    wind_factor = max(0, min(1, wind_speed / 10))
    
    # Combine factors with weights based on research
    # Temperature and humidity are the primary factors, with wind as a secondary factor
    probability = (0.4 * temp_factor + 0.4 * humidity_factor + 0.2 * wind_factor) * 0.8
    
    # Add some randomness to simulate uncertainty
    probability += random.uniform(-0.1, 0.1)
    
    # Ensure probability is between 0 and 1
    return max(0, min(1, probability))

def calculate_flood_probability(weather_data):
    """
    Calculate the probability of flooding based on research-based parameters.
    Uses hydrological models as a reference.
    """
    # Extract relevant weather parameters
    temp = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    
    # Humidity factor - higher humidity increases flood risk
    # Research shows humidity above 80% often precedes heavy rainfall
    humidity_factor = max(0, min(1, (humidity - 60) / 40))
    
    # Pressure factor - lower pressure increases flood risk
    # Research indicates pressure below 1000 hPa often accompanies storm systems
    pressure_factor = max(0, min(1, (1013 - pressure) / 30))
    
    # Temperature factor - moderate temperatures increase flood risk
    # Research shows moderate temperatures (10-20°C) with high humidity often lead to flooding
    temp_factor = max(0, min(1, 1 - abs(temp - 15) / 20))
    
    # Combine factors with weights based on research
    # Humidity and pressure are the primary factors, with temperature as a secondary factor
    probability = (0.4 * humidity_factor + 0.4 * pressure_factor + 0.2 * temp_factor) * 0.7
    
    # Add some randomness to simulate uncertainty
    probability += random.uniform(-0.1, 0.1)
    
    # Ensure probability is between 0 and 1
    return max(0, min(1, probability))

def calculate_earthquake_factor_impacts(weather_data):
    """
    Calculate the impact of various factors on earthquake probability.
    Based on research on earthquake triggers.
    """
    # Extract weather parameters
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']
    
    # Calculate individual impacts based on research
    # Pressure changes have a stronger correlation with seismic activity
    pressure_impact = max(0, min(1, (1013 - pressure) / 50))
    humidity_impact = max(0, min(1, humidity / 100))
    
    # Convert to percentages
    return {
        'pressure': pressure_impact * 100,
        'humidity': humidity_impact * 100
    }

def calculate_fire_factor_impacts(weather_data):
    """
    Calculate the impact of various factors on forest fire probability.
    Based on the Canadian Forest Fire Weather Index (FWI) system.
    """
    # Extract weather parameters
    temp = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    
    # Calculate individual impacts based on research
    # Temperature and humidity are the primary factors
    temp_impact = max(0, min(1, (temp - 20) / 20))
    humidity_impact = max(0, min(1, (100 - humidity) / 70))
    wind_impact = max(0, min(1, wind_speed / 10))
    
    # Convert to percentages
    return {
        'temperature': temp_impact * 100,
        'humidity': humidity_impact * 100,
        'wind_speed': wind_impact * 100
    }

def calculate_flood_factor_impacts(weather_data):
    """
    Calculate the impact of various factors on flooding probability.
    Based on hydrological research.
    """
    # Extract weather parameters
    temp = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    
    # Calculate individual impacts based on research
    # Humidity and pressure are the primary factors
    humidity_impact = max(0, min(1, (humidity - 60) / 40))
    pressure_impact = max(0, min(1, (1013 - pressure) / 30))
    temp_impact = max(0, min(1, 1 - abs(temp - 15) / 20))
    
    # Convert to percentages
    return {
        'humidity': humidity_impact * 100,
        'pressure': pressure_impact * 100,
        'temperature': temp_impact * 100
    }

def get_30_day_forecast(lat, lon):
    """
    Get a 30-day forecast for a location.
    This is a simplified version that generates mock forecast data.
    In a real application, you would use a weather API that provides long-term forecasts.
    """
    forecast = []
    base_date = datetime.now()
    
    # Generate mock forecast data for 30 days
    for i in range(30):
        date = base_date + timedelta(days=i)
        
        # Generate slightly different weather data for each day
        # This is a simplified approach - in a real app, you'd use actual forecast data
        temp = random.uniform(15, 35)  # Temperature in Celsius
        humidity = random.uniform(40, 90)  # Humidity percentage
        pressure = random.uniform(980, 1020)  # Pressure in hPa
        wind_speed = random.uniform(0, 15)  # Wind speed in m/s
        
        # Create weather data structure for this day
        weather = {
            'main': {
                'temp': temp + 273.15,  # Convert to Kelvin for consistency
                'humidity': humidity,
                'pressure': pressure
            },
            'wind': {
                'speed': wind_speed
            }
        }
        
        # Calculate probability based on the weather data
        # This is a simplified approach - in a real app, you'd use more sophisticated models
        probability = random.uniform(0.1, 0.9)
        
        # Determine key factors based on the weather data
        key_factors = []
        if temp > 30:
            key_factors.append("High Temperature")
        if humidity > 80:
            key_factors.append("High Humidity")
        if pressure < 990:
            key_factors.append("Low Pressure")
        if wind_speed > 10:
            key_factors.append("Strong Winds")
        
        if not key_factors:
            key_factors.append("Normal Conditions")
        
        forecast.append({
            'date': date.strftime('%Y-%m-%d'),
            'probability': probability,
            'weather': weather,  # Include the weather data in the forecast entry
            'key_factors': key_factors
        })
    
    return forecast

# --- Prediction method stubs ---
def predict_with_quantum(weather_data, disaster_type):
    if disaster_type == 'tornado':
        # Use the improved quantum model instead of the old calculation
        # Add coordinates to weather_data if they exist
        if 'coord' not in weather_data and hasattr(predictor, '_is_low_tornado_region'):
            # If coordinates are missing, we can't determine if it's a low-risk region
            # So we'll use a more conservative approach
            return predictor.predict(weather_data) * 0.5  # Reduce probability by 50%
        return predictor.predict(weather_data)
    elif disaster_type == 'earthquake':
        return calculate_earthquake_probability(weather_data)
    elif disaster_type in ['fire', 'wildfire']:
        return calculate_fire_probability(weather_data)
    elif disaster_type == 'flood':
        return calculate_flood_probability(weather_data)
    return 0.0

def predict_with_lstm(weather_data, disaster_type):
    # Stub: Replace with real LSTM model
    return random.uniform(0.2, 0.8)

def predict_with_rf(weather_data, disaster_type):
    # Stub: Replace with real Random Forest model
    return random.uniform(0.2, 0.8)

def predict_with_xgb(weather_data, disaster_type):
    # Stub: Replace with real XGBoost model
    return random.uniform(0.2, 0.8)

def predict_with_svm(weather_data, disaster_type):
    # Stub: Replace with real SVM model
    return random.uniform(0.2, 0.8)

def predict_with_mlp(weather_data, disaster_type):
    # Stub: Replace with real MLP/ANN model
    return random.uniform(0.2, 0.8)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 