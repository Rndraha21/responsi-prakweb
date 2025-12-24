const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resizeCanvas();

window.addEventListener("resize", resizeCanvas);

const particlesArray = [];
let hue = 0;

const mouse = {
  x: undefined,
  y: undefined,
};

let lastSpawn = 0;

function isInsideCanvas(x, y) {
  const rect = canvas.getBoundingClientRect();
  return x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom;
}

function updateMousePosition(e) {
  const rect = canvas.getBoundingClientRect();
  mouse.x = e.clientX - rect.left;
  mouse.y = e.clientY - rect.top;
}

window.addEventListener("mousemove", (e) => {
  const now = Date.now();
  if (now - lastSpawn < 16) return;

  if (!isInsideCanvas(e.clientX, e.clientY)) return;

  lastSpawn = now;
  updateMousePosition(e);
  particlesArray.push(new Particle());
});

window.addEventListener("click", (e) => {
  if (!isInsideCanvas(e.clientX, e.clientY)) return;

  updateMousePosition(e);
  for (let i = 0; i < 3; i++) {
    particlesArray.push(new Particle());
  }
});

class Particle {
  constructor() {
    this.x = mouse.x;
    this.y = mouse.y;
    this.size = Math.random() * 15 + 1;
    this.speedX = Math.random() * 3 - 1.5;
    this.speedY = Math.random() * 3 - 1.5;
    this.color = `hsl(${hue}, 100%, 50%)`;
  }

  update() {
    this.x += this.speedX;
    this.y += this.speedY;
    if (this.size > 0.3) this.size -= 0.15;
  }

  draw() {
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill();
  }
}

function handleParticles() {
  for (let i = 0; i < particlesArray.length; i++) {
    const p = particlesArray[i];
    p.update();
    p.draw();

    for (let j = i + 1; j < particlesArray.length; j++) {
      const dx = p.x - particlesArray[j].x;
      const dy = p.y - particlesArray[j].y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < 100) {
        ctx.beginPath();
        ctx.strokeStyle = p.color;
        ctx.lineWidth = 0.2;
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(particlesArray[j].x, particlesArray[j].y);
        ctx.stroke();
      }
    }

    if (p.size <= 0.3) {
      particlesArray.splice(i, 1);
      i--;
    }
  }
}

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  handleParticles();
  hue += 2;
  requestAnimationFrame(animate);
}

animate();
