async function urlCapture(event) {
    var url = event.target.elements.url.value;

    document.getElementById("message").innerHTML = "Loading...";
    var server_response = await (await fetch('/level6_capture?url=' + url)).json();
    if (server_response.success) {
        document.getElementById("img").src = server_response.url;
        document.getElementById("message").innerHTML = '';
    }
    else {
        document.getElementById("message").innerHTML = server_response.message;
    }
}