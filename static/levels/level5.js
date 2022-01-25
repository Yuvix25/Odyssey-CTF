async function streamingService() {
    var server_response = await (await fetch('/level5_streaming')).json();
    if (server_response.success) {
        document.getElementById('stream').innerHTML = `<iframe width="560" height="315" src="${server_response.url}" frameborder="0" allow="picture-in-picture" allowfullscreen></iframe>`;
    }
    document.getElementById('message').innerHTML = server_response.message;
}