// Arquivo de scripts globais e de utilidade

// Utilitário: Escapar HTML para evitar XSS ao renderizar dados do backend
function escapeHTML(str) {
    if (!str) return '';
    return str.toString().replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}

// Lida com o Token
function getToken() {
    return localStorage.getItem('access_token');
}

// Verifica se o usuário tem token antes de exibir a página.
// Como não temos uma página de login server-side, faremos essa checagem via JS.
function checkAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = "/view/login"; // Redireciona para view de login
    }
}

// Lógica de logout
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = "/view/login";
    });
}

// Exibe mensagens de feedback visual (Flash messages do JS)
function showFlash(message, type = 'success') {
    const flashContainer = document.getElementById('flash-messages');
    if (!flashContainer) return;

    const msgDiv = document.createElement('div');
    msgDiv.className = `alert alert-${type}`;
    msgDiv.textContent = message;
    
    flashContainer.innerHTML = ''; // Limpa mensagens anteriores
    flashContainer.appendChild(msgDiv);

    // Some após 4 segundos
    setTimeout(() => {
        msgDiv.remove();
    }, 4000);
}