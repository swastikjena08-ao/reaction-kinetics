# Reaction Kinetics Simulations

Three chemical-engineering simulation projects implemented in Python:

1. **First-order reaction decay** - analytical concentration decay and half-life.
2. **Arrhenius temperature dependence** - reaction-rate comparison from 280 K to 340 K.
3. **Sequential reaction A -> B -> C** - species profiles and optimal time for maximizing intermediate B.

## Run

```bash
pip install -r requirements.txt
python projects_1_to_3_reaction_kinetics.py
```

The script creates PNG charts and CSV datasets under `results/`.

## Main findings

- First-order half-life: **6.93 s**
- Rate increase from 280 K to 340 K: **44.3x**
- Intermediate B peaks at **0.500 mol/L after 13.86 s**

The Arrhenius plot uses a millisecond scale because the supplied kinetic parameters imply sub-millisecond reaction times.
