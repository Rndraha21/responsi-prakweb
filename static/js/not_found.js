const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

const characters =
  "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const fontSize = 16;
const columns = Math.floor(canvas.width / fontSize);

const drops = [];
for (let i = 0; i < columns; i++) {
  drops[i] = 1;
}

function drawMatrix() {
  ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#0F0";
  ctx.font = fontSize + "px 'Fira Code', monospace";

  for (let i = 0; i < drops.length; i++) {
    const text = characters.charAt(
      Math.floor(Math.random() * characters.length)
    );

    ctx.fillText(text, i * fontSize, drops[i] * fontSize);

    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
      drops[i] = 0;
    }

    drops[i]++;
  }
}

window.addEventListener("mousemove", (e) => {
  const col = Math.floor(e.clientX / fontSize);
  if (drops[col]) drops[col] = 0;
});

function animate() {
  drawMatrix();
  requestAnimationFrame(animate);
}

animate();

const sound = document.getElementById("hackerSound");

function playScarySound() {
  sound.play().catch(() => {
    console.log("Waiting for user trigger.");
  });
}

window.addEventListener("click", () => {
  playScarySound();
  sound.volume = 0.5;

  document.body.classList.add("glitch-vibrate");
});
