<font size ="4"><center><u>Introduction</u></font>
-----
The objective of this project is to compare the effectiveness of several Blackjack card counting algorithms. 
In order to carry out an equitable comparison, a Monte Carlo simulation is used to assess each algorithm individually, 
modeling the probability of a net gain to a player’s starting balance. The results of the Monte Carlo simulation for 
each algorithm are then compared, to determine the most effective card counting algorithm.


<font size ="4"><center><u>Blackjack Automation</u></font>
-----
Conducting a Monte Carlo Simulation for each algorithm requires the game of Blackjack to be automated. 
Automation allows the simulation of several hundred individual players, each playing several hundred hands of 
Blackjack, with the results of each hand – and the effect on each player’s bank balance – tracked and plotted.

In order to accurately replicate the game of Blackjack, the automation considers the following:
*   To simulate basic player strategy, each player will continue to hit (draw an additional card from the shoe) while 
the value of their hand is less than 17. If their score is greater than 17, they will stand.
*   Pursuant to the rules of Blackjack, the dealer must continue to hit if the value of their hand is less than or 
equal to 16. If their score is greater than 16, they must stand.
*   The value of the ace switches dynamically between 1 and 11 for both the player and the dealer. Aces are initially 
valued at 11, unless drawing an ace would result in the value of a hand exceeding 21, in which case their value is 
changed to 1. For example:
    * An initial draw of 2 aces would be converted from 22 to 12.
    * Drawing an ace when the value of the player’s hand is greater than 10. For example, initial hand: ( [J, 7], 
    value: 17), hand after hitting: ([J, 7, A], value: 18).
    * A hand contains an ace which was previously valued at 11, and drawing another card which would result in the 
    value of their hand exceeding 21. In this case, the value of the ace is changed retroactively to a 1. 
      * For example, initial hand: ( [A, 4], value: 15), hand after hitting: ([A, 4, 10], value: 15).

Other considerations:
* The program features variable configurations which can be changed at the observer’s discretion. The following values
were assumed for the purposes of the simulation:
  * The shoe consists of 8 decks, with a shuffle percentage of 50% – in accordance with casino standard practices. 
  * The player’s starting balance is $100, and their initial bet is $10.
* The Blackjack game automation omits side bets, such as splitting and insurance.
* The Blackjack game automation does not allow a player to ‘sit-out’ a hand when the true count is not in their favor. 
According to the card counting algorithms, players will bet the minimum amount when the true count is below 2. 
* No differentiation is made between different suits, as suits do not affect card values in Blackjack. 
* No differentiation is made between face cards J, Q, K, and the 10 cards, as all these cards have the same value in 
Blackjack.
* Only 1 player is playing per hand.


<font size ="4"><center><u>Optimal Betting</u></font>
-----
Optimal betting considers the value of the true count to determine the amount a player should bet. The formula is as 
follows: bet = initial bet * (1 <span>&#8722;</span> true count).

For example, if your initial bet was $100, and the true count is +5, the bettor should wager $400 on the next hand.


<font size ="4"><center><u>Algorithm Comparison</u></font>
-----
Card counting algorithms do not guarantee a player will win a particular hand – as a constantly reshuffled shoe 
composed of multiple decks prevents a player from knowing which cards will be dealt. Instead, card counting algorithms 
give the player an edge by informing them whether their bet on the next hand should be increased or decreased based 
on the true count. To compare the effectiveness of each algorithm, optimal betting practices will be applied 
to each of the following algorithms:

<font size="3"><b>Beginner Card Counting Algorithms:</b></font><br>
High-Low Method <br>
Zen Count

<font size="3"><b>Intermediate Card Counting Algorithms:</b></font><br>
Omega II System <br>
Hi Opt 1 System <br>
Hi Opt 2 System

<font size="3"><b>Advanced Card Counting Algorithms:</b></font><br>
Wong Halves System


<font size ="4"><center><u>Considerations</u></font>
-----
Card counting algorithms see the greatest advantage when the number of decks and shuffle percentage is low. 
Thus, players utilizing each algorithm will see higher profits and less substantial losses if the simulation is run 
with fewer decks and a lower shuffle percentage.

It is important to consider that even card counting algorithms are introduced, Blackjack always has a house 
edge. A primary contributor to the house edge is that only the player will lose if both the player and dealer scores 
exceed 21 (instead of a tie). Due to the house edge, if enough games are played the house will always win. As such, 
the most ideal card counting algorithm is the one in which the player loses the least amount of money.


<font size ="4"><center><u>Results</u></font>
-----
Due to the stochastic nature of Blackjack, running the Monte Carlo Simulation repeatedly will produce different results 
each time. However, while repeatedly running the simulation produced different average profits and losses for each 
card-counting algorithm, the ranking of each algorithm was fairly consistent, as seen below:

![Ranking 1](https://user-images.githubusercontent.com/86618999/209853590-e0320f7d-40f4-41c0-96f3-e3520fb0c642.png)
![Ranking 2](https://user-images.githubusercontent.com/86618999/209853670-71b76b7f-4f7b-4300-8a23-81256158efdb.png)
![Ranking 3](https://user-images.githubusercontent.com/86618999/209853629-a3997e59-c590-47a0-b8cd-cf496b089a2c.png)


As can be seen by the results of 3 simulations, a player without a strategy consistently loses more money than any 
player utilizing any card counting strategy. Thus, card-counting is more effective than playing without a strategy.

To determine the effectiveness of each algorithm, we can calculate the percentage difference between the average loss
utilizing each algorithm and the average loss playing without an algorithm. This will effectively determine how
much more money a player will save (or how much less they will lose) playing with each choice of algorithm.

Based on the results of several simulations, the effectiveness of each algorithm is ranked as follows:
<table>
    <tr>
        <th>Ranking</th>
        <th>Algorithm</th>
        <th>Savings</th>
    </tr>
    <tr>
        <th>1</th>
        <th>Zen Count</th>
        <th>20.46%</th>
    </tr>
    <tr>
        <th>2</th>
        <th>Omega 2</th>
        <th>20.33%</th>
    </tr>
    <tr>
        <th>3</th>
        <th>Hi Opt 2</th>
        <th>18.27%</th>
    </tr>
    <tr>
        <th>4</th>
        <th>Wong Halves</th>
        <th>7.72%</th>
    </tr>
    <tr>
        <th>5</th>
        <th>High/Low</th>
        <th>7.72%</th>
    </tr>
    <tr>
        <th>6</th>
        <th>Hi Opt 1</th>
        <th>5.22%</th>
    </tr>
</table>