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

async function watchdog(delay = 3000) {
    try {
        const response = await fetchWithTimeout('/hartbeat', 500);
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