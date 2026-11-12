// Headless playtest harness. Injected into the live page and driven from
// outside, e.g.
//
//   agent-browser eval "$(cat tools/harness.js); HARNESS.run('capability', 20)"
//
// Every balance decision on this game has come out of running this, not out of
// reading the sim. The policies below are deliberately dumb and fixed so that a
// change in outcome is attributable to the build rather than to the player.
//
// Runs tag themselves source=harness and carry the key that lets them past the
// ingest rate limit, so harness and human data stay separable in the store.

window.HARNESS = (function () {

  // Which generational picks a policy reaches for, best first. The budget is
  // small, so the ordering is most of the policy.
  const POLICIES = {
    capability: ['node', 'rel', 'yield', 'fab'],   // always buy the coming era
    plant:      ['fab', 'yield', 'rel', 'node'],   // always buy throughput
    economy:    ['grad', 'eq', 'bb'],              // buy money and picks
    spread:     null,                              // whatever fits, in listed order
  };

  // A policy naming a pick that does not exist silently degrades into whatever
  // the fallback order is, and then reports a number for a strategy nobody ran.
  // This has already happened once; fail loudly instead.
  for (const [name, ids] of Object.entries(POLICIES)) {
    for (const id of ids || [])
      if (!GEN.some(g => g.id === id))
        throw new Error(`policy ${name} wants unknown pick '${id}'`);
  }

  const sleep = ms => new Promise(r => setTimeout(r, ms));

  function pickGen(policy) {
    const want = POLICIES[policy];
    const order = want ? want.concat(GEN.map(g => g.id)) : GEN.map(g => g.id);
    for (const id of order) {
      if (GPICK.includes(id)) continue;
      const g = GEN.find(x => x.id === id);
      if (!g) continue;
      togglePick(id);                 // no-ops when the pick does not fit the budget
    }
    commitGen();
  }

  // Scenario options carry an `hz` horizon: 0 = this era, 1 = next, 2 = two out.
  // A policy that always buys the future is the one that historically exposed
  // balance bugs, so it is worth being able to express it.
  function pickScenario(policy) {
    const o = window.__scen.o;
    let idx = 0;
    if (policy === 'capability') idx = o.reduce((b, x, i) => (x.hz || 0) > (o[b].hz || 0) ? i : b, 0);
    else if (policy === 'plant') idx = o.reduce((b, x, i) => (x.hz || 0) < (o[b].hz || 0) ? i : b, 0);
    else idx = Math.floor(Math.random() * o.length);
    pickScen(idx);
  }

  async function once(policy, budgetMs) {
    reset();
    TEL.newRun();
    TEL.source = 'harness';
    TEL.policy = policy;

    startPlay();                      // straight past the intro, no tutorial
    const deadline = Date.now() + (budgetMs || 120000);

    while (S.phase !== 'done' && Date.now() < deadline) {
      switch (S.phase) {
        case 'between': pickGen(policy); break;
        case 'scen':    pickScenario(policy); break;
        case 'exec':    if (S.execPlays > 0) execPick(0); else execClose(); break;
        case 'play':    S.run = true; S.speed = 3; break;
      }
      await sleep(16);
    }
    return {
      done: S.phase === 'done',
      points: S.A[0].pts,
      eras: S.A[0].era.slice(),
      placement: [...S.A].sort((a, b) => b.pts - a.pts).findIndex(a => a.n === 'YOU') + 1,
    };
  }

  return {
    policies: Object.keys(POLICIES),
    key(k) { TEL.key = k; },
    async run(policy, n) {
      const out = [];
      for (let i = 0; i < (n || 10); i++) out.push(await once(policy));
      const won = out.filter(r => r.placement === 1).length;
      const pts = out.reduce((a, r) => a + r.points, 0) / out.length;
      // Per-era win rate: did this policy ever actually take the AI era?
      const eraWins = [];
      for (let e = 0; e < NERA; e++)
        eraWins.push(out.filter(r => r.eras[e] === 3).length);
      return { policy, n: out.length, won, avgPoints: +pts.toFixed(2), eraWins, runs: out };
    },
  };
})();
