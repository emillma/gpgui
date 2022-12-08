
console.log("Loading midi.js");

navigator.requestMIDIAccess().then((midiAccess) => {
    console.log(Array.from(midiAccess.inputs));
    let key = input => input[1].name === "Midi Fighter Twister"
    input = Array.from(midiAccess.inputs).find(key);
    output = Array.from(midiAccess.outputs).find(key);
    console.log(output);
    if (input && output) {
        console.log("Found Midi Fighter Twister");
        let socket = new WebSocket('ws://localhost:5000/midi')

        socket.addEventListener('message', (event) => {
            console.log('Message from server ', event.data);
        });

        async function handleMidi(midi_message) {
            if (socket.readyState == WebSocket.OPEN) {
                socket.send(midi_message.data);
            }
            else {
                console.log("Socket not open", socket.readyState);
            }
        };
        input[1].onmidimessage = handleMidi
    }
    else {
        console.log("Midi Fighter Twister not found");
    }
});
