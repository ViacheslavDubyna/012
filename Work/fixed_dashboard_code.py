import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import requests
from datetime import datetime, timedelta
from collections import Counter
import uuid

# Ініціалізація додатку Dash
app = dash.Dash(__name__)

# Стилі
colors = {
    'visualization': '#FFF9C4',  # світло-жовтий
    'threats': '#FFCCBC',        # світло-оранжевий
    'resources': '#FFCDD2',      # світло-червоний
    'forecasting': '#F8BBD0',    # світло-рожевий
    'background': '#F5F5F5',     # світло-сірий фон
    'text': '#333333'            # темно-сірий текст
}

# Завантаження GeoJSON
# Використовуємо правильне джерело GeoJSON для України
ukraine_geojson_url = "https://raw.githubusercontent.com/vsapsai/ukraine_map_data/master/ukraine_geojson.json"
try:
    response = requests.get(ukraine_geojson_url)
    ukraine_geojson = response.json()
except Exception as e:
    print(f"Помилка при завантаженні GeoJSON: {e}")
    # Створюємо спрощений GeoJSON для України як запасний варіант
    ukraine_geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"shapeName": region},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[lon-1, lat-1], [lon+1, lat-1], [lon+1, lat+1], [lon-1, lat+1], [lon-1, lat-1]]]
            }
        } for region, (lon, lat) in {
            'Kyiv': (30.5, 50.4),
            'Lviv': (24.0, 49.8),
            'Kharkiv': (36.2, 49.9),
            'Odesa': (30.7, 46.5),
            'Dnipropetrovsk': (35.0, 48.5),
            'Donetsk': (37.8, 48.0),
            'Luhansk': (39.3, 48.9),
            'Zaporizhia': (35.4, 47.8),
            'Kherson': (33.5, 46.6),
            'Mykolaiv': (32.0, 47.0),
            'Vinnytsia': (28.5, 49.2),
            'Poltava': (34.6, 49.6),
            'Sumy': (34.8, 51.0),
            'Chernihiv': (31.3, 51.5),
            'Cherkasy': (32.0, 49.4),
            'Khmelnytskyi': (27.0, 49.4),
            'Rivne': (26.2, 50.6),
            'Volyn': (25.0, 51.0),
            'Ivano-Frankivsk': (24.7, 48.9),
            'Ternopil': (25.6, 49.6),
            'Zakarpattia': (22.3, 48.6),
            'Chernivtsi': (25.9, 48.3),
            'Zhytomyr': (28.7, 50.3),
            'Kirovohrad': (32.3, 48.5)
        }.items()]
    }

# Словник для відповідності назв регіонів
region_name_mapping = {
    'Київська': 'Kyiv',
    'Львівська': 'Lviv',
    'Харківська': 'Kharkiv',
    'Одеська': 'Odesa',
    'Дніпропетровська': 'Dnipropetrovsk',
    'Донецька': 'Donetsk',
    'Луганська': 'Luhansk',
    'Запорізька': 'Zaporizhia',
    'Херсонська': 'Kherson',
    'Миколаївська': 'Mykolaiv',
    'Вінницька': 'Vinnytsia',
    'Полтавська': 'Poltava',
    'Сумська': 'Sumy',
    'Чернігівська': 'Chernihiv',
    'Черкаська': 'Cherkasy',
    'Хмельницька': 'Khmelnytskyi',
    'Рівненська': 'Rivne',
    'Волинська': 'Volyn',
    'Івано-Франківська': 'Ivano-Frankivsk',
    'Тернопільська': 'Ternopil',
    'Закарпатська': 'Zakarpattia',
    'Чернівецька': 'Chernivtsi',
    'Житомирська': 'Zhytomyr',
    'Кіровоградська': 'Kirovohrad'
}

# Генерація тестових даних
def generate_test_data():
    regions = list(region_name_mapping.keys())
    security_levels = np.random.randint(10, 100, size=len(regions))
    high_risk_regions = ['Харківська', 'Донецька', 'Луганська', 'Запорізька', 'Херсонська', 'Сумська', 'Чернігівська']
    for region in high_risk_regions:
        if region in regions:
            idx = regions.index(region)
            security_levels[idx] = np.random.randint(10, 40)
    visualization_data = pd.DataFrame({'Область': regions, 'Рівень безпеки': security_levels})
    visualization_data['Region English'] = visualization_data['Область'].map(region_name_mapping)

    threat_types = [
        'Ракетні удари', 'Артилерійські обстріли', 'Безпілотники', 'Кібератаки',
        'Диверсійні групи', 'Інформаційні операції', 'Інфраструктурні атаки'
    ]
    risk_levels = np.random.randint(3, 10, size=len(threat_types))
    threat_categories = [
        'Військова загроза', 'Військова загроза', 'Військова загроза', 'Кібер загроза',
        'Фізична загроза', 'Інформаційна загроза', 'Критична інфраструктура'
    ]
    threats_data = pd.DataFrame({
        'Тип загрози': threat_types, 
        'Рівень ризику': risk_levels,
        'Категорія': threat_categories
    })

    resources = [
        'Військове обладнання', 'Гуманітарна допомога', 'Енергетичні ресурси',
        'Медичні засоби', 'Системи зв\'язку', 'Транспорт', 'Продовольство'
    ]
    usage = np.random.randint(50, 100, size=len(resources))
    resources_data = pd.DataFrame({'Ресурс': resources, 'Використання (%)': usage})

    dates = pd.date_range(start='2025-01-01', periods=30)
    forecasted = np.cumsum(np.random.normal(0, 2, size=len(dates))) + 50
    actual = forecasted[:20] + np.random.normal(0, 3, size=20)
    forecast_data = pd.DataFrame({
        'Дата': dates,
        'Прогноз': forecasted,
        'Фактично': np.append(actual, [None] * 10)
    })

    return visualization_data, threats_data, resources_data, forecast_data

viz_data, threats_data, resources_data, forecast_data = generate_test_data()

# Отримання даних ACLED
def fetch_acled_data():
    api_key = "your_api_key"  # Замініть на ваш ключ API
    email = "your_email"      # Замініть на вашу електронну пошту
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # Для карти (усі події)
    url = f"https://api.acleddata.com/acled/read?key={api_key}&email={email}&country=Ukraine&event_date={thirty_days_ago}&event_date_where=>&fields=admin1"
    try:
        response = requests.get(url)
        data = response.json()
        events = data.get('data', [])
        region_counts = Counter([event['admin1'] for event in events])
    except Exception as e:
        print(f"Помилка при отриманні даних ACLED: {e}")
        region_counts = Counter()
    
    # Для аналізу загроз
    try:
        url_threats = f"https://api.acleddata.com/acled/read?key={api_key}&email={email}&country=Ukraine&event_type=Explosions/Remote violence&event_date={thirty_days_ago}&event_date_where=>&fields=sub_event_type"
        response_threats = requests.get(url_threats)
        data_threats = response_threats.json()
        threat_events = data_threats.get('data', [])
        sub_event_counts = Counter([event['sub_event_type'] for event in threat_events])
    except Exception as e:
        print(f"Помилка при отриманні даних загроз ACLED: {e}")
        sub_event_counts = Counter()
    
    return region_counts, sub_event_counts

region_counts, sub_event_counts = fetch_acled_data()

# Оновлення даних візуалізації
max_count = max(region_counts.values()) if region_counts else 1
for i, row in viz_data.iterrows():
    oblast = row['Область']
    english_name = region_name_mapping.get(oblast)
    count = region_counts.get(english_name, 0)
    security_level = 100 - (count / max_count * 90) if max_count > 0 else 100
    viz_data.at[i, 'Рівень безпеки'] = round(security_level, 1)

# Оновлення даних загроз
threat_mapping = {
    'Shelling/artillery/missile attack': ['Ракетні удари', 'Артилерійські обстріли'],
    'Air/drone strike': ['Безпілотники']
}
threat_risk = {threat: 0 for threat in threats_data['Тип загрози']}
for sub_event, count in sub_event_counts.items():
    if sub_event in threat_mapping:
        for threat in threat_mapping[sub_event]:
            threat_risk[threat] = count
max_threat_count = max(threat_risk.values()) if any(threat_risk.values()) else 0
for i, row in threats_data.iterrows():
    threat = row['Тип загрози']
    if threat in threat_risk:
        if max_threat_count > 0:
            scaled_risk = (threat_risk[threat] / max_threat_count) * 10
        else:
            scaled_risk = 0
        threats_data.at[i, 'Рівень ризику'] = round(scaled_risk, 1)

# Створення графіків
def create_ukraine_map():
    # Перевіряємо, чи маємо правильний GeoJSON
    if 'features' in ukraine_geojson and len(ukraine_geojson['features']) > 0:
        # Використовуємо choropleth з GeoJSON
        fig = px.choropleth(
            viz_data,
            geojson=ukraine_geojson,
            locations='Region English',
            featureidkey='properties.shapeName',
            color='Рівень безпеки',
            color_continuous_scale='RdYlGn',
            range_color=(10, 100),
            title='Оперативна ситуація в Україні'
        )
        fig.update_geos(fitbounds="locations", visible=False)
    else:
        # Запасний варіант - використовуємо scatter map
        fig = go.Figure()
        
        # Додаємо контур для представлення України
        ukraine_lons = [22, 40, 40, 22, 22]  # Координати longitude
        ukraine_lats = [44, 44, 52, 52, 44]  # Координати latitude
        
        fig.add_trace(go.Scatter(
            x=ukraine_lons,
            y=ukraine_lats,
            mode='lines',
            line=dict(width=2, color='blue'),
            name='Контур України',
            showlegend=False
        ))
        
        # Додаємо точки для кожної області
        # Приблизні координати для областей (спрощено)
        region_coords = {
            'Київська': (30.5, 50.4),
            'Львівська': (24.0, 49.8),
            'Харківська': (36.2, 49.9),
            'Одеська': (30.7, 46.5),
            'Дніпропетровська': (35.0, 48.5),
            'Донецька': (37.8, 48.0),
            'Луганська': (39.3, 48.9),
            'Запорізька': (35.4, 47.8),
            'Херсонська': (33.5, 46.6),
            'Миколаївська': (32.0, 47.0),
            'Вінницька': (28.5, 49.2),
            'Полтавська': (34.6, 49.6),
            'Сумська': (34.8, 51.0),
            'Чернігівська': (31.3, 51.5),
            'Черкаська': (32.0, 49.4),
            'Хмельницька': (27.0, 49.4),
            'Рівненська': (26.2, 50.6),
            'Волинська': (25.0, 51.0),
            'Івано-Франківська': (24.7, 48.9),
            'Тернопільська': (25.6, 49.6),
            'Закарпатська': (22.3, 48.6),
            'Чернівецька': (25.9, 48.3),
            'Житомирська': (28.7, 50.3),
            'Кіровоградська': (32.3, 48.5)
        }
        
        # Додаємо маркери для областей з кольором залежно від рівня безпеки
        for i, row in viz_data.iterrows():
            region = row['Область']
            security = row['Рівень безпеки']
            
            if region in region_coords:
                lon, lat = region_coords[region]
                
                # Визначаємо колір (червоний для небезпечних, жовтий для середніх, зелений для безпечних)
                if security < 40:
                    marker_color = 'red'
                elif security < 70:
                    marker_color = 'orange'
                else:
                    marker_color = 'green'
                    
                fig.add_trace(go.Scatter(
                    x=[lon],
                    y=[lat],
                    mode='markers+text',
                    marker=dict(size=15, color=marker_color),
                    text=region,
                    textposition="top center",
                    name=f"{region} ({security})",
                    showlegend=False
                ))
    
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

def create_threat_analysis():
    fig = px.bar(
        threats_data,
        x='Тип загрози',
        y='Рівень ризику',
        color='Категорія',
        color_discrete_map={
            'Військова загроза': '#FF5733',
            'Кібер загроза': '#33A1FF',
            'Фізична загроза': '#FF33FC',
            'Інформаційна загроза': '#33FF57',
            'Критична інфраструктура': '#FFD433'
        },
        title='Аналіз загроз (Російсько-Українська війна)'
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(tickangle=45),
        yaxis=dict(title='Рівень загрози (1-10)')
    )
    return fig

def create_resource_management():
    fig = go.Figure()
    for i, row in resources_data.iterrows():
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=row['Використання (%)'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': row['Ресурс']},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkred" if row['Використання (%)'] > 80 else "orange" if row['Використання (%)'] > 60 else "green"},
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
    fig.update_layout(
        grid={'rows': 3, 'columns': 3, 'pattern': "independent"},
        title='Використання ресурсів',
        margin=dict(l=0, r=0, t=30, b=0)
    )
    return fig

def create_forecast_chart():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecast_data['Дата'],
        y=forecast_data['Фактично'],
        mode='markers+lines',
        name='Фактичні дані',
        line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=forecast_data['Дата'],
        y=forecast_data['Прогноз'],
        mode='lines',
        name='Прогноз',
        line=dict(color='red', dash='dash')
    ))
    fig.update_layout(
        title='Прогнозування потреб у ресурсах',
        xaxis_title='Дата',
        yaxis_title='Значення',
        margin=dict(l=0, r=0, t=30, b=0)
    )
    return fig

# Макет додатку
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'}, children=[
    html.H1(
        'Компоненти панелі управління',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'fontFamily': 'Arial',
            'marginBottom': '30px'
        }
    ),
    
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'}, children=[
        html.Div(
            style={
                'backgroundColor': colors['visualization'],
                'padding': '15px',
                'borderRadius': '15px 15px 50px 50px',
                'width': '22%',
                'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',
                'marginBottom': '20px'
            },
            children=[
                html.H3('Візуалізація', style={'textAlign': 'center', 'color': '#B58500'}),
                html.P('Відображає оперативну ситуацію в реальному часі.', style={'textAlign': 'center'}),
                dcc.Graph(
                    id='ukraine-map',
                    figure=create_ukraine_map(),
                    style={'height': '200px'}
                ),
                html.Div(id='live-update-text'),
                dcc.Interval(
                    id='interval-component',
                    interval=60*1000,  # оновлення кожну хвилину
                    n_intervals=0
                )
            ]
        ),
        
        html.Div(
            style={
                'backgroundColor': colors['threats'],
                'padding': '15px',
                'borderRadius': '15px 15px 50px 50px',
                'width': '22%',
                'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',
                'marginBottom': '20px'
            },
            children=[
                html.H3('Аналіз загроз', style={'textAlign': 'center', 'color': '#B54300'}),
                html.P('Оцінює потенційні ризики та загрози.', style={'textAlign': 'center'}),
                dcc.Graph(
                    id='threat-analysis',
                    figure=create_threat_analysis(),
                    style={'height': '200px'}
                )
            ]
        ),
        
        html.Div(
            style={
                'backgroundColor': colors['resources'],
                'padding': '15px',
                'borderRadius': '15px 15px 50px 50px',
                'width': '22%',
                'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',
                'marginBottom': '20px'
            },
            children=[
                html.H3('Управління ресурсами', style={'textAlign': 'center', 'color': '#B50000'}),
                html.P('Контролює розподіл та використання ресурсів.', style={'textAlign': 'center'}),
                dcc.Graph(
                    id='resource-management',
                    figure=create_resource_management(),
                    style={'height': '200px'}
                ),
                html.Div(
                    id='resource-alerts',
                    style={'marginTop': '10px', 'color': 'red', 'textAlign': 'center'}
                )
            ]
        ),
        
        html.Div(
            style={
                'backgroundColor': colors['forecasting'],
                'padding': '15px',
                'borderRadius': '15px 15px 50px 50px',
                'width': '22%',
                'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',
                'marginBottom': '20px'
            },
            children=[
                html.H3('Інструменти прогнозування', style={'textAlign': 'center', 'color': '#B5006A'}),
                html.P('Надає інструменти для прогнозного аналізу.', style={'textAlign': 'center'}),
                dcc.Graph(
                    id='forecast-chart',
                    figure=create_forecast_chart(),
                    style={'height': '200px'}
                )
            ]
        )
    ]),
    
    html.Div(style={'marginTop': '30px'}, children=[
        html.H2('Деталізована інформація', style={'textAlign': 'center', 'color': colors['text']}),
        dcc.Tabs([
            dcc.Tab(label='Карта України', children=[
                html.Div(style={'padding': '20px'}, children=[
                    dcc.Graph(figure=create_ukraine_map())
                ])
            ]),
            dcc.Tab(label='Аналіз загроз війни', children=[
                html.Div(style={'padding': '20px'}, children=[
                    dcc.Graph(figure=create_threat_analysis()),
                    html.Div([
                        html.H4('Контекст Російсько-Української війни'),
                        html.P('Дашборд відображає актуальні дані по різним типам загроз, пов\'язаних з воєнними діями. '
                               'Моніторинг включає як військові загрози (обстріли, атаки), так і супутні ризики для '
                               'цивільної інфраструктури та інформаційної безпеки.')
                    ])
                ])
            ]),
            dcc.Tab(label='Управління ресурсами', children=[
                html.Div(style={'padding': '20px'}, children=[
                    dcc.Graph(figure=create_resource_management())
                ])
            ]),
            dcc.Tab(label='Прогнозування', children=[
                html.Div(style={'padding': '20px'}, children=[
                    dcc.Graph(figure=create_forecast_chart())
                ])
            ])
        ])
    ])
])

# Оновлення інформації в реальному часі
@app.callback(
    Output('live-update-text', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_live_info(n):
    return html.Div([
        html.P(f"Останнє оновлення: {pd.Timestamp.now().strftime('%H:%M:%S')}")
    ])

# Оновлення повідомлень про стан ресурсів
@app.callback(
    Output('resource-alerts', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_resource_alerts(n):
    critical_resources = resources_data[resources_data['Використання (%)'] > 80]['Ресурс'].tolist()
    if critical_resources:
        return html.P(f"Критичний рівень: {', '.join(critical_resources)}")
    return html.P("Усі ресурси в нормі")

# Запуск сервера
if __name__ == '__main__':
    app.run_server(debug=True)