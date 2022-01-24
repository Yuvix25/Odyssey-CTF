async function checkCorrect(event) {
    var username = event.target.elements.username.value;
    var password = event.target.elements.password.value;

    var server_response = await (await betterFetch('/level4_validate_login?username=' + username + '&password=' + password)).json();
    document.getElementById("response").innerHTML = server_response.message;
}