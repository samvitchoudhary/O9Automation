// Login Handler
function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Accept any username/password for testing
    // In real app, this would validate against backend
    if (username && password) {
        // Store username in sessionStorage
        sessionStorage.setItem('o9-username', username);
        sessionStorage.setItem('o9-logged-in', 'true');
        
        // Redirect to dashboard
        window.location.href = 'dashboard.html';
        return false;
    } else {
        document.getElementById('error-message').style.display = 'block';
        return false;
    }
}

// Logout Handler
function handleLogout() {
    sessionStorage.removeItem('o9-username');
    sessionStorage.removeItem('o9-logged-in');
    window.location.href = 'index.html';
}

// Check if user is logged in
function checkAuth() {
    const isLoggedIn = sessionStorage.getItem('o9-logged-in');
    const currentPage = window.location.pathname;
    
    if (!isLoggedIn && !currentPage.includes('index.html') && currentPage !== '/') {
        window.location.href = 'index.html';
    }
    
    // Display username if logged in
    const username = sessionStorage.getItem('o9-username');
    const usernameDisplay = document.getElementById('username-display');
    if (usernameDisplay && username) {
        usernameDisplay.textContent = username;
    }
}

// Toggle submenu
function toggleSubmenu(event, menuId) {
    event.preventDefault();
    const submenu = document.getElementById(menuId);
    if (submenu) {
        submenu.classList.toggle('active');
    }
}

// Apply Filters
function applyFilters() {
    const iteration = document.getElementById('forecast-iteration')?.value;
    const channel = document.getElementById('channel')?.value;
    const region = document.getElementById('region')?.value;
    
    console.log('Filters applied:', { iteration, channel, region });
    alert('Filters applied successfully!');
}

// Load BOM Data
function loadBOMData() {
    const version = document.getElementById('version-bom')?.value;
    const item = document.getElementById('item')?.value;
    
    console.log('Loading BOM data:', { version, item });
    alert('BOM data loaded!');
}

// Show Consumed Items
function showConsumedItems(itemId) {
    const consumedSection = document.getElementById('consumed-items');
    
    if (consumedSection) {
        consumedSection.innerHTML = `
            <h4>Consumed Items for ${itemId}</h4>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Material ID</th>
                        <th>Description</th>
                        <th>Quantity</th>
                        <th>Unit</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>MAT-001</td>
                        <td>Raw Material A</td>
                        <td>2.5</td>
                        <td>kg</td>
                    </tr>
                    <tr>
                        <td>MAT-002</td>
                        <td>Component B</td>
                        <td>5</td>
                        <td>pcs</td>
                    </tr>
                </tbody>
            </table>
        `;
    }
}

// Run on page load
window.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});

