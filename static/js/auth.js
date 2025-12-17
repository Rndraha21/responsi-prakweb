const iconEl = document.getElementById("toggle-visibility");
const passwordInput = document.getElementById("password");

if (iconEl && passwordInput) {
  passwordInput.addEventListener("input", () => {
    if (passwordInput.value.length > 0) {
      iconEl.classList.remove("hidden");
    } else {
      iconEl.classList.add("hidden");
    }
  });

  iconEl.addEventListener("click", () => {
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      iconEl.src = "/icons/invisible.svg";
      iconEl.alt = "hidden";
    } else {
      passwordInput.type = "password";
      iconEl.src = "/icons/visible.svg";
      iconEl.alt = "show";
    }
  });
}

const form = document.querySelector("form");
const btn = document.getElementById("submitBtn");
const text = document.getElementById("btnText");
const spinner = document.getElementById("spinner");

if (form) {
  form.addEventListener("submit", () => {
    btn.disabled = true;
    text.innerText = "Loading...";
    spinner.classList.remove("d-none");
  });
}
