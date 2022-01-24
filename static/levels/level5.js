async function streamingService() {
    var server_response = await (await fetch('/level5_streaming')).json();
    if (server_response.success) {
        document.getElementById('stream').innerHTML = `<iframe width="560" height="315" src="https://www.youtube.com/watch?v=kzYfRLMtP9c" frameborder="0" allow="picture-in-picture" allowfullscreen></iframe>`;
    }
    else {
        document.getElementById('message').innerHTML = server_response.message;
    }
}