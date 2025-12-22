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

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const particlesArray = [];

window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});

const mouse = {
  x: undefined,
  y: undefined,
};

window.addEventListener("click", (e) => {
  mouse.x = e.x;
  mouse.y = e.y;
  for (let i = 0; i < 10; i++) {
    particlesArray.push(new Particle());
  }
});

window.addEventListener("mousemove", (e) => {
  mouse.x = e.x;
  mouse.y = e.y;
  for (let i = 0; i < 5; i++) {
    particlesArray.push(new Particle());
  }
});

class Particle {
  constructor() {
    this.x = mouse.x;
    this.y = mouse.y;
    // this.x = Math.random() * canvas.width;
    // this.y = Math.random() * canvas.height;
    this.size = Math.random() * 15 + 1;
    this.speedX = Math.random() * 3 - 1.5;
    this.speedY = Math.random() * 3 - 1.5;
    this.color = "white";
  }

  update() {
    this.x += this.speedX;
    this.y += this.speedY;
    if (this.size > 0.2) this.size -= 0.1;
  }

  draw() {
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill();
  }
}

const handleParticles = () => {
  for (let i = 0; i < particlesArray.length; i++) {
    particlesArray[i].update();
    particlesArray[i].draw();
  }
};

const animate = () => {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  handleParticles();
  requestAnimationFrame(animate);
};

animate();
