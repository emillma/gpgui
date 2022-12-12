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

async function watchdog() {
    try {
        const response = await fetchWithTimeout('/hartbeat', 1000);
        if (response.status === 200 && reload) {
            location.reload();
        }
        setTimeout(watchdog, 1000);
    } catch (error) {
        reload = true;
        console.log('could not fetch resource')
        watchdog();
    }
}
watchdog();