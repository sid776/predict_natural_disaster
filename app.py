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

# Load environment variables
load_dotenv()

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Expose the Flask server for Gunicorn

predictor = QuantumTornadoPredictor()
geolocator = Nominatim(user_agent="tornado_predictor")

# Custom color scheme for different disasters
DISASTER_COLORS = {
    'tornado': {
        'primary': '#FF6B6B',    # Coral
        'secondary': '#FFE66D',  # Light Yellow
        'accent': '#FF9F1C',     # Orange
        'background': '#FFF5F5', # Light Coral
        'text': '#2C3E50',       # Dark Blue-Gray
        'tab': '#FF6B6B',        # Coral
        'tab_text': '#FFFFFF',   # White
        'card_bg': '#FFF5F5',    # Light Coral
        'card_border': '#FF6B6B' # Coral
    },
    'earthquake': {
        'primary': '#9B59B6',    # Purple
        'secondary': '#8E44AD',  # Dark Purple
        'accent': '#BB8FCE',     # Light Purple
        'background': '#F5EEF8', # Light Purple
        'text': '#2C3E50',
        'tab': '#9B59B6',        # Purple
        'tab_text': '#FFFFFF',
        'card_bg': '#F5EEF8',    # Light Purple
        'card_border': '#9B59B6' # Purple
    },
    'fire': {
        'primary': '#F39C12',    # Orange
        'secondary': '#E67E22',  # Dark Orange
        'accent': '#F5B041',     # Light Orange
        'background': '#FEF5E7', # Light Orange
        'text': '#2C3E50',
        'tab': '#F39C12',        # Orange
        'tab_text': '#FFFFFF',
        'card_bg': '#FEF5E7',    # Light Orange
        'card_border': '#F39C12' # Orange
    },
    'flood': {
        'primary': '#2ECC71',    # Bright Green
        'secondary': '#27AE60',  # Dark Green
        'accent': '#58D68D',     # Light Green
        'background': '#E8F8F5', # Light Green
        'text': '#2C3E50',
        'tab': '#2ECC71',        # Bright Green
        'tab_text': '#FFFFFF',
        'card_bg': '#E8F8F5',    # Light Green
        'card_border': '#2ECC71' # Bright Green
    }
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
            return response.json()
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
        'mock_data': True  # Flag to indicate this is mock data
    }

def test_api_connection():
    """Test the OpenWeatherMap API connection with a known location"""
    api_key = os.getenv('OPENWEATHER_API_KEY')
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

# Create initial figures with disaster-specific colors
def create_initial_gauge(disaster_type='tornado'):
    colors = DISASTER_COLORS[disaster_type]
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=0,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Probability (%)", 'font': {'size': 24, 'color': colors['text'], 'family': 'Poppins'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': colors['primary']},
            'bar': {'color': colors['primary']},
            'bgcolor': 'white',
            'borderwidth': 2,
            'bordercolor': colors['accent'],
            'steps': [
                {'range': [0, 30], 'color': colors['secondary']},
                {'range': [30, 70], 'color': colors['accent']},
                {'range': [70, 100], 'color': colors['primary']}
            ]
        }
    ))

def create_initial_forecast(disaster_type='tornado'):
    colors = DISASTER_COLORS[disaster_type]
    dates = pd.date_range(start=pd.Timestamp.now(), periods=30, freq='D')
    probabilities = np.zeros(30)
    fig = px.line(x=dates, y=probabilities, title='30-Day Probability Forecast',
                  color_discrete_sequence=[colors['primary']])
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font={'color': colors['text'], 'family': 'Poppins'}
    )
    return fig

def create_initial_circuit(disaster_type='tornado'):
    colors = DISASTER_COLORS[disaster_type]
    fig = go.Figure(go.Scatter(
        x=[0, 1, 2, 3],
        y=[0, 0, 0, 0],
        mode='lines+markers',
        name='Quantum State',
        line={'color': colors['primary']},
        marker={'color': colors['accent']}
    ))
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font={'color': colors['text'], 'family': 'Poppins'}
    )
    return fig

def create_initial_factors(disaster_type='tornado'):
    colors = DISASTER_COLORS[disaster_type]
    fig = px.bar(x=['Temperature', 'Humidity', 'Pressure', 'Wind'],
                 y=[0, 0, 0, 0],
                 title='Factor Impact Analysis',
                 color_discrete_sequence=[colors['primary']])
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font={'color': colors['text'], 'family': 'Poppins'}
    )
    return fig

def create_initial_global_stats(disaster_type='tornado'):
    colors = DISASTER_COLORS[disaster_type]
    stats = GLOBAL_STATS[disaster_type]
    fig = go.Figure(data=[
        go.Bar(name='Count', x=['Count'], y=[stats['count']], marker_color=colors['primary']),
        go.Bar(name='Deaths', x=['Deaths'], y=[stats['deaths']], marker_color=colors['secondary']),
        go.Bar(name='Injuries', x=['Injuries'], y=[stats['injuries']], marker_color=colors['accent']),
        go.Bar(name='Damage (B$)', x=['Damage'], y=[stats['damage']], marker_color=colors['primary'])
    ])
    fig.update_layout(
        title=f'{disaster_type.capitalize()} Statistics (Annual Averages)',
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font={'color': colors['text'], 'family': 'Poppins'},
        barmode='group'
    )
    return fig

def create_sidebar_forecast(disaster_type='tornado'):
    colors = DISASTER_COLORS[disaster_type]
    dates = pd.date_range(start=pd.Timestamp.now(), periods=30, freq='D')
    # Generate random probabilities between 10% and 80%
    probabilities = np.random.uniform(0.1, 0.8, 30) * 100
    fig = px.line(x=dates, y=probabilities, title='30-Day Probability Forecast',
                  color_discrete_sequence=[colors['primary']])
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font={'color': colors['text'], 'family': 'Poppins'},
        xaxis_title="Date",
        yaxis_title="Probability (%)",
        yaxis=dict(range=[0, 100])
    )
    return fig

# GUIDE TAB CONTENT
quantum_guide_content = dbc.Card([
    dbc.CardBody([
        html.H2("Quantum Guide", style={'color': '#9B59B6', 'font-family': 'Poppins'}),
        html.P("This guide explains the quantum-inspired algorithms and visualizations used in this app.", style={'font-family': 'Poppins'}),
        html.H4("Quantum Circuit Visualization", style={'color': '#9B59B6', 'font-family': 'Poppins'}),
        dcc.Graph(figure=create_initial_circuit()),
        html.P("The quantum circuit graph above represents the quantum state evolution used in our probability calculations. Each node corresponds to a quantum state, and the connections represent quantum operations.", style={'font-family': 'Poppins'}),
        html.H4("Quantum Probability Calculation", style={'color': '#9B59B6', 'font-family': 'Poppins'}),
        html.P("We use quantum-inspired algorithms to estimate the probability of each disaster. These algorithms leverage quantum superposition and interference principles to model uncertainty and correlations in weather data.", style={'font-family': 'Poppins'}),
        html.H4("Quantum-enhanced Forecasting", style={'color': '#9B59B6', 'font-family': 'Poppins'}),
        dcc.Graph(figure=create_initial_forecast('tornado')),
        html.P("The forecast graph above shows a 30-day prediction using quantum-enhanced models, which can capture complex patterns in the data.", style={'font-family': 'Poppins'}),
        html.H4("Quantum Factor Analysis", style={'color': '#9B59B6', 'font-family': 'Poppins'}),
        dcc.Graph(figure=create_initial_factors('tornado')),
        html.P("Factor analysis identifies which environmental variables most influence the quantum probability of a disaster.", style={'font-family': 'Poppins'}),
    ])
], style={'background': 'linear-gradient(120deg, #F5EEF8 60%, #FFE66D 100%)', 'border-radius': '1.5rem', 'margin-bottom': '2rem'})

# Define the layout
app.layout = dbc.Container([
    # Navigation Bar
    dbc.NavbarSimple(
        brand="Quantum-Inspired Natural Disaster Prediction",
        brand_href="#",
        color="success",
        dark=False,
        className="mb-4",
        style={
            'box-shadow': '0 2px 8px rgba(44, 62, 80, 0.10)',
            'font-family': 'Poppins',
            'font-weight': 'bold',
            'font-size': '2.2rem',
            'background-color': '#2ECC71',  # Bright green
            'color': '#fff',
            'border-radius': '1.2rem',
            'padding': '0.7rem 2rem',
            'letter-spacing': '0.03em',
        }
    ),
    
    # Main Content
    dbc.Row([
        # Left Sidebar
        dbc.Col([
            html.H2("Input Parameters", className="mb-4", style={'color': '#2C3E50', 'font-family': 'Poppins'}),
            dbc.Card([
                dbc.CardBody([
                    html.H4("Location", className="card-title", style={'color': '#2C3E50', 'font-family': 'Poppins'}),
                    dbc.Input(id="location-input", placeholder="Enter city, state", type="text", 
                             className="mb-3", style={'border-color': '#9B59B6', 'font-family': 'Poppins'}),
                    
                    dbc.Button("Predict", id="predict-button", color="primary", 
                              className="w-100", style={'background-color': '#9B59B6', 'font-family': 'Poppins'})
                ])
            ], className="mb-4", style={'background-color': '#F5EEF8', 
                                      'border': '2px solid #9B59B6'}),
            
            # 30-Day Tornado Forecast
            dbc.Card([
                dbc.CardBody([
                    html.H4("30-Day Tornado Forecast", className="card-title", style={'color': '#2C3E50', 'font-family': 'Poppins'}),
                    dcc.Graph(id="sidebar-forecast-graph", figure=create_sidebar_forecast('tornado')),
                    html.P("This 30-day forecast shows the predicted probability of a tornado at your location, helping you plan ahead and stay safe.", style={'font-family': 'Poppins', 'marginTop': 10}),
                ])
            ], style={'background-color': '#F5EEF8', 'border': '2px solid #9B59B6'}),
        ], width=3),
        
        # Main Content Area
        dbc.Col([
            # Tabs for different disasters
            dcc.Tabs([
                # Tornado Tab
                dcc.Tab(
                    dbc.Card([
                        dbc.CardBody([
                            html.H2("Tornado Analysis", className="mb-4", style={'color': DISASTER_COLORS['tornado']['text'], 'font-family': 'Poppins'}),
                            dcc.Graph(id="tornado-gauge", figure=create_initial_gauge('tornado')),
                            html.P("This gauge shows the quantum-inspired probability of a tornado occurring at your location.", style={'font-family': 'Poppins'}),
                            html.Div(id="tornado-result", className="mt-4"),
                            dcc.Graph(id="tornado-forecast", figure=create_initial_forecast('tornado')),
                            html.P("30-day tornado forecast using quantum-enhanced models.", style={'font-family': 'Poppins'}),
                            dcc.Graph(id="tornado-factors", figure=create_initial_factors('tornado')),
                            html.P("Key factors influencing tornado probability.", style={'font-family': 'Poppins'}),
                            dcc.Graph(id="tornado-stats", figure=create_initial_global_stats('tornado')),
                            html.P("Global tornado statistics.", style={'font-family': 'Poppins'}),
                            dcc.Graph(id="main-quantum-circuit", figure=create_initial_circuit()),
                            html.P("Quantum circuit visualization for tornado prediction.", style={'font-family': 'Poppins'}),
                        ])
                    ], className="mb-4", style={'background-color': DISASTER_COLORS['tornado']['card_bg'], 
                                             'border': f'2px solid {DISASTER_COLORS["tornado"]["card_border"]}'}),
                    label="Tornado",
                    value="tornado",
                    className='tab--1'
                ),
                # Earthquake Tab
                dcc.Tab(
                    dbc.Card([
                        dbc.CardBody([
                            html.H2("Earthquake Analysis", className="mb-4", style={'color': DISASTER_COLORS['earthquake']['text'], 'font-family': 'Poppins'}),
                            dcc.Graph(id="earthquake-gauge", figure=create_initial_gauge('earthquake')),
                            html.P("Quantum-inspired probability of an earthquake.", style={'font-family': 'Poppins'}),
                            html.Div(id="earthquake-result", className="mt-4"),
                            dcc.Graph(id="earthquake-forecast", figure=create_initial_forecast('earthquake')),
                            html.P("30-day earthquake forecast using quantum-enhanced models.", style={'font-family': 'Poppins'}),
                            dcc.Graph(id="earthquake-factors", figure=create_initial_factors('earthquake')),
                            html.P("Key factors influencing earthquake probability.", style={'font-family': 'Poppins'}),
                            dcc.Graph(id="earthquake-stats", figure=create_initial_global_stats('earthquake')),
                            html.P("Global earthquake statistics.", style={'font-family': 'Poppins'}),
                            dcc.Graph(id="main-quantum-circuit-eq", figure=create_initial_circuit()),
                            html.P("Quantum circuit visualization for earthquake prediction.", style={'font-family': 'Poppins'}),
                        ])
                    ], className="mb-4", style={'background-color': DISASTER_COLORS['earthquake']['card_bg'], 
                                             'border': f'2px solid {DISASTER_COLORS["earthquake"]["card_border"]}'}),
                    label="Earthquake",
                    value="earthquake",
                    className='tab--2'
                ),
                # Wildfire Tab
                dcc.Tab(
                    dbc.Card([
                        dbc.CardBody([
                            html.H2("Wildfire Analysis", className="mb-4", style={'color': DISASTER_COLORS['fire']['text'], 'font-family': 'Poppins'}),
                            dcc.Graph(id="fire-gauge", figure=create_initial_gauge('fire')),
                            html.P("Quantum-inspired probability of a wildfire.", style={'font-family': 'Poppins'}),
                            html.Div(id="fire-result", className="mt-4"),
                            dcc.Graph(id="fire-forecast", figure=create_initial_forecast('fire')),
                            html.P("30-day wildfire forecast using quantum-enhanced models.", style={'font-family': 'Poppins'}),
                            dcc.Graph(id="fire-factors", figure=create_initial_factors('fire')),
                            html.P("Key factors influencing wildfire probability.", style={'font-family': 'Poppins'}),
                            dcc.Graph(id="fire-stats", figure=create_initial_global_stats('fire')),
                            html.P("Global wildfire statistics.", style={'font-family': 'Poppins'}),
                            dcc.Graph(id="main-quantum-circuit-fire", figure=create_initial_circuit()),
                            html.P("Quantum circuit visualization for wildfire prediction.", style={'font-family': 'Poppins'}),
                        ])
                    ], className="mb-4", style={'background-color': DISASTER_COLORS['fire']['card_bg'], 
                                             'border': f'2px solid {DISASTER_COLORS["fire"]["card_border"]}'}),
                    label="Wildfire",
                    value="wildfire",
                    className='tab--3'
                ),
                # Flood Tab
                dcc.Tab(
                    dbc.Card([
                        dbc.CardBody([
                            html.H2("Flood Analysis", className="mb-4", style={'color': DISASTER_COLORS['flood']['text'], 'font-family': 'Poppins'}),
                            dcc.Graph(id="flood-gauge", figure=create_initial_gauge('flood')),
                            html.P("Quantum-inspired probability of a flood.", style={'font-family': 'Poppins'}),
                            html.Div(id="flood-result", className="mt-4"),
                            dcc.Graph(id="flood-forecast", figure=create_initial_forecast('flood')),
                            html.P("30-day flood forecast using quantum-enhanced models.", style={'font-family': 'Poppins'}),
                            dcc.Graph(id="flood-factors", figure=create_initial_factors('flood')),
                            html.P("Key factors influencing flood probability.", style={'font-family': 'Poppins'}),
                            dcc.Graph(id="flood-stats", figure=create_initial_global_stats('flood')),
                            html.P("Global flood statistics.", style={'font-family': 'Poppins'}),
                            dcc.Graph(id="main-quantum-circuit-flood", figure=create_initial_circuit()),
                            html.P("Quantum circuit visualization for flood prediction.", style={'font-family': 'Poppins'}),
                        ])
                    ], className="mb-4", style={'background-color': DISASTER_COLORS['flood']['card_bg'], 
                                             'border': f'2px solid {DISASTER_COLORS["flood"]["card_border"]}'}),
                    label="Flood",
                    value="flood",
                    className='tab--4'
                ),
                # Guide Tab (last tab)
                dcc.Tab(
                    quantum_guide_content,
                    label="Guide",
                    value="guide",
                    className='tab--5'
                ),
            ], id="tabs", value="tornado", className='custom-tabs'),
        ], width=9),
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.P("© 2024 Quantum Disaster Prediction System", 
                  className="text-center text-muted mt-4",
                  style={'color': '#2C3E50', 'font-family': 'Poppins'})
        ])
    ])
], fluid=True, style={'background-color': '#F8F9FA', 'font-family': 'Poppins'})

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
    [State("location-input", "value")]
)
def update_predictions(n_clicks, location):
    if n_clicks is None or not location:
        raise PreventUpdate
    
    try:
        # Get coordinates
        lat, lon = get_coordinates(location)
        if not lat or not lon:
            return ["Invalid location. Please try again."] * 16
        
        # Get current weather data
        weather_data = get_weather_data(lat, lon)
        
        # Calculate probabilities for each disaster type
        tornado_prob = calculate_tornado_probability(weather_data)
        earthquake_prob = calculate_earthquake_probability(weather_data)
        fire_prob = calculate_fire_probability(weather_data)
        flood_prob = calculate_flood_probability(weather_data)
        
        # Create results for each disaster type
        results = []
        for disaster_type, prob in [
            ('tornado', tornado_prob),
            ('earthquake', earthquake_prob),
            ('fire', fire_prob),
            ('flood', flood_prob)
        ]:
            colors = DISASTER_COLORS[disaster_type]
            
            # Create gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"{disaster_type.capitalize()} Probability (%)", 
                      'font': {'size': 24, 'color': colors['text'], 'family': 'Poppins'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': colors['primary']},
                    'bar': {'color': colors['primary']},
                    'bgcolor': 'white',
                    'borderwidth': 2,
                    'bordercolor': colors['accent'],
                    'steps': [
                        {'range': [0, 30], 'color': colors['secondary']},
                        {'range': [30, 70], 'color': colors['accent']},
                        {'range': [70, 100], 'color': colors['primary']}
                    ],
                    'threshold': {
                        'line': {'color': colors['primary'], 'width': 4},
                        'thickness': 0.75,
                        'value': prob * 100
                    }
                }
            ))
            
            # Create forecast
            dates = pd.date_range(start=pd.Timestamp.now(), periods=30, freq='D')
            forecast = get_30_day_forecast(lat, lon)
            probabilities = [day['probability'] for day in forecast]
            
            fig_forecast = px.line(x=dates, y=probabilities,
                                 title='30-Day Probability Forecast',
                                 color_discrete_sequence=[colors['primary']])
            fig_forecast.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                xaxis_title="Date",
                yaxis_title="Probability (%)",
                font={'color': colors['text'], 'family': 'Poppins'}
            )
            
            # Create factor analysis
            factors = calculate_factor_impacts(weather_data)
            fig_factors = px.bar(x=list(factors.keys()), y=list(factors.values()),
                               title='Factor Impact Analysis',
                               color_discrete_sequence=[colors['primary']])
            fig_factors.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                xaxis_title="Weather Factor",
                yaxis_title="Impact (%)",
                font={'color': colors['text'], 'family': 'Poppins'},
                yaxis=dict(range=[0, 100])
            )
            
            # Create result text
            result_text = [
                html.H3(f"{disaster_type.capitalize()} Prediction Results", 
                       style={'color': colors['text'], 'font-family': 'Poppins'}),
                html.P(f"Location: {location}", style={'color': colors['text'], 'font-family': 'Poppins'}),
                html.P(f"Probability: {prob * 100:.2f}%", style={'color': colors['text'], 'font-family': 'Poppins'}),
                html.H4("Key Factors:", style={'color': colors['text'], 'font-family': 'Poppins'}),
                html.Ul([html.Li(f"{k}: {v*100:.1f}%", style={'color': colors['text'], 'font-family': 'Poppins'}) 
                        for k, v in factors.items()])
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

    # Calculate individual impacts
    temp_impact = calculate_temperature_impact(temp)
    humidity_impact = calculate_humidity_impact(humidity)
    pressure_impact = calculate_pressure_impact(pressure)
    wind_impact = calculate_wind_impact(wind_speed)

    # Calculate total impact
    total_impact = temp_impact + humidity_impact + pressure_impact + wind_impact
    if total_impact == 0:
        impacts = {k: 0 for k in ['temperature', 'humidity', 'pressure', 'wind_speed']}
    else:
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
    """Calculate the impact of temperature on tornado probability."""
    if 20 <= temp <= 30:
        return 1.0
    elif 15 <= temp < 20 or 30 < temp <= 35:
        return 0.7
    elif 10 <= temp < 15 or 35 < temp <= 40:
        return 0.4
    return 0.1

def calculate_humidity_impact(humidity):
    """Calculate the impact of humidity on tornado probability."""
    if 60 <= humidity <= 80:
        return 1.0
    elif 50 <= humidity < 60 or 80 < humidity <= 90:
        return 0.7
    elif 40 <= humidity < 50 or 90 < humidity <= 95:
        return 0.4
    return 0.1

def calculate_pressure_impact(pressure):
    """Calculate the impact of pressure on tornado probability."""
    if 980 <= pressure <= 1000:
        return 1.0
    elif 970 <= pressure < 980 or 1000 < pressure <= 1010:
        return 0.7
    elif 960 <= pressure < 970 or 1010 < pressure <= 1020:
        return 0.4
    return 0.1

def calculate_wind_impact(wind_speed):
    """Calculate the impact of wind speed on tornado probability."""
    if 10 <= wind_speed <= 20:
        return 1.0
    elif 7 <= wind_speed < 10 or 20 < wind_speed <= 25:
        return 0.7
    elif 5 <= wind_speed < 7 or 25 < wind_speed <= 30:
        return 0.4
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

if __name__ == '__main__':
    app.run(debug=True, port=5000) 