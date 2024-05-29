const canvas = document.getElementById("sine-wave");
const ctx = canvas.getContext("2d");

const amplitude = 50;
const frequency = 0.02;
let phase = 0;

function draw() {
    requestAnimationFrame(draw);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.beginPath();

    for (let x = 0; x < canvas.width; x += 5) {
        const y = amplitude * Math.sin(frequency * x + phase) + canvas.height / 2;
        ctx.lineTo(x, y);
    }

    ctx.strokeStyle = "blue";
    ctx.lineWidth = 2;
    ctx.stroke();

    phase += 0.1;
}

draw();
