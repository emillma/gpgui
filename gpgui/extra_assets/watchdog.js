async function fetchWithTimeout(resource, timeout = 1000, fetch_options = {}) {

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    const response = await fetch(resource, {
        ...fetch_options,
        signal: controller.signal
    });
    clearTimeout(id);
    return response;
}

let reload = false;
let hash = '';

async function watchdog(delay = 3000) {
    try {
        const response = await fetchWithTimeout('/hartbeat', 1000);
        const text = await response.text();

        if (hash && hash !== text) {
            location.reload();
        } else {
            hash = text;
        }
        if (response.status === 200 && reload) {
            location.reload();
        }
        setTimeout(watchdog, delay);
    } catch (error) {
        reload = true;
        console.log('could not fetch resource')
        watchdog(200);
    }
}
watchdog();