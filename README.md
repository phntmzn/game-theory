# game-theory

Absolutely. If you're building a **game-theory Python collection**, there are many classic strategic games and repeated-game strategies similar to **Mutual Assured Destruction (MAD)** and **Grim Trigger**.

### Repeated-game / strategic scenarios

| Game / Strategy | Basic idea |
|---|---|
| **Prisoner's Dilemma** | Two players choose cooperation or defection |
| **Grim Trigger** | Cooperate until the opponent defects once; then defect forever |
| **Tit-for-Tat** | Start cooperating, then copy the opponent's previous move |
| **Generous Tit-for-Tat** | Usually copy defection, but occasionally forgive |
| **Pavlov / Win-Stay Lose-Shift** | Keep successful actions; change after unsuccessful ones |
| **Always Cooperate** | Always choose cooperation |
| **Always Defect** | Always choose defection |
| **Tit-for-Two-Tats** | Forgive one isolated defection |
| **Suspicious Tit-for-Tat** | Start with defection, then copy the opponent |
| **Trigger Strategy** | Punishment begins after a specified violation |
| **Mutual Assured Destruction** | Escalation makes mutual attack extremely costly |
| **Chicken / Hawk-Dove** | Two players escalate until one backs down |
| **Stag Hunt** | Cooperation has a large payoff, but requires trust |
| **Battle of the Sexes** | Players prefer different coordinated outcomes |
| **Coordination Game** | Players benefit from choosing the same action |
| **Volunteer’s Dilemma** | Everyone benefits if someone takes the costly action |
| **Public Goods Game** | Players decide whether to contribute to a shared resource |
| **Tragedy of the Commons** | Individual incentives can deplete a shared resource |
| **Ultimatum Game** | One player proposes how to divide resources |
| **Dictator Game** | One player unilaterally chooses a division |
| **Trust Game** | One player sends resources and relies on another to reciprocate |
| **Centipede Game** | Players repeatedly choose between taking resources or continuing |
| **War of Attrition** | Players decide how long to keep competing |
| **Stackelberg Game** | One player moves first and another responds |
| **Bertrand Competition** | Firms compete by choosing prices |
| **Cournot Competition** | Firms compete by choosing quantities |
| **Zero-Sum Game** | One player's gain equals another player's loss |
| **Matching Pennies** | Players benefit from making opposite/same choices |
| **Minority Game** | Players want to be in the smaller group |

### A particularly interesting 4-player version

You can model **Mary, Bob, Alice, and Sue** as countries in a repeated escalation game:

```text
Each round:

        Cooperate
            |
            v
       ┌─────────┐
       │ Observe │
       └────┬────┘
            |
       Did someone
          defect?
        /       \
      No         Yes
      |           |
      v           v
 Continue      Punish
 cooperating     |
                  v
             Escalation
```

And give each player a strategy:

```python
strategies = {
    "Mary": "grim_trigger",
    "Bob": "tit_for_tat",
    "Alice": "always_defect",
    "Sue": "generous_tit_for_tat",
}
```

Then simulate hundreds of rounds:

```python
import random


PLAYERS = ["Mary", "Bob", "Alice", "Sue"]


def grim_trigger(history, player):
    if not history:
        return "C"

    for round_ in history:
        if round_[player] == "D":
            return "D"

    return "C"


def tit_for_tat(history, player):
    if not history:
        return "C"

    opponents = [
        p for p in PLAYERS
        if p != player
    ]

    # Copy the previous action of the first opponent.
    return history[-1][opponents[0]]


def always_defect(history, player):
    return "D"


def always_cooperate(history, player):
    return "C"


def choose(strategy, history, player):
    if strategy == "grim_trigger":
        return grim_trigger(history, player)

    if strategy == "tit_for_tat":
        return tit_for_tat(history, player)

    if strategy == "always_defect":
        return always_defect(history, player)

    if strategy == "always_cooperate":
        return always_cooperate(history, player)

    raise ValueError(strategy)


strategies = {
    "Mary": "grim_trigger",
    "Bob": "tit_for_tat",
    "Alice": "always_defect",
    "Sue": "always_cooperate",
}


history = []

for round_number in range(10):
    actions = {}

    for player in PLAYERS:
        actions[player] = choose(
            strategies[player],
            history,
            player,
        )

    history.append(actions)

    print(
        f"Round {round_number + 1}:",
        actions
    )
```

A good next step would be to build a **`game_theory/` Python repo with 30 separate simulations**, including MAD, Grim Trigger, Tit-for-Tat, Chicken, Stag Hunt, Prisoner's Dilemma, Tragedy of the Commons, War of Attrition, and evolutionary strategies.