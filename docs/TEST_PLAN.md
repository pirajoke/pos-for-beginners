# Test Plan

## Local Tests

```bash
python3 -m unittest discover -s tests
```

## Skills Pack Test

This test requires network access because it clones public GitHub repos.

```bash
rm -rf /tmp/pos-skill-vault
python3 scripts/bootstrap_client.py --vault /tmp/pos-skill-vault --allow-non-obsidian
python3 scripts/install_skills.py --vault /tmp/pos-skill-vault
python3 scripts/check_vault.py --vault /tmp/pos-skill-vault
```

Expected folders:

```text
/tmp/pos-skill-vault/30-Resources/claude-skills/
/tmp/pos-skill-vault/30-Resources/superpowers/
/tmp/pos-skill-vault/30-Resources/ris-claude-code/
```

## Demo Vault Test

```bash
rm -rf /tmp/pos-demo-vault
python3 scripts/bootstrap_client.py --vault /tmp/pos-demo-vault --allow-non-obsidian
python3 scripts/check_vault.py --vault /tmp/pos-demo-vault
```

## Source Discovery Test

```bash
mkdir -p /tmp/pos-source-sample
printf "Granola transcript" > /tmp/pos-source-sample/granola-call.txt
python3 scripts/source_discovery.py --vault /tmp/pos-demo-vault --scan-path /tmp/pos-source-sample
```

## Manual QA

- Open `START HERE - POS FOR BEGINNERS Setup.md`.
- Confirm the first prompt asks only one question.
- Confirm connector prompt requires approval before external access.
