/* ==================== API BASE URL ==================== */

const API_BASE = '/api';

/* ==================== DOM ELEMENTS ==================== */

const navBtns = document.querySelectorAll('.nav-btn');
const tabContents = document.querySelectorAll('.tab-content');
const loadingSpinner = document.getElementById('loadingSpinner');

// Essay elements
const essayForm = document.getElementById('essayForm');
const essayResult = document.getElementById('essayResult');

// Email elements
const emailForm = document.getElementById('emailForm');
const emailResult = document.getElementById('emailResult');

// Improve elements
const improveForm = document.getElementById('improveForm');
const improveResult = document.getElementById('improveResult');

// Grammar elements
const grammarForm = document.getElementById('grammarForm');
const grammarResult = document.getElementById('grammarResult');

/* ==================== EVENT LISTENERS ==================== */

// Navigation
navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        showTab(tabName);
    });
});

// Chat elements
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const chatMessages = document.getElementById('chatMessages');

// Form submissions
essayForm.addEventListener('submit', handleEssaySubmit);
emailForm.addEventListener('submit', handleEmailSubmit);
improveForm.addEventListener('submit', handleImproveSubmit);
grammarForm.addEventListener('submit', handleGrammarSubmit);
chatForm.addEventListener('submit', handleChatSubmit);

/* ==================== TAB NAVIGATION ==================== */

function showTab(tabName) {
    // Hide all tabs
    tabContents.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all buttons
    navBtns.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

/* ==================== LOADING STATE ==================== */

function showLoading() {
    loadingSpinner.classList.remove('hidden');
}

function hideLoading() {
    loadingSpinner.classList.add('hidden');
}

/* ==================== CHAT HANDLER ==================== */

async function handleChatSubmit(e) {
    e.preventDefault();
    
    const message = chatInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addChatMessage(message, 'user');
    chatInput.value = '';
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to get response');
        }
        
        // Add AI response to chat
        addChatMessage(data.reply, 'ai');
    } catch (error) {
        addChatMessage('❌ Error: ' + error.message, 'ai');
    } finally {
        hideLoading();
    }
}

function addChatMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    messageDiv.innerHTML = `<div class="chat-text">${escapeHtml(text)}</div>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/* ==================== ESSAY HANDLER ==================== */

async function handleEssaySubmit(e) {
    e.preventDefault();
    
    const topic = document.getElementById('essayTopic').value.trim();
    const style = document.getElementById('essayStyle').value;
    const length = document.getElementById('essayLength').value;
    const checkGrammar = document.getElementById('essayGrammar').checked;
    
    if (!topic) {
        showError('Please enter an essay topic');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/generate/essay`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic,
                style,
                length,
                check_grammar: checkGrammar
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate essay');
        }
        
        displayEssayResult(data);
    } catch (error) {
        showError('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayEssayResult(data) {
    document.getElementById('essayOutput').textContent = data.essay;
    
    // Show stats
    const statsHtml = `
        <div class="stat-box">
            <div class="label">Word Count</div>
            <div class="value">${data.word_count}</div>
        </div>
        <div class="stat-box">
            <div class="label">Style</div>
            <div class="value">${data.style_used}</div>
        </div>
    `;
    document.getElementById('essayStats').innerHTML = statsHtml;
    
    // Show grammar issues if any
    if (data.grammar_issues && data.grammar_issues.length > 0) {
        displayGrammarIssues('essay', data.grammar_issues);
    } else {
        document.getElementById('essayIssues').classList.add('hidden');
    }
    
    essayResult.classList.remove('hidden');
    essayResult.scrollIntoView({ behavior: 'smooth' });
}

/* ==================== EMAIL HANDLER ==================== */

async function handleEmailSubmit(e) {
    e.preventDefault();
    
    const recipient = document.getElementById('emailRecipient').value.trim();
    const purpose = document.getElementById('emailPurpose').value.trim();
    const tone = document.getElementById('emailTone').value;
    const pointsText = document.getElementById('emailPoints').value;
    const keyPoints = pointsText.split('\n').filter(p => p.trim());
    const checkGrammar = document.getElementById('emailGrammar').checked;
    
    if (!purpose) {
        showError('Please enter an email purpose');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/generate/email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                recipient,
                purpose,
                tone,
                key_points: keyPoints,
                check_grammar: checkGrammar
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate email');
        }
        
        displayEmailResult(data);
    } catch (error) {
        showError('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayEmailResult(data) {
    document.getElementById('emailOutput').textContent = data.email;
    
    // Show grammar issues if any
    if (data.grammar_issues && data.grammar_issues.length > 0) {
        displayGrammarIssues('email', data.grammar_issues);
    } else {
        document.getElementById('emailIssues').classList.add('hidden');
    }
    
    emailResult.classList.remove('hidden');
    emailResult.scrollIntoView({ behavior: 'smooth' });
}

/* ==================== IMPROVE HANDLER ==================== */

async function handleImproveSubmit(e) {
    e.preventDefault();
    
    const text = document.getElementById('improveText').value.trim();
    const improvementType = document.getElementById('improveType').value;
    
    if (!text) {
        showError('Please enter text to improve');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/improve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text,
                improvement_type: improvementType
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to improve text');
        }
        
        displayImproveResult(data);
    } catch (error) {
        showError('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayImproveResult(data) {
    document.getElementById('improveOriginal').textContent = data.original;
    document.getElementById('improveImproved').textContent = data.improved;
    
    improveResult.classList.remove('hidden');
    improveResult.scrollIntoView({ behavior: 'smooth' });
}

/* ==================== GRAMMAR HANDLER ==================== */

async function handleGrammarSubmit(e) {
    e.preventDefault();
    
    const text = document.getElementById('grammarText').value.trim();
    
    if (!text) {
        showError('Please enter text to check');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/check-grammar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to check grammar');
        }
        
        displayGrammarResult(data);
    } catch (error) {
        showError('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayGrammarResult(data) {
    const statsHtml = `
        <div class="stat-box">
            <div class="label">Issues Found</div>
            <div class="value">${data.issues_found}</div>
        </div>
    `;
    document.getElementById('grammarStats').innerHTML = statsHtml;
    
    const issuesContainer = document.getElementById('grammarIssues');
    issuesContainer.innerHTML = '';
    
    if (data.issues_found === 0) {
        issuesContainer.innerHTML = '<div class="grammar-issue" style="background: #dcfce7; border-left-color: #10b981; color: #166534;">✓ No issues found! Your text looks great.</div>';
    } else {
        data.issues.forEach((issue, index) => {
            const issueEl = document.createElement('div');
            issueEl.className = 'grammar-issue';
            
            let suggestionsHtml = '';
            if (issue.suggestions && issue.suggestions.length > 0) {
                suggestionsHtml = `<div class="suggestion">💡 Suggestion: <strong>${issue.suggestions[0]}</strong></div>`;
            }
            
            issueEl.innerHTML = `
                <div style="font-weight: 600; margin-bottom: 5px;">${index + 1}. ${issue.message}</div>
                ${suggestionsHtml}
            `;
            
            issuesContainer.appendChild(issueEl);
        });
    }
    
    grammarResult.classList.remove('hidden');
    grammarResult.scrollIntoView({ behavior: 'smooth' });
}

/* ==================== GRAMMAR ISSUES DISPLAY ==================== */

function displayGrammarIssues(type, issues) {
    const issuesContainer = document.getElementById(`${type}Issues`);
    issuesContainer.innerHTML = '';
    issuesContainer.classList.remove('hidden');
    
    if (issues.length === 0) {
        issuesContainer.innerHTML = '<div style="color: var(--success-color); font-weight: 600;">✓ No grammar issues found!</div>';
        return;
    }
    
    const issuesHtml = issues.map((issue, index) => `
        <div class="issue-item">
            <div class="message">${index + 1}. ${issue.message}</div>
            ${issue.suggestions.length > 0 ? `<div class="suggestion">💡 Suggestion: <strong>${issue.suggestions[0]}</strong></div>` : ''}
        </div>
    `).join('');
    
    issuesContainer.innerHTML = `<h4>⚠️ Grammar Issues (${issues.length})</h4>${issuesHtml}`;
}

/* ==================== UTILITY FUNCTIONS ==================== */

function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).textContent;
    navigator.clipboard.writeText(text).then(() => {
        showSuccess('Copied to clipboard!');
    }).catch(() => {
        showError('Failed to copy');
    });
}

function downloadText(elementId, filename) {
    const text = document.getElementById(elementId).textContent;
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', `${filename}_${new Date().toISOString().split('T')[0]}.txt`);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    showSuccess('File downloaded!');
}

function showError(message) {
    alert('❌ ' + message);
}

function showSuccess(message) {
    console.log('✅ ' + message);
}

/* ==================== INITIALIZATION ==================== */

document.addEventListener('DOMContentLoaded', () => {
    console.log('RakanGPT Web Interface Loaded');
});
