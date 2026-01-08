// Forecast Analysis JavaScript

function updateAnalysis() {
    const timePeriod = document.getElementById('time-period').value;
    const aggregation = document.getElementById('aggregation').value;
    console.log(`Updating analysis: ${timePeriod}, ${aggregation}`);
    alert('Analysis updated!');
}

function refreshAnalysis() {
    console.log('Refreshing analysis data...');
    alert('Analysis data refreshed successfully!');
}

function exportToExcel() {
    console.log('Exporting to Excel...');
    alert('Export started! File will download shortly.');
}

function drillDown(sku) {
    console.log(`Drilling down into ${sku}`);
    alert(`Showing detailed breakdown for ${sku}`);
}

// Initialize chart
window.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('forecastChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
                datasets: [
                    {
                        label: 'Forecast',
                        data: [1200, 1500, 1800, 1600, 2000, 2200],
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'Actual',
                        data: [1150, 1600, 1750, 1700, 1950, 2100],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: false
                    }
                }
            }
        });
    }
});
