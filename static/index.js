

function setCookie(name,value) {
    document.cookie = name + "=" + (value || "")  + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i=0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function eraseCookie(name) {   
    document.cookie = name +'=; path=/;';
}


async function gotoLevel(event, level) {
    var pwd = event.target.elements.password.value;

    var server_response = await (await fetch('/check_level?level=' + level + '&password=' + pwd)).json();
    if (server_response.success) {
        // save password in cookies:
        let current_passwords = JSON.parse(getCookie('passwords') || '{}');
        current_passwords[level] = pwd;
        setCookie('passwords', JSON.stringify(current_passwords));

        window.location.href = '/levels/' + level;
    } else {
        alert(server_response.message);
    }
}



function goBack() {
    var current_level = location.pathname.split('/')[2];
    current_level = current_level.split('.')[0].substring(5);

    var level_index = parseInt(current_level);
    location.href = '/levels/level' + (level_index - 1);
}




function gotoGame() {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            document.getElementById('game').innerHTML = xhr.responseText;
        }
    }

    xhr.open('GET', '/game', true);
    xhr.setRequestHeader('user-type', 'normal');
    xhr.send('');
}