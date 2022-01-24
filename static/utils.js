// Ignore this file, just managing the level movememnt and stuff like that, nothing to do with the actual levels

function setCookie(name, value, hours) {
    var expires = "";
    if (hours) {
        var date = new Date();
        date.setTime(date.getTime() + (hours*60*60*1000));
        expires = "; Expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; Path=/";
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
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}


const cookie_expiration_hours = 24;


async function gotoLevel(event, level) {
    var pwd = event.target.elements.password.value;

    var server_response = await (await fetch('/check_level?level=' + level + '&password=' + pwd)).json();
    if (server_response.success) {
        // save password in cookies:
        let current_passwords = JSON.parse(getCookie('passwords') || '{}');
        current_passwords[level] = pwd;
        setCookie('passwords', JSON.stringify(current_passwords), cookie_expiration_hours);

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


function addNextLevelDiv() {
    var level = location.pathname.split('/')[2];
    level = level.split('.')[0].substring(5);
    level = parseInt(level);

    var form = `
    <hr>
    <div style="position: absolute; bottom: 50px;">
        <h2>Next Level:</h2>
        <form onsubmit="gotoLevel(event, 'level${level+1}')" action="javascript:void(0);">
            <p>
                <label for="password">Level${level+1} Password:</label>
                <input type="password" name="password" id="level${level+1}-password" style="width: 400px;">
            </p>
            <p>
                <input type="submit" value="Submit">
            </p>
        </form>
    </div>
    `

    document.body.innerHTML += form;
}

// on dom load:
document.addEventListener('DOMContentLoaded', function() {
    addNextLevelDiv();
});