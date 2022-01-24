// Ignore this file, just managing the level movememnt and stuff like that, nothing to do with the actual levels

async function better_fetch(local_url) {
    if (location.href.includes('127.0.0.1')) {
        return await fetch(local_url);
    } else {
        return await fetch('https://odyssey-ctf.herokuapp.com' + local_url);
    }
}

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

    var server_response = await (await better_fetch('/check_level?level=' + level + '&password=' + pwd)).json();
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
    var level = document.title.split(' ')[1];
    level = parseInt(level);

    location.href = '/levels/level' + (level - 1);
}


function addNextLevelDiv(level) {
    var next = true;
    level = document.title.split(' ')[1];
    level = parseInt(level);

    if (isNaN(level)) {
        level = document.querySelector('meta[name="description"]').content.split(' ')[1];
        level = parseInt(level) - 1;
        next = false;
    }
    

    var form = `
    <hr>
    <div style="position: absolute; bottom: 50px;">
        <h2>${next ? 'Next' : 'Current'} Level:</h2>
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