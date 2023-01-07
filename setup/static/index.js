/*   the time for the games works by having two clocks. One for the front end and one for the back end.
     The front end clock just ticks from whatever time it is given. The back end 'clock' just has the start time of the
    game saved from the time module and everytime the backend is called we calculate the current time and update the
    time that is displayed omn the front end. The reason we need to do this is because every time a player interacts
    with the front end there is lag and the clock will not run. So if there wasn't a way to update time in the back end
    then a player could just keep clicking on nodes to stop the time from running and get a really low score. */
// var sec is the time for each game
var sec = 0;
function pad ( val ) { return val > 9 ? val : "0" + val; }
setInterval( function(){
    // fetch game status to know if we should stop updating the time
    // if className == 'hide' then the game over message has not shown and we can keep updating the time
    let game_status = document.getElementById('game_over');
    if (game_status.className == 'hide') {
        // update time
        $("#seconds").html(pad(++sec%60));
        $("#minutes").html(pad(parseInt(sec/60,10)));
    }
}, 1000);

// this function is to pass info to the backend and then refresh the page
function check_value(node_id) {
    window.location.href = `/check-node-value/${node_id}`;
}

// this function is used as an onload function in the body tag to update the game's time everytime the page is refreshed
function update_time(time) {
    sec = time;
}

// this function is to let the user add and remove flags with the 'm' key
window.addEventListener("keydown", function(e) {
    // code 77 if for 'm' so if m is clicked then the user is trying to flag/unflag something
    if (e.keyCode === 77) {
        // fetch all buttons to see which node the user is hovering over
        const nodes = document.querySelectorAll('button');
        // loop through the nodes to update their styles
        for (const node of nodes) {
            // find the node that is being hovered over when the user pressed 'm'
            // this will only call the back end function for nodes that are inactive and flagged
            if (node.matches(':hover') && ['grid inactive', 'grid flagged_node'].includes(node.className)) {
                // call the back end flag function
                window.location.href = `/flag-node/${node.id}`;
            }
        }
    }
})

function help() {
    var x = document.getElementById("key");
    x.classList.toggle("hide");
}

