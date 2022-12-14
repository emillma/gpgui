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

let hash = '';

async function watchdog() {
    try {
        const response = await fetchWithTimeout('/hartbeat', 1000);
        const text = await response.text();

        if (hash && hash !== text) {
            location.reload();
        } else {
            hash = text;
        }
        setTimeout(watchdog, 3000);
    } catch (error) {
        console.log('could not fetch resource')
        watchdog();
    }
}
watchdog(); 