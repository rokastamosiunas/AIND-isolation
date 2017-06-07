# Isolation tactics - heuristic analysis

In this short note I will try to reason why and how my custom scoring metrics were selected. First, let's see if those metrics perform well compared with other demo scoring functions.

```
                        *************************
                             Playing Matches
                        *************************

 Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3
                        Won | Lost   Won | Lost   Won | Lost   Won | Lost
    1       Random      10  |   0    10  |   0    10  |   0    10  |   0
    2       MM_Open      7  |   3     7  |   3     6  |   4     6  |   4
    3      MM_Center    10  |   0     9  |   1     9  |   1     7  |   3
    4     MM_Improved    4  |   6     9  |   1     4  |   6     5  |   5
    5       AB_Open      4  |   6     7  |   3     7  |   3     5  |   5
    6      AB_Center     7  |   3     6  |   4     8  |   2     8  |   2
    7     AB_Improved    4  |   6     5  |   5     5  |   5     4  |   6
--------------------------------------------------------------------------
           Win Rate:      65.7%        75.7%        70.0%        64.3%
```

Definitions:

* **AB_Custom** - combination of *AB_Custom_2* and *AB_Custom_3*.
* **AB_Custom_2** - combination of my available moves vs. opponent available moves which adjust weights to my favor as the game progresses. 
* **AB_Custom_3** - my available moves adjusted by current player positions relative to the center and themselves.

You will note that *AB_Custom_2* has only a slight change compared to scoring function presented in the lectures, but is able to beat *Improved* score from time to time. Intuition behind this change follows a simple reasoning. At the beginning of the game it might be wise to block you opponent and at the same time choose positions which have more movement freedom. As the game progresses there are less free spaces and trying to block your opponent might be a waist of resources, thus opponent moves are weighted by game state multilayer, which is close to 1 at the beginning of the game and decreases as the game progresses.

*AB_Custom_3* takes completely different approach and favors positions which are close to the center, but further from the opponent. Distance is measured by log Manhattan distance. The main reasoning is to capture the center while keeping position which has more available moves at the same time pushing opponent to the border. If opponent will try to fight for the center such scoring will ensure that I get close to the center too, but if opponent gets close to the border I have complete freedom of movement on the other side of the board.

After running *AB_Custom_3* and *AB_Custom_2* for multiple times I have noted, that *AB_Custom_3* outperforms *AB_Custom_2* if my agent is player 1. In the game of Isolation, player 2 has slightly better starting point since he can follow player 1 and if they both end up in a closed region, then almost player 1 will almost certainly loose since he has to start. This reasoning is especially evident if you try to think about small boards first. Thus, it is reasonable for player 1 to run away (this is the feature of *AB_Custom_3*) and for player 2 to hunt down player 1 (this is the featore of *AB_Custom_2*). Thus, *AB_Custom* is a simple combination which chooses *AB_Custom_3* if my agent is player 1 and *AB_Custom_2* otherwise. As seen in the score board above, it turns out to be quite good tactic, leading to ~75% of victories.

**A note on AB_Custom performance:** combination of *AB_Custom_2* and *AB_Custom_3* outperforms simple *AB_Improved* and leads to **15% increase in win rate** when comparing those two methods. Not only that, the complexity of *AB_Custom* is still on the low side and **uses only current tree layer info**: board dimensions; number of blank spaces; player locations and available moves. Note, that *AB_Custom* **outperforms *AB_Improved* or produces nearly identical score while playing with other opponents**, thus it is almost certainly a better option. Still it's a pitty, that *AB_Custom* is not able to beat *AB_Improved*, even running the game between those two opponents for 100 times led only to 56% win rate for *AB_Custom* (this does not seem to be significant).

**What's next:** scoring is highly affected by chance, thus to get better approximations of win rates would need much more games. Either way it looks like the idea of having separate tactics for player 1 and player 2 is a good way to proceed. *AB_Custom_2* and *AB_Custom_3* were not created especially for such purpose, thus there is huge opportunity for optimizing weights or even adding more complexity, especially designed based on who is a starting player.


---
For Udacity AI Nanodegree (Project 2 submitted 2017-06-06), more details: https://www.udacity.com/ai.
