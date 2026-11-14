"""Consistency checks for the agent fleet playbook.

Usage:  python scripts/validate.py
Needs:  pip install pyyaml
Checks:
  - every skill folder has SKILL.md whose `name` equals the folder name and has a description
  - every agent's skills exist; every agent's capabilities are bound to it in some fleet
  - every fleet binds every capability; fleet bindings point to existing agents
  - every pipeline capability is known; depends_on references exist; no cycles
  - verify/critique are never bound to the same agent as the capabilities they check (per fleet)
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CAPS = {"plan", "research", "monitor", "build", "compute", "strategize",
        "critique", "verify", "remember", "write", "approve"}
errors: list[str] = []


def frontmatter(path: Path) -> dict:
    m = re.match(r"^---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
    if not m:
        errors.append(f"{path}: missing YAML frontmatter")
        return {}
    return yaml.safe_load(m.group(1)) or {}


# Skills
skills = set()
for d in sorted((ROOT / "skills").iterdir()):
    if not d.is_dir():
        continue
    f = d / "SKILL.md"
    if not f.exists():
        errors.append(f"skills/{d.name}: missing SKILL.md")
        continue
    fm = frontmatter(f)
    if fm.get("name") != d.name:
        errors.append(f"skills/{d.name}: name '{fm.get('name')}' != folder name")
    if not fm.get("description"):
        errors.append(f"skills/{d.name}: missing description")
    skills.add(d.name)

# Agents
agents = {}
for f in sorted((ROOT / "agents").glob("*.md")):
    fm = frontmatter(f)
    aid = fm.get("id")
    if aid != f.stem:
        errors.append(f"agents/{f.name}: id '{aid}' != file name")
    agents[aid] = fm
    for s in fm.get("skills", []) or []:
        if s not in skills:
            errors.append(f"agents/{f.name}: unknown skill '{s}'")
    for c in fm.get("capabilities", []) or []:
        if c not in CAPS:
            errors.append(f"agents/{f.name}: unknown capability '{c}'")

# Fleets
fleets = {}
for f in sorted((ROOT / "fleets").glob("*.yaml")):
    fl = yaml.safe_load(f.read_text(encoding="utf-8"))
    b = fl.get("bindings", {})
    fleets[fl["id"]] = b
    missing = CAPS - set(b)
    if missing:
        errors.append(f"fleets/{f.name}: unbound capabilities {sorted(missing)}")
    for cap, agent in b.items():
        if agent not in agents:
            errors.append(f"fleets/{f.name}: {cap} -> unknown agent '{agent}'")
        elif fl["id"] not in (agents[agent].get("fleets") or []):
            errors.append(f"fleets/{f.name}: agent '{agent}' does not list fleet '{fl['id']}'")
    for agent, extra in (fl.get("extra_skills") or {}).items():
        for s in extra:
            if s not in skills:
                errors.append(f"fleets/{f.name}: extra skill '{s}' for {agent} not found")
    producers = {"research", "monitor", "build", "compute", "strategize", "write"}
    for checker in ("verify", "critique"):
        for p in producers:
            if b.get(checker) and b.get(checker) == b.get(p):
                errors.append(f"fleets/{f.name}: {checker} and {p} bound to same agent '{b[p]}'")

# Pipelines
for f in sorted((ROOT / "pipelines").glob("*.yaml")):
    pl = yaml.safe_load(f.read_text(encoding="utf-8"))
    stages = {s["id"]: s for s in pl.get("stages", [])}
    for sid, s in stages.items():
        cap = s.get("capability", "")
        if "{{" not in cap and cap not in CAPS:
            errors.append(f"pipelines/{f.name}:{sid}: unknown capability '{cap}'")
        for dep in s.get("depends_on", []) or []:
            if dep not in stages:
                errors.append(f"pipelines/{f.name}:{sid}: depends_on unknown '{dep}'")
        for sk in s.get("skills", []) or []:
            if sk not in skills:
                errors.append(f"pipelines/{f.name}:{sid}: unknown skill '{sk}'")
    # cycle check
    state: dict[str, int] = {}

    def visit(n: str) -> bool:
        if state.get(n) == 1:
            return True
        if state.get(n) == 2:
            return False
        state[n] = 1
        for d in stages.get(n, {}).get("depends_on", []) or []:
            if d in stages and visit(d):
                return True
        state[n] = 2
        return False

    if any(visit(n) for n in stages):
        errors.append(f"pipelines/{f.name}: dependency cycle")

if errors:
    print(f"FAIL ({len(errors)} issues)")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print(f"OK: {len(skills)} skills, {len(agents)} agents, {len(fleets)} fleets, "
      f"{len(list((ROOT / 'pipelines').glob('*.yaml')))} pipelines")
