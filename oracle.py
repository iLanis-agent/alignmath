#!/usr/bin/env python3
# Align Math oracle - mirrors engine.js. It finds shared days by walking the slowest schedule's days, and counts by walking every day.
import json, re, random
from math import gcd, lcm

REP_ERR = "enter 2 to 4 repeats as period:first day, separated by commas, for example 4:1, 6:2 (periods 1 to 100 days, first days 1 to 10000)"
HOR_ERR = "the number of days must be a whole number from 1 to 100000"

def reps(t):
    t = t.strip() if isinstance(t, str) else ""
    parts = [x.strip() for x in t.split(",")]
    if not 2 <= len(parts) <= 4: raise ValueError(REP_ERR)
    out = []
    for x in parts:
        m = re.fullmatch(r"([0-9]{1,3})\s*:\s*([0-9]{1,5})", x)
        if not m: raise ValueError(REP_ERR)
        p, f = int(m.group(1)), int(m.group(2))
        if not (1 <= p <= 100 and 1 <= f <= 10000): raise ValueError(REP_ERR)
        out.append((p, f))
    return out

def plural(n, one, many): return f"{n} {one if n == 1 else many}"
def lst(a): return a[0] if len(a) == 1 else ", ".join(a[:-1]) + " and " + a[-1]

def lands(p, f, d): return d >= f and (d - f) % p == 0

def first_shared(r):
    # walk the days of the item with the biggest period, from its first day, for one full pattern length
    big = max(r, key=lambda x: x[0])
    span = 1
    for p, _ in r: span = lcm(span, p)
    start = max(f for _, f in r)
    # first day >= start where the big item lands
    d = big[1]
    if d < start:
        d += -(-(start - d) // big[0]) * big[0]
    for _ in range(span // big[0] + 2):
        if all(lands(p, f, d) for p, f in r):
            return d, span
        d += big[0]
    return None

def cycle(t):
    r = reps(t)
    L = 1; G = 0
    for p, _ in r: L = lcm(L, p); G = gcd(G, p)
    last = r[-1][0]
    return f"Repeating every {lst([str(p) for p, _ in r])} {'day' if last == 1 else 'days'}: the pattern restarts after {plural(L,'day','days')}, the least common multiple. The greatest common divisor is {G}."

def meeting(t):
    r = reps(t)
    s = first_shared(r)
    if s is None:
        return "These never land on the same day. Each pair of schedules needs the gap between its first days to be a multiple of the greatest common divisor of its two periods, and at least one pair here is not."
    return f"All {len(r)} land on the same day for the first time on day {s[0]}, then every {plural(s[1],'day','days')} after that."

def count(t, days):
    r = reps(t)
    days = days.strip() if isinstance(days, str) else ""
    if not re.fullmatch(r"[0-9]{1,6}", days) or not 1 <= int(days) <= 100000: raise ValueError(HOR_ERR)
    n = int(days)
    counts = [0] * len(r); shared = 0
    for d in range(1, n + 1):
        hit = [lands(p, f, d) for p, f in r]
        for i, h in enumerate(hit):
            if h: counts[i] += 1
        if all(hit): shared += 1
    head = "On day 1: " if n == 1 else f"In days 1 to {n}: "
    return head + ", ".join(f"{chr(65+i)} lands {plural(c,'time','times')}" for i, c in enumerate(counts)) + f". All of them land on the same day {plural(shared,'time','times')}."

FNS = {"cycleTruth": cycle, "meetingTruth": meeting, "countTruth": count}

def cases():
    c = []
    rnd = random.Random(693)
    sets = ["4:1, 6:2", "4:1, 6:3", "6:2, 8:4, 9:5", "1:1, 1:1", "1:5, 7:3", "100:10000, 99:9999", "100:1, 99:1, 98:1, 97:1",
            "7:1, 7:1", "7:1, 7:2", "7:3, 14:10", "12:12, 18:18", "2:1, 3:1, 5:1, 7:1", "10:7, 15:2", "4:9, 6:3",
            " 4 : 1 , 6 : 3 ", "4:1", "4:1, 6:2, 8:3, 9:4, 10:5", "4:0, 6:1", "0:1, 6:1", "101:1, 6:1", "4:10001, 6:1", "4:1;6:2", "4-1, 6-2", "", "a:b, c:d", "6:1,6:1,6:1,6:1", "60:1, 45:1, 20:1"]
    for _ in range(45):
        k = rnd.randint(2, 4)
        sets.append(", ".join(f"{rnd.randint(1,100)}:{rnd.randint(1,10000)}" for _ in range(k)))
    for _ in range(25):
        k = rnd.randint(2, 4)
        sets.append(", ".join(f"{rnd.randint(1,30)}:{rnd.randint(1,60)}" for _ in range(k)))
    for s in sets:
        c.append(("cycleTruth", [s])); c.append(("meetingTruth", [s]))
    for s in sets[:30] + sets[-30:]:
        for h in ["60", "1"] + ([str(rnd.randint(1, 3000))] if s in sets[-30:] else []):
            c.append(("countTruth", [s, h]))
    for h in ["0", "100001", "100000", "abc", "", " 12 ", "1.5", "-4", "0012"]:
        c.append(("countTruth", ["4:1, 6:3", h]))
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1); f.write("\n")
print(len(out), "cases written")
