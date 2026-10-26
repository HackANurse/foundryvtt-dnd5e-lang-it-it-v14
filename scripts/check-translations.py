#!/usr/bin/env python3
"""Check localization coverage against a specific dnd5e English dictionary."""

import argparse
import json
import re
from collections import Counter
from pathlib import Path


PROTECTED = re.compile(r"\{[^{}]+\}|<[^>]+>|&[A-Za-z0-9#]+;")


def flatten(value, prefix=""):
    for key, item in value.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(item, dict):
            yield from flatten(item, path)
        else:
            yield path, item


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("english", type=Path, help="Official dnd5e lang/en.json")
    parser.add_argument("--italian", type=Path, default=Path("it-IT/it.json"))
    parser.add_argument("--baseline", type=Path, help="Previous Italian JSON; check tokens only in new strings")
    args = parser.parse_args()

    english = dict(flatten(json.loads(args.english.read_text())))
    italian = dict(flatten(json.loads(args.italian.read_text())))
    baseline = dict(flatten(json.loads(args.baseline.read_text()))) if args.baseline else {}

    missing = sorted(english.keys() - italian.keys())
    changed = sorted(english.keys() & italian.keys() - baseline.keys())
    errors = []
    for key in changed:
        source, translated = english[key], italian[key]
        if not isinstance(source, str) or not isinstance(translated, str):
            errors.append((key, "non-string value"))
        elif Counter(PROTECTED.findall(source)) != Counter(PROTECTED.findall(translated)):
            errors.append((key, "placeholder/HTML token mismatch"))

    print(f"English strings: {len(english)}")
    print(f"Missing Italian strings: {len(missing)}")
    scope = "New strings" if args.baseline else "Strings"
    print(f"{scope} with invalid protected tokens: {len(errors)}")
    for key in missing[:20]:
        print(f"MISSING {key}")
    for key, reason in errors[:20]:
        print(f"INVALID {key}: {reason}")
    raise SystemExit(bool(missing or errors))


if __name__ == "__main__":
    main()
