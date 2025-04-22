
function playlistadder()
{
    const audiotag = document.getElementById('audiotag')
    audiotag.replaceChildren();
    const username = document.getElementById('username').value;
    fetch('/playlistgetter',{
        method: "POST",
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify({ "username":username}),
    })
    .then(res=>res.json())
    .then(data=>{
        for (const [key, value] of Object.entries(data)) {
            console.log(`${key}: ${value}`);
            var sound      = document.createElement('audio');
            sound.id       = 'audio-player';
            sound.controls = 'controls';
            sound.src      = 'static/audios/'+key;
            sound.type     = 'audio/webm';
            var tittle      = document.createElement('h4');
            tittle.innerHTML = value;
            audiotag.appendChild(tittle);
            audiotag.appendChild(sound);
          }
    })

}