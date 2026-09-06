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

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/ledger-dark.svg?v=165"><img src="assets/ledger-light.svg?v=165" width="100%" alt="ROFL ledger, height 165"></picture>

| | |
|---|---|
| **height** | `165` |
| **tip** | `69d131b5a7070c4226526edb8c26f7ff6cec51a4ab1a385503948bd658a215e6` |
| **difficulty** | `56,085.4`  (bits `0x1c12b230`) |
| **chainwork** | `666,961,228,068` expected hashes |
| **supply** | `8300.00000000 ROFL` in `165` unspent outputs |
| **next reward** | `50.00000000 ROFL` |
| **next retarget** | in `10` block(s) |
| **next halving** | in `44` block(s) |
| **transactions** | `167` |

### Recent blocks

| # | hash | miner | message | txs | reward | mined |
|--:|---|---|---|--:|--:|---|
| `165` | `69d131b5a7070c422652…` | [@ksanjeev284](https://github.com/ksanjeev284) | `gm` | `1` | `50.00000000` | 2026-09-06 21:16 UTC |
| `164` | `e53ee2ce1412ae195bb1…` | [@ksanjeev284](https://github.com/ksanjeev284) | `gm` | `1` | `50.00000000` | 2026-09-06 21:15 UTC |
| `163` | `9b1e7a391a73294d8518…` | [@ksanjeev284](https://github.com/ksanjeev284) | `gm` | `1` | `50.00000000` | 2026-09-06 21:15 UTC |
| `162` | `1ec1dcc15711f54dc85d…` | [@ksanjeev284](https://github.com/ksanjeev284) | `gm` | `1` | `50.00000000` | 2026-09-06 21:14 UTC |
| `161` | `0eb38a9613fc20ae2a86…` | [@ksanjeev284](https://github.com/ksanjeev284) | `gm` | `1` | `50.00000000` | 2026-09-06 21:13 UTC |
| `160` | `04cd234c0576e25245c0…` | [@ksanjeev284](https://github.com/ksanjeev284) | `gm` | `1` | `50.00000000` | 2026-09-06 21:13 UTC |
| `159` | `93bdd8a0f68dbec39aed…` | [@ksanjeev284](https://github.com/ksanjeev284) | `gm` | `1` | `50.00000000` | 2026-09-06 21:12 UTC |
| `158` | `f1ac5584fbf162d4ed6f…` | [@ksanjeev284](https://github.com/ksanjeev284) | `gm` | `1` | `50.00000000` | 2026-09-06 21:11 UTC |
| `157` | `9498238b9605f8e33788…` | [@ksanjeev284](https://github.com/ksanjeev284) | `gm` | `1` | `50.00000000` | 2026-09-06 21:11 UTC |
| `156` | `e770a9255054fc4588a1…` | [@ksanjeev284](https://github.com/ksanjeev284) | `gm` | `1` | `50.00000000` | 2026-09-06 21:10 UTC |

### Miners

| miner | blocks | share |
|---|--:|--:|
| [@ksanjeev284](https://github.com/ksanjeev284) | `127` | `76.5%` |
| [@ram0verflow](https://github.com/ram0verflow) | `37` | `22.3%` |
| [@axewhyzed](https://github.com/axewhyzed) | `1` | `0.6%` |
| [@notram0verflow](https://github.com/notram0verflow) | `1` | `0.6%` |

### Balances

_Find your own name here once you have run `python3 wallet.py identity`._

| holder | address | balance |
|---|---|--:|
| _unclaimed_ | `rofl1qn2wv00sq9a875c7pmqf4hfu2ca2y7fa0le96wk` | `6350.00000000 ROFL` |
| _unclaimed_ | `rofl1qhkhmy848s09y2jyly8jexk4gd3gnrrclxj2exx` | `1750.00000000 ROFL` |
| _unclaimed_ | `rofl1q3jwm3gz2s9xy7wa5hg0cgcn9k2s56uma79ynfl` | `150.00000000 ROFL` |
| _unclaimed_ | `rofl1q5yjjcsx8nmxxej5djurawqyxepzhqwcxumhret` | `50.00000000 ROFL` |

### Recent transfers

| block | from | to | amount | note |
|--:|---|---|--:|---|
| `11` | `rofl1qhkhmy848s0…` | `rofl1q3jwm3gz2s9…` | `100.00000000` | gm @notram0verflow |

<sub>Rendered from `chain/blocks.jsonl` at height 165. Verify it yourself: <code>python3 verify.py</code></sub>

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
