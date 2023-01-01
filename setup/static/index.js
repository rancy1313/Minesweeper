var sec = 0;
function pad ( val ) { return val > 9 ? val : "0" + val; }
setInterval( function(){
    let game_status = document.getElementById('game_over');
    if (game_status.className == 'hide') {
        $("#seconds").html(pad(++sec%60));
        $("#minutes").html(pad(parseInt(sec/60,10)));
    }
}, 1000);

function check_value(node_id, time) {
  fetch(`/test-check-node-value/${node_id}/${time}`, {
    method: "POST"
  }).then((_res) => {
    window.location.href = `/refresh-game/${time}`;
  });
}

function update_time(time) {
    sec = time;
}


