#!/bin/sh
# Recreate the user's working tree in a COPY of this folder: one hunk of
# Greeter.swift staged, a second hunk unstaged, and an unrelated staged README edit.
# Usage: cp -R swift-partial /tmp/work && sh /tmp/work/setup-git-state.sh /tmp/work
set -eu
dir="${1:?usage: setup-git-state.sh <copy-of-fixture>}"
cd "$dir"
[ ! -e .git ] || { echo "refusing: $dir is already a git repository" >&2; exit 1; }
git init -q
git config user.email fixture@example.invalid
git config user.name fixture
git add Package.swift Sources Tests README.md
git commit -qm baseline
f=Sources/Greeter/Greeter.swift
# Hunk 1 (staged): formatting-violating change to greeting().
sed 's/"Hello, \\(name)!"/"Hello,   \\(name)!" /' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
git add "$f"
# Hunk 2 (unstaged): change to farewell().
sed 's/"Goodbye, \\(name)."/"See you, \\(name)."/' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
printf '\nSee CONTRIBUTING for setup.\n' >> README.md
git add README.md
git diff --cached --stat
git diff --stat
