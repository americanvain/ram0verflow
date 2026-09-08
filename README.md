<h1 align="center">ROFL</h1>

<p align="center">
  <em>A small Bitcoin-like chain whose canonical ledger is this README.</em><br>
  <sub>Proof of work is subset-sum, not hashing — so mining rewards a better solver, not better hardware</sub>
</p>

<p align="center">
  <a href="https://ram0verflow.github.io/ram0verflow/"><b>Block explorer</b></a> ·
  <a href="SPEC.md"><b>Consensus spec</b></a> ·
  <a href="../../issues/1"><b>Mine a block</b></a> ·
  <a href="../../issues/2"><b>Send coins</b></a> ·
  <a href="../../actions"><b>Node</b></a>
</p>

---

<!-- ROFL:BEGIN -->

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/ledger-dark.svg?v=576"><img src="assets/ledger-light.svg?v=576" width="100%" alt="ROFL ledger, height 576"></picture>

| | |
|---|---|
| **height** | `576` |
| **tip** | `c1488e8f4e3f2a881101e3616e9eb775ebcea128a803259c8f168584625b0fbd` |
| **difficulty** | `110,947,920,439,919,360.0`  (bits `0x170a643d`) |
| **chainwork** | `44,633,694,352,467,524,310,977,140` expected hashes |
| **supply** | `17712.50000000 ROFL` in `576` unspent outputs |
| **next reward** | `12.50000000 ROFL` |
| **next retarget** | in `15` block(s) |
| **next halving** | in `53` block(s) |
| **transactions** | `578` |

### Recent blocks

| # | hash | miner | message | txs | reward | mined |
|--:|---|---|---|--:|--:|---|
| `576` | `c1488e8f4e3f2a881101…` | [@eltociear](https://github.com/eltociear) | `gm - block 2 of 4` | `1` | `12.50000000` | 2026-09-08 06:11 UTC |
| `575` | `23e9277e04d8ef482bd7…` | [@eltociear](https://github.com/eltociear) | `gm - block 1 of 4` | `1` | `12.50000000` | 2026-09-08 06:06 UTC |
| `574` | `bf8ff91770cfcfbb1520…` | [@eltociear](https://github.com/eltociear) | `gm - block 4 of 4` | `1` | `12.50000000` | 2026-09-08 05:59 UTC |
| `573` | `47d27169488eae0c4d33…` | [@eltociear](https://github.com/eltociear) | `gm - block 3 of 4` | `1` | `12.50000000` | 2026-09-08 05:53 UTC |
| `572` | `95df73180d3c6c8dfccc…` | [@eltociear](https://github.com/eltociear) | `gm - block 2 of 4` | `1` | `12.50000000` | 2026-09-08 05:48 UTC |
| `571` | `88cc87d08de266f9670d…` | [@eltociear](https://github.com/eltociear) | `gm - block 1 of 4` | `1` | `12.50000000` | 2026-09-08 05:42 UTC |
| `570` | `e1e9e4ba77f851a3fafb…` | [@eltociear](https://github.com/eltociear) | `gm - block 1 of 2` | `1` | `12.50000000` | 2026-09-08 04:48 UTC |
| `569` | `3bb63d2127d90edd094a…` | [@eltociear](https://github.com/eltociear) | `gm - block 2 of 2` | `1` | `12.50000000` | 2026-09-08 04:36 UTC |
| `568` | `17fd39c0b3b8ff3674fd…` | [@eltociear](https://github.com/eltociear) | `gm - block 1 of 2` | `1` | `12.50000000` | 2026-09-08 04:28 UTC |
| `567` | `fa996fecbd3836da4261…` | [@eltociear](https://github.com/eltociear) | `gm - block 1 of 4` | `1` | `12.50000000` | 2026-09-08 04:00 UTC |

### Miners

| miner | blocks | share |
|---|--:|--:|
| [@ksanjeev284](https://github.com/ksanjeev284) | `484` | `83.9%` |
| [@eltociear](https://github.com/eltociear) | `46` | `8.0%` |
| [@ram0verflow](https://github.com/ram0verflow) | `45` | `7.8%` |
| [@axewhyzed](https://github.com/axewhyzed) | `1` | `0.2%` |
| [@notram0verflow](https://github.com/notram0verflow) | `1` | `0.2%` |

### Balances

_Find your own name here once you have run `python3 wallet.py identity`._

| holder | address | balance |
|---|---|--:|
| [@ksanjeev284](https://github.com/ksanjeev284) | `rofl1qn2wv00sq9a875c7pmqf4hfu2ca2y7fa0le96wk` | `15087.50000000 ROFL` |
| _unclaimed_ | `rofl1qhkhmy848s09y2jyly8jexk4gd3gnrrclxj2exx` | `1850.00000000 ROFL` |
| [@eltociear](https://github.com/eltociear) | `rofl1qdsfz9v9r2hc798k26egt33zxj8ysg4cgwgcw2z` | `575.00000000 ROFL` |
| _unclaimed_ | `rofl1q3jwm3gz2s9xy7wa5hg0cgcn9k2s56uma79ynfl` | `150.00000000 ROFL` |
| _unclaimed_ | `rofl1q5yjjcsx8nmxxej5djurawqyxepzhqwcxumhret` | `50.00000000 ROFL` |

### Recent transfers

| block | from | to | amount | note |
|--:|---|---|--:|---|
| `11` | `rofl1qhkhmy848s0…` | `rofl1q3jwm3gz2s9…` | `100.00000000` | gm @notram0verflow |

<sub>Rendered from `chain/blocks.jsonl` at height 576. Verify it yourself: <code>python3 verify.py</code></sub>

<!-- ROFL:END -->

---

## What this is

Everything here is real except the money. Coins move in UTXOs, spent by ECDSA
signatures over secp256k1 — the same curve Bitcoin uses, with RFC 6979
deterministic nonces and low-s enforcement. Difficulty retargets every 16
blocks against how long the last window actually took, clamped to a factor of
four. The subsidy starts at 50 ROFL and halves every 210 blocks. Coinbase
outputs need 10 confirmations before they can be spent.

The one deliberate departure is the work function. **Mining ROFL means
solving subset-sum puzzles, not grinding hashes.**

Given 40 numbers and a target, find the subset that adds up to it exactly.
Verifying an answer is one loop of additions. Finding one is meet-in-the-middle
at 2²⁰ time *and* memory — and memory is what binds, which is why difficulty
comes from solving *more* puzzles rather than bigger ones. A block at the floor
needs 1; ten-minute spacing lands near 340.

Nobody has built an ASIC for subset-sum. The reference solver in `miner.py` is
deliberately plain, and beating it is the entire sport.

The full rules, the measurements behind every constant, and each place this
knowingly diverges from Bitcoin, are in [SPEC.md](SPEC.md).

## Mine a block

No dependencies. Python 3.9 or newer, standard library only.

```bash
git clone https://github.com/ram0verflow/ram0verflow.git rofl && cd rofl
python3 wallet.py new                                  # make a key pair
python3 miner.py --miner YOUR_GITHUB_HANDLE --message "gm"
```

It solves puzzles until the block is complete, then prints a line starting
with `rofl-block-v1:`. Paste that as a comment on
**[the block issue](../../issues/1)**. A workflow validates it and, if it
holds up, appends it to the chain and updates this page.

About half a minute at the starting difficulty. If the chain gets busy,
difficulty rises and you solve more puzzles — that is the point.

**Your GitHub handle seeds your puzzles.** Two things follow. Nobody can
submit your solved block as their own, because a different handle means
different puzzles and the work would have to be redone. And copying a solution
out of the comment thread gets you nothing, because it answers a question only
you were asked.

## Send coins

```bash
python3 wallet.py balance
python3 wallet.py send --to rofl1... --amount 1.5 --memo "gg"
```

That prints a `rofl-tx-v1:` line. The memo rides inside the signature, so it
cannot be altered or stripped on the way, and it shows up in the ledger above.

Two ways to submit it, and they do the same thing:

- **Comment** on **[the mempool issue](../../issues/2)**. Ten seconds.
- **Pull request** adding one file under `chain/pending/`, if you want the
  contribution on your profile. The node reads the file, applies the
  transaction to `main` and closes the PR — it is never merged, so your
  submission can't conflict with anyone else's.

Either way it waits in the mempool until a miner includes it. Higher fees get
picked first, and the fee goes to whoever mines the block.

## Put your name on your balance

```bash
python3 wallet.py identity --handle YOUR_GITHUB_HANDLE
```

Post the `rofl-id-v1:` line it prints on **[the mempool issue](../../issues/2)**
from the account it names. The signature proves you hold the key; posting it
from your account proves you hold the handle. Your name then appears beside
your balance in the table above.

This is display only. It gives nobody any authority over your coins — those
are spendable by signature and nothing else — and `verify.py` ignores the
registry completely.

## The explorer

A README is one file served identically to everyone — no scripts, no
per-visitor anything. So the personal view lives one click away, at
**[the block explorer](https://ram0verflow.github.io/ram0verflow/)**.

It fetches `chain/blocks.jsonl` and replays the entire chain in your browser:
every hash, every merkle root, every difficulty retarget, every signature,
every subset-sum puzzle re-checked against its target. The consensus rules in
`docs/app.js` are a direct port of the Python, and the two agree bit for bit.

Tell it your GitHub handle once and it remembers — your balance, the blocks
you mined, your transfers, your rank. That is stored in your browser and sent
nowhere. Search takes a block height, a block hash, a txid, a `rofl1…`
address or an `@handle`.

Nothing on that page is served by a backend. There isn't one.

## Verify everything yourself

```bash
python3 verify.py
```

Replays every block from genesis: recomputes each hash, re-derives every
difficulty retarget, rebuilds every merkle root, checks every signature and
every coinbase amount against the subsidy schedule, and asserts that emitted
supply equals unspent supply.

It reads only `chain/blocks.jsonl`. It does not trust this README, the
workflow, or any cached state. If I ever rewrite history, this is what
catches me.

```bash
python3 tests/test_chain.py
```

Builds a chain in memory, spends real coins with real signatures, then tries
to break it nine ways — tampered subsets, forged signatures, inflated
coinbases, double spends, stolen blocks, padded solutions, wrong difficulty,
deleted blocks, stale tips — and asserts every one is rejected. Runs at a
shrunk puzzle size so the whole suite takes seconds.

## Layout

```
rofl/crypto.py       secp256k1, RFC 6979 ECDSA, bech32
rofl/pow.py          subset-sum: instances, solver, verification
rofl/consensus.py    nBits, retargeting, merkle, UTXO set, validation
rofl/chain.py        load, replay, extend
rofl/render.py       this page
docs/                the block explorer — consensus ported to JavaScript
miner.py             the reference solver — beat it
wallet.py            keys, balances, signed transactions
verify.py            independent full-chain verification
submit.py            what the workflow runs
SPEC.md              the consensus rules
```

## Limitations

One writer, so no reorgs. Two miners who solve the same height race on
submission time; the loser is handed the new tip and mines again.

The reference solver is pure Python and wants about 200 MB while it runs.
That is the memory wall meet-in-the-middle hits, and the reason difficulty
scales by puzzle count instead of puzzle size.

Proof of work makes a rewritten history detectable to anyone holding an
earlier copy. It does not make one impossible. This chain lives in a single
repository and is exactly as durable as that. [SPEC.md](SPEC.md) §13 and §16
say the same thing in more detail.

ROFL coins are worth nothing and always will be. `rofl-wallet.json` holds a
private key in plain text — never reuse it anywhere that matters.

## License

MIT.
