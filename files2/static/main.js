let lastAction = '';
let lastTimestamp = 0;
const overlay = document.getElementById('overlay');

// Show the overlay for 4 seconds per new action
function showAction(message) {
    overlay.textContent = message;
    overlay.classList.add('show');
    clearTimeout(overlay._timeout);
    overlay._timeout = setTimeout(() => {
        overlay.classList.remove('show');
    }, 4000);
}

async function fetchEvents() {
    const resp = await fetch('/events');
    const events = await resp.json();
    if (events.length > 0) {
        const latest = events[events.length - 1];
        if (latest.timestamp !== lastTimestamp || latest.message !== lastAction) {
            lastAction = latest.message;
            lastTimestamp = latest.timestamp;
            showAction(latest.message);
        }
    }
}

setInterval(fetchEvents, 2000);
window.onload = fetchEvents;