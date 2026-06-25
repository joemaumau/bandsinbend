// ─────────────────────────────────────────────
// BANDS IN BEND — Main JS
// ─────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {

  // ── Render hero highlights ──────────────────
  const highlightsList = document.getElementById('highlights-list');
  if (highlightsList && typeof HIGHLIGHTS !== 'undefined') {
    highlightsList.innerHTML = HIGHLIGHTS.map(h => `
      <div class="highlight-item">
        <span class="highlight-arrow">→</span>
        <span>${h.artist}</span>
        <span class="highlight-day">${h.day}</span>
      </div>
    `).join('');
  }

  // ── Render week label ───────────────────────
  const weekLabel = document.getElementById('week-label');
  if (weekLabel && typeof WEEK !== 'undefined') {
    weekLabel.textContent = WEEK.label;
  }

  // ── Render day nav buttons ──────────────────
  const weekNav = document.getElementById('week-nav');
  if (weekNav && typeof SHOWS !== 'undefined') {
    const allBtn = document.createElement('button');
    allBtn.className = 'day-btn active';
    allBtn.dataset.day = 'all';
    allBtn.textContent = 'All Shows';
    weekNav.appendChild(allBtn);

    SHOWS.forEach(d => {
      const btn = document.createElement('button');
      btn.className = 'day-btn';
      btn.dataset.day = d.day;
      btn.textContent = d.day;
      weekNav.appendChild(btn);
    });
  }

  // ── Render show listings ────────────────────
  const showsContainer = document.getElementById('shows-container');
  if (showsContainer && typeof SHOWS !== 'undefined') {
    showsContainer.innerHTML = SHOWS.map(dayData => `
      <div class="day-block" data-day="${dayData.day}" id="day-${dayData.day.toLowerCase()}">
        <div class="day-header">
          <div class="day-name">${dayData.day.toUpperCase()}</div>
          <div class="day-date">${dayData.date}</div>
        </div>
        <div class="day-rule"></div>
        <div class="shows-list">
          ${dayData.shows.map(show => `
            <div class="show-item">
              <div>
                <div class="show-artist">${show.artist}</div>
                <div class="show-meta">
                  <span class="show-venue">${show.venue}</span>
                </div>
              </div>
              <div class="show-time-badge">${show.time}</div>
            </div>
          `).join('')}
        </div>
      </div>
    `).join('');
  }

  // ── Day filter ──────────────────────────────
  const dayBlocks = () => document.querySelectorAll('.day-block');
  const dayBtns   = () => document.querySelectorAll('.day-btn');

  document.addEventListener('click', e => {
    const btn = e.target.closest('.day-btn');
    if (!btn) return;

    dayBtns().forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const selected = btn.dataset.day;

    dayBlocks().forEach(block => {
      if (selected === 'all' || block.dataset.day === selected) {
        block.classList.remove('hidden');
        // Trigger visible for scroll animation
        setTimeout(() => block.classList.add('visible'), 10);
      } else {
        block.classList.add('hidden');
        block.classList.remove('visible');
      }
    });

    // Scroll to first visible block
    if (selected !== 'all') {
      const target = document.getElementById(`day-${selected.toLowerCase()}`);
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });

  // ── Scroll-triggered fade-in ────────────────
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  // Observe after a short delay to allow render
  setTimeout(() => {
    dayBlocks().forEach(block => observer.observe(block));
  }, 100);

  // ── Newsletter form ─────────────────────────
  const form = document.getElementById('newsletter-form');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const email = form.querySelector('input[type="email"]').value;
      if (!email) return;
      // Replace this with your Mailchimp embed action URL
      form.innerHTML = `<p style="color: var(--gold); font-size: 14px; font-weight: 600;">
        You're in. See you Thursday. 🎸
      </p>`;
    });
  }

});
