# EuchrePy
An implementation of Euchre written to satisfy my final project requirement for CS50P

<img width="1020" alt="Screenshot 2023-07-22 at 10 09 51 PM" src="https://github.com/anishjv/EuchrePy/assets/119087858/11def7b5-1981-4b46-836f-246cc7adfcc0">


# Implementation 
This program runs a version of euchre called "screw the dealer" in which the dealer is forced to choose Trump after the 7th move, this program currently does not support the "classic" version or a strategy known as "going-alone"

# Rules
For detailed rules on how to play euchre see https://bicyclecards.com/how-to-play/euchre/ 

# TODO
* Implement an AI to play as players 1, 2, and 3
* Allow support for "classic" mode and "going-alone" gameplay
* Improve the Graphics to keep images centered
* Remove the need to interact with pygame through the command-line

# Keys & CLI Instruction
**The following are Keys to press in the pygame window**
* P: Pass on your move
* T: Call Trump
  
**The following are commands to type, when prompted, into the command-line**
* (0, 1, 2, 3, or 4): When asked what card you would like to play. 0, 1, 2, 3 and 4 correspond to the index of the card in your hand
* (0, 1, 2, 3, or 4): After pressing T, you will be prompted to select the Trump suit through the command-line
* (Yes or No): After pressing T, player 0 will be asked if they would like to pick up the "kitty" or not
* (0, 1, 2, 3, or 4): After agreeing to pick up the "kitty", player 0 will be asked for the index of the card in their hand that they would like to discard





