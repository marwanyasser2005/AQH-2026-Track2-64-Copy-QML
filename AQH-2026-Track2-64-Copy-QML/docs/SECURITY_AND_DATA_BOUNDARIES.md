# Security and data boundaries

This repository is intended to be safe for public GitHub publication.

Excluded by policy:

- organizer `hidden_test.npz`
- organizer `answer_key.csv`
- organizer commitment passwords / secrets
- hidden labels or per-state hidden predictions
- private organizer evaluation directories

The notebooks may contain **disabled code paths or textual references** to hidden evaluation because they document the experimental firewall. They do not bundle the hidden files themselves.

Before every push, run `python scripts/validate_repo.py`.
