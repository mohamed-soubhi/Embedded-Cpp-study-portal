// Embedded C++ Study Portal Interactive Engine
document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initCopyButtons();
  initQuiz();
  initSearchAndFilters();
});

// Tab Switching
function initTabs() {
  const tabContainers = document.querySelectorAll('.code-viewer');
  tabContainers.forEach(container => {
    const tabs = container.querySelectorAll('.code-tab');
    const panels = container.querySelectorAll('.code-panel');

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetId = tab.getAttribute('data-target');

        tabs.forEach(t => t.classList.remove('active'));
        panels.forEach(p => p.classList.remove('active'));

        tab.classList.add('active');
        const activePanel = container.querySelector(`#${targetId}`);
        if (activePanel) {
          activePanel.classList.add('active');
        }
      });
    });
  });
}

// Copy Code Button
function initCopyButtons() {
  const copyButtons = document.querySelectorAll('.btn-copy');
  copyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const viewer = btn.closest('.code-viewer');
      const activePanel = viewer ? viewer.querySelector('.code-panel.active pre') : null;
      if (!activePanel) return;

      const codeText = activePanel.innerText;
      navigator.clipboard.writeText(codeText).then(() => {
        const originalText = btn.innerHTML;
        btn.innerHTML = '✓ Copied!';
        btn.classList.add('copied');
        setTimeout(() => {
          btn.innerHTML = originalText;
          btn.classList.remove('copied');
        }, 2000);
      }).catch(err => {
        console.error('Failed to copy code: ', err);
      });
    });
  });
}

// Interactive MCQ Quiz Engine
function initQuiz() {
  const quizCards = document.querySelectorAll('.quiz-card');

  quizCards.forEach(card => {
    const options = card.querySelectorAll('.quiz-option');
    const explanation = card.querySelector('.quiz-explanation');
    const correctIndex = parseInt(card.getAttribute('data-correct'), 10);

    options.forEach((opt, index) => {
      opt.addEventListener('click', () => {
        if (card.classList.contains('answered')) return;
        card.classList.add('answered');

        // Disable all options
        options.forEach(o => o.classList.add('disabled'));

        if (index === correctIndex) {
          opt.classList.add('correct');
        } else {
          opt.classList.add('incorrect');
          if (options[correctIndex]) {
            options[correctIndex].classList.add('correct');
          }
        }

        // Reveal explanation
        if (explanation) {
          explanation.classList.add('show');
        }
      });
    });
  });
}

// Index Search and Filtering
function initSearchAndFilters() {
  const searchInput = document.getElementById('projectSearch');
  const chips = document.querySelectorAll('.filter-chips .chip');
  const cards = document.querySelectorAll('.project-card');

  if (!cards.length) return;

  let activeFilter = 'all';
  let searchTerm = '';

  function filterCards() {
    cards.forEach(card => {
      const title = card.querySelector('.card-title')?.innerText.toLowerCase() || '';
      const desc = card.querySelector('.card-desc')?.innerText.toLowerCase() || '';
      const tags = Array.from(card.querySelectorAll('.tag')).map(t => t.innerText.toLowerCase()).join(' ');
      const section = card.getAttribute('data-section') || '';
      const relevance = card.getAttribute('data-relevance') || '';

      const matchesSearch = !searchTerm || title.includes(searchTerm) || desc.includes(searchTerm) || tags.includes(searchTerm);
      
      let matchesFilter = true;
      if (activeFilter.startsWith('sec-')) {
        matchesFilter = (section === activeFilter.replace('sec-', ''));
      } else if (activeFilter === 'emb-high') {
        matchesFilter = (relevance === 'high');
      }

      if (matchesSearch && matchesFilter) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchTerm = e.target.value.toLowerCase().trim();
      filterCards();
    });
  }

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeFilter = chip.getAttribute('data-filter') || 'all';
      filterCards();
    });
  });
}
