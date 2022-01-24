async function streamingService() {
    var url;
    if (window.location.href.includes('127.0.0.1')) {
        url = '/level5_streaming';
    } else {
        url = 'odyssey-ctf.herokuapp.com/level5_streaming';
    }
    var server_response = await (await fetch(url)).json();
    if (server_response.success) {
        document.getElementById('stream').innerHTML = `<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allow="picture-in-picture" allowfullscreen></iframe>`;
    }
    else {
        document.getElementById('message').innerHTML = server_response.message;
    }
}