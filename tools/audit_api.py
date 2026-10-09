"""audit_api.py -- checks every Autoload.<member> usage against the real script.

Cheap static contract check: parses scripts/**/*.gd for `Autoload.member`
references and verifies the member exists as a func/var/const/signal/enum in the
autoload's own file, or is a call on a returned value we cannot resolve (ignored).
"""
from __future__ import annotations
import os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUTOLOADS = {
    "Data": "scripts/core/data_manager.gd",
    "Settings": "scripts/core/settings_manager.gd",
    "Audio": "scripts/core/audio_manager.gd",
    "Notify": "scripts/core/notify_manager.gd",
    "Game": "scripts/core/game_manager.gd",
    "Save": "scripts/core/save_manager.gd",
    "Items": "scripts/core/inventory_manager.gd",
    "Culture": "scripts/core/culture_manager.gd",
    "Quest": "scripts/core/quest_manager.gd",
    "Achievements": "scripts/core/achievement_manager.gd",
    "Dialogue": "scripts/core/dialogue_manager.gd",
    "Puzzle": "scripts/core/puzzle_manager.gd",
    "World": "scripts/core/world_manager.gd",
    "UI": "scripts/ui/ui_manager.gd",
}

DECL = re.compile(r"^(?:@\w+\s+)*\s*(?:static\s+)?(?:func\s+(\w+)|var\s+(\w+)|const\s+(\w+)|"
                  r"signal\s+(\w+)|enum\s+(\w+))", re.M)


def members(path):
    text = open(os.path.join(ROOT, path)).read()
    out = set()
    for m in DECL.finditer(text):
        for g in m.groups():
            if g:
                out.add(g)
    # enums declare their constants in caps: State -> State.ACTIVE
    for em in re.finditer(r"enum\s+(\w+)\s*\{([^}]*)\}", text):
        out.add(em.group(1))
    return out


def main():
    decls = {name: members(path) for name, path in AUTOLOADS.items()}
    problems = collections.defaultdict(list)
    usage = collections.Counter()
    files = []
    for base, _dirs, names in os.walk(os.path.join(ROOT, "scripts")):
        for n in names:
            if n.endswith(".gd"):
                files.append(os.path.join(base, n))
    for path in files:
        text = open(path).read()
        rel = os.path.relpath(path, ROOT)
        for name in AUTOLOADS:
            for m in re.finditer(r"\b%s\.(\w+)" % name, text):
                member = m.group(1)
                usage[(name, member)] += 1
                if member not in decls[name]:
                    problems[(name, member)].append(rel)
    if problems:
        print("UNRESOLVED AUTOLOAD MEMBERS:")
        for (name, member), where in sorted(problems.items()):
            print("  %s.%s   <- %s" % (name, member, ", ".join(sorted(set(where)))))
        return 1
    print("all autoload member references resolve (%d distinct members used)"
          % len(usage))
    return 0


if __name__ == "__main__":
    sys.exit(main())
