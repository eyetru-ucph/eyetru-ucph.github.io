// Small progressive enhancements. The site works without JavaScript.
(function () {
  // Mobile menu
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  // Light / dark toggle (remembered per browser)
  var themeBtn = document.querySelector(".theme-toggle");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var root = document.documentElement;
      var dark = root.dataset.theme
        ? root.dataset.theme === "dark"
        : window.matchMedia("(prefers-color-scheme: dark)").matches;
      root.dataset.theme = dark ? "light" : "dark";
      try { localStorage.setItem("theme", root.dataset.theme); } catch (e) {}
    });
  }

  // Publication filters
  var form = document.querySelector("[data-pub-filters]");
  if (form) {
    var items = Array.prototype.slice.call(document.querySelectorAll("[data-pub]"));
    var years = Array.prototype.slice.call(document.querySelectorAll("[data-pub-year]"));
    var count = form.querySelector("[data-count]");
    var empty = document.querySelector("[data-empty]");
    var params = new URLSearchParams(location.search);
    ["q", "type", "status", "project"].forEach(function (k) {
      if (params.get(k) && form.elements[k]) form.elements[k].value = params.get(k);
    });

    function apply() {
      var q = form.elements.q.value.trim().toLowerCase();
      var type = form.elements.type.value;
      var status = form.elements.status.value;
      var project = form.elements.project ? form.elements.project.value : "";
      var shown = 0;
      items.forEach(function (el) {
        var ok = (!q || el.dataset.search.indexOf(q) !== -1) &&
          (!type || el.dataset.group === type) &&
          (!status || el.dataset.status === status) &&
          (!project || (" " + el.dataset.projects + " ").indexOf(" " + project + " ") !== -1);
        el.hidden = !ok;
        if (ok) shown++;
      });
      years.forEach(function (y) {
        var any = y.nextElementSibling && y.nextElementSibling.querySelector("[data-pub]:not([hidden])");
        y.hidden = !any; y.nextElementSibling.hidden = !any;
      });
      if (count) count.textContent = shown + " of " + items.length + " shown";
      if (empty) empty.hidden = shown !== 0;
      var p = new URLSearchParams();
      if (q) p.set("q", q); if (type) p.set("type", type); if (status) p.set("status", status); if (project) p.set("project", project);
      history.replaceState(null, "", p.toString() ? "?" + p : location.pathname);
    }
    form.addEventListener("input", apply);
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    apply();
  }
})();
