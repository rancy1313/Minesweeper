var sec = 0;
function pad ( val ) { return val > 9 ? val : "0" + val; }
setInterval( function(){
    let game_status = document.getElementById('game_over');
    if (game_status.className == 'hide') {
        $("#seconds").html(pad(++sec%60));
        $("#minutes").html(pad(parseInt(sec/60,10)));
    }
}, 1000);

function check_value(node_id) {
  fetch(`/test-check-node-value/${node_id}`, {
    method: "POST"
  }).then((_res) => {
    window.location.href = `/refresh-game`;
  });
}

function update_time(time) {
    sec = time;
}

  window.addEventListener("keydown", function(e) {
    //tested in IE/Chrome/Firefox
    if (e.keyCode === 77) {
        const nodes = document.querySelectorAll('button');
        let time = document.getElementById('time').innerText;
        for (const node of nodes) {
            if (node.matches(':hover') && ['grid inactive', 'grid flagged_node'].includes(node.className)) {
                window.location.href = `/flag-node/${node.id}`;
            }
        }
    }
  })



