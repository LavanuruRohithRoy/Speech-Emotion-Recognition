const canvas = document.getElementById('backgroundCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

let waveRadius = 0;

function drawBackground() {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Background gradient
    const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
    gradient.addColorStop(0, '#1e1e2f'); // Dark blue
    gradient.addColorStop(1, '#3a3a5f'); // Lighter blue
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function drawHumanSilhouette() {
    // Draw a human silhouette on the left side
    ctx.fillStyle = '#ffffff'; // White silhouette
    ctx.beginPath();
    ctx.arc(150, canvas.height / 2 - 100, 50, 0, Math.PI * 2); // Circle for head
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(150, canvas.height / 2 - 50); // Neck
    ctx.lineTo(130, canvas.height / 2 + 100); // Left shoulder
    ctx.lineTo(170, canvas.height / 2 + 100); // Right shoulder
    ctx.closePath();
    ctx.fill();
}

function drawPulsingSoundWaves() {
    // Draw pulsing sound waves emanating from the silhouette
    for (let i = 0; i < 5; i++) {
        ctx.beginPath();
        ctx.arc(
            150, // Starting point near the silhouette
            canvas.height / 2 - 100,
            waveRadius + i * 30, // Radius increases with each wave
            0,
            Math.PI * 2
        );
        ctx.strokeStyle = `rgba(100, 150, 255, ${0.8 - i * 0.15})`; // Gradient-like wave colors
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    waveRadius += 1;
    if (waveRadius > 50) waveRadius = 0; // Reset wave radius for looping
}

function animate() {
    drawBackground();
    drawHumanSilhouette();
    drawPulsingSoundWaves();
    requestAnimationFrame(animate);
}

animate();