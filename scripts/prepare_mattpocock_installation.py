#!/usr/bin/env python3
"""
Prepare Matt Pocock skills for installation into Antigravity/Gemini skills & plugins directories.
"""

import json
import shutil
from pathlib import Path

SOURCE_REPO = Path("/Users/k.sathvik/.gemini/antigravity/scratch/mattpocock-skills")
STAGING_DIR = Path("/Users/k.sathvik/.gemini/antigravity/scratch/mattpocock-staged")

if STAGING_DIR.exists():
    shutil.rmtree(STAGING_DIR)

plugin_dir = STAGING_DIR / "plugins" / "mattpocock-skills"
plugin_skills_dir = plugin_dir / "skills"
plugin_skills_dir.mkdir(parents=True, exist_ok=True)

skills_flat_dir = STAGING_DIR / "skills"
skills_flat_dir.mkdir(parents=True, exist_ok=True)

# Find all SKILL.md
skill_files = list((SOURCE_REPO / "skills").glob("**/*/SKILL.md"))

manifest_skills = []

for sf in skill_files:
    source_skill_folder = sf.parent
    skill_name = source_skill_folder.name
    category = source_skill_folder.parent.name

    # Target in plugin
    target_plugin_skill = plugin_skills_dir / skill_name
    shutil.copytree(source_skill_folder, target_plugin_skill)
    manifest_skills.append(f"./skills/{skill_name}")

    # Target in flat skills
    flat_name = skill_name
    if skill_name == "prototype":
        flat_name = "matt-pocock-prototype"
        # Update SKILL.md name in flat version if needed
        target_flat_skill = skills_flat_dir / flat_name
        shutil.copytree(source_skill_folder, target_flat_skill)
        skill_md = target_flat_skill / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        content = content.replace("name: prototype", "name: matt-pocock-prototype", 1)
        skill_md.write_text(content, encoding="utf-8")
    else:
        target_flat_skill = skills_flat_dir / flat_name
        shutil.copytree(source_skill_folder, target_flat_skill)

# Create plugin.json
plugin_meta = {
    "name": "mattpocock-skills",
    "version": "1.3.1",
    "description": "Matt Pocock's agent skills for real engineering: grilling, spec/ticket flows, TDD, code review, domain modelling and more.",
    "author": {"name": "Matt Pocock", "url": "https://www.aihero.dev"},
    "homepage": "https://www.aihero.dev/s/skills-newsletter",
    "repository": "https://github.com/mattpocock/skills",
    "license": "MIT",
    "skills": manifest_skills,
}

(plugin_dir / "plugin.json").write_text(json.dumps(plugin_meta, indent=2), encoding="utf-8")

# Copy root documentation
for doc in ["README.md", "LICENSE", "CLAUDE.md", "CHANGELOG.md"]:
    src_file = SOURCE_REPO / doc
    if src_file.exists():
        shutil.copy2(src_file, plugin_dir / doc)

print(f"Staged {len(manifest_skills)} skills into {STAGING_DIR}")
