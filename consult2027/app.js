(function () {
  const btn = document.getElementById("langBtn");
  const nodes = document.querySelectorAll("[data-zh][data-en]");

  function apply(lang) {
    const en = lang === "en";
    document.documentElement.lang = en ? "en" : "zh-Hans";
    nodes.forEach(function (node) {
      node.textContent = en ? node.getAttribute("data-en") : node.getAttribute("data-zh");
    });
    btn.textContent = en ? "中文" : "English";
    btn.setAttribute("aria-pressed", en ? "true" : "false");
    document.title = en
      ? "Statistics Consultation 2026–27"
      : "统计咨询 2026–27 · Statistics Consultation";
    try {
      localStorage.setItem("consult2027-lang", lang);
    } catch (err) {
      /* ignore private-mode storage errors */
    }
  }

  btn.addEventListener("click", function () {
    const next = document.documentElement.lang === "en" ? "zh" : "en";
    apply(next);
  });

  let saved = "zh";
  try {
    saved = localStorage.getItem("consult2027-lang") || "zh";
  } catch (err) {
    saved = "zh";
  }
  if (saved === "en") apply("en");
})();
