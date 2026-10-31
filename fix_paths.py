#!/usr/bin/env python3

from pathlib import Path
import re

docs = Path("docs")
pattern = re.compile(r"(?<=\]\()((?:\.\./)+)media/")

total = 0

for file in docs.rglob("*.md"):
    original = file.read_text()

    updated, count = pattern.subn(
        lambda m: m.group(1)[3:] + "media/",
        original,
    )

    if count:
        file.write_text(updated)
        print(f"{file}: {count} references updated")
        total += count

print(f"\nTotal: {total} media references updated")

#  vim: ft=python ts=4 sts=4 sw=4 et
