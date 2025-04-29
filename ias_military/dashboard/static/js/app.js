// Базова ініціалізація веб-інтерфейсу
document.addEventListener('DOMContentLoaded', function() {
    // Ініціалізація інтерактивних елементів
    const menuItems = document.querySelectorAll('.nav-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            // Обробник кліку для навігації
            const target = this.dataset.target;
            document.querySelectorAll('.content-section').forEach(section => {
                section.style.display = 'none';
            });
            document.querySelector(`#${target}`).style.display = 'block';
        });
    });

    // Ініціалізація графіків
    const charts = document.querySelectorAll('.chart-container');
    charts.forEach(chart => {
        new ApexCharts(chart, {
            chart: { type: 'line', height: 350 },
            series: [{ data: [] }],
            xaxis: { type: 'datetime' }
        }).render();
    });
});