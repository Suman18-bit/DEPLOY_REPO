const API_URL = window.location.origin;

const elements = {
    messages: document.getElementById('messages'),
    questionInput: document.getElementById('questionInput'),
    sendBtn: document.getElementById('sendBtn'),
    uploadZone: document.getElementById('uploadZone'),
    fileInput: document.getElementById('fileInput'),
    uploadStatusArea: document.getElementById('uploadStatusArea'),
    uploadProgress: document.getElementById('uploadProgress'),
    uploadResult: document.getElementById('uploadResult'),
    progressCircle: document.getElementById('progressCircle'),
    progressPercent: document.getElementById('progressPercent'),
    progressFilename: document.getElementById('progressFilename'),
    progressStatus: document.getElementById('progressStatus'),
    resultIcon: document.getElementById('resultIcon'),
    resultFilename: document.getElementById('resultFilename'),
    resultDetail: document.getElementById('resultDetail'),
    modelName: document.getElementById('modelName'),
    docCount: document.getElementById('docCount'),
    clearBtn: document.getElementById('clearBtn')
};

let documentCount = 0;

fetch(`${API_URL}/health`)
    .then(r => r.json())
    .then(data => {
        elements.modelName.textContent = data.model || 'Mistral Small';
    })
    .catch(() => {
        elements.modelName.textContent = 'Offline';
    });

async function sendMessage() {
    const question = elements.questionInput.value.trim();
    if (!question) return;
    if (question === '0') {
        clearChat();
        elements.questionInput.value = '';
        return;
    }
    addMessage(question, 'user');
    elements.questionInput.value = '';
    elements.sendBtn.disabled = true;
    const typingId = addTypingIndicator();
    try {
        const res = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        removeTypingIndicator(typingId);
        if (!res.ok) throw new Error('Server error');
        const data = await res.json();
        addMessage(data.answer, 'bot', data.sources);
    } catch (err) {
        removeTypingIndicator(typingId);
        addMessage('Sorry, something went wrong. Please try again.', 'bot');
    } finally {
        elements.sendBtn.disabled = false;
        elements.questionInput.focus();
    }
}

function addMessage(text, sender, sources = null) {
    const welcome = elements.messages.querySelector('.welcome-message');
    if (welcome && sender === 'user') welcome.remove();
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    const avatarIcon = sender === 'bot' 
        ? `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/></svg>`
        : `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`;
    let sourcesHtml = '';
    if (sources && sources.length > 0) {
        sourcesHtml = `<div class="sources"><div class="sources-title">Sources</div>${sources.map(s => `<div class="source-item"><strong>${escapeHtml(s.metadata.source || 'Unknown')}</strong> — ${escapeHtml(s.content.substring(0, 120))}...</div>`).join('')}</div>`;
    }
    div.innerHTML = `<div class="message-avatar">${avatarIcon}</div><div class="bubble"><p>${escapeHtml(text)}</p>${sourcesHtml}</div>`;
    elements.messages.appendChild(div);
    scrollToBottom();
}

function addTypingIndicator() {
    const id = 'typing-' + Date.now();
    const div = document.createElement('div');
    div.className = 'message bot';
    div.id = id;
    div.innerHTML = `<div class="message-avatar"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/></svg></div><div class="bubble"><div class="typing-indicator"><span></span><span></span><span></span></div></div>`;
    elements.messages.appendChild(div);
    scrollToBottom();
    return id;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function clearChat() {
    elements.messages.innerHTML = `<div class="welcome-message"><div class="welcome-avatar"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/></svg></div><div class="welcome-content"><h3>Chat Cleared!</h3><p>Upload a document and ask me anything about it.</p><div class="welcome-tips"><div class="tip"><span class="tip-dot tip-blue"></span><span>Upload PDF or TXT files</span></div><div class="tip"><span class="tip-dot tip-green"></span><span>Ask specific questions</span></div><div class="tip"><span class="tip-dot tip-orange"></span><span>Get sourced answers</span></div></div></div></div>`;
}

function scrollToBottom() {
    elements.messages.scrollTop = elements.messages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function setProgress(percent) {
    const circumference = 2 * Math.PI * 16;
    const offset = circumference - (percent / 100) * circumference;
    elements.progressCircle.style.strokeDashoffset = offset;
    elements.progressPercent.textContent = percent + '%';
}

function showUploadProgress(filename) {
    elements.uploadStatusArea.classList.add('active');
    elements.uploadProgress.style.display = 'flex';
    elements.uploadResult.style.display = 'none';
    elements.progressFilename.textContent = filename;
    elements.progressStatus.textContent = 'Uploading...';
    setProgress(0);
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15 + 5;
        if (progress > 90) { progress = 90; clearInterval(interval); }
        setProgress(Math.min(progress, 90));
    }, 200);
    return interval;
}

function showUploadResult(success, filename, detail) {
    elements.uploadProgress.style.display = 'none';
    elements.uploadResult.style.display = 'flex';
    elements.uploadResult.className = 'upload-result ' + (success ? 'success' : 'error');
    elements.resultIcon.textContent = success ? '✓' : '✕';
    elements.resultFilename.textContent = filename;
    elements.resultDetail.textContent = detail;
    if (success) {
        documentCount++;
        elements.docCount.textContent = documentCount + ' indexed';
    }
    setTimeout(() => { elements.uploadStatusArea.classList.remove('active'); }, 5000);
}

elements.sendBtn.addEventListener('click', sendMessage);
elements.questionInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });
elements.clearBtn.addEventListener('click', clearChat);

elements.uploadZone.addEventListener('click', () => elements.fileInput.click());
elements.uploadZone.addEventListener('dragover', (e) => { e.preventDefault(); elements.uploadZone.classList.add('dragover'); });
elements.uploadZone.addEventListener('dragleave', () => { elements.uploadZone.classList.remove('dragover'); });
elements.uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    elements.uploadZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
});
elements.fileInput.addEventListener('change', (e) => { if (e.target.files.length) handleFile(e.target.files[0]); });

async function handleFile(file) {
    const allowedExt = ['.pdf', '.txt'];
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    if (!allowedExt.includes(ext)) {
        showUploadResult(false, file.name, 'Only PDF and TXT files allowed');
        return;
    }
    const progressInterval = showUploadProgress(file.name);
    const formData = new FormData();
    formData.append('file', file);
    try {
        const res = await fetch(`${API_URL}/upload`, { method: 'POST', body: formData });
        clearInterval(progressInterval);
        setProgress(100);
        const contentType = res.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await res.text();
            throw new Error(`Server error: ${text.substring(0, 100)}`);
        }
        const data = await res.json();
        if (res.ok) {
            setTimeout(() => { showUploadResult(true, file.name, `${data.details.chunks} chunks indexed successfully`); }, 300);
        } else {
            throw new Error(data.detail || 'Upload failed');
        }
    } catch (err) {
        clearInterval(progressInterval);
        showUploadResult(false, file.name, err.message);
    }
}