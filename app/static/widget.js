(function() {
  var API_BASE = '__API_BASE_URL__';

  class ChatWidget extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
      this.isOpen = false;
      this.messages = [{ role: 'assistant', content: 'Olá! Como posso ajudar você hoje?' }];
    }

    connectedCallback() {
      this.render();
    }

    toggleChat() {
      this.isOpen = !this.isOpen;
      var container = this.shadowRoot.querySelector('.widget-container');
      container.style.display = this.isOpen ? 'flex' : 'none';
    }

    buildHistory() {
      return this.messages.map(function(m) { return { role: m.role, content: m.content }; });
    }

    appendMessage(role, content) {
      this.messages.push({ role: role, content: content });
      var area = this.shadowRoot.querySelector('.chat-messages');
      var div = document.createElement('div');
      div.className = 'message ' + (role === 'user' ? 'user' : 'bot');
      div.textContent = content;
      area.appendChild(div);
      area.scrollTop = area.scrollHeight;
    }

    setLoading(loading) {
      var btn = this.shadowRoot.querySelector('#send');
      var input = this.shadowRoot.querySelector('.chat-input-area input');
      btn.disabled = loading;
      input.disabled = loading;
      var loadingEl = this.shadowRoot.querySelector('.chat-loading');
      if (loadingEl) loadingEl.style.display = loading ? 'block' : 'none';
    }

    sendMessage() {
      var input = this.shadowRoot.querySelector('.chat-input-area input');
      var text = (input.value || '').trim();
      if (!text) return;
      input.value = '';
      this.appendMessage('user', text);
      this.setLoading(true);

      var loadingEl = this.shadowRoot.querySelector('.chat-loading');
      if (loadingEl) loadingEl.style.display = 'block';

      var self = this;
      fetch(API_BASE + '/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history: this.buildHistory().slice(0, -1) })
      })
        .then(function(r) { return r.json(); })
        .then(function(data) {
          self.appendMessage('assistant', data.response || 'Desculpe, ocorreu um erro.');
        })
        .catch(function() {
          self.appendMessage('assistant', 'Não foi possível conectar. Tente novamente.');
        })
        .finally(function() {
          self.setLoading(false);
          if (self.shadowRoot.querySelector('.chat-loading'))
            self.shadowRoot.querySelector('.chat-loading').style.display = 'none';
        });
    }

    render() {
      var self = this;
      this.shadowRoot.innerHTML = `
        <style>
          :host {
            --primary-color: #ffffff;
            --text-color: #333;
            --accent-color: #007bff;
            --shadow: 0 8px 24px rgba(0,0,0,0.15);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          }
          .chat-trigger {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--accent-color);
            box-shadow: var(--shadow);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 999999;
            transition: transform 0.3s ease;
          }
          .chat-trigger:hover { transform: scale(1.1); }
          .widget-container {
            position: fixed;
            bottom: 90px;
            right: 20px;
            width: 350px;
            height: 500px;
            background: var(--primary-color);
            border-radius: 12px;
            box-shadow: var(--shadow);
            display: none;
            flex-direction: column;
            overflow: hidden;
            z-index: 999999;
            border: 1px solid #eee;
          }
          .chat-header {
            padding: 15px;
            background: #f8f9fa;
            border-bottom: 1px solid #eee;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
          }
          .chat-messages {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            background: #fff;
          }
          .message {
            margin-bottom: 10px;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 14px;
            max-width: 80%;
          }
          .message.user { background: #007bff; color: #fff; margin-left: auto; }
          .message.bot { background: #e9ecef; }
          .chat-loading {
            display: none;
            padding: 8px 12px;
            font-size: 13px;
            color: #666;
          }
          .chat-input-area {
            padding: 15px;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
          }
          .chat-input-area input {
            flex: 1;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px;
            outline: none;
          }
          button#send {
            background: var(--accent-color);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 4px;
            cursor: pointer;
          }
          button#send:disabled { opacity: 0.6; cursor: not-allowed; }
        </style>
        <div class="widget-container">
          <div class="chat-header">
            <span>Suporte Online</span>
            <span style="cursor:pointer" id="close-chat">✕</span>
          </div>
          <div class="chat-messages">
            <div class="message bot">Olá! Como posso ajudar você hoje?</div>
          </div>
          <div class="chat-loading">Digitando...</div>
          <div class="chat-input-area">
            <input type="text" placeholder="Digite sua mensagem..." id="chat-input">
            <button id="send">Enviar</button>
          </div>
        </div>
        <div class="chat-trigger">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        </div>
      `;

      this.shadowRoot.querySelector('.chat-trigger').addEventListener('click', function() { self.toggleChat(); });
      this.shadowRoot.querySelector('#close-chat').addEventListener('click', function() { self.toggleChat(); });
      this.shadowRoot.querySelector('#send').addEventListener('click', function() { self.sendMessage(); });
      this.shadowRoot.querySelector('#chat-input').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') self.sendMessage();
      });
    }
  }

  customElements.define('chat-widget', ChatWidget);
  var widget = document.createElement('chat-widget');
  document.body.appendChild(widget);
})();
