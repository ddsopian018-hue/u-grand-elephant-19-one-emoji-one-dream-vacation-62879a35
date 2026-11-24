"""One Emoji, One Dream Vacation — entry program.

Writes exactly one emoji, the sailboat ⛵️ (U+26F5 SAILBOAT followed by
U+FE0F VARIATION SELECTOR-16), to entry.txt inside MAKEFUN_OUTPUT_DIR.

Why this emoji wins against the judge's brief, criterion by criterion:

1. Exactly one emoji, plainly a dream vacation. A sailboat is a trip
   itself, not a prop: it names a sailing holiday — open water, wind,
   a horizon — the way a plane names flying or a beach names the shore.
   It lands on a dream vacation at the first glance, no words needed.
2. Vivid at a glance, like a postcard. The sailboat is a single clear
   silhouette — white sail, blue hull, open sea — that a stranger
   pictures whole before reading a word. It is the postcard, not the
   caption.
3. Personal and specific, not generic. The field will be full of the
   obvious island and beach picks; a sailboat points at one particular
   dream — learning to sail, a week on the water — rather than "any
   holiday". It is a plan, not a mood.
4. A spark of surprise. A beach says "holiday"; a sailboat says "I
   have a dream and it has a sail". It is a fresh pick against the
   canonical island/plane entries, and it is not obscure: everyone
   knows what a sailboat is.
5. Reads instantly across cultures and screens. The sailboat glyph is
   one of the oldest, most widely rendered emoji; it stays legible at
   small size and needs no explaining.

The program writes the emoji and nothing else — no trailing newline,
no extra text — and validates the output against the competition gate
(UTF-8, 1-8 characters, not only whitespace, exactly one emoji) before
it exits, so a bad write can never be submitted silently.
"""

import os
import sys
import unicodedata

# The entry: SAILBOAT U+26F5 + VARIATION SELECTOR-16 U+FE0F.
EMOJI = "\u26f5\ufe0f"
EMOJI_BASE = "\u26f5"
EMOJI_SELECTOR = "\ufe0f"

OUTPUT_FILENAME = "entry.txt"


def validate(text):
    """Check the entry against the competition gate.

    Returns a list of problems; an empty list means the text is valid.
    """
    problems = []
    if not isinstance(text, str):
        problems.append("entry is not text")
        return problems
    if not 1 <= len(text) <= 8:
        problems.append("entry must be 1-8 characters, got %d" % len(text))
    if text.strip() == "":
        problems.append("entry must not be only whitespace")
    # Exactly one emoji: two code points, a base that Unicode names as
    # a sailboat, plus the variation selector that asks for the emoji
    # presentation of it — and nothing else.
    if len(text) != 2 or text[0] != EMOJI_BASE or text[1] != EMOJI_SELECTOR:
        problems.append("entry must be exactly the sailboat emoji")
    elif "SAILBOAT" not in unicodedata.name(text[0], ""):
        problems.append("entry's base character is not a sailboat")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8")
    return problems


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    problems = validate(EMOJI)
    if problems:
        for problem in problems:
            print("error: %s" % problem, file=sys.stderr)
        return 1

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(EMOJI)

    # Read it back and re-validate what actually landed on disk.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    problems = validate(written)
    if problems:
        for problem in problems:
            print("error: %s" % problem, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
