document.addEventListener('DOMContentLoaded', () => {
  // Allow multiple help panels to be open at once (no accordion behavior)

  document.querySelectorAll('.info-toggle').forEach((btn) => {
    const targetId = btn.getAttribute('aria-controls');
    const panel = document.getElementById(targetId);
    if (!panel) return;
    panel.style.display = 'none';
    btn.setAttribute('aria-expanded', 'false');
    btn.textContent = '▼';

    btn.addEventListener('click', () => {
      const isOpen = panel.classList.contains('open');
      if (isOpen) {
        panel.classList.remove('open');
        panel.style.display = 'none';
        btn.setAttribute('aria-expanded', 'false');
        btn.textContent = '▼';
        return;
      }
      // Toggle current panel only (no closing others)
      panel.classList.add('open');
      panel.style.display = 'block';
      btn.setAttribute('aria-expanded', 'true');
      btn.textContent = '▲';
    });
  });
});
