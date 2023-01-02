# Intro
This is a project to code Minesweeper. 

# Game Play
I coded this game to be as how the original is intended to play. 
There is a game full of nodes laid out in the dimensions selected 
by the player based off of difficulty(Beginner 10x10, Medium 15x15,
Hard 25x25, and Test 5x5). Each node has a value that represents
how many mines are surrounding it. If there are no mines surrounding
the node, then it is blank. The player can flag down any node 
they believe to be a mine (by pressing the 'M' key while hovering
over the node they wish to flag). If they believe they have flagged down
the right nodes, then they can select the base node(the node with
the flagged nodes surrounding it) to check if they guessed right.
If they guessed right then the inactive nodes surrounding the base 
node will activate. However, if they guessed wrong, then any wrongly
flagged nodes will turn purple, and the player will get a penalty
of +10 seconds added to their score (there is a timer displaying the
player's time/score) for each wrongly flagged node. In order for the 
player to win the game, they must activate all nodes that do not 
have a mine in (this includes purple nodes). If a player clicks
on a node with a mine, they will activate all the mines and lose
the game. There is a mine counter that will let the player know how many 
mines are left based off of how many nodes were flagged. However, the
counter does not tell the player if they accurately flagged down the right
nodes because if they flag too many nodes then the counter will go negative.
The counter is mostly there to let the player keep track of how many mines
are left to go if they wish to flag nodes down. If the player 
forgot any of the rules, they can click on the '?' button, and the 
instructions will be displayed(it can be toggled). Lastly, the test section 
is just to try out the mechanics, and currently the number of mines
for each game difficulty is 15% of the total nodes.

# Leaderboard
There is a leaderboard on the home page that displays the top 10 players
for each difficulty. Their scores are just the time it took them to complete
the game. The score box will only display for a player if they beat a
score on the leaderboard(except it displays after completing every 
test game because those are displayed on the leaderboard for testing
purposes and only the 5 most recent games are kept). Players who rank 1st
place get a trophy depending on the difficulty of their game(bronze, 
silver, and gold). In addition, there is a chance to win a game on the first
node and getting a score of 0 time and that is not a bug it is part of the
game. The mines are randomly selected. If they all bunch up together, then
there is a chance of winning the game on the first node clicked. However, there
is a very low chance of winning like that (1 in 800,000 on a 8x8 game), and 
with the game difficulties I have laid out it is even rarer to get a first node
win. Yet, I still chose to make a section on the leaderboard for any first
node winner (minus test games because the chances of getting a first node win
is very high if you select the middle node first) that comes with a four
leaf clover next to their name.

# To do list
- add a custom game mode that will allow players to customize any 
detail of the game such as (length, width, and number of mines).
- add a custom section to the leaderboard that ranks custom games
based off of the number of mines, score, and dimensions of the game.
- add more shapes to the game. I think it would be really fun
if the player could select what shape game they wanted to play. 
There could be a feature to draw somthing in a small MS Paint type
field, then a game is generated based off of the drawn image.
- there should be a hint button that when pressed flags down a
mine on the game (with a special style to set it apart from
normal flags) that the player could use if they were having a 
hard time completing the game. However, taking hints should maybe come with penalties(maybe 
+60 seconds to the score).