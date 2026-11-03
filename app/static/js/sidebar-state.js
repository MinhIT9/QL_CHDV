"use strict";

// Apply before first paint, including when HTMX replaces the body.
try {
  document.documentElement.classList.toggle(
    "sidebar-collapsed",
    localStorage.getItem("chdv-sidebar-collapsed") === "true"
  );
} catch { /* Storage may be disabled. */ }
