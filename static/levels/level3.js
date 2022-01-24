function gotoGame() {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            document.getElementById('game').innerHTML = xhr.responseText;
        }
    }

    xhr.open('GET', '/level3_game', true);
    xhr.setRequestHeader('privileges', 'normal');
    xhr.send('');
}