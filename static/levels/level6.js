async function urlCapture(event) {
    var url = event.target.elements.url.value;

    var server_response = await (await fetch('/level6_capture?url=' + url)).json();
    if (server_response.success) {
        document.getElementById("img").src = server_response.url;
    }
    else {
        document.getElementById("message").innerHTML = server_response.message;
    }
}