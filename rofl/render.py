"""
Render the live ledger into README.md and assets/ledger.svg.

The README between the ROFL:BEGIN and ROFL:END markers is generated; every
other word in it is hand-written and is never touched.
"""

import html
import json
import os

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


def _when(ts: int) -> str:
    """Absolute UTC time — README is static, so relative 'ago' would freeze."""
    from datetime import datetime, timezone

    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


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


def render_readme_section(state: ChainState) -> str:
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
    out.append(
        f'<picture>'
        f'<source media="(prefers-color-scheme: dark)" '
        f'srcset="assets/ledger-dark.svg?v={height}">'
        f'<img src="assets/ledger-light.svg?v={height}" width="100%" '
        f'alt="ROFL ledger, height {height}">'
        f'</picture>'
    )
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
            f"`{len(b.txs)}` | `{reward}` | {_when(b.timestamp)} |"
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

PALETTES = {
    "light": dict(bg="#eef1ec", panel="#e4e8e1", ink="#121916", dim="#68746e",
                  accent="#8a5f10", teal="#1c5b52", divider="#c8cec6",
                  pending_top="#e8c878", pending_left="#c9a84a", pending_right="#a88632",
                  mined_top="#6ec4b0", mined_left="#3d8f7c", mined_right="#2a6b5f"),
    "dark": dict(bg="#0a0e0c", panel="#0f1512", ink="#e6eae4", dim="#8a968f",
                 accent="#d9a64c", teal="#5cab9b", divider="#2c3a33",
                 pending_top="#d9a64c", pending_left="#b8863a", pending_right="#8a6a2a",
                 mined_top="#6ec4b0", mined_left="#3d8f7c", mined_right="#1f4a42"),
}

SVG_HEAD = """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" \
viewBox="0 0 {w} {h}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">
<rect fill="{bg}" width="{w}" height="{h}" rx="8"/>
<rect fill="{panel}" x="12" y="38" width="{iw}" height="{ih}" rx="6"/>
"""


def _iso_cube(out, cx, cy, size, top_c, left_c, right_c, *, stroke=None, dash=None):
    """Isometric cube, bottom edge at cy."""
    s = size
    d = s * 0.34
    h = s * 0.62
    by = cy - h
    top = f"{cx},{by} {cx + s / 2 + d},{by + s * 0.17} {cx},{by + s * 0.34} {cx - s / 2 - d},{by + s * 0.17}"
    right = (
        f"{cx + s / 2 + d},{by + s * 0.17} {cx + s / 2 + d},{by + s * 0.17 + h} "
        f"{cx},{by + s * 0.34 + h} {cx},{by + s * 0.34}"
    )
    left = (
        f"{cx - s / 2 - d},{by + s * 0.17} {cx},{by + s * 0.34} "
        f"{cx},{by + s * 0.34 + h} {cx - s / 2 - d},{by + s * 0.17 + h}"
    )
    sw = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    ds = f' stroke-dasharray="4 3"' if dash else ""
    out.append(f'<polygon points="{left}" fill="{left_c}"{sw}{ds}/>')
    out.append(f'<polygon points="{right}" fill="{right_c}"{sw}{ds}/>')
    out.append(f'<polygon points="{top}" fill="{top_c}"{sw}{ds}/>')


def _svg(state: ChainState, pal: dict, mined_slots: int = 5) -> str:
    """Mempool.space-style block stream for the README ledger tape."""
    blocks = state.blocks[-mined_slots:]
    col_w, pad, div_w = 108, 18, 28
    pending_cols = 1
    cols = pending_cols + mined_slots
    iw = cols * col_w + div_w + 24
    w = iw + pad * 2
    h = 198
    strip_y = 46
    cube_y = 108
    cube_s = 46
    out = [SVG_HEAD.format(w=w, h=h, bg=pal["bg"], panel=pal["panel"], iw=iw, ih=148)]

    out.append(
        f'<text x="{pad}" y="24" fill="{pal["ink"]}" font-size="14" font-weight="700">ROFL</text>'
        f'<text x="{pad + 52}" y="24" fill="{pal["dim"]}" font-size="11.5">'
        f'height {state.height} &#183; difficulty {difficulty(state.tip.bits):,.0f} &#183; '
        f'{state.tip.puzzles()} puzzles / block</text>'
    )

    x0 = pad + 24
    # Pending / next block (left of divider)
    px = x0 + col_w / 2
    out.append(
        f'<text x="{px}" y="{strip_y + 14}" fill="{pal["accent"]}" font-size="13" '
        f'font-weight="600" text-anchor="middle">next</text>'
    )
    _iso_cube(out, px, cube_y, cube_s, pal["pending_top"], pal["pending_left"],
              pal["pending_right"], stroke=pal["divider"], dash=True)
    out.append(
        f'<text x="{px}" y="{cube_y + 18}" fill="{pal["dim"]}" font-size="9" '
        f'text-anchor="middle">~10m target</text>'
    )

    # Divider
    dx = x0 + col_w + 8
    out.append(
        f'<line x1="{dx + div_w / 2}" y1="{strip_y + 8}" x2="{dx + div_w / 2}" y2="{cube_y + 36}" '
        f'stroke="{pal["divider"]}" stroke-width="1.5" stroke-dasharray="5 4"/>'
    )

    # Mined blocks (newest nearest divider)
    for i, b in enumerate(reversed(blocks)):
        cx = dx + div_w + col_w / 2 + i * col_w
        out.append(
            f'<text x="{cx}" y="{strip_y + 14}" fill="{pal["teal"]}" font-size="13" '
            f'font-weight="600" text-anchor="middle">{b.height}</text>'
        )
        _iso_cube(out, cx, cube_y, cube_s, pal["mined_top"], pal["mined_left"], pal["mined_right"])
        reward = format_amount(sum(o.value for o in b.txs[0].outputs))
        out.append(
            f'<text x="{cx}" y="{cube_y + 16}" fill="{pal["ink"]}" font-size="9" '
            f'text-anchor="middle">{reward} ROFL</text>'
            f'<text x="{cx}" y="{cube_y + 28}" fill="{pal["dim"]}" font-size="8.5" '
            f'text-anchor="middle">{len(b.txs)} tx &#183; @{html.escape(b.miner[:12])}</text>'
        )

    out.append("</svg>\n")
    return "".join(out)


def render_svg(state: ChainState, directory: str = "assets", slots: int = 5) -> None:
    """
    Write one tape per theme. GitHub selects between them with <picture>,
    which follows the site theme rather than the reader's operating system.
    """
    os.makedirs(directory, exist_ok=True)
    for name, pal in PALETTES.items():
        with open(os.path.join(directory, f"ledger-{name}.svg"), "w", encoding="utf-8") as fh:
            fh.write(_svg(state, pal, slots))
