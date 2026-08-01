document.documentElement.classList.add("js-ready");

document.addEventListener("DOMContentLoaded", function () {
  // Dashboard sidebar collapse toggle (base_admin.html / base_student.html)
  var sidebar = document.getElementById("sidebar");
  var sidebarToggle = document.getElementById("sidebar-toggle");
  if (sidebar && sidebarToggle) {
    sidebarToggle.addEventListener("click", function () {
      sidebar.classList.toggle("collapsed");
    });
  }

  // Sidebar dropdown groups (e.g. Events → Add Event / View Event)
  document.querySelectorAll(".nav-item-toggle").forEach(function (btn) {
    var submenu = document.getElementById(btn.getAttribute("data-toggle"));
    if (!submenu) return;
    btn.addEventListener("click", function () {
      var isOpen = submenu.classList.toggle("open");
      btn.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  });

  // Profile-style tabbed forms (e.g. Add/Edit Student): any element with
  // data-tab-target="panel-id" activates that panel — used by both the
  // sidebar tab list and in-panel Back/Next buttons.
  document.querySelectorAll("[data-tab-target]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var targetId = btn.getAttribute("data-tab-target");
      document.querySelectorAll(".profile-tab-panel").forEach(function (panel) {
        panel.classList.toggle("hidden", panel.id !== targetId);
      });
      document.querySelectorAll(".profile-tab").forEach(function (tab) {
        tab.classList.toggle("active", tab.getAttribute("data-tab-target") === targetId);
      });
    });
  });

  // Confirm-before-submit for destructive actions (e.g. delete event).
  // Uses SweetAlert2 when available, falls back to window.confirm otherwise.
  document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (form.dataset.confirmed === "true") return;
      e.preventDefault();

      if (typeof Swal === "undefined") {
        if (window.confirm(form.getAttribute("data-confirm"))) {
          form.dataset.confirmed = "true";
          form.submit();
        }
        return;
      }

      Swal.fire({
        title: "Are you sure?",
        text: form.getAttribute("data-confirm"),
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it",
        confirmButtonColor: "#E02B20",
        cancelButtonColor: "#6b7280",
      }).then(function (result) {
        if (result.isConfirmed) {
          form.dataset.confirmed = "true";
          form.submit();
        }
      });
    });
  });

  // Generic "quick view" modal (list.html "eye" action, used by Events and
  // Blog): populates a modal from the clicked trigger's data-* attributes.
  // data-meta is a "|"-separated list of meta chips (date, time, author, …).
  function initViewModal(modalId, triggerSelector) {
    var modal = document.getElementById(modalId);
    if (!modal) return;

    var modalTitle = modal.querySelector("[data-modal-title]");
    var modalMeta = modal.querySelector("[data-modal-meta]");
    var modalDescription = modal.querySelector("[data-modal-description]");
    var modalImage = modal.querySelector("[data-modal-image]");

    var open = function (btn) {
      if (modalTitle) modalTitle.textContent = btn.getAttribute("data-title") || "";
      if (modalDescription) modalDescription.textContent = btn.getAttribute("data-description") || "";

      if (modalMeta) {
        modalMeta.innerHTML = "";
        (btn.getAttribute("data-meta") || "")
          .split("|")
          .map(function (value) { return value.trim(); })
          .filter(function (value) { return value; })
          .forEach(function (value) {
            var span = document.createElement("span");
            span.textContent = value;
            modalMeta.appendChild(span);
          });
      }

      if (modalImage) {
        var image = btn.getAttribute("data-image");
        if (image) {
          modalImage.src = image;
          modalImage.classList.remove("hidden");
        } else {
          modalImage.classList.add("hidden");
        }
      }

      modal.classList.remove("hidden");
      modal.classList.add("flex");
      modal.setAttribute("aria-hidden", "false");
    };

    var close = function () {
      modal.classList.add("hidden");
      modal.classList.remove("flex");
      modal.setAttribute("aria-hidden", "true");
    };

    document.querySelectorAll(triggerSelector).forEach(function (btn) {
      btn.addEventListener("click", function () { open(btn); });
    });
    modal.querySelectorAll("[data-modal-close]").forEach(function (btn) {
      btn.addEventListener("click", close);
    });
    modal.addEventListener("click", function (e) {
      if (e.target === modal) close();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  initViewModal("event-modal", ".event-view-btn");
  initViewModal("blog-modal", ".blog-view-btn");
  initViewModal("student-modal", ".student-view-btn");
  initViewModal("due-modal", ".due-view-btn");
  initViewModal("loan-modal", ".loan-view-btn");
  initViewModal("request-modal", ".request-open-btn");
  initViewModal("message-modal", ".message-view-btn");
  initViewModal("member-modal", ".member-view-btn");

  // Auto-dismiss flash messages (login/register/logout + dashboard alerts)
  document.querySelectorAll(".flash-message").forEach(function (el) {
    setTimeout(function () {
      el.classList.add("opacity-0");
      setTimeout(function () { el.remove(); }, 500);
    }, 3000);
  });
});
