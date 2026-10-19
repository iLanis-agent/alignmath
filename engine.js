// Align Math engine: when repeating schedules (every N days, from a first day) line up. BigInt gcd, lcm and congruence solving.
var REP_ERR = "enter 2 to 4 repeats as period:first day, separated by commas, for example 4:1, 6:2 (periods 1 to 100 days, first days 1 to 10000)";
var HOR_ERR = "the number of days must be a whole number from 1 to 100000";

function _reps(t) {
  t = typeof t === "string" ? t.trim() : "";
  var parts = t.split(",").map(function (x) { return x.trim(); });
  if (parts.length < 2 || parts.length > 4) throw new Error(REP_ERR);
  return parts.map(function (x) {
    var m = /^([0-9]{1,3})\s*:\s*([0-9]{1,5})$/.exec(x);
    if (!m) throw new Error(REP_ERR);
    var p = parseInt(m[1], 10), f = parseInt(m[2], 10);
    if (p < 1 || p > 100 || f < 1 || f > 10000) throw new Error(REP_ERR);
    return { p: BigInt(p), f: BigInt(f) };
  });
}
function _gcd(a, b) { while (b !== 0n) { var t = a % b; a = b; b = t; } return a; }
function _lcm(a, b) { return (a / _gcd(a, b)) * b; }
function _mod(a, m) { return ((a % m) + m) % m; }
function _inv(a, m) {
  // modular inverse of a mod m by extended Euclid (m >= 1, gcd(a, m) = 1)
  if (m === 1n) return 0n;
  var r0 = m, r1 = _mod(a, m), s0 = 0n, s1 = 1n;
  while (r1 !== 0n) {
    var q = r0 / r1;
    var r2 = r0 - q * r1; r0 = r1; r1 = r2;
    var s2 = s0 - q * s1; s0 = s1; s1 = s2;
  }
  return _mod(s0, m);
}
function _plural(n, one, many) { return n + " " + (String(n) === "1" ? one : many); }
function _list(a) {
  if (a.length === 1) return a[0];
  return a.slice(0, -1).join(", ") + " and " + a[a.length - 1];
}
function _name(i) { return String.fromCharCode(65 + i); }

// Returns null when no day is shared, else {d, M}: first shared day and the gap between shared days.
function _meet(reps) {
  var x = _mod(reps[0].f, reps[0].p), M = reps[0].p;
  for (var i = 1; i < reps.length; i++) {
    var a = _mod(reps[i].f, reps[i].p), m = reps[i].p;
    var g = _gcd(M, m);
    if (_mod(a - x, g) !== 0n) return null;
    var m2 = m / g;
    var k = _mod(((a - x) / g) * _inv(M / g, m2), m2);
    x = x + M * k;
    M = M * m2;
    x = _mod(x, M);
  }
  var big = reps.reduce(function (acc, r) { return r.f > acc ? r.f : acc; }, 0n);
  var d = x;
  if (d < big) d = x + M * ((big - x + M - 1n) / M);
  return { d: d, M: M };
}

function cycleTruth(reps) {
  var r = _reps(reps);
  var L = r.reduce(function (a, x) { return _lcm(a, x.p); }, 1n);
  var G = r.reduce(function (a, x) { return _gcd(a, x.p); }, 0n);
  var last = r[r.length - 1].p;
  return "Repeating every " + _list(r.map(function (x) { return String(x.p); })) + (last === 1n ? " day" : " days") + ": the pattern restarts after " + _plural(L, "day", "days") + ", the least common multiple. The greatest common divisor is " + G + ".";
}
function meetingTruth(reps) {
  var r = _reps(reps);
  var m = _meet(r);
  if (m === null) {
    return "These never land on the same day. Each pair of schedules needs the gap between its first days to be a multiple of the greatest common divisor of its two periods, and at least one pair here is not.";
  }
  return "All " + r.length + " land on the same day for the first time on day " + m.d + ", then every " + _plural(m.M, "day", "days") + " after that.";
}
function countTruth(reps, days) {
  var r = _reps(reps);
  days = typeof days === "string" ? days.trim() : "";
  if (!/^[0-9]{1,6}$/.test(days)) throw new Error(HOR_ERR);
  var n = parseInt(days, 10);
  if (n < 1 || n > 100000) throw new Error(HOR_ERR);
  var N = BigInt(n);
  var counts = r.map(function (x) { return N < x.f ? 0n : (N - x.f) / x.p + 1n; });
  var m = _meet(r);
  var shared = m === null || N < m.d ? 0n : (N - m.d) / m.M + 1n;
  var head = n === 1 ? "On day 1: " : "In days 1 to " + n + ": ";
  return head + counts.map(function (c, i) { return _name(i) + " lands " + _plural(c, "time", "times"); }).join(", ") + ". All of them land on the same day " + _plural(shared, "time", "times") + ".";
}
