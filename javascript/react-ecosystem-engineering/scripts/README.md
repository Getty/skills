# Offline tooling

All scripts use Python's standard library. Run from any directory with explicit paths. They never install packages, execute project scripts, contact the network, or modify the inspected project.

```sh
python scripts/inventory_project.py /path/to/project
python scripts/library_lookup.py react
python scripts/validate_bundle.py
python -m unittest discover -s tests -p 'test_*.py' -v
```

Inventory is bounded, skips symlinks/generated/dependency directories, and labels its findings as heuristics. It distinguishes manifest ranges from parsed npm-lock versions; other lockfile formats are identified but not parsed. Large lockfiles may exceed the configured bound. Its report contains project metadata and may require redaction.

The validator checks local Markdown targets, reference reachability, basic frontmatter conventions, JSON syntax, and the manifest. It does not fetch external URLs, validate the entire Agent Skills specification, certify security, or run application dependencies. Installing dependencies or changing package content can intentionally invalidate the original manifest. The manifest excludes itself because a file cannot contain its own ordinary cryptographic digest; archive-level SHA-256 is supplied outside the ZIP.
