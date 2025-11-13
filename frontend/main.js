// ============================================
// CONFIGURACIÓN GLOBAL
// ============================================

const API_URL = 'http://127.0.0.1:8000';

// ============================================
// ESTADO GLOBAL
// ============================================

let authState = {
    isAuthenticated: false,
    user: null,
    accessToken: null,
    refreshToken: null,
    tokenExpiry: null
};

// ============================================
// INICIALIZACIÓN
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    checkAPIHealth();
    restoreAuthState();
    updateUI();
});

function initializeEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => switchTab(e.target.dataset.tab));
    });

    // Form submissions
    document.getElementById('register-form').addEventListener('submit', handleRegister);
    document.getElementById('login-form').addEventListener('submit', handleLogin);

    // Dashboard actions
    document.getElementById('logout-btn')?.addEventListener('click', handleLogout);
    document.getElementById('get-user-btn')?.addEventListener('click', handleGetUser);
    document.getElementById('refresh-token-btn')?.addEventListener('click', handleRefreshToken);

    // Test endpoints
    document.getElementById('health-btn')?.addEventListener('click', () => testEndpoint('/health'));
    document.getElementById('protected-btn')?.addEventListener('click', () => testEndpoint('/users/me'));
}

// ============================================
// AUTENTICACIÓN - REGISTRO
// ============================================

async function handleRegister(e) {
    e.preventDefault();

    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const passwordConfirm = document.getElementById('register-password-confirm').value;
    const messageDiv = document.getElementById('register-message');

    // Validaciones
    if (username.length < 3) {
        showMessage(messageDiv, 'El usuario debe tener al menos 3 caracteres', 'error');
        return;
    }

    if (password.length < 8) {
        showMessage(messageDiv, '⚠️ La contraseña debe tener al menos 8 caracteres (tienes ' + password.length + ')', 'error');
        return;
    }

    if (password.length > 72) {
        showMessage(messageDiv, '⚠️ La contraseña no puede exceder 72 caracteres', 'error');
        return;
    }

    if (password !== passwordConfirm) {
        showMessage(messageDiv, 'Las contraseñas no coinciden', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(messageDiv, '✓ Registro exitoso. Puedes iniciar sesión ahora.', 'success');
            document.getElementById('register-form').reset();
            setTimeout(() => {
                switchTab('login');
                document.getElementById('login-username').value = username;
            }, 1500);
        } else {
            const errorMsg = data.detail || 'Error en el registro';
            showMessage(messageDiv, `Error: ${errorMsg}`, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage(messageDiv, 'Error de conexión. Verifica que la API esté en línea.', 'error');
    }
}

// ============================================
// AUTENTICACIÓN - LOGIN
// ============================================

async function handleLogin(e) {
    e.preventDefault();

    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const messageDiv = document.getElementById('login-message');

    try {
        const response = await fetch(`${API_URL}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        });

        const data = await response.json();

        if (response.ok) {
            // Guardar tokens
            authState.accessToken = data.access_token;
            authState.refreshToken = data.refresh_token;
            authState.isAuthenticated = true;
            authState.tokenExpiry = new Date(Date.now() + (data.expires_in * 1000));

            // Guardar en localStorage
            saveAuthState();

            // Obtener información del usuario
            await fetchCurrentUser();

            showMessage(messageDiv, '✓ Sesión iniciada correctamente', 'success');
            document.getElementById('login-form').reset();

            setTimeout(() => {
                updateUI();
            }, 1000);
        } else {
            showMessage(messageDiv, `Error: ${data.detail || 'Credenciales inválidas'}`, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage(messageDiv, 'Error de conexión. Verifica que la API esté en línea.', 'error');
    }
}

// ============================================
// AUTENTICACIÓN - LOGOUT
// ============================================

function handleLogout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        authState = {
            isAuthenticated: false,
            user: null,
            accessToken: null,
            refreshToken: null,
            tokenExpiry: null
        };
        localStorage.removeItem('authState');
        updateUI();
        switchTab('login');
        showMessage(
            document.getElementById('login-message'),
            'Sesión cerrada correctamente',
            'success'
        );
    }
}

// ============================================
// USUARIO - OBTENER INFORMACIÓN
// ============================================

async function fetchCurrentUser() {
    try {
        const response = await fetch(`${API_URL}/users/me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authState.accessToken}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            authState.user = data;
            return data;
        } else {
            console.error('Error fetching user:', response.status);
            return null;
        }
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

async function handleGetUser() {
    const resultDiv = document.getElementById('endpoint-result');
    resultDiv.classList.remove('show');

    try {
        const user = await fetchCurrentUser();
        
        if (user) {
            resultDiv.textContent = JSON.stringify(user, null, 2);
            resultDiv.classList.add('show');
        } else {
            resultDiv.textContent = 'Error: No se pudo obtener la información del usuario';
            resultDiv.classList.add('show');
        }
    } catch (error) {
        resultDiv.textContent = `Error: ${error.message}`;
        resultDiv.classList.add('show');
    }
}

// ============================================
// TOKEN - RENOVAR
// ============================================

async function handleRefreshToken() {
    const resultDiv = document.getElementById('endpoint-result');
    resultDiv.classList.remove('show');

    try {
        const response = await fetch(`${API_URL}/refresh`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authState.refreshToken}`,
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (response.ok) {
            // Actualizar tokens
            authState.accessToken = data.access_token;
            authState.refreshToken = data.refresh_token;
            authState.tokenExpiry = new Date(Date.now() + (data.expires_in * 1000));

            saveAuthState();
            updateTokenDisplay();

            resultDiv.textContent = JSON.stringify({
                message: '✓ Token renovado exitosamente',
                new_access_token: data.access_token,
                refresh_token: data.refresh_token,
                expires_in: data.expires_in
            }, null, 2);
            resultDiv.classList.add('show');
        } else {
            resultDiv.textContent = `Error: ${data.detail || 'No se pudo renovar el token'}`;
            resultDiv.classList.add('show');
        }
    } catch (error) {
        resultDiv.textContent = `Error: ${error.message}`;
        resultDiv.classList.add('show');
    }
}

// ============================================
// ENDPOINTS - PRUEBAS
// ============================================

async function testEndpoint(endpoint) {
    const resultDiv = document.getElementById('endpoint-result');
    resultDiv.classList.remove('show');
    resultDiv.textContent = 'Verificando...';
    resultDiv.classList.add('show');

    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (endpoint !== '/health' && authState.accessToken) {
            headers['Authorization'] = `Bearer ${authState.accessToken}`;
        }

        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'GET',
            headers: headers
        });

        const data = await response.json();

        const result = {
            method: 'GET',
            endpoint: endpoint,
            status: response.status,
            statusText: response.statusText,
            data: data
        };

        resultDiv.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        resultDiv.textContent = `Error: ${error.message}`;
    }
}

// ============================================
// API - VERIFICAR SALUD
// ============================================

async function checkAPIHealth() {
    const healthIndicator = document.getElementById('api-health');

    try {
        const response = await fetch(`${API_URL}/health`);
        
        if (response.ok) {
            healthIndicator.textContent = '🟢 En línea';
            healthIndicator.className = 'health-indicator online';
        } else {
            healthIndicator.textContent = '🔴 Offline';
            healthIndicator.className = 'health-indicator offline';
        }
    } catch (error) {
        healthIndicator.textContent = '🔴 Offline';
        healthIndicator.className = 'health-indicator offline';
    }

    // Verificar cada 30 segundos
    setInterval(checkAPIHealth, 30000);
}

// ============================================
// UI - ACTUALIZAR INTERFAZ
// ============================================

function updateUI() {
    const authSection = document.getElementById('auth-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const userStatus = document.getElementById('user-status');

    if (authState.isAuthenticated && authState.user) {
        // Mostrar dashboard
        authSection.style.display = 'none';
        dashboardSection.style.display = 'block';

        // Actualizar información
        document.getElementById('user-info-username').textContent = authState.user.username;
        document.getElementById('user-info-id').textContent = authState.user.id;
        document.getElementById('user-info-created').textContent = 
            new Date(authState.user.created_at).toLocaleString();

        userStatus.textContent = `✓ Autenticado como ${authState.user.username}`;
        userStatus.style.color = '#10b981';

        updateTokenDisplay();
    } else {
        // Mostrar formularios
        authSection.style.display = 'block';
        dashboardSection.style.display = 'none';
        userStatus.textContent = '✗ No autenticado';
        userStatus.style.color = '#ef4444';
    }
}

function updateTokenDisplay() {
    if (authState.accessToken) {
        document.getElementById('access-token-display').value = authState.accessToken;
    }

    if (authState.refreshToken) {
        document.getElementById('refresh-token-display').value = authState.refreshToken;
    }

    if (authState.tokenExpiry) {
        const now = new Date();
        const timeLeft = authState.tokenExpiry - now;
        const minutesLeft = Math.floor(timeLeft / 60000);
        const secondsLeft = Math.floor((timeLeft % 60000) / 1000);

        document.getElementById('token-expiry').textContent = 
            `${minutesLeft}m ${secondsLeft}s (${authState.tokenExpiry.toLocaleTimeString()})`;
    }
}

// ============================================
// TABS - CAMBIAR PESTAÑA
// ============================================

function switchTab(tabName) {
    // Ocultar todas las pestañas
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Desactivar todos los botones
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Mostrar pestaña seleccionada
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // Activar botón seleccionado
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Limpiar mensajes
    const messages = document.querySelectorAll('.message');
    messages.forEach(msg => {
        msg.classList.remove('show', 'success', 'error', 'warning');
    });
}

// ============================================
// MENSAJES
// ============================================

function showMessage(element, message, type = 'success') {
    element.textContent = message;
    element.className = `message show ${type}`;

    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        element.classList.remove('show');
    }, 5000);
}

// ============================================
// LOCAL STORAGE - PERSISTENCIA
// ============================================

function saveAuthState() {
    localStorage.setItem('authState', JSON.stringify({
        isAuthenticated: authState.isAuthenticated,
        user: authState.user,
        accessToken: authState.accessToken,
        refreshToken: authState.refreshToken,
        tokenExpiry: authState.tokenExpiry
    }));
}

function restoreAuthState() {
    const stored = localStorage.getItem('authState');

    if (stored) {
        try {
            const parsed = JSON.parse(stored);
            authState = {
                ...authState,
                ...parsed,
                tokenExpiry: parsed.tokenExpiry ? new Date(parsed.tokenExpiry) : null
            };

            // Verificar si el token ha expirado
            if (authState.tokenExpiry && authState.tokenExpiry < new Date()) {
                authState.isAuthenticated = false;
                authState.accessToken = null;
                localStorage.removeItem('authState');
            }
        } catch (error) {
            console.error('Error restoring auth state:', error);
            localStorage.removeItem('authState');
        }
    }
}

// ============================================
// UTILIDADES
// ============================================

// Actualizar contador de tokens cada segundo
setInterval(() => {
    if (authState.isAuthenticated) {
        updateTokenDisplay();
    }
}, 1000);
