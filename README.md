# The Classic BINGO

This is a virtual version of classic 5*5 grid BINGO game using pygame. The user and bot compete to select 5 rows either horizontally, vertically or diagonally to win.

***

<div align="center">
    <img src="https://github.com/Advait-Shrivastava/The-Classic-BINGO/assets/59224726/2af3a093-3bd5-4cc2-94a2-0694149026b9">
</div>

***

<div align="center">
    <img src="https://github.com/Advait-Shrivastava/The-Classic-BINGO/assets/59224726/d5a3aaa2-c1d1-4050-bc89-05f75f93d82f">
</div>

***

## Description


The game operates with two distinct grids: one designated for the user and another for the bot. Each grid comprises numbers ranging from 1 to 25.The user interactively populates their grid by selecting individual cells through mouse clicks.On the other hand, the bot's grid is randomly generated.The game proceeds in turns, with the user initiating the gameplay.Upon selecting and striking off a number, the corresponding number on the bot's grid is also struck off.Subsequently, the bot reciprocates by selecting and marking a number, which is then reflected on the user's grid.This alternating sequence persists until one of the grids accumulates five struck-off rows in a horizontal, vertical, or diagonal arrangement.The player who accomplishes this milestone first is declared the winner. 

***


## Requirements

* python 3.10
* Packages :
    * pygame
    * playsound

***

## Execution
 1. `pip install -r requirements.txt`
 2. `python3 bingo.py`
