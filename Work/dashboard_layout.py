# Макет додатку та запуск сервера

# Імпортуємо необхідні функції з попереднього файлу
from fixed_dashboard_code import app, colors, create_ukraine_map, create_threat_analysis, create_resource_management, create_forecast_chart
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from fixed_dashboard_code import resources_data

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
    print("Сервер запущено. Відкрийте http://127.0.0.1:8050/ у вашому браузері.")