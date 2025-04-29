# Документація компонентів

## Компонент графіків (chart.html)

### Використання:
```jinja2
{% from 'components/chart.html' import render_chart %}

{{ render_chart(
    chart_id='uniqueChartId',
    chart_type='bar|line|pie|doughnut',
    chart_data=chart_data_variable,
    chart_options={...}
) }}
```

### Параметри:
- `chart_id` (обов'язковий) - Унікальний ідентифікатор canvas елемента
- `chart_type` (обов'язковий) - Тип графіка з доступних Chart.js
- `chart_data` (обов'язковий) - Дані для візуалізації у форматі JSON
- `chart_options` (опційний) - Кастомні налаштування графіка

### Приклад контролера:
```python
@route('/chart-data')
def get_chart_data():
    return jsonify({
        'labels': ['Січень', 'Лютий', 'Березень'],
        'datasets': [{
            'label': 'Статистика',
            'data': [12, 19, 3]
        }]
    })
```

## Правила створення компонентів
1. Використовувати макроси Jinja2 для повторного використання
2. Дотримуватися структури каталогів: /components
3. Забезпечувати унікальні ID для DOM-елементів
4. Додавати коментарі з прикладами використання
5. Тестувати компонент в ізоляції перед інтеграцією