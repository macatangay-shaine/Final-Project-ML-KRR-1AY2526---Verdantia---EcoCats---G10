document.addEventListener('DOMContentLoaded', () => {
  let openHelpId = null;

  function closeOpen() {
    if (!openHelpId) return;
    const openPanel = document.getElementById(openHelpId);
    if (openPanel) {
      openPanel.classList.remove('open');
      openPanel.style.display = 'none';
    }
    const prevBtn = document.querySelector(`[aria-controls="${openHelpId}"]`);
    if (prevBtn) {
      prevBtn.setAttribute('aria-expanded', 'false');
      prevBtn.textContent = '▼';
    }
    openHelpId = null;
  }

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
        openHelpId = null;
        return;
      }
      // Accordion behavior: close any open panel first
      closeOpen();
      panel.classList.add('open');
      panel.style.display = 'block';
      btn.setAttribute('aria-expanded', 'true');
      btn.textContent = '▲';
      openHelpId = targetId;
    });
  });
});
