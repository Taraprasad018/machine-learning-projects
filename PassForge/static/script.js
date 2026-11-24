/* =========================
   Navigation
========================= */
function showPage(id) {
  document.querySelectorAll(".page").forEach(p =>
    p.classList.remove("active")
  );
  document.getElementById(id)?.classList.add("active");
}

/* =========================
   Glitch Effect
========================= */
function glitchText(el) {
  const text = el.innerText;
  let i = 0;
  const interval = setInterval(() => {
    el.innerText =
      text.substring(0, i) +
      String.fromCharCode(33 + Math.random() * 94);
    i++;
    if (i > text.length) {
      el.innerText = text;
      clearInterval(interval);
    }
  }, 40);
}

document.querySelectorAll(".glitch").forEach(h =>
  h.addEventListener("mouseenter", () => glitchText(h))
);

/* =========================
   Analyzer UI Rules
========================= */
const pwd = document.getElementById("password");
const exposure = document.getElementById("exposure-warning");

const rules = {
  length: document.getElementById("rule-length"),
  upper: document.getElementById("rule-upper"),
  number: document.getElementById("rule-number"),
  special: document.getElementById("rule-special")
};

const leaked = ["password", "123", "admin", "qwerty"];

pwd?.addEventListener("input", () => {
  const p = pwd.value;
  if (p.length === 0) return;

  if (rules.length) rules.length.style.opacity = p.length >= 10 ? 1 : 0.4;
  if (rules.upper) rules.upper.style.opacity = /[A-Z]/.test(p) ? 1 : 0.4;
  if (rules.number) rules.number.style.opacity = /\d/.test(p) ? 1 : 0.4;
  if (rules.special) rules.special.style.opacity = /[^A-Za-z0-9]/.test(p) ? 1 : 0.4;

  if (exposure) {
    if (leaked.some(x => p.toLowerCase().includes(x))) {
      exposure.textContent = "⚠ Pattern found in leaked passwords";
    } else {
      exposure.textContent = "";
    }
  }
});

/* =========================
   Toggle password
========================= */
function togglePwd() {
  if(pwd) {
    pwd.type = pwd.type === "password" ? "text" : "password";
  }
}

/* =========================
   Generator
========================= */
function copyPassword() {
  const p = document.getElementById("generated-password")?.textContent;
  if (!p) return alert("Generate first!");
  navigator.clipboard.writeText(p);
  alert("Password Copied");
}