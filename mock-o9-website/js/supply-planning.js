// Supply Planning JavaScript

function generatePlan() {
    const horizon = document.getElementById('planning-horizon').value;
    const plant = document.getElementById('plant').value;
    const line = document.getElementById('production-line').value;
    
    console.log(`Generating plan: ${horizon}, ${plant}, ${line}`);
    alert('Production plan generated successfully!');
}

function optimizePlan() {
    console.log('Optimizing production plan...');
    alert('Plan optimization complete! Capacity utilization improved by 5%.');
}

function editOrder(orderId) {
    console.log(`Editing order: ${orderId}`);
    alert(`Opening editor for order ${orderId}`);
}
