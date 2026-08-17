// Embedded C++ Study Portal Interactive Engine & Theme Manager
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initTabs();
  initCopyButtons();
  initQuiz();
  initSearchAndFilters();
  initGlossary();
});

// Day & Night Theme Toggle Manager
function initTheme() {
  const savedTheme = localStorage.getItem('study-portal-theme') || 'dark';
  applyTheme(savedTheme);

  const toggleBtns = document.querySelectorAll('#themeToggle, .theme-toggle-btn');
  toggleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
      const newTheme = (currentTheme === 'dark') ? 'light' : 'dark';
      applyTheme(newTheme);
    });
  });
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('study-portal-theme', theme);

  const toggleBtns = document.querySelectorAll('#themeToggle, .theme-toggle-btn');
  toggleBtns.forEach(btn => {
    const iconSpan = btn.querySelector('.theme-icon');
    const textSpan = btn.querySelector('.theme-text');
    if (theme === 'light') {
      if (iconSpan) iconSpan.textContent = '🌙';
      if (textSpan) textSpan.textContent = 'Dark';
      btn.setAttribute('title', 'Switch to Cyber Dark Theme');
    } else {
      if (iconSpan) iconSpan.textContent = '☀️';
      if (textSpan) textSpan.textContent = 'Light';
      btn.setAttribute('title', 'Switch to Light Theme');
    }
  });
}

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

// Index Search, Category Tracks, and Filtering
function initSearchAndFilters() {
  const searchInput = document.getElementById('projectSearch');
  const trackBtns = document.querySelectorAll('.track-btn');
  const chips = document.querySelectorAll('.filter-chips .chip');
  const cards = document.querySelectorAll('.project-card');
  const resultsCounter = document.getElementById('resultsCounter');
  const headerFoundations = document.getElementById('header-foundations');
  const headerAdvanced = document.getElementById('header-advanced');
  const gridFoundations = document.getElementById('grid-foundations');
  const gridAdvanced = document.getElementById('grid-advanced');

  if (!cards.length) return;

  let activeTrack = 'all'; // 'all', 'foundations', 'advanced', 'emb-high'
  let activeSection = 'all'; // 'all', '1', '2', ..., '12'
  let searchTerm = '';

  function filterCards() {
    let totalVisible = 0;
    let foundationsVisible = 0;
    let advancedVisible = 0;

    cards.forEach(card => {
      const title = card.querySelector('.card-title')?.innerText.toLowerCase() || '';
      const desc = card.querySelector('.card-desc')?.innerText.toLowerCase() || '';
      const tags = Array.from(card.querySelectorAll('.tag')).map(t => t.innerText.toLowerCase()).join(' ');
      const section = card.getAttribute('data-section') || '';
      const track = card.getAttribute('data-track') || '';
      const relevance = card.getAttribute('data-relevance') || '';

      const matchesSearch = !searchTerm || title.includes(searchTerm) || desc.includes(searchTerm) || tags.includes(searchTerm);
      
      let matchesTrack = true;
      if (activeTrack === 'foundations') {
        matchesTrack = (track === 'foundations');
      } else if (activeTrack === 'advanced') {
        matchesTrack = (track === 'advanced');
      } else if (activeTrack === 'emb-high') {
        matchesTrack = (relevance === 'high');
      }

      let matchesSection = true;
      if (activeSection !== 'all') {
        matchesSection = (section === activeSection);
      }

      if (matchesSearch && matchesTrack && matchesSection) {
        card.style.display = 'flex';
        totalVisible++;
        if (track === 'foundations') foundationsVisible++;
        if (track === 'advanced') advancedVisible++;
      } else {
        card.style.display = 'none';
      }
    });

    // Update Track Header Visibility
    if (headerFoundations) {
      headerFoundations.style.display = (foundationsVisible > 0) ? 'flex' : 'none';
    }
    if (gridFoundations) {
      gridFoundations.style.display = (foundationsVisible > 0) ? 'grid' : 'none';
    }

    if (headerAdvanced) {
      headerAdvanced.style.display = (advancedVisible > 0) ? 'flex' : 'none';
    }
    if (gridAdvanced) {
      gridAdvanced.style.display = (advancedVisible > 0) ? 'grid' : 'none';
    }

    // Update Results Counter
    if (resultsCounter) {
      resultsCounter.innerHTML = `Showing <strong>${totalVisible}</strong> of <strong>${cards.length}</strong> Projects`;
    }
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchTerm = e.target.value.toLowerCase().trim();
      filterCards();
    });
  }

  // Track buttons (All, Foundations, Advanced, Embedded High)
  trackBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      trackBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeTrack = btn.getAttribute('data-track') || 'all';

      // Reset section chips to all
      chips.forEach(c => c.classList.remove('active'));
      const allChip = document.querySelector('.filter-chips .chip[data-filter="all"]');
      if (allChip) allChip.classList.add('active');
      activeSection = 'all';

      filterCards();
    });
  });

  // Section Chips
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const filterVal = chip.getAttribute('data-filter') || 'all';

      if (filterVal === 'all') {
        activeSection = 'all';
      } else if (filterVal.startsWith('sec-')) {
        activeSection = filterVal.replace('sec-', '');
      } else if (filterVal === 'emb-high') {
        activeTrack = 'emb-high';
        activeSection = 'all';
        trackBtns.forEach(b => b.classList.remove('active'));
        const embBtn = document.querySelector('.track-btn[data-track="emb-high"]');
        if (embBtn) embBtn.classList.add('active');
      }

      filterCards();
    });
  });

  filterCards();
}

// ==============================================================================
// TECHNICAL GLOSSARY ENGINE
// ==============================================================================
function initGlossary() {
  const searchInput = document.getElementById('glossarySearch');
  const chips = document.querySelectorAll('.glossary-chips .chip');
  const cards = document.querySelectorAll('.glossary-card');
  const letterGroups = document.querySelectorAll('.glossary-letter-group');
  const resultsCounter = document.getElementById('glossaryCounter');
  const copyButtons = document.querySelectorAll('.btn-copy-term');
  const alphaJumpButtons = document.querySelectorAll('.alpha-jump-btn');

  if (!cards.length) return;

  let activeCategory = 'all';
  let searchTerm = '';

  function filterGlossary() {
    let visibleCount = 0;
    const visibleLetters = new Set();

    cards.forEach(card => {
      const term = card.querySelector('.glossary-term-title')?.innerText.toLowerCase() || '';
      const expansion = card.querySelector('.glossary-expansion')?.innerText.toLowerCase() || '';
      const def = card.querySelector('.glossary-def')?.innerText.toLowerCase() || '';
      const hw = card.querySelector('.glossary-hw-box')?.innerText.toLowerCase() || '';
      const tags = Array.from(card.querySelectorAll('.tag')).map(t => t.innerText.toLowerCase()).join(' ');
      const category = card.getAttribute('data-category') || '';
      const letter = card.getAttribute('data-letter') || '';

      const matchesSearch = !searchTerm || 
        term.includes(searchTerm) || 
        expansion.includes(searchTerm) || 
        def.includes(searchTerm) || 
        hw.includes(searchTerm) || 
        tags.includes(searchTerm);

      const matchesCategory = (activeCategory === 'all') || (category === activeCategory);

      if (matchesSearch && matchesCategory) {
        card.style.display = 'block';
        visibleCount++;
        if (letter) visibleLetters.add(letter);
      } else {
        card.style.display = 'none';
      }
    });

    // Hide or show letter group headers based on visible cards
    letterGroups.forEach(group => {
      const groupLetter = group.getAttribute('data-letter');
      if (visibleLetters.has(groupLetter)) {
        group.style.display = 'block';
      } else {
        group.style.display = 'none';
      }
    });

    // Update Alphabet Jump buttons active / disabled states
    alphaJumpButtons.forEach(btn => {
      const btnLetter = btn.getAttribute('data-letter');
      if (visibleLetters.has(btnLetter)) {
        btn.style.opacity = '1';
        btn.style.pointerEvents = 'auto';
      } else {
        btn.style.opacity = '0.3';
        btn.style.pointerEvents = 'none';
      }
    });

    // Update Result Counter
    if (resultsCounter) {
      resultsCounter.innerHTML = `Showing <strong>${visibleCount}</strong> of <strong>${cards.length}</strong> Technical Terms`;
    }
  }

  // Search Input Listener
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchTerm = e.target.value.toLowerCase().trim();
      filterGlossary();
    });
  }

  // Category Filter Chips
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeCategory = chip.getAttribute('data-filter') || 'all';
      filterGlossary();
    });
  });

  // 1-Click Copy Term Anchor Link
  copyButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const anchorId = btn.getAttribute('data-anchor');
      const url = `${window.location.origin}${window.location.pathname}#${anchorId}`;
      navigator.clipboard.writeText(url).then(() => {
        const originalText = btn.innerHTML;
        btn.innerHTML = '✓ Copied Link!';
        btn.classList.add('copied');
        setTimeout(() => {
          btn.innerHTML = originalText;
          btn.classList.remove('copied');
        }, 2000);
      }).catch(err => {
        console.error('Failed to copy anchor link:', err);
      });
    });
  });

  // Highlight targeted card if opened with hash (e.g. glossary.html#aapcs)
  function handleHashHighlight() {
    if (window.location.hash) {
      const targetId = window.location.hash.substring(1);
      const targetEl = document.getElementById(targetId);
      if (targetEl && targetEl.classList.contains('glossary-card')) {
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        targetEl.style.borderColor = 'var(--accent-neon)';
        targetEl.style.boxShadow = '0 0 20px rgba(0, 255, 136, 0.35)';
        setTimeout(() => {
          targetEl.style.borderColor = '';
          targetEl.style.boxShadow = '';
        }, 3000);
      }
    }
  }

  handleHashHighlight();
  window.addEventListener('hashchange', handleHashHighlight);

  filterGlossary();
}
