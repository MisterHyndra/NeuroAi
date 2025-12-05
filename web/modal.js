/**
 * Sistema de Modais Minimalista e Clean
 * Design inspirado em interfaces modernas (figma, stripe, etc)
 */

let modalStack = [];

// Criar elementos do modal uma única vez
function initializeModalSystem() {
    // Verifica se já foi inicializado
    if (document.getElementById('modal-overlay')) {
        return;
    }

    // Cria overlay
    const overlay = document.createElement('div');
    overlay.id = 'modal-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 9998;
        opacity: 0;
        transition: opacity 0.2s ease;
        display: none;
    `;

    // Cria container do modal
    const container = document.createElement('div');
    container.id = 'modal-container';
    container.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        padding: 20px;
    `;

    // Cria conteúdo do modal
    const content = document.createElement('div');
    content.id = 'modal-content';
    content.style.cssText = `
        background: white;
        border-radius: 12px;
        padding: 32px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        max-width: 400px;
        width: 100%;
        text-align: center;
        animation: modalAppear 0.2s ease;
    `;

    // Adiciona animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes modalAppear {
            from {
                opacity: 0;
                transform: scale(0.95);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }

        @keyframes modalDisappear {
            from {
                opacity: 1;
                transform: scale(1);
            }
            to {
                opacity: 0;
                transform: scale(0.95);
            }
        }

        .modal-exiting {
            animation: modalDisappear 0.2s ease !important;
        }

        .modal-icon {
            font-size: 48px;
            margin-bottom: 16px;
            display: block;
        }

        .modal-title {
            color: #222;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 12px;
            line-height: 1.4;
        }

        .modal-message {
            color: #666;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 32px;
        }

        .modal-buttons {
            display: flex;
            gap: 12px;
            justify-content: center;
        }

        .modal-btn {
            padding: 10px 24px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            min-width: 100px;
        }

        .modal-btn-cancel {
            background: transparent;
            color: #666;
            border: 1px solid #ddd;
        }

        .modal-btn-cancel:hover {
            background: #f5f5f5;
            border-color: #bbb;
        }

        .modal-btn-confirm {
            background: #ff6b6b;
            color: white;
            border: none;
        }

        .modal-btn-confirm:hover {
            background: #ff5252;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
        }

        .modal-btn-confirm:active {
            transform: translateY(0);
        }
    `;

    document.head.appendChild(style);
    document.body.appendChild(overlay);
    container.appendChild(content);
    document.body.appendChild(container);
}

/**
 * Mostra modal de confirmação
 * @param {string} title - Título do modal
 * @param {string} message - Mensagem principal
 * @param {function} onConfirm - Callback ao confirmar
 * @param {object} options - Opções adicionais
 */
function showConfirmModal(title, message, onConfirm, options = {}) {
    initializeModalSystem();

    const {
        icon = '⚠️',
        confirmText = 'Sim, confirmar',
        cancelText = 'Cancelar'
    } = options;

    const overlay = document.getElementById('modal-overlay');
    const container = document.getElementById('modal-container');
    const content = document.getElementById('modal-content');

    // Constrói HTML do modal
    content.innerHTML = `
        <span class="modal-icon">${icon}</span>
        <h3 class="modal-title">${title}</h3>
        <p class="modal-message">${message}</p>
        <div class="modal-buttons">
            <button class="modal-btn modal-btn-cancel" onclick="closeModal()">
                ${cancelText}
            </button>
            <button class="modal-btn modal-btn-confirm" onclick="executeModalConfirm()">
                ${confirmText}
            </button>
        </div>
    `;

    // Armazena callback
    window._modalCallback = onConfirm;

    // Mostra modal
    overlay.style.display = 'block';
    container.style.display = 'flex';

    // Trigger animation
    setTimeout(() => {
        overlay.style.opacity = '1';
    }, 10);

    // Fecha ao clicar no overlay
    overlay.onclick = () => closeModal();

    // Impede propagação ao clicar no conteúdo
    content.onclick = (e) => e.stopPropagation();

    // Suporte a ESC
    document.addEventListener('keydown', handleEscapeKey);
}

/**
 * Mostra modal de alerta
 * @param {string} title - Título do modal
 * @param {string} message - Mensagem principal
 * @param {object} options - Opções adicionais
 */
function showAlertModal(title, message, options = {}) {
    initializeModalSystem();

    const {
        icon = 'ℹ️',
        buttonText = 'OK'
    } = options;

    const overlay = document.getElementById('modal-overlay');
    const container = document.getElementById('modal-container');
    const content = document.getElementById('modal-content');

    content.innerHTML = `
        <span class="modal-icon">${icon}</span>
        <h3 class="modal-title">${title}</h3>
        <p class="modal-message">${message}</p>
        <div class="modal-buttons">
            <button class="modal-btn modal-btn-confirm" onclick="closeModal()" style="width: 100%;">
                ${buttonText}
            </button>
        </div>
    `;

    overlay.style.display = 'block';
    container.style.display = 'flex';

    setTimeout(() => {
        overlay.style.opacity = '1';
    }, 10);

    overlay.onclick = () => closeModal();
    content.onclick = (e) => e.stopPropagation();

    document.addEventListener('keydown', handleEscapeKey);
}

/**
 * Executa o callback do modal
 */
function executeModalConfirm() {
    if (window._modalCallback && typeof window._modalCallback === 'function') {
        window._modalCallback();
    }
    closeModal();
}

/**
 * Fecha o modal com animação
 */
function closeModal() {
    const overlay = document.getElementById('modal-overlay');
    const container = document.getElementById('modal-container');
    const content = document.getElementById('modal-content');

    if (!overlay || !container) return;

    content.classList.add('modal-exiting');
    overlay.style.opacity = '0';

    setTimeout(() => {
        overlay.style.display = 'none';
        container.style.display = 'none';
        content.classList.remove('modal-exiting');
        window._modalCallback = null;
        document.removeEventListener('keydown', handleEscapeKey);
    }, 200);
}

/**
 * Manipula tecla ESC
 */
function handleEscapeKey(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
}

// Inicializa ao carregar
document.addEventListener('DOMContentLoaded', initializeModalSystem);
