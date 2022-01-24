async function streamingService() {
    var server_response = await (await betterFetch('/level5_streaming')).json();
    if (server_response.success) {
        document.getElementById('stream').innerHTML = `<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1" frameborder="0" allow="picture-in-picture" allowfullscreen></iframe>`;
    }
    else {
        document.getElementById('message').innerHTML = server_response.message;
    }
}