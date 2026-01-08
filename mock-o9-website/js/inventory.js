// Inventory Management JavaScript

function filterInventory() {
    const warehouse = document.getElementById('warehouse').value;
    const status = document.getElementById('inventory-status').value;
    const category = document.getElementById('product-category').value;
    console.log(`Filtering: ${warehouse}, ${status}, ${category}`);
}

function applyInventoryFilters() {
    filterInventory();
    alert('Filters applied successfully!');
}

function resetFilters() {
    document.getElementById('warehouse').value = '';
    document.getElementById('inventory-status').value = '';
    document.getElementById('product-category').value = '';
    console.log('Filters reset');
    alert('Filters have been reset!');
}

function selectAll(checkbox) {
    const checkboxes = document.querySelectorAll('.row-checkbox');
    checkboxes.forEach(cb => cb.checked = checkbox.checked);
}

function editItem(sku) {
    console.log(`Editing item: ${sku}`);
    alert(`Opening editor for ${sku}`);
}

function viewHistory(sku) {
    console.log(`Viewing history for: ${sku}`);
    alert(`Showing inventory history for ${sku}`);
}

function downloadReport() {
    console.log('Downloading inventory report...');
    alert('Report download started!');
}

function openBulkUpdate() {
    const selected = document.querySelectorAll('.row-checkbox:checked').length;
    if (selected === 0) {
        alert('Please select items to update');
    } else {
        alert(`Opening bulk update for ${selected} items`);
    }
}
