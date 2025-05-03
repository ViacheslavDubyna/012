# Вдосконалений дашборд для інформаційно-аналітичної системи Національної гвардії України
# Інтеграція з API-ендпоіттами та покращена візуалізація

import dash
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import requests
from datetime import datetime, timedelta
from collections import Counter
import json
import os
 
# Ініціалізація додатку Dash з покращеними метаданими та префіксами шляхів
app = dash.Dash(
    __name__,
    # server=False, # Видалено, оскільки init_app буде використано
    routes_pathname_prefix='/dashboard/improved/',
    requests_pathname_prefix='/dashboard/improved/',
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    title="Інформаційно-аналітична система НГУ",
    suppress_callback_exceptions=True,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
    ]
)

# Покращена кольорова схема з національними кольорами України
colors = {
    'visualization': '#E3F2FD',  # світло-блакитний
    'threats': '#FFF3E0',        # світло-оранжевий
    'resources': '#E8F5E9',      # світло-зелений
    'forecasting': '#F3E5F5',    # світло-фіолетовий
    'background': '#FAFAFA',     # світло-сірий фон
    'text': '#37474F',           # темно-сірий текст
    'accent': '#0057b7',         # синій (національний колір України)
    'accent2': '#ffd700',        # жовтий (національний колір України)
    'warning': '#FF9800',        # оранжевий для попереджень
    'danger': '#F44336',         # червоний для небезпеки
    'success': '#4CAF50'         # зелений для успіху
}

# Базовий URL для API-ендпоінтів
# Використовуємо localhost для підключення до API, оскільки сервер запускається на 0.0.0.0:5000
API_BASE_URL = "http://localhost:5000/api"

# Функції для отримання даних з API
def get_dashboard_statistics():
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard/statistics")
        return response.json()
    except Exception as e:
        print(f"Помилка при отриманні статистики: {e}")
        # Повертаємо тестові дані у випадку помилки
        return {
            'units_count': 25,
            'resources_count': 150,
            'incidents_count': 42,
            'critical_situations_count': 3
        }

def get_recent_incidents():
    try:
        response = requests.get(f"{API_BASE_URL}/incidents/recent")
        return response.json()
    except Exception as e:
        print(f"Помилка при отриманні інцидентів: {e}")
        # Повертаємо тестові дані у випадку помилки
        return [
            {
                'id': 1,
                'type': 'Порушення громадського порядку',
                'subtype': 'Масові заворушення',
                'location': 'Київ',
                'timestamp': datetime.now().isoformat(),
                'severity': 'Високий',
                'status': 'Активний'
            }
        ]

def get_threat_level_history():
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/threat-level-history")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Помилка мережі при отриманні історії рівня загрози: {e}")
    except json.JSONDecodeError as e:
        print(f"Помилка декодування JSON історії рівня загрози: {e}")
    except Exception as e:
        print(f"Загальна помилка при отриманні історії рівня загрози: {e}")
    # Повертаємо порожні дані у випадку помилки
    return {'dates': [], 'threat_levels': []}

def get_resources_distribution():
    try:
        response = requests.get(f"{API_BASE_URL}/resources/distribution")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Помилка мережі при отриманні розподілу ресурсів: {e}")
    except json.JSONDecodeError as e:
        print(f"Помилка декодування JSON розподілу ресурсів: {e}")
    except Exception as e:
        print(f"Загальна помилка при отриманні розподілу ресурсів: {e}")
    # Повертаємо порожні дані у випадку помилки
    return {'resources': [], 'by_type': {}, 'by_status': {}}

def get_map_data():
    try:
        response = requests.get(f"{API_BASE_URL}/situations/map-data")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Помилка мережі при отриманні даних для карти: {e}")
    except json.JSONDecodeError as e:
        print(f"Помилка декодування JSON даних для карти: {e}")
    except Exception as e:
        print(f"Загальна помилка при отриманні даних для карти: {e}")
    # Повертаємо порожній список у випадку помилки
    return []

def get_ai_predictions():
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/predictions")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Помилка мережі при отриманні прогнозів AI: {e}")
    except json.JSONDecodeError as e:
        print(f"Помилка декодування JSON прогнозів AI: {e}")
    except Exception as e:
        print(f"Загальна помилка при отриманні прогнозів AI: {e}")
    # Повертаємо порожній список у випадку помилки
    return []

# Функції для створення графіків
def create_ukraine_map(map_data):
    # Створюємо базову карту
    fig = go.Figure()

    # Додаємо маркери для кожної ситуації
    if map_data:
        lats = []
        lons = []
        texts = []
        colors_map = []
        for situation in map_data:
            # Парсимо координати
            try:
                lat, lon = map(float, situation['coordinates'].split(','))
                lats.append(lat)
                lons.append(lon)
                texts.append(f"{situation.get('location', 'N/A')} ({situation.get('status', 'N/A')})")
                # Визначаємо колір маркера залежно від статусу
                status = situation.get('status', 'Нормальна')
                if status == 'Критична':
                    colors_map.append(colors['danger'])
                elif status == 'Напружена':
                    colors_map.append(colors['warning'])
                else:
                    colors_map.append(colors['success'])
            except Exception as e:
                print(f"Помилка обробки даних ситуації для карти: {e}, Дані: {situation}")
                continue

        if lats:
             fig.add_trace(go.Scattergeo(
                lon=lons,
                lat=lats,
                text=texts,
                mode='markers',
                marker=dict(
                    color=colors_map,
                    size=10,
                    opacity=0.8,
                    line=dict(width=1, color='rgba(68, 68, 68, 0)')
                ),
                name='Ситуації'
            ))

    # Налаштування вигляду карти
    fig.update_layout(
        title='Оперативна карта України',
        geo=dict(
            scope='europe',
            center=dict(lon=31, lat=48.5), # Центр України
            projection_scale=5, # Масштаб
            landcolor='rgb(217, 217, 217)',
            subunitcolor='rgb(255, 255, 255)',
            bgcolor='rgba(0,0,0,0)',
            lataxis_range=[44, 53], # Обмежуємо широту
            lonaxis_range=[22, 41]  # Обмежуємо довготу
        ),
        margin={"r":0,"t":40,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color=colors['text']
    )
    return fig

def create_threat_analysis():
    # Отримуємо дані про рівень загрози
    threat_data = get_threat_level_history()
    
    # Створюємо графік
    fig = go.Figure()
    
    # Додаємо лінію рівня загрози
    fig.add_trace(go.Scatter(
        x=threat_data['dates'],
        y=threat_data['threat_levels'],
        mode='lines+markers',
        name='Рівень загрози',
        line=dict(color=colors['accent'], width=3),
        marker=dict(size=8, color=colors['accent']),
        fill='tozeroy',
        fillcolor=f"rgba({int(colors['accent'][1:3], 16)}, {int(colors['accent'][3:5], 16)}, {int(colors['accent'][5:7], 16)}, 0.2)"
    ))
    
    # Додаємо зони рівнів загрози
    fig.add_shape(
        type="rect",
        x0=0,
        y0=70,
        x1=len(threat_data['dates']),
        y1=100,
        fillcolor="rgba(76, 175, 80, 0.1)",
        line=dict(width=0),
        layer="below"
    )
    
    fig.add_shape(
        type="rect",
        x0=0,
        y0=40,
        x1=len(threat_data['dates']),
        y1=70,
        fillcolor="rgba(255, 152, 0, 0.1)",
        line=dict(width=0),
        layer="below"
    )
    
    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=len(threat_data['dates']),
        y1=40,
        fillcolor="rgba(244, 67, 54, 0.1)",
        line=dict(width=0),
        layer="below"
    )
    
    # Додаємо анотації для зон
    fig.add_annotation(
        x=len(threat_data['dates']) - 1,
        y=85,
        text="Низький рівень загрози",
        showarrow=False,
        font=dict(size=10, color="rgba(76, 175, 80, 0.7)")
    )
    
    fig.add_annotation(
        x=len(threat_data['dates']) - 1,
        y=55,
        text="Середній рівень загрози",
        showarrow=False,
        font=dict(size=10, color="rgba(255, 152, 0, 0.7)")
    )
    
    fig.add_annotation(
        x=len(threat_data['dates']) - 1,
        y=20,
        text="Високий рівень загрози",
        showarrow=False,
        font=dict(size=10, color="rgba(244, 67, 54, 0.7)")
    )
    
    # Налаштовуємо вигляд графіка
    fig.update_layout(
        title={
            'text': 'Динаміка рівня загрози',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': colors['text']}
        },
        xaxis=dict(
            title='Дата',
            tickangle=45,
            tickmode='array',
            tickvals=[i for i in range(0, len(threat_data['dates']), 5)],
            ticktext=[threat_data['dates'][i] for i in range(0, len(threat_data['dates']), 5)],
            gridcolor='rgba(230, 230, 230, 0.5)'
        ),
        yaxis=dict(
            title='Рівень загрози',
            range=[0, 100],
            gridcolor='rgba(230, 230, 230, 0.5)'
        ),
        margin=dict(l=40, r=40, t=50, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    
    return fig

def create_resource_management():
    # Отримуємо дані про ресурси
    resource_data = get_resources_distribution()
    
    # Створюємо дані для графіка
    resource_types = list(resource_data['by_type'].keys())
    resource_counts = [data['count'] for data in resource_data['by_type'].values()]
    resource_percentages = [data['percentage'] for data in resource_data['by_type'].values()]
    
    # Створюємо графік розподілу ресурсів за типами
    fig = go.Figure()
    
    # Додаємо стовпчики для кожного типу ресурсів
    fig.add_trace(go.Bar(
        x=resource_types,
        y=resource_counts,
        marker_color=colors['accent'],
        text=resource_percentages,
        texttemplate='%{text}%',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Кількість: %{y}<br>Відсоток: %{text}%<extra></extra>'
    ))
    
    # Налаштовуємо вигляд графіка
    fig.update_layout(
        title={
            'text': 'Розподіл ресурсів за типами',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': colors['text']}
        },
        xaxis=dict(
            title='Тип ресурсу',
            tickangle=45,
            gridcolor='rgba(230, 230, 230, 0.5)'
        ),
        yaxis=dict(
            title='Кількість',
            gridcolor='rgba(230, 230, 230, 0.5)'
        ),
        margin=dict(l=40, r=40, t=50, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_resource_status_chart():
    # Отримуємо дані про ресурси
    resource_data = get_resources_distribution()
    
    # Створюємо дані для графіка
    status_labels = list(resource_data['by_status'].keys())
    status_values = [data['percentage'] for data in resource_data['by_status'].values()]
    
    # Визначаємо кольори для статусів
    status_colors = {
        'Доступний': colors['success'],
        'В ремонті': colors['warning'],
        'Недоступний': colors['danger']
    }
    
    # Створюємо графік розподілу ресурсів за статусами
    fig = go.Figure()
    
    # Додаємо кругову діаграму
    fig.add_trace(go.Pie(
        labels=status_labels,
        values=status_values,
        marker=dict(
            colors=[status_colors.get(status, colors['accent']) for status in status_labels],
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        insidetextorientation='radial',
        hole=0.4
    ))
    
    # Налаштовуємо вигляд графіка
    fig.update_layout(
        title={
            'text': 'Статус ресурсів',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': colors['text']}
        },
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def create_incidents_chart():
    # Отримуємо дані про інциденти
    incidents = get_recent_incidents()
    
    # Групуємо інциденти за типами
    incident_types = {}
    for incident in incidents:
        incident_type = incident['type']
        if incident_type in incident_types:
            incident_types[incident_type] += 1
        else:
            incident_types[incident_type] = 1
    
    # Створюємо дані для графіка
    types = list(incident_types.keys())
    counts = list(incident_types.values())
    
    # Створюємо графік інцидентів
    fig = go.Figure()
    
    # Додаємо стовпчики для кожного типу інцидентів
    fig.add_trace(go.Bar(
        x=types,
        y=counts,
        marker_color=colors['warning'],
        text=counts,
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Кількість: %{y}<extra></extra>'
    ))
    
    # Налаштовуємо вигляд графіка
    fig.update_layout(
        title={
            'text': 'Розподіл інцидентів за типами',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': colors['text']}
        },
        xaxis=dict(
            title='Тип інциденту',
            tickangle=45,
            gridcolor='rgba(230, 230, 230, 0.5)'
        ),
        yaxis=dict(
            title='Кількість',
            gridcolor='rgba(230, 230, 230, 0.5)'
        ),
        margin=dict(l=40, r=40, t=50, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Макет додатку Dash
app.layout = html.Div(style={'backgroundColor': colors['background'], 'color': colors['text'], 'padding': '20px'}, children=[
    # Заголовок
    html.Div(className="container-fluid", children=[
        html.Div(className="row mb-4", children=[
            html.Div(className="col-12", children=[
                html.H1("ІНФОРМАЦІЙНО-АНАЛІТИЧНА СИСТЕМА НГУ", className="display-5 fw-bold text-center mt-4 animate__animated animate__fadeIn"),
                html.P("Інтерактивний дашборд для моніторингу та управління ресурсами Національної гвардії України", 
                       className="lead text-muted text-center animate__animated animate__fadeIn")
            ])
        ])
    ]),
    
    # Статистика
    html.Div(className="container-fluid", children=[
        html.Div(className="row g-4 mb-4", children=[
            # Кількість підрозділів
            html.Div(className="col-md-6 col-lg-3", children=[
                html.Div(className="card h-100 animate__animated animate__fadeInUp", children=[
                    html.Div(className="card-body text-center", children=[
                        html.Div(className="d-flex align-items-center justify-content-center mb-3", children=[
                            html.I(className="fas fa-users fa-3x text-primary me-3"),
                            html.H2(id="units-count", className="display-4 mb-0")
                        ]),
                        html.H3("Підрозділи", className="card-title h5 mb-2"),
                        html.P("Загальна кількість підрозділів НГУ", className="card-text text-muted")
                    ])
                ])
            ]), # <<< Додано кому між елементами другого ряду
            
            # Кількість ресурсів
            html.Div(className="col-md-6 col-lg-3", children=[
                html.Div(className="card h-100 animate__animated animate__fadeInUp", 
                         style={"animation-delay": "0.1s"}, children=[
                    html.Div(className="card-body text-center", children=[
                        html.Div(className="d-flex align-items-center justify-content-center mb-3", children=[
                            html.I(className="fas fa-boxes fa-3x text-success me-3"),
                            html.H2(id="resources-count", className="display-4 mb-0")
                        ]),
                        html.H3("Ресурси", className="card-title h5 mb-2"),
                        html.P("Доступні ресурси в системі", className="card-text text-muted")
                    ])
                ])
            ]), # <<< Додано кому

            # Кількість інцидентів
            html.Div(className="col-md-6 col-lg-3", children=[
                html.Div(className="card h-100 animate__animated animate__fadeInUp", 
                         style={"animation-delay": "0.2s"}, children=[
                    html.Div(className="card-body text-center", children=[
                        html.Div(className="d-flex align-items-center justify-content-center mb-3", children=[
                            html.I(className="fas fa-exclamation-triangle fa-3x text-warning me-3"),
                            html.H2(id="incidents-count", className="display-4 mb-0")
                        ]),
                        html.H3("Інциденти", className="card-title h5 mb-2"),
                        html.P("Зареєстровані інциденти за 30 днів", className="card-text text-muted")
                    ])
                ])
            ]), # <<< Додано кому між елементами другого ряду
            
            # Критичні ситуації
            html.Div(className="col-md-6 col-lg-3", children=[
                html.Div(className="card h-100 animate__animated animate__fadeInUp", 
                         style={"animation-delay": "0.3s"}, children=[
                    html.Div(className="card-body text-center", children=[
                        html.Div(className="d-flex align-items-center justify-content-center mb-3", children=[
                            html.I(className="fas fa-radiation fa-3x text-danger me-3"),
                            html.H2(id="critical-count", className="display-4 mb-0")
                        ]),
                        html.H3("Критичні ситуації", className="card-title h5 mb-2"),
                        html.P("Активні критичні ситуації", className="card-text text-muted")
                    ])
                ])
            ]), # <<< Додано кому між елементами другого ряду
        ])
    ]),
    
    # Основні графіки
    html.Div(className="container-fluid", children=[
        html.Div(className="row g-4 mb-4", children=[
            # Карта України
            html.Div(className="col-lg-8", children=[
                html.Div(className="card h-100 animate__animated animate__fadeIn", 
                         style={"animation-delay": "0.4s"}, children=[
                    html.Div(className="card-header d-flex justify-content-between align-items-center", children=[
                        html.H5("Карта оперативної обстановки", className="mb-0"),
                        html.Button("Оновити", id="update-map", className="btn btn-sm btn-outline-primary")
                    ]),
                    html.Div(className="card-body p-0", children=[
                        dcc.Graph(id="ukraine-map", figure=create_ukraine_map(), config={'displayModeBar': False})
                    ])
                ])
            ]), # <<< Додано кому між елементами другого ряду, # <<< Виправлено: додано кому
            # Аналіз загроз
            html.Div(className="col-lg-4", children=[
                html.Div(className="card h-100 animate__animated animate__fadeIn", 
                         style={"animation-delay": "0.5s"}, children=[
                    html.Div(className="card-header", children=[
                        html.H5("Аналіз загроз", className="mb-0")
                    ]),
                    html.Div(className="card-body", children=[
                        dcc.Graph(id="threat-analysis", figure=create_threat_analysis(), config={'displayModeBar': False})
                    ])
                ])
            ]), # <<< Додано кому між елементами другого ряду
        ]), # <<< END OF FIRST ROW OF GRAPHS,

        # Другий ряд графіків
        html.Div(className="row g-4 mb-4", children=[
            # Управління ресурсами
            html.Div(className="col-lg-6", children=[
                html.Div(className="card h-100 animate__animated animate__fadeIn", 
                         style={"animation-delay": "0.6s"}, children=[
                    html.Div(className="card-header d-flex justify-content-between align-items-center", children=[
                        html.H5("Управління ресурсами", className="mb-0"),
                        html.Div(className="btn-group", children=[
                            html.Button("За типами", id="resource-type-btn", className="btn btn-sm btn-outline-primary active"),
                            html.Button("За статусом", id="resource-status-btn", className="btn btn-sm btn-outline-primary")
                        ])
                    ]),
                    html.Div(className="card-body", children=[
                        html.Div(id="resource-chart-container", children=[
                            dcc.Graph(id="resource-chart", figure=create_resource_management(), config={'displayModeBar': False})
                        ])
                    ])
                ])
            ]), # <<< Додано кому між елементами другого ряду
            
            # Інциденти
            html.Div(className="col-lg-6", children=[
                html.Div(className="card h-100 animate__animated animate__fadeIn", 
                         style={"animation-delay": "0.7s"}, children=[
                    html.Div(className="card-header", children=[
                        html.H5("Останні інциденти", className="mb-0")
                    ]),
                    html.Div(className="card-body", children=[
                        html.Div(id="incidents-table-container", style={"maxHeight": "400px", "overflow": "auto"}, children=[
                            html.Table(className="table table-hover", children=[
                                html.Thead(className="table-light", children=[
                                    html.Tr(children=[
                                        html.Th("Тип"),
                                        html.Th("Локація"),
                                        html.Th("Дата"),
                                        html.Th("Статус"),
                                        html.Th("Рівень")
                                    ])
                                ]),
                                html.Tbody(id="incidents-table-body")
                            ])
                        ])
                    ])
                ])
            ]), # <<< Додано кому між елементами другого ряду
        ])
        
        # Третій ряд - AI прогнози
        html.Div(className="row g-4 mb-4", children=[
            html.Div(className="col-12", children=[
                html.Div(className="card animate__animated animate__fadeIn", 
                         style={"animation-delay": "0.8s"}, children=[
                    html.Div(className="card-header d-flex justify-content-between align-items-center", children=[
                        html.H5("Прогнози штучного інтелекту", className="mb-0"),
                        html.Span(className="badge bg-primary", children=["AI"])
                    ]),
                    html.Div(className="card-body", children=[
                        html.Div(className="row", id="ai-predictions-container")
                    ])
                ])
            ]), # <<< Додано кому між елементами другого ряду
        ])
    ])
    
    # Інтервал для автоматичного оновлення даних
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # оновлення кожну хвилину
        n_intervals=0
    )
])

# Колбеки для оновлення даних
@app.callback(
    [
        Output("units-count", "children"),
        Output("resources-count", "children"),
        Output("incidents-count", "children"),
        Output("critical-count", "children")
    ],
    [Input("interval-component", "n_intervals")]
)
def update_statistics(n):
    """Оновлення статистичних даних"""
    stats = get_dashboard_statistics()
    return [
        stats['units_count'],
        stats['resources_count'],
        stats['incidents_count'],
        stats['critical_situations_count']
    ]

@app.callback(
    Output("ukraine-map", "figure"),
    [Input("update-map", "n_clicks"), Input("interval-component", "n_intervals")]
)
def update_map(n_clicks, n_intervals):
    """Оновлення карти"""
    return create_ukraine_map()

@app.callback(
    Output("threat-analysis", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_threat_analysis(n):
    """Оновлення аналізу загроз"""
    return create_threat_analysis()

@app.callback(
    Output("resource-chart-container", "children"),
    [Input("resource-type-btn", "n_clicks"), Input("resource-status-btn", "n_clicks")]
)
def update_resource_chart(type_clicks, status_clicks):
    """Перемикання між різними видами графіків ресурсів"""
    ctx = dash.callback_context
    if not ctx.triggered:
        # За замовчуванням показуємо розподіл за типами
        return [dcc.Graph(id="resource-chart", figure=create_resource_management(), config={'displayModeBar': False})]
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "resource-status-btn":
            return [dcc.Graph(id="resource-chart", figure=create_resource_status_chart(), config={'displayModeBar': False})]
        else:
            return [dcc.Graph(id="resource-chart", figure=create_resource_management(), config={'displayModeBar': False})]

@app.callback(
    Output("incidents-table-body", "children"),
    [Input("interval-component", "n_intervals")]
)
def update_incidents_table(n):
    """Оновлення таблиці інцидентів"""
    incidents = get_recent_incidents()
    rows = []
    for incident in incidents:
        # Визначаємо клас для рядка залежно від рівня важливості
        severity_class = ""
        if incident['severity'] == 'Високий':
            severity_class = "table-danger"
        elif incident['severity'] == 'Середній':
            severity_class = "table-warning"
        
        # Форматуємо дату
        try:
            date_obj = datetime.fromisoformat(incident['timestamp'])
            formatted_date = date_obj.strftime("%d.%m.%Y %H:%M")
        except:
            formatted_date = incident['timestamp']
        
        # Додаємо рядок до таблиці
        rows.append(html.Tr(className=severity_class, children=[
            html.Td(f"{incident['type']} - {incident['subtype']}"),
            html.Td(incident['location']),
            html.Td(formatted_date),
            html.Td(incident['status']),
            html.Td(incident['severity'])
        ]))
    
    return rows

@app.callback(
    Output("ai-predictions-container", "children"),
    [Input("interval-component", "n_intervals")]
)
def update_ai_predictions(n):
    """Оновлення прогнозів AI"""
    predictions = get_ai_predictions()
    prediction_cards = []
    
    for prediction in predictions:
        # Визначаємо колір картки залежно від значення прогнозу
        if prediction['value'] > 7:
            card_class = "border-danger"
            header_class = "bg-danger text-white"
        elif prediction['value'] > 4:
            card_class = "border-warning"
            header_class = "bg-warning"
        else:
            card_class = "border-success"
            header_class = "bg-success text-white"
        
        # Форматуємо дату
        try:
            date_obj = datetime.fromisoformat(prediction['timestamp'])
            formatted_date = date_obj.strftime("%d.%m.%Y")
        except:
            formatted_date = prediction['timestamp']
        
        # Створюємо картку прогнозу
        prediction_cards.append(html.Div(className="col-md-4 mb-3", children=[
            html.Div(className=f"card h-100 {card_class}", children=[
                html.Div(className=f"card-header {header_class}", children=[
                    html.H6(prediction['type'], className="mb-0")
                ]),
                html.Div(className="card-body", children=[
                    html.H5(prediction['region'], className="card-title"),
                    html.P(prediction['description'], className="card-text"),
                    html.Div(className="d-flex justify-content-between align-items-center", children=[
                        html.Span(f"Значення: {prediction['value']}"),
                        html.Span(f"Достовірність: {int(prediction['confidence']*100)}%")
                    ])
                ]),
                html.Div(className="card-footer text-muted", children=[
                    f"Оновлено: {formatted_date}"
                ])
            ])
        ]))
    
    return prediction_cards

# НЕ ЗАПУСКАЄМО app.run_server() тут, оскільки інтеграція здійснюється через DispatcherMiddleware у Flask
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
    print("Сервер запущено. Відкрийте http://127.0.0.1:8050/ у вашому браузері.")