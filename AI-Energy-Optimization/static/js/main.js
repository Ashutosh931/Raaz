/**
 * Main Application Scripts
 * Theme toggler, responsive sidebar, alert dismissal, and global utilities.
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Theme Management (Light / Dark)
  const themeToggleBtn = document.getElementById("themeToggleBtn");
  const storedTheme = localStorage.getItem("smart_energy_theme") || "light";
  
  document.documentElement.setAttribute("data-theme", storedTheme);
  updateThemeIcon(storedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", () => {
      const currentTheme = document.documentElement.getAttribute("data-theme");
      const newTheme = currentTheme === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", newTheme);
      localStorage.setItem("smart_energy_theme", newTheme);
      updateThemeIcon(newTheme);

      // Trigger window resize event so Chart.js charts refresh colors seamlessly
      window.dispatchEvent(new Event('resize'));
    });
  }

  function updateThemeIcon(theme) {
    if (!themeToggleBtn) return;
    const icon = themeToggleBtn.querySelector("i");
    if (icon) {
      if (theme === "dark") {
        icon.className = "bi bi-sun-fill text-warning";
      } else {
        icon.className = "bi bi-moon-stars-fill";
      }
    }
  }

  // 2. Mobile Sidebar Toggle
  const sidebarToggleBtn = document.getElementById("sidebarToggleBtn");
  const sidebar = document.querySelector(".app-sidebar");
  const backdrop = document.getElementById("sidebarBackdrop");

  if (sidebarToggleBtn && sidebar) {
    sidebarToggleBtn.addEventListener("click", () => {
      sidebar.classList.toggle("show");
      if (backdrop) backdrop.classList.toggle("show");
    });
  }

  if (backdrop) {
    backdrop.addEventListener("click", () => {
      sidebar.classList.remove("show");
      backdrop.classList.remove("show");
    });
  }

  // 3. Auto dismiss flash alerts after 5 seconds
  setTimeout(() => {
    const flashAlerts = document.querySelectorAll(".alert-dismissible");
    flashAlerts.forEach(alert => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    });
  }, 5000);
});
