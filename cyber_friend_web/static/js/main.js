// Utility: Show/hide loading spinner
function showLoading() {}
function hideLoading() {}

// Welcome Page Flow
document.getElementById('get-started-btn').addEventListener('click', () => {
    fadeOutIn('welcome-page', 'avatar-setup-page');
});

// Avatar Setup
let selectedGender = 'male';
let selectedAvatar = 'male-avatar';

// Gender buttons
document.querySelectorAll('.gender-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.gender-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedGender = btn.dataset.gender;
        updateAvatarOptions();
    });
});

// Avatar options
document.querySelectorAll('.avatar-option').forEach(option => {
    option.addEventListener('click', () => {
        document.querySelectorAll('.avatar-option').forEach(o => o.classList.remove('active'));
        option.classList.add('active');
        selectedAvatar = option.dataset.avatar;
    });
});

function updateAvatarOptions() {
    const avatarOptions = document.querySelectorAll('.avatar-option');
    if (selectedGender === 'male') {
        avatarOptions[0].style.display = 'block';
        avatarOptions[1].style.display = 'none';
        avatarOptions[0].classList.add('active');
        selectedAvatar = 'male-avatar';
    } else {
        avatarOptions[0].style.display = 'none';
        avatarOptions[1].style.display = 'block';
        avatarOptions[1].classList.add('active');
        selectedAvatar = 'female-avatar';
    }
}

// Function to update avatar display
function updateAvatarDisplay(avatarType) {
    const preview = document.getElementById('avatar-preview');
    const sidebarAvatar = document.getElementById('sidebar-avatar');
    
    let avatarUrl = '';
    if (avatarType === 'male-avatar') {
        avatarUrl = 'https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/svg/1f468.svg';
    } else if (avatarType === 'female-avatar') {
        avatarUrl = 'https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/svg/1f469.svg';
    }
    
    if (preview) {
        preview.innerHTML = `<img src="${avatarUrl}" alt="Avatar Preview" class="avatar-gif">`;
        preview.className = `animated-avatar ${avatarType}`;
    }
    
    if (sidebarAvatar) {
        sidebarAvatar.innerHTML = `<img src="${avatarUrl}" alt="Avatar" class="avatar-gif">`;
        sidebarAvatar.className = `animated-avatar ${avatarType}`;
    }
}

// Avatar setup form
document.getElementById('avatar-setup-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('Form submitted!');
    
    const userName = document.getElementById('user-name').value.trim();
    const aiName = document.getElementById('setup-name').value.trim();
    
    console.log('User name:', userName);
    console.log('AI name:', aiName);
    console.log('Selected gender:', selectedGender);
    console.log('Selected avatar:', selectedAvatar);
    
    if (!userName || !aiName) {
        alert('Please enter both your name and your companion\'s name!');
        return;
    }
    
    const avatarInfo = {
        user_name: userName,
        name: aiName,
        gender: selectedGender,
        avatar: selectedAvatar
    };
    
    console.log('Sending avatar info:', avatarInfo);
    
    try {
        const response = await fetch('/api/avatar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(avatarInfo)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        console.log('Avatar setup successful!');
        fadeOutIn('avatar-setup-page', 'main-app', true);
        document.getElementById('sidebar-name').textContent = aiName;
        updateAvatarDisplay(selectedAvatar);
        window.avatarInfo = avatarInfo;
    } catch (error) {
        console.error('Error setting up avatar:', error);
        alert('Error setting up avatar. Please try again.');
    }
});

// Navigation
const navItems = document.querySelectorAll('.sidebar nav li');
const sections = document.querySelectorAll('.section');
navItems.forEach((item, idx) => {
    item.addEventListener('click', () => {
        navItems.forEach(i => i.classList.remove('active'));
        item.classList.add('active');
        sections.forEach(s => s.classList.remove('active', 'fade-in', 'slide-in'));
        let section;
        if (idx === 0) section = document.getElementById('chat-section');
        if (idx === 1) section = document.getElementById('mood-section');
        if (idx === 2) section = document.getElementById('journal-section');
        if (idx === 3) section = document.getElementById('avatar-section');
        section.classList.add('active', 'fade-in');
        setTimeout(() => section.classList.remove('fade-in'), 500);
    });
});

// Chat
let chatHistory = [];
const chatArea = document.getElementById('chat-area');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');

function addChatBubble(message, isUser) {
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble ' + (isUser ? 'user' : 'ai') + ' fade-in';
    bubble.textContent = message;
    chatArea.appendChild(bubble);
    chatArea.scrollTop = chatArea.scrollHeight;
    setTimeout(() => bubble.classList.remove('fade-in'), 500);
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = chatInput.value.trim();
    if (!msg) return;
    addChatBubble(msg, true);
    chatHistory.push({ role: 'user', content: msg });
    chatInput.value = '';
    addChatBubble('...', false);
    const resp = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: chatHistory, user_info: window.avatarInfo || {} })
    });
    const data = await resp.json();
    chatArea.removeChild(chatArea.lastChild);
    addChatBubble(data.reply, false);
    chatHistory.push({ role: 'assistant', content: data.reply });
});

// --- MOOD DASHBOARD LOGIC (NEW) ---

// Mood Dashboard selectors
const moodSelector = document.getElementById('moodSelector');
const moodNote = document.getElementById('moodNote');
const saveMoodBtn = document.getElementById('saveMoodBtn');
const moodHistory = document.getElementById('moodHistory');
const statTotal = document.getElementById('totalEntries');
const statStreak = document.getElementById('currentStreak');
const statAvg = document.getElementById('avgMood');
const statWeek = document.getElementById('thisWeek');

let selectedMood = null;

const moodEmojis = {
    Amazing: '🤩',
    Happy: '😊',
    Good: '🙂',
    Neutral: '😐',
    Sad: '😢',
    Anxious: '😰'
};

// Mood selection (card-based, only .mood-option)
if (moodSelector && saveMoodBtn) {
    moodSelector.addEventListener('click', (e) => {
        const moodOption = e.target.closest('.mood-option');
        if (!moodOption) return;
        document.querySelectorAll('.mood-option').forEach(option => option.classList.remove('selected'));
        moodOption.classList.add('selected');
        selectedMood = moodOption.dataset.mood;
        saveMoodBtn.disabled = false;
    });
}

// Save mood entry
if (saveMoodBtn && moodNote) {
    saveMoodBtn.addEventListener('click', async () => {
        if (!selectedMood) return;
        const note = moodNote.value.trim();
        const today = new Date().toISOString().slice(0, 10);
        // Save to backend
        await fetch('/api/mood', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ date: today, mood: selectedMood, note })
        });
        // Add to UI
        if (typeof loadMoodDashboard === 'function') await loadMoodDashboard();
        // Reset form
        document.querySelectorAll('.mood-option').forEach(option => option.classList.remove('selected'));
        moodNote.value = '';
        selectedMood = null;
        saveMoodBtn.disabled = true;
        // Feedback
        saveMoodBtn.textContent = 'Saved! ✓';
        saveMoodBtn.style.background = '#059669';
        setTimeout(() => {
            saveMoodBtn.textContent = 'Save Mood Entry';
            saveMoodBtn.style.background = '#10b981';
        }, 2000);
    });
}

// Load mood dashboard (stats + history)
async function loadMoodDashboard() {
    // Fetch all moods
    const resp = await fetch('/api/mood/history');
    const moods = await resp.json();
    // Render history
    if (moodHistory) {
        moodHistory.innerHTML = '';
        moods.slice(0, 10).forEach(entry => {
            const div = document.createElement('div');
            div.className = 'mood-entry';
            div.innerHTML = `
                <div class="entry-header">
                    <div class="entry-mood">
                        <span class="entry-emoji">${moodEmojis[entry.mood] || '❓'}</span>
                        <span class="entry-mood-name">${entry.mood}</span>
                    </div>
                    <span class="entry-date">${formatDate(entry.date)}</span>
                </div>
                <div class="entry-note">${entry.note ? escapeHtml(entry.note) : 'No notes added.'}</div>
            `;
            moodHistory.appendChild(div);
        });
    }
    // Stats
    if (statTotal) statTotal.textContent = moods.length;
    if (statWeek) statWeek.textContent = countThisWeek(moods);
    if (statStreak) statStreak.textContent = calcStreak(moods);
    if (statAvg) statAvg.textContent = getMostCommonMood(moods);
}

function formatDate(dateStr) {
    const today = new Date().toISOString().slice(0, 10);
    if (dateStr === today) return 'Today';
    const d = new Date(dateStr);
    const diff = Math.floor((new Date(today) - d) / (1000*60*60*24));
    if (diff === 1) return 'Yesterday';
    if (diff < 7) return `${diff} days ago`;
    return d.toLocaleDateString();
}
function escapeHtml(str) {
    return str.replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\'':'&#39;','"':'&quot;'}[c]));
}
function countThisWeek(moods) {
    const now = new Date();
    return moods.filter(m => {
        const d = new Date(m.date);
        return (now - d) / (1000*60*60*24) < 7;
    }).length;
}
function getMostCommonMood(moods) {
    if (!moods.length) return '-';
    const freq = {};
    moods.forEach(m => { freq[m.mood] = (freq[m.mood]||0)+1; });
    let max = 0, mood = '-';
    Object.entries(freq).forEach(([k,v]) => { if (v>max) { max=v; mood=k; } });
    return moodEmojis[mood] || '-';
}
function calcStreak(moods) {
    if (!moods.length) return 0;
    let streak = 0;
    let prev = new Date();
    for (const m of moods) {
        const d = new Date(m.date);
        if (streak === 0) {
            if ((new Date().toISOString().slice(0,10)) !== m.date) break;
        } else {
            if ((prev - d) !== 1000*60*60*24) break;
        }
        streak++;
        prev = d;
    }
    return streak;
}

// Load dashboard on nav or page load
const navMood = document.getElementById('nav-mood');
if (navMood) navMood.addEventListener('click', loadMoodDashboard);
if (document.getElementById('mood-section') && document.getElementById('mood-section').classList.contains('active')) loadMoodDashboard();

// Journal
const journalText = document.getElementById('journal-text');
document.getElementById('save-journal').onclick = async () => {
    const today = new Date().toISOString().slice(0, 10);
    await fetch('/api/journal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ date: today, text: journalText.value })
    });
    alert('Journal entry saved!');
};
async function loadJournal() {
    const today = new Date().toISOString().slice(0, 10);
    const resp = await fetch('/api/journal?date=' + today);
    const data = await resp.json();
    journalText.value = data.text || '';
}
loadJournal();

// Avatar (in main app)
const avatarForm = document.getElementById('avatar-form');
const avatarName = document.getElementById('avatar-name');
const avatarGender = document.getElementById('avatar-gender');
const avatarSelect = document.getElementById('avatar-select');
const avatarPreview = document.getElementById('avatar-preview');

avatarSelect.onchange = () => {
    updateAvatarDisplay(avatarSelect.value);
};
avatarForm.onsubmit = async (e) => {
    e.preventDefault();
    const info = {
        name: avatarName.value,
        gender: avatarGender.value,
        avatar: avatarSelect.value,
        user_name: window.avatarInfo ? window.avatarInfo.user_name : ''
    };
    await fetch('/api/avatar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(info)
    });
    window.avatarInfo = info;
    document.getElementById('sidebar-name').textContent = info.name;
    updateAvatarDisplay(info.avatar);
    alert('Avatar updated!');
};
async function loadAvatar() {
    const resp = await fetch('/api/avatar');
    const data = await resp.json();
    if (data.name) {
        avatarName.value = data.name;
        avatarGender.value = data.gender;
        avatarSelect.value = data.avatar;
        updateAvatarDisplay(data.avatar);
        document.getElementById('sidebar-name').textContent = data.name;
        window.avatarInfo = data;
    }
}
loadAvatar();

// Animation helpers
function fadeOutIn(hideId, showId, isFlex) {
    const hideEl = document.getElementById(hideId);
    const showEl = document.getElementById(showId);
    hideEl.classList.add('fade-out');
    setTimeout(() => {
        hideEl.style.display = 'none';
        hideEl.classList.remove('fade-out');
        showEl.style.display = isFlex ? 'flex' : 'block';
        showEl.classList.add('fade-in');
        setTimeout(() => showEl.classList.remove('fade-in'), 500);
    }, 400);
}

// Emoji Picker
const emojiBtn = document.getElementById('emoji-picker-btn');
const emojiPopover = document.getElementById('emoji-popover');
const chatInputBox = document.getElementById('chat-input');
const emojiList = [
  '😀','😃','😄','😁','😆','😅','😂','🤣','😊','😇','🙂','🙃','😉','😌','😍','🥰','😘','😗','😙','😚','😋','😜','😝','😛','🤑','🤗','🤩','🤔','🤨','😐','😑','😶','🙄','😏','😣','😥','😮','🤐','😯','😪','😫','🥱','😴','😌','😛','😜','😝','🤤','😒','😓','😔','😕','🙃','🫠','🫡','🥲','🥹','😎','🤓','🧐','😕','😟','🙁','☹️','😮‍💨','😤','😠','😡','🤬','😶‍🌫️','😱','😨','😰','😢','😭','😤','😩','😫','🥱','😵','🤯','🤠','🥳','🥸','😺','😸','😹','😻','😼','😽','🙀','😿','😾','👋','🤚','🖐️','✋','🖖','👌','🤌','🤏','✌️','🤞','🫰','🤟','🤘','🤙','🫵','🫱','🫲','🫳','🫴','👏','🙌','👐','🤲','🙏','✍️','💅','🤳','💪','🦾','🦵','🦿','🦶','👣','👀','👁️','👅','👄','🧠','🦷','🦴','👶','🧒','👦','👧','🧑','👱‍♂️','👱‍♀️','👨','👩','🧔','👵','🧓','👴','👲','👳‍♂️','👳‍♀️','🧕','👮‍♂️','👮‍♀️','👷‍♂️','👷‍♀️','💂‍♂️','💂‍♀️','🕵️‍♂️','🕵️‍♀️','👩‍⚕️','👨‍⚕️','👩‍🎓','👨‍🎓','👩‍🏫','👨‍🏫','👩‍⚖️','👨‍⚖️','👩‍🌾','👨‍🌾','👩‍🍳','👨‍🍳','👩‍🎤','👨‍🎤','👩‍🎨','👨‍🎨','👩‍✈️','👨‍✈️','👩‍🚀','👨‍🚀','👩‍🚒','👨‍🚒','👸','🤴','👰','🤵','🤰','🤱','👩‍🍼','👨‍🍼','🧑‍🍼','👼','🎅','🤶','🧑‍🎄','🦸‍♀️','🦸‍♂️','🦹‍♀️','🦹‍♂️','🧙‍♀️','🧙‍♂️','🧚‍♀️','🧚‍♂️','🧛‍♀️','🧛‍♂️','🧜‍♀️','🧜‍♂️','🧝‍♀️','🧝‍♂️','🧞‍♀️','🧞‍♂️','🧟‍♀️','🧟‍♂️','💆‍♀️','💆‍♂️','💇‍♀️','💇‍♂️','🚶‍♀️','🚶‍♂️','🏃‍♀️','🏃‍♂️','💃','🕺','🕴️','👯‍♀️','👯‍♂️','🧖‍♀️','🧖‍♂️','🧘‍♀️','🧘‍♂️','👭','👫','👬','💏','💑','👪','🗣️','👤','👥','🫂','👣'];

emojiBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (emojiPopover.style.display === 'none') {
        emojiPopover.innerHTML = emojiList.map(e => `<span>${e}</span>`).join('');
        emojiPopover.style.display = 'flex';
        // Position popover near the button
        const rect = emojiBtn.getBoundingClientRect();
        emojiPopover.style.left = (rect.left - 60) + 'px';
        emojiPopover.style.bottom = '60px';
    } else {
        emojiPopover.style.display = 'none';
    }
});

emojiPopover.addEventListener('click', (e) => {
    if (e.target.tagName === 'SPAN') {
        chatInputBox.value += e.target.textContent;
        emojiPopover.style.display = 'none';
        chatInputBox.focus();
    }
});

document.addEventListener('click', (e) => {
    if (!emojiPopover.contains(e.target) && e.target !== emojiBtn) {
        emojiPopover.style.display = 'none';
    }
});

// Mobile optimizations
function initMobileOptimizations() {
    // Prevent zoom on input focus for iOS
    const inputs = document.querySelectorAll('input[type="text"], textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            if (window.innerWidth <= 768) {
                input.style.fontSize = '16px'; // Prevents zoom on iOS
            }
        });
    });
    
    // Better touch handling for buttons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.95)';
        });
        
        button.addEventListener('touchend', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Auto-hide emoji picker on mobile when clicking outside
    document.addEventListener('click', (e) => {
        const emojiPopover = document.getElementById('emoji-popover');
        const emojiBtn = document.getElementById('emoji-picker-btn');
        
        if (window.innerWidth <= 768 && emojiPopover && emojiPopover.style.display === 'block') {
            if (!emojiPopover.contains(e.target) && !emojiBtn.contains(e.target)) {
                emojiPopover.style.display = 'none';
            }
        }
    });
    
    // Prevent double-tap zoom on mobile
    let lastTouchEnd = 0;
    document.addEventListener('touchend', function (event) {
        const now = (new Date()).getTime();
        if (now - lastTouchEnd <= 300) {
            event.preventDefault();
        }
        lastTouchEnd = now;
    }, false);
}

// Initialize mobile optimizations when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initMobileOptimizations();
}); 