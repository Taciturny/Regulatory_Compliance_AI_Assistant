const form = document.querySelector('#assistant-form');
const input = document.querySelector('#message-input');
const tabs = [...document.querySelectorAll('.mode-tab')];
const description = document.querySelector('#mode-description');
const suggestions = document.querySelector('#suggestions');
const inputLabel = document.querySelector('#input-label');
const inputHint = document.querySelector('#input-hint');
const buttonLabel = document.querySelector('#button-label');
const answerCard = document.querySelector('#answer-card');
const answerText = document.querySelector('#answer-text');
const errorBanner = document.querySelector('#error-banner');
let mode = 'ask';
let answerMarkdown = '';

const themeToggle = document.querySelector('#theme-toggle');
const savedTheme = (() => {
  try { return localStorage.getItem('civicdata-theme'); } catch { return null; }
})();
const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
let hasSavedTheme = savedTheme === 'dark' || savedTheme === 'light';

function applyTheme(theme, save = false) {
  const isDark = theme === 'dark';
  document.documentElement.dataset.theme = isDark ? 'dark' : 'light';
  document.querySelector('meta[name="theme-color"]').content = isDark ? '#101713' : '#f7faf7';
  themeToggle.setAttribute('aria-pressed', String(isDark));
  themeToggle.setAttribute('aria-label', `Switch to ${isDark ? 'light' : 'dark'} mode`);
  themeToggle.querySelector('.theme-icon').textContent = isDark ? '☀' : '☾';
  themeToggle.querySelector('.theme-label').textContent = isDark ? 'Light mode' : 'Dark mode';
  if (save) {
    try { localStorage.setItem('civicdata-theme', theme); } catch { /* Theme still works for this visit. */ }
  }
}

applyTheme(hasSavedTheme ? savedTheme : (systemTheme.matches ? 'dark' : 'light'));
themeToggle.addEventListener('click', () => {
  const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  hasSavedTheme = true;
  applyTheme(nextTheme, true);
});

systemTheme.addEventListener('change', (event) => {
  if (!hasSavedTheme) applyTheme(event.matches ? 'dark' : 'light');
});

function escapeHTML(value) {
  return value.replace(/[&<>"']/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  })[character]);
}

function renderInlineMarkdown(value) {
  return escapeHTML(value)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*([^*]+)\*(?!\*)/g, '$1<em>$2</em>')
    .replace(/\[(\d+)\]/g, '<sup class="citation">[$1]</sup>');
}

function renderMarkdown(markdown) {
  const output = [];
  const lines = markdown.replace(/\r/g, '').split('\n');
  let paragraph = [];
  let list = '';

  const closeList = () => {
    if (list) output.push(`</${list}>`);
    list = '';
  };
  const flushParagraph = () => {
    if (paragraph.length) output.push(`<p>${renderInlineMarkdown(paragraph.join(' '))}</p>`);
    paragraph = [];
  };

  for (const line of lines) {
    const trimmed = line.trim();
    const heading = trimmed.match(/^(#{1,3})\s+(.+)$/);
    const unordered = trimmed.match(/^[-*]\s+(.+)$/);
    const ordered = trimmed.match(/^\d+[.)]\s+(.+)$/);
    if (!trimmed || heading || unordered || ordered || /^[-*_]{3,}$/.test(trimmed)) {
      flushParagraph();
      if (!unordered && !ordered) closeList();
      if (heading) {
        const level = Math.min(heading[1].length + 1, 4);
        output.push(`<h${level}>${renderInlineMarkdown(heading[2])}</h${level}>`);
      } else if (unordered || ordered) {
        const nextList = unordered ? 'ul' : 'ol';
        if (list && list !== nextList) closeList();
        if (!list) {
          list = nextList;
          output.push(`<${list}>`);
        }
        output.push(`<li>${renderInlineMarkdown((unordered || ordered)[1])}</li>`);
      }
      continue;
    }
    closeList();
    paragraph.push(trimmed);
  }
  flushParagraph();
  closeList();
  answerText.innerHTML = output.join('');
}

const askMode = {
  description: 'Ask anything about your rights and how organisations should handle your personal data.',
  placeholder: 'Type your question here…', label: 'Your question', hint: 'Be as specific as you like. Please leave out names, account numbers, or other personal details.', button: 'Get an answer',
  examples: ['What are my data rights?', 'Can my data be shared?', 'How does consent work?'],
  prompts: ['What rights do I have if a company has my personal information?', 'Can an organisation share my personal data with another company?', 'What does the Nigeria Data Protection Act say about consent?'],
};

function setMode(nextMode) {
  mode = nextMode;
  tabs.forEach((tab) => {
    const active = tab.dataset.mode === mode;
    tab.classList.toggle('active', active);
    tab.setAttribute('aria-selected', String(active));
  });
  const copy = askMode;
  description.textContent = copy.description;
  input.placeholder = copy.placeholder;
  inputLabel.textContent = copy.label;
  inputHint.textContent = copy.hint;
  buttonLabel.textContent = copy.button;
  suggestions.replaceChildren(...copy.examples.map((label, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = label;
    button.dataset.prompt = copy.prompts[index];
    return button;
  }));
  answerCard.hidden = true;
  errorBanner.hidden = true;
}

tabs.forEach((tab) => tab.addEventListener('click', () => setMode(tab.dataset.mode)));
suggestions.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-prompt]');
  if (button) {
    input.value = button.dataset.prompt;
    input.dispatchEvent(new Event('input'));
    input.focus();
  }
});
input.addEventListener('input', () => { document.querySelector('#char-count').textContent = `${input.value.length.toLocaleString()} / 12,000`; });

async function checkStatus() {
  const pill = document.querySelector('#status-pill');
  const label = document.querySelector('#status-label');
  try {
    const response = await fetch('/api/status');
    const status = await response.json();
    pill.classList.toggle('ready', status.ready && status.sources_loaded);
    label.textContent = status.ready ? (status.sources_loaded ? 'Ready to help' : 'Legal library unavailable') : 'Model setup needed';
  } catch {
    label.textContent = 'Connection unavailable';
  }
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  const button = document.querySelector('#submit-button');
  const previousLabel = buttonLabel.textContent;
  button.disabled = true;
  buttonLabel.textContent = 'Reading the law…';
  errorBanner.hidden = true;
  answerCard.hidden = true;
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, mode }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Could not generate an answer. Please try again.');
    answerMarkdown = data.answer;
    renderMarkdown(answerMarkdown);
    const modeLabel = 'Question answered';
    document.querySelector('#answer-mode').textContent = data.provider === 'cohere'
      ? `${modeLabel} · Cohere backup`
      : `${modeLabel} · Gemini`;
    const sourceArea = document.querySelector('#sources-area');
    sourceArea.replaceChildren();
    if (data.sources?.length) {
      const title = document.createElement('div');
      title.className = 'sources-title';
      title.textContent = 'LEGAL SOURCES';
      sourceArea.append(title);
      for (const source of data.sources) {
        const link = document.createElement('a');
        link.className = 'source-chip';
        link.href = source.url;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = `${source.label} ↗`;
        sourceArea.append(link);
      }
    }
    answerCard.hidden = false;
    answerCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } catch (error) {
    errorBanner.textContent = error.message;
    errorBanner.hidden = false;
  } finally {
    button.disabled = false;
    buttonLabel.textContent = previousLabel;
  }
});

document.querySelector('#copy-answer').addEventListener('click', async (event) => {
  try {
    await navigator.clipboard.writeText(answerMarkdown);
    event.currentTarget.textContent = 'Copied';
    setTimeout(() => { event.currentTarget.textContent = 'Copy'; }, 1500);
  } catch {
    event.currentTarget.textContent = 'Select to copy';
  }
});

document.querySelector('.mobile-menu').addEventListener('click', (event) => {
  const nav = document.querySelector('.top-nav');
  const expanded = event.currentTarget.getAttribute('aria-expanded') === 'true';
  event.currentTarget.setAttribute('aria-expanded', String(!expanded));
  nav.classList.toggle('open', !expanded);
});

checkStatus();
