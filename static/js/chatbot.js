(function () {
  var isOpen = false;
  var messages = [];
  var isLoading = false;

  var container = null;
  var toggleBtn = null;
  var chatWindow = null;
  var messagesArea = null;
  var inputField = null;

  function getCsrfToken() {
    var meta = document.querySelector('[name=csrfmiddlewaretoken]');
    if (meta) return meta.value;
    var cookie = document.cookie.match(/csrftoken=([^;]+)/);
    return cookie ? cookie[1] : '';
  }

  function createWidget() {
    container = document.createElement('div');
    container.id = 'gc-chatbot';
    container.style.cssText = 'position:fixed;bottom:96px;right:24px;z-index:50;';

    toggleBtn = document.createElement('button');
    toggleBtn.setAttribute('aria-label', 'Ouvrir le chat');
    toggleBtn.style.cssText =
      'width:56px;height:56px;border-radius:50%;background:#1B3A6B;color:#fff;border:none;' +
      'cursor:pointer;display:flex;align-items:center;justify-content:center;' +
      'box-shadow:0 4px 12px rgba(0,0,0,0.15);transition:transform 0.2s;';
    toggleBtn.innerHTML =
      '<svg width="28" height="28" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">' +
      '<path stroke-linecap="round" stroke-linejoin="round" ' +
      'd="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"/>' +
      '<path stroke-linecap="round" stroke-linejoin="round" ' +
      'd="M2.25 12.76c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.076-4.076a1.526 1.526 0 011.037-.443h.004c6.088 0 8.633-2.06 8.633-5.72 0-3.66-2.545-5.72-8.633-5.72-6.088 0-8.634 2.06-8.634 5.72v1.997z"/>' +
      '</svg>';
    toggleBtn.addEventListener('click', toggle);
    toggleBtn.addEventListener('mouseenter', function () {
      toggleBtn.style.transform = 'scale(1.08)';
    });
    toggleBtn.addEventListener('mouseleave', function () {
      toggleBtn.style.transform = 'scale(1)';
    });

    chatWindow = document.createElement('div');
    chatWindow.style.cssText =
      'display:none;position:absolute;bottom:68px;right:0;width:384px;max-height:500px;' +
      'background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.18);' +
      'overflow:hidden;flex-direction:column;';

    var header = document.createElement('div');
    header.style.cssText =
      'background:#1B3A6B;color:#fff;padding:14px 16px;display:flex;' +
      'align-items:center;justify-content:space-between;border-radius:12px 12px 0 0;';
    header.innerHTML =
      '<span style="font-weight:600;font-size:14px;">Assistant GéoConsulting</span>';

    var closeBtn = document.createElement('button');
    closeBtn.setAttribute('aria-label', 'Fermer');
    closeBtn.style.cssText =
      'background:none;border:none;color:#fff;cursor:pointer;padding:4px;display:flex;';
    closeBtn.innerHTML =
      '<svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">' +
      '<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>';
    closeBtn.addEventListener('click', toggle);
    header.appendChild(closeBtn);

    messagesArea = document.createElement('div');
    messagesArea.style.cssText =
      'flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;' +
      'gap:10px;min-height:280px;max-height:360px;';

    var inputBar = document.createElement('div');
    inputBar.style.cssText =
      'display:flex;border-top:1px solid #e5e7eb;padding:10px 12px;gap:8px;align-items:center;';

    inputField = document.createElement('input');
    inputField.type = 'text';
    inputField.placeholder = 'Tapez votre message...';
    inputField.style.cssText =
      'flex:1;border:1px solid #d1d5db;border-radius:8px;padding:8px 12px;font-size:14px;' +
      'outline:none;transition:border-color 0.2s;';
    inputField.addEventListener('focus', function () {
      inputField.style.borderColor = '#1B3A6B';
    });
    inputField.addEventListener('blur', function () {
      inputField.style.borderColor = '#d1d5db';
    });
    inputField.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    });

    var sendBtn = document.createElement('button');
    sendBtn.setAttribute('aria-label', 'Envoyer');
    sendBtn.style.cssText =
      'width:36px;height:36px;border-radius:8px;background:#1B3A6B;color:#fff;border:none;' +
      'cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background 0.2s;';
    sendBtn.innerHTML =
      '<svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">' +
      '<path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"/>' +
      '</svg>';
    sendBtn.addEventListener('click', handleSend);
    sendBtn.addEventListener('mouseenter', function () {
      sendBtn.style.background = '#15305a';
    });
    sendBtn.addEventListener('mouseleave', function () {
      sendBtn.style.background = '#1B3A6B';
    });

    inputBar.appendChild(inputField);
    inputBar.appendChild(sendBtn);

    chatWindow.appendChild(header);
    chatWindow.appendChild(messagesArea);
    chatWindow.appendChild(inputBar);

    container.appendChild(chatWindow);
    container.appendChild(toggleBtn);
    document.body.appendChild(container);

    addBotMessage('Bonjour ! Comment puis-je vous aider ?');
  }

  function toggle() {
    isOpen = !isOpen;
    chatWindow.style.display = isOpen ? 'flex' : 'none';
    if (isOpen) {
      inputField.focus();
      scrollToBottom();
    }
  }

  function handleSend() {
    var text = inputField.value.trim();
    if (!text || isLoading) return;
    inputField.value = '';
    sendMessage(text);
  }

  function addUserMessage(text) {
    messages.push({ role: 'user', content: text });
    var bubble = document.createElement('div');
    bubble.style.cssText =
      'align-self:flex-end;background:#dbeafe;color:#1e3a5f;padding:8px 14px;' +
      'border-radius:12px 12px 2px 12px;max-width:80%;font-size:14px;line-height:1.5;word-break:break-word;';
    bubble.textContent = text;
    messagesArea.appendChild(bubble);
    scrollToBottom();
  }

  function addBotMessage(text) {
    messages.push({ role: 'assistant', content: text });
    var bubble = createBotBubble();
    bubble.textContent = text;
    messagesArea.appendChild(bubble);
    scrollToBottom();
    return bubble;
  }

  function createBotBubble() {
    var bubble = document.createElement('div');
    bubble.style.cssText =
      'align-self:flex-start;background:#f3f4f6;color:#374151;padding:8px 14px;' +
      'border-radius:12px 12px 12px 2px;max-width:80%;font-size:14px;line-height:1.5;word-break:break-word;';
    return bubble;
  }

  function showLoading() {
    var loader = document.createElement('div');
    loader.id = 'gc-chatbot-loader';
    loader.style.cssText = 'align-self:flex-start;display:flex;gap:4px;padding:8px 14px;';
    for (var i = 0; i < 3; i++) {
      var dot = document.createElement('span');
      dot.style.cssText =
        'width:8px;height:8px;border-radius:50%;background:#9ca3af;' +
        'animation:gc-dot-bounce 1.2s ' + (i * 0.2) + 's infinite ease-in-out;';
      loader.appendChild(dot);
    }
    messagesArea.appendChild(loader);
    scrollToBottom();
  }

  function hideLoading() {
    var loader = document.getElementById('gc-chatbot-loader');
    if (loader) loader.remove();
  }

  function buildHistory() {
    return messages.map(function (m) {
      return { role: m.role, content: m.content };
    });
  }

  async function sendMessage(text) {
    addUserMessage(text);
    isLoading = true;
    showLoading();

    try {
      var response = await fetch('/api/chatbot/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ message: text, history: buildHistory() }),
      });

      hideLoading();

      if (response.status === 429) {
        addBotMessage('Trop de requêtes. Veuillez patienter quelques instants avant de réessayer.');
        isLoading = false;
        return;
      }

      if (!response.ok) {
        addBotMessage("Désolé, une erreur s'est produite. Veuillez réessayer plus tard.");
        isLoading = false;
        return;
      }

      if (response.body && typeof response.body.getReader === 'function') {
        await readStream(response);
      } else {
        var data = await response.json();
        addBotMessage(data.response || data.message || "Désolé, je n'ai pas compris.");
      }
    } catch (_err) {
      hideLoading();
      addBotMessage("Désolé, une erreur s'est produite. Veuillez réessayer plus tard.");
    }

    isLoading = false;
  }

  async function readStream(response) {
    var reader = response.body.getReader();
    var decoder = new TextDecoder();
    var botText = '';
    var bubble = createBotBubble();
    messagesArea.appendChild(bubble);

    while (true) {
      var result = await reader.read();
      if (result.done) break;
      var chunk = decoder.decode(result.value, { stream: true });
      botText += chunk;
      bubble.textContent = botText;
      scrollToBottom();
    }

    if (botText) {
      messages.push({ role: 'assistant', content: botText });
    }
  }

  function scrollToBottom() {
    messagesArea.scrollTop = messagesArea.scrollHeight;
  }

  function injectStyles() {
    var style = document.createElement('style');
    style.textContent =
      '@keyframes gc-dot-bounce {' +
      '0%,80%,100%{transform:translateY(0)}' +
      '40%{transform:translateY(-6px)}' +
      '}';
    document.head.appendChild(style);
  }

  document.addEventListener('DOMContentLoaded', function () {
    injectStyles();
    createWidget();
  });
})();
