// Ignore this file, just managing the level movememnt and stuff like that, nothing to do with the actual levels

async function gotoLevel(event, level) {
    var pwd = event.target.elements.password.value;

    var server_response = await (await fetch('/check_level?level=' + level + '&password=' + pwd)).json();
    if (server_response.success) {
        location.href = '/levels/' + level;
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