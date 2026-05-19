# Systems Biology 2025/26

### Spatiotemporal Signal Propagation
---

#### Authors:
- Karol Chądzyński
- Paweł Galek
---

#### Table of Contents:
1. Technical Description.
    Simply run the neccesary scripts and the notebook cells.
2. General Description.
    - Short explanation what is the Data, biological context etc.
3. Task A Description.
    - Spatiotemporal analysis executed by using modified existing scripts adn notebooks from the labs and lectures.
ables
4. Task B Description.
    - Our struggle with independent research based on Data.
---
---

## Technical Description 

#### How to obtain Data?

> [TODO]

#### Where to put data?

> You should paste data such as `single-cell-tracks_exp1-6_noErbB2.csv.gz` into the `raw_data/` directory.

#### How to install dependencies?

> To run project properly you should install dependecies by `pip install -r Task[A|B]/requirements.txt`

#### How to run Task A?

> Simply run the neccesary script - "compare_spatiotemporal_behavior.py" and the notebook cells from top to bottom.

#### How to run Task B?

> Run [TODO].py file from `TaskB/run_everything/[TODO].py`

#### Project Structure

```
ROOT/
    TaskA/[the provided structure from the assignment pdf]
    TaskB/
        data_in_processing/ - Temporary Data
        notebooks/ - Notebooks (.ipynb)
        outputs/ - pictures & GIFs used in Report.pdf & README.md
        run_everything/ - Scripts for reproducting TaskA (.py)
        scripts/ - Scripts (.py)
    Assigment.pdf - Assigment File by Krzysztof Gogolewski
    README.md - You are reading it right now!
    requirements.txt - requirements in python for project to run
    Report.pdf - Report for Krzysztof Googolewski
```

## General Description

#### What does Data consist of?

Spatiotemporal Data concerning the spread of ERK signal waves.

#### What is the Biological Context?

We wish to study how the signal spreads through tissue in real time and how variables such us mutations impact this phenomenon.

## Task A Description

Guided analysis modifying existing scripts with clear deliver-
ables

## Task B Description

Independent Research.

We have:

1. Scaled Data with `MinMaxScaler` `track_id`-independently, across all time-steps.
2. Make Bounded Voronoi Graph from each time-step.
3. Create Graph where nodes are `track_id`s and edges neighbourhoods based on (2.).
4. Calculated `Time-Chain`s - by what we mean:
    - `n = 5` time-steps with diffrence in `ERKKTR_ratio_scaled` (on `T -> T+1`) from recursive search across neighbours of neighbours of neighbours [...] of all nodes in each time.
    - Basically we have analyzed `n` nodes in from `T=0`, to `T=n-1`, each node corresponding as the neighbour of previous, in previous time.
