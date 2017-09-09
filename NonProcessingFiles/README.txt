# Python with Processing

This project was written in Processing's Python mode, which can be installed by clicking the Mode
dropdown in the top right > Add Mode > Install Python Mode for Processing 3. Sorry if including
those instructions was patronizing; I'm sure you know how to do this, but I didn't want to take
any chances.

# IMPORTANT NOTICE ABOUT "COMPILE" ERRORS (aka please don't penalize me for Processing's problems)

There is an issue with Processing that has plagued me throughout this assignment. Every time I try 
to run the code immediately after opening the Processing project, it gives me a nondescript Java 
error and won't run. The error starts with:

    Exception in thread "AWT-EventQueue-0" java.lang.NullPointerException

and I have no idea what causes it. It seems to be fixed by switching to every tab in the project 
at least once, and once it's run once it will work until you close Processing. I'm extremely sorry 
for this inconvenience; if you have any problems getting it to work, let me know. 

# Known bugs

Sometimes the ball gets reset to the very edge of the screen, instead of in the middle. Since 
the reset() function is only capable of placing it at width/2 I have no clue how this could 
possibly happen. If it happens once, it keeps happening until the player bounces it away from 
the edge.

# How to play

Standard slime volleyball. Nothing special about it, other than the game waits a second after a 
score and doesn't wait for user input.

# Gamemodes

The various "gamemodes" available (run bot training, play against bots, watch bot vs bot, etc) are
controlled by the variables at the top of the main file. 

	BOT_MODE: 
		True:  Run evolutionary arms race (the latest generation plays a round robin and the two 
		best scoring bots crossover/mutate to create the next generation)
		False: The human plays against a bot
	BOT_V_BOT:
		True:  A live, non-learning match is played by two bots
		False: The human plays against a bot
	TEST_GEN:
		<Number of a generation>: Load bots from the given generation
		None: Load bots from the latest generation
	TEST_INDEX:
		<Number 0-9>: Load the bot corresponding with the given number from whatever generation 
		has been selected
		None: Load a random bot from whatever generation has been selected

