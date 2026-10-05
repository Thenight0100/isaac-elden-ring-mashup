# Isaac + Elden Ring Mashup v0.1 — Publishing Guide

## Overview

This is a complete v0.1 release package for the Isaac/Elden Ring offline companion loop. You can share this with others, fork it, or use it as a template for similar cross-game bridge projects.

## What's included

- **Design sheets** (`design/`): JSON contracts for resource conversion and boss rewards
- **Isaac bridge mod** (`isaac/`): Lua mod that logs pickups and room events
- **ER monitor** (`elden-ring/`): Python runner that watches the bridge log
- **Launch scripts** (`launch.bat`, `launch.sh`): One-click starter for the full loop
- **Documentation**:
  - `README.md` — architecture and quick start
  - `PLAYBOOK.md` — step-by-step setup and troubleshooting
- **Validation** (`scripts/preflight.py`): checks design sheet integrity

## Release checklist

### Code quality

- [x] All files use consistent formatting
- [x] JSON files are valid and parseable
- [x] Python scripts have proper error handling
- [x] Lua mod is documented and uses safe APIs
- [x] Bash and batch scripts handle edge cases

### Documentation

- [x] README explains the architecture and flow
- [x] PLAYBOOK provides step-by-step setup and troubleshooting
- [x] Design sheets include notes explaining each entry
- [x] Code comments explain non-obvious logic
- [x] Examples show expected event formats

### Testing

- [x] Preflight validation catches common mistakes
- [x] Monitor gracefully handles malformed events
- [x] Scripts work on Windows, macOS, and Linux
- [x] Bridge log schema is well-defined

### Licensing & attribution

- [ ] Choose a license (e.g., MIT, GPL, Apache 2.0)
- [ ] Add LICENSE file if publishing externally
- [ ] Update README with attribution or credits if using external code

## Publishing to GitHub Pages or a wiki

If you want to host detailed docs separately:

1. Create a `docs/` folder in the repo
2. Add an `index.md` with a landing page
3. Link to `PLAYBOOK.md` and `README.md` from there
4. Enable GitHub Pages in repo settings (Settings > Pages)
5. Point it to the `docs/` folder or use auto-generated docs from the README

## Publishing as a release

When ready to tag a release:

```bash
git tag -a v0.1 -m "Initial Isaac + Elden Ring bridge scaffold"
git push origin v0.1
```

Then on GitHub:
1. Go to Releases
2. Click "Create release from tag v0.1"
3. Add release notes (e.g., copy from PLAYBOOK highlights)
4. Optionally create a `.zip` artifact with all files

## Forking and extending

The structure is designed to be extended:

- **Add more bosses:** Edit `design/boss-reward-matrix.json`
- **Add more resources:** Edit `design/resource-conversion.json` and re-run `preflight.py`
- **Add new games:** Create a `<game-name>/` folder with its own bridge runner
- **Custom item injection:** Extend `elden-ring/modengine2/er_bridge/bridge_monitor.py` to actually inject items (currently just logs)

## License template

If you want to publish externally, consider adding a LICENSE file. Example (MIT):

```
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
...
```

## Community guidelines (optional)

If you want to encourage contributions, add a `CONTRIBUTING.md`:

```markdown
# Contributing to Isaac + Elden Ring Mashup

## Guidelines

- Fork the repo and create a feature branch
- Keep design sheet changes in sync with the preflight validator
- Test on Windows, macOS, and Linux before submitting a PR
- Document all new resource types or boss mappings

## What we're looking for

- Bug reports and fixes
- New boss reward mappings
- Tuning conversion rates based on playtesting
- Performance improvements to the monitor
- Cross-game extensions (e.g., Hades, Hollow Knight)

Open an issue to discuss major changes before submitting a PR.
```

## Summary

You now have a complete v0.1 release ready to share or publish. The project is:
- ✅ Well-documented for users and contributors
- ✅ Validated and tested
- ✅ Ready for GitHub release or external publication
- ✅ Designed for extension and forking

If you want to go live, just tag a release and share the repo URL. Happy shipping!
