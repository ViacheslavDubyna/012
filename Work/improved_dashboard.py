# Покращений код дашборду з удосконаленою візуалізацією

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

# Ініціалізація додатку Dash з покращеними метаданими
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    title="Інформаційно-аналітична система НГУ"
)

# Покращена кольорова схема
colors = {
    'visualization': '#E3F2FD',  # світло-блакитний
    'threats': '#FFF3E0',        # світло-оранжевий
    'resources': '#E8F5E9',      # світло-зелений
    'forecasting': '#F3E5F5',    # світло-фіолетовий
    'background': '#FAFAFA',     # світло-сірий фон
    'text': '#37474F',           # темно-сірий текст
    'accent': '#1976D2',         # акцентний синій
    'warning': '#FF9800',        # оранжевий для попереджень
    'danger': '#F44336',         # червоний для небезпеки
    'success': '#4CAF50'         # зелений для успіху
}

# Завантаження GeoJSON
# Використовуємо правильне джерело GeoJSON для України
ukraine_geojson_url = "https://raw.githubusercontent.com/vsapsai/ukraine_map_data/master/ukraine_geojson.json"
try:
    response = requests.get(ukraine_geojson_url)
    ukraine_geojson = response.json()
    print("GeoJSON успішно завантажено")
except Exception as e:
    print(f"Помилка при завантаженні GeoJSON: {e}")
    # Створюємо спрощений GeoJSON для України як запасний варіант
    # Координати областей України
    region_coords = {
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
    }
    
    # Створюємо спрощений GeoJSON
    ukraine_geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"shapeName": region},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[lon-1, lat-1], [lon+1, lat-1], [lon+1, lat+1], [lon-1, lat+1], [lon-1, lat-1]]]
            }
        } for region, (lon, lat) in region_coords.items()]
    }
    print("Створено запасний GeoJSON")

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
    try:
        url = f"https://api.acleddata.com/acled/read?key={api_key}&email={email}&country=Ukraine&event_date={thirty_days_ago}&event_date_where=>&fields=admin1"
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

# Створення покращених графіків
def create_ukraine_map():
    # Перевіряємо, чи маємо правильний GeoJSON
    if 'features' in ukraine_geojson and len(ukraine_geojson['features']) > 0:
        # Використовуємо choropleth з GeoJSON
        try:
            fig = px.choropleth(
                viz_data,
                geojson=ukraine_geojson,
                locations='Region English',
                featureidkey='properties.shapeName',
                color='Рівень безпеки',
                color_continuous_scale=[
                    [0, 'rgb(220, 53, 69)'],   # Червоний для низьких значень
                    [0.4, 'rgb(255, 193, 7)'], # Жовтий для середніх значень
                    [1, 'rgb(40, 167, 69)']    # Зелений для високих значень
                ],
                range_color=(10, 100),
                labels={'Рівень безпеки': 'Рівень безпеки'},
                hover_name='Область',
                hover_data={'Region English': False, 'Рівень безпеки': True}
            )
            fig.update_geos(
                fitbounds="locations", 
                visible=False,
                showcoastlines=True, 
                coastlinecolor="RebeccaPurple",
                showland=True, 
                landcolor="LightGray"
            )
            fig.update_layout(
                margin={"r":0,"t":0,"l":0,"b":0},
                coloraxis_colorbar={
                    'title': 'Рівень безпеки',
                    'tickvals': [10, 40, 70, 100],
                    'ticktext': ['Критичний', 'Небезпечний', 'Середній', 'Безпечний'],
                    'lenmode': 'fraction',
                    'len': 0.75
                }
            )
            print("Карта створена з використанням GeoJSON")
            return fig
        except Exception as e:
            print(f"Помилка при створенні карти з GeoJSON: {e}")
            # Якщо виникла помилка, використовуємо запасний варіант
    
    # Запасний варіант - використовуємо scatter map з покращеним дизайном
    print("Використовуємо запасний варіант карти")
    fig = go.Figure()
    
    # Додаємо контур для представлення України
    ukraine_lons = [22, 40, 40, 22, 22]  # Координати longitude
    ukraine_lats = [44, 44, 52, 52, 44]  # Координати latitude
    
    fig.add_trace(go.Scatter(
        x=ukraine_lons,
        y=ukraine_lats,
        mode='lines',
        line=dict(width=2, color='rgba(70, 130, 180, 0.8)'),
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
                marker_color = 'rgb(220, 53, 69)'  # Червоний
                security_text = 'Критичний'
            elif security < 70:
                marker_color = 'rgb(255, 193, 7)'  # Жовтий
                security_text = 'Середній'
            else:
                marker_color = 'rgb(40, 167, 69)'  # Зелений
                security_text = 'Безпечний'
                
            fig.add_trace(go.Scatter(
                x=[lon],
                y=[lat],
                mode='markers+text',
                marker=dict(
                    size=20, 
                    color=marker_color,
                    line=dict(width=2, color='white')
                ),
                text=region,
                textposition="top center",
                hoverinfo='text',
                hovertext=f"{region}<br>Рівень безпеки: {security} ({security_text})",
                name=f"{region} ({security})",
                showlegend=False
            ))
    
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        plot_bgcolor='rgba(240, 240, 240, 0.5)',
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            projection_type='mercator',
            showland=True,
            landcolor='rgb(240, 240, 240)',
            countrycolor='rgb(204, 204, 204)'
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    return fig

def create_threat_analysis():
    # Сортуємо дані за рівнем ризику для кращої візуалізації
    sorted_threats = threats_data.sort_values('Рівень ризику', ascending=False)
    
    fig = px.bar(
        sorted_threats,
        x='Тип загрози',
        y='Рівень ризику',
        color='Категорія',
        color_discrete_map={
            'Військова загроза': '#dc3545',      # Червоний
            'Кібер загроза': '#0dcaf0',         # Блакитний
            'Фізична загроза': '#fd7e14',       # Оранжевий
            'Інформаційна загроза': '#6f42c1',  # Фіолетовий
            'Критична інфраструктура': '#ffc107' # Жовтий
        },
        title='',
        labels={
            'Тип загрози': 'Тип загрози',
            'Рівень ризику': 'Рівень загрози (1-10)',
            'Категорія': 'Категорія загрози'
        },
        text='Рівень ризику'
    )
    
    # Покращення дизайну графіка
    fig.update_traces(
        texttemplate='%{text:.1f}',
        textposition='outside',
        marker_line_color='rgb(255, 255, 255)',
        marker_line_width=1.5,
        opacity=0.9
    )
    
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(
            tickangle=45,
            title_font=dict(size=14),
            tickfont=dict(size=12),
            gridcolor='rgba(230, 230, 230, 0.5)'
        ),
        yaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12),
            gridcolor='rgba(230, 230, 230, 0.5)',
            range=[0, 10.5]  # Встановлюємо діапазон для осі Y
        ),
        plot_bgcolor='rgba(255, 255, 255, 0.9)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12)
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    
    # Додаємо горизонтальні лінії для позначення рівнів ризику
    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=7,
        x1=len(sorted_threats)-0.5,
        y1=7,
        line=dict(color="rgba(220, 53, 69, 0.5)", width=2, dash="dash"),
    )
    
    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=4,
        x1=len(sorted_threats)-0.5,
        y1=4,
        line=dict(color="rgba(255, 193, 7, 0.5)", width=2, dash="dash"),
    )
    
    # Додаємо анотації для рівнів ризику
    fig.add_annotation(
        x=len(sorted_threats)-0.5,
        y=7,
        text="Високий ризик",
        showarrow=False,
        font=dict(size=10, color="rgba(220, 53, 69, 0.8)"),
        xshift=50,
        yshift=0
    )
    
    fig.add_annotation(
        x=len(sorted_threats)-0.5,
        y=4,
        text="Середній ризик",
        showarrow=False,
        font=dict(size=10, color="rgba(255, 193, 7, 0.8)"),
        xshift=50,
        yshift=0
    )
    
    return fig

def create_resource_management():
    # Сортуємо ресурси за рівнем використання
    sorted_resources = resources_data.sort_values('Використання (%)', ascending=False)
    
    # Створюємо покращений графік з індикаторами
    fig = go.Figure()
    
    # Визначаємо кількість рядків і стовпців для сітки
    num_resources = len(sorted_resources)
    cols = 3
    rows = (num_resources + cols - 1) // cols  # Округлення вгору
    
    # Розраховуємо розміри для кожного індикатора
    for i, row in sorted_resources.iterrows():
        resource = row['Ресурс']
        usage = row['Використання (%)']
        
        # Визначаємо колір індикатора залежно від рівня використання
        if usage > 80:
            color = "#dc3545"  # Червоний (критичний)
        elif usage > 60:
            color = "#fd7e14"  # Оранжевий (високий)
        else:
            color = "#28a745"  # Зелений (нормальний)
        
        # Розраховуємо позицію для індикатора в сітці
        row_idx = i // cols
        col_idx = i % cols
        
        # Розраховуємо домен для індикатора
        x_domain = [col_idx/cols, (col_idx+0.9)/cols]
        y_domain = [1 - (row_idx+1)/rows, 1 - row_idx/rows]
        
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=usage,
            domain={'x': x_domain, 'y': y_domain},
            title={
                'text': resource,
                'font': {'size': 14, 'color': colors['text']}
            },
            delta={'reference': 50, 'increasing': {'color': "#dc3545"}, 'decreasing': {'color': "#28a745"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': colors['text']},
                'bar': {'color': color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 60], 'color': 'rgba(40, 167, 69, 0.2)'},
                    {'range': [60, 80], 'color': 'rgba(253, 126, 20, 0.3)'},
                    {'range': [80, 100], 'color': 'rgba(220, 53, 69, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
    
    # Оновлюємо макет
    fig.update_layout(
        grid={'rows': rows, 'columns': cols, 'pattern': "independent"},
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=rows*150,  # Динамічна висота залежно від кількості рядків
        showlegend=False
    )
    
    return fig

def create_forecast_chart():
    fig = go.Figure()
    
    # Додаємо фактичні дані
    fig.add_trace(go.Scatter(
        x=forecast_data['Дата'],
        y=forecast_data['Фактично'],
        mode='markers+lines',
        name='Фактичні дані',
        line=dict(color='#1976D2', width=3),
        marker=dict(size=8, color='#1976D2', line=dict(width=2, color='white')),
        hovertemplate='%{x|%d.%m.%Y}<br>Значення: %{