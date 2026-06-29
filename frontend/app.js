const questionInput = document.querySelector('#question');
const userStoryIdInput = document.querySelector('#userStoryId');
const generateBtn = document.querySelector('#generateBtn');
const refreshBtn = document.querySelector('#refreshBtn');
const statusEl = document.querySelector('#status');
const previewEl = document.querySelector('#preview');
const rawEl = document.querySelector('#raw');

function setStatus(message, type = '') {
  statusEl.textContent = message;
  statusEl.className = `status ${type}`.trim();
}

function escapeHtml(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function inlineMarkdown(value) {
  return escapeHtml(value)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>');
}

function renderMarkdown(markdown) {
  const lines = markdown.split('\n');
  const html = [];
  let inList = false;
  let inCode = false;
  let codeLines = [];

  function closeList() {
    if (inList) {
      html.push('</ul>');
      inList = false;
    }
  }

  for (const line of lines) {
    if (line.trim().startsWith('```')) {
      if (inCode) {
        html.push(`<pre><code>${escapeHtml(codeLines.join('\n'))}</code></pre>`);
        codeLines = [];
        inCode = false;
      } else {
        closeList();
        inCode = true;
      }
      continue;
    }

    if (inCode) {
      codeLines.push(line);
      continue;
    }

    if (!line.trim()) {
      closeList();
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      closeList();
      const level = heading[1].length;
      html.push(`<h${level}>${inlineMarkdown(heading[2])}</h${level}>`);
      continue;
    }

    const bullet = line.match(/^\s*[-*]\s+(.+)$/);
    if (bullet) {
      if (!inList) {
        html.push('<ul>');
        inList = true;
      }
      html.push(`<li>${inlineMarkdown(bullet[1])}</li>`);
      continue;
    }

    const quote = line.match(/^>\s?(.+)$/);
    if (quote) {
      closeList();
      html.push(`<blockquote>${inlineMarkdown(quote[1])}</blockquote>`);
      continue;
    }

    closeList();
    html.push(`<p>${inlineMarkdown(line)}</p>`);
  }

  closeList();
  if (inCode) {
    html.push(`<pre><code>${escapeHtml(codeLines.join('\n'))}</code></pre>`);
  }

  return html.join('\n');
}

async function loadMarkdown() {
  setStatus('Loading generated markdown...');
  const response = await fetch('/generated_md/user_story.md', { cache: 'no-store' });

  if (!response.ok) {
    throw new Error('Could not load generated_md/user_story.md. Generate a user story first.');
  }

  const markdown = await response.text();
  rawEl.textContent = markdown || 'File is empty.';
  previewEl.classList.toggle('empty', !markdown.trim());
  previewEl.innerHTML = markdown.trim() ? renderMarkdown(markdown) : 'File is empty.';
  setStatus('Markdown loaded from generated_md/user_story.md', 'success');
}

async function generateUserStory() {
  const question = questionInput.value.trim();
  const userStoryId = userStoryIdInput.value.trim();

  if (!userStoryId) {
    setStatus('Please enter a user story ID first.', 'error');
    userStoryIdInput.focus();
    return;
  }

  if (!question) {
    setStatus('Please enter a requirement first.', 'error');
    questionInput.focus();
    return;
  }

  generateBtn.disabled = true;
  refreshBtn.disabled = true;
  setStatus('Generating user story. This can take a while...');

  try {
    const response = await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_input: question,
        UserStoryId: userStoryId,
      }),
    });
    const data = await response.json();

    if (!response.ok || data.success === false) {
      throw new Error(data.error || 'Backend returned an error.');
    }

    if (data.user_story) {
      rawEl.textContent = data.user_story;
      previewEl.classList.remove('empty');
      previewEl.innerHTML = renderMarkdown(data.user_story);
      setStatus('Generated successfully and displayed latest user story.', 'success');
      return;
    }

    await loadMarkdown();
  } catch (error) {
    setStatus(error.message, 'error');
  } finally {
    generateBtn.disabled = false;
    refreshBtn.disabled = false;
  }
}

refreshBtn.addEventListener('click', () => {
  loadMarkdown().catch((error) => setStatus(error.message, 'error'));
});

generateBtn.addEventListener('click', generateUserStory);

loadMarkdown().catch(() => {
  setStatus('Start FastAPI on port 8000, then generate or refresh.');
});
