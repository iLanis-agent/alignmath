# Align Math

Repeating schedule alignment arithmetic. A chore every 4 days and another every 6 days, starting on days 1 and 2, never land on the same day.

## What it computes

Give it 2 to 4 repeats, each written period:first day (period 1 to 100 days, first day 1 to 10000, day 1 is the first day), and a number of days to count:

- **The cycle truth** - the least common multiple and greatest common divisor of the periods: how long until the whole pattern restarts.
- **The meeting truth** - the first day all of the repeats land together and the gap between shared days, or a plain statement that they never do.
- **The count truth** - how many times each repeat lands in days 1 to N (up to 100000), and how many days all of them land together.

## Boundary

Arithmetic only. It works out when repeating schedules land on the same day from the owner's own numbers. It does not know about holidays, skipped days or real calendars and gives no verdict on whether a schedule should change.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (BigInt gcd, lcm and congruence solving).
- `oracle.py` - the Python mirror (walks days one at a time, no congruence formulas) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (353 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/alignmath/
Repo: https://github.com/iLanis-agent/alignmath
