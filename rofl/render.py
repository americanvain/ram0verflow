"""
Render the live ledger into README.md and assets/ledger.svg.

The README between the ROFL:BEGIN and ROFL:END markers is generated; every
other word in it is hand-written and is never touched.
"""

import html
import json
import os
import time

from .chain import ChainState, emitted_supply
from .consensus import (
    COINBASE_MATURITY,
    HALVING_INTERVAL,
    RETARGET_INTERVAL,
    TARGET_SPACING,
    block_subsidy,
    difficulty,
    format_amount,
)

REGISTRY = os.path.join("chain", "registry.json")

BEGIN = "<!-- ROFL:BEGIN -->"
END = "<!-- ROFL:END -->"
RECENT = 10


def _ago(ts: int, now: int) -> str:
    d = max(0, now - ts)
    if d < 90:
        return f"{d}s ago"
    if d < 5400:
        return f"{d // 60}m ago"
    if d < 172800:
        return f"{d // 3600}h ago"
    return f"{d // 86400}d ago"


def load_registry():
    """Handle -> address bindings. Display only; not consensus."""
    if not os.path.exists(REGISTRY):
        return {}
    try:
        with open(REGISTRY, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def _who(address: str, by_address) -> str:
    """Render an address as a GitHub handle when one has claimed it."""
    handle = by_address.get(address)
    if handle:
        return f"[@{handle}](https://github.com/{handle})"
    return f"`{address[:16]}…`"


def render_readme_section(state: ChainState, now: int | None = None) -> str:
    now = now or int(time.time())
    registry = load_registry()
    by_address = {v["address"]: h for h, v in registry.items()}
    tip = state.tip
    height = state.height
    emitted = emitted_supply(height)
    next_h = height + 1

    halving_in = HALVING_INTERVAL - (next_h % HALVING_INTERVAL)
    retarget_in = RETARGET_INTERVAL - (next_h % RETARGET_INTERVAL)

    out = []
    out.append(BEGIN)
    out.append("")
    out.append(f'<img src="assets/ledger.svg?v={height}" alt="ROFL chain, height '
               f'{height}" width="100%">')
    out.append("")
    out.append("| | |")
    out.append("|---|---|")
    out.append(f"| **height** | `{height}` |")
    out.append(f"| **tip** | `{state.tip_hash}` |")
    out.append(f"| **difficulty** | `{difficulty(tip.bits):,.1f}`  (bits `{tip.bits:#010x}`) |")
    out.append(f"| **chainwork** | `{state.chainwork:,}` expected hashes |")
    out.append(f"| **supply** | `{format_amount(emitted)} ROFL` in "
               f"`{len(state.utxos.utxos)}` unspent outputs |")
    out.append(f"| **next reward** | `{format_amount(block_subsidy(next_h))} ROFL` |")
    out.append(f"| **next retarget** | in `{retarget_in}` block(s) |")
    out.append(f"| **next halving** | in `{halving_in}` block(s) |")
    out.append(f"| **transactions** | `{state.tx_count}` |")
    out.append("")

    out.append("### Recent blocks")
    out.append("")
    out.append("| # | hash | miner | message | txs | reward | mined |")
    out.append("|--:|---|---|---|--:|--:|---|")
    for b in reversed(state.blocks[-RECENT:]):
        msg = html.escape(b.txs[0].coinbase or "")
        msg = f"`{msg}`" if msg else "&nbsp;"
        reward = format_amount(sum(o.value for o in b.txs[0].outputs))
        out.append(
            f"| `{b.height}` | `{b.block_hash()[:20]}…` | "
            f"[@{b.miner}](https://github.com/{b.miner}) | {msg} | "
            f"`{len(b.txs)}` | `{reward}` | {_ago(b.timestamp, now)} |"
        )
    out.append("")

    if state.miners:
        out.append("### Miners")
        out.append("")
        out.append("| miner | blocks | share |")
        out.append("|---|--:|--:|")
        total = sum(state.miners.values())
        for handle, count in sorted(state.miners.items(), key=lambda p: (-p[1], p[0]))[:12]:
            out.append(
                f"| [@{handle}](https://github.com/{handle}) | `{count}` | "
                f"`{100 * count / total:.1f}%` |"
            )
        out.append("")

    balances = state.utxos.balances()
    if balances:
        out.append("### Balances")
        out.append("")
        out.append("_Find your own name here once you have run "
                   "`python3 wallet.py identity`._")
        out.append("")
        out.append("| holder | address | balance |")
        out.append("|---|---|--:|")
        for addr, val in sorted(balances.items(), key=lambda p: -p[1]):
            handle = by_address.get(addr)
            who = f"[@{handle}](https://github.com/{handle})" if handle else "_unclaimed_"
            out.append(f"| {who} | `{addr}` | `{format_amount(val)} ROFL` |")
        out.append("")

    transfers = []
    for b in reversed(state.blocks):
        for t in b.txs[1:]:
            transfers.append((b, t))
        if len(transfers) >= 8:
            break
    if transfers:
        out.append("### Recent transfers")
        out.append("")
        out.append("| block | from | to | amount | note |")
        out.append("|--:|---|---|--:|---|")
        for b, t in transfers[:8]:
            src = "&nbsp;"
            first = t.inputs[0] if t.inputs else None
            if first:
                try:
                    import binascii

                    from .crypto import pubkey_to_address

                    src = _who(pubkey_to_address(bytes.fromhex(first.pubkey)), by_address)
                except (ValueError, binascii.Error):
                    src = "&nbsp;"
            dest = t.outputs[0]
            memo = html.escape(t.memo) if t.memo else "&nbsp;"
            out.append(
                f"| `{b.height}` | {src} | {_who(dest.address, by_address)} | "
                f"`{format_amount(dest.value)}` | {memo} |"
            )
        out.append("")

    out.append(f"<sub>Rendered from `chain/blocks.jsonl` at height {height}. "
               f"Verify it yourself: <code>python3 verify.py</code></sub>")
    out.append("")
    out.append(END)
    return "\n".join(out)


def update_readme(state: ChainState, path: str = "README.md") -> None:
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    if BEGIN not in content or END not in content:
        raise RuntimeError(f"{path} is missing the ROFL:BEGIN/ROFL:END markers")
    head = content.split(BEGIN)[0]
    tail = content.split(END, 1)[1]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(head + render_readme_section(state) + tail)


# --------------------------------------------------------------------------
# SVG ledger tape
# --------------------------------------------------------------------------

SVG_HEAD = """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" \
viewBox="0 0 {w} {h}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">
<style>
  .bg{{fill:#f1f3ef}} .card{{fill:#ffffff;stroke:#d5dbd2}} .ink{{fill:#121916}}
  .dim{{fill:#68746e}} .accent{{fill:#8a5f10}} .teal{{fill:#1c5b52}}
  .link{{stroke:#b3bcb4}}
  @media (prefers-color-scheme:dark){{
    .bg{{fill:#0c1210}} .card{{fill:#131b17;stroke:#28332e}} .ink{{fill:#e5e9e3}}
    .dim{{fill:#7a867f}} .accent{{fill:#d9a64c}} .teal{{fill:#5cab9b}}
    .link{{stroke:#38443e}}
  }}
</style>
<rect class="bg" width="{w}" height="{h}" rx="6"/>
"""


def render_svg(state: ChainState, path: str = "assets/ledger.svg", count: int = 6) -> None:
    """A small chain-of-blocks tape. Self-contained, theme-aware, no fonts loaded."""
    blocks = state.blocks[-count:]
    bw, gap, pad = 148, 26, 18
    w = pad * 2 + len(blocks) * bw + (len(blocks) - 1) * gap
    h = 132
    parts = [SVG_HEAD.format(w=w, h=h)]

    parts.append(
        f'<text x="{pad}" y="24" class="ink" font-size="13" font-weight="700">ROFL</text>'
        f'<text x="{pad + 46}" y="24" class="dim" font-size="11">'
        f'height {state.height} &#183; difficulty {difficulty(state.tip.bits):,.0f}</text>'
    )

    for idx, b in enumerate(blocks):
        x = pad + idx * (bw + gap)
        y = 40
        if idx:
            lx = x - gap
            parts.append(
                f'<line x1="{lx}" y1="{y + 32}" x2="{x}" y2="{y + 32}" '
                f'class="link" stroke-width="1.5" stroke-dasharray="3 3"/>'
            )
        parts.append(f'<rect class="card" x="{x}" y="{y}" width="{bw}" height="{h - y - 14}" '
                     f'rx="4" stroke-width="1"/>')
        parts.append(f'<text x="{x + 10}" y="{y + 20}" class="accent" font-size="12" '
                     f'font-weight="700">#{b.height}</text>')
        parts.append(f'<text x="{x + 10}" y="{y + 38}" class="ink" font-size="9.5">'
                     f'{b.block_hash()[:18]}&#8230;</text>')
        parts.append(f'<text x="{x + 10}" y="{y + 54}" class="teal" font-size="10">'
                     f'@{html.escape(b.miner[:15])}</text>')
        msg = html.escape((b.txs[0].coinbase or "")[:18])
        parts.append(f'<text x="{x + 10}" y="{y + 70}" class="dim" font-size="9">{msg}</text>')
        ntx = len(b.txs)
        parts.append(f'<text x="{x + 10}" y="{y + 84}" class="dim" font-size="9">'
                     f'{ntx} tx &#183; {b.puzzles()} puzzles</text>')

    parts.append("</svg>\n")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("".join(parts))
