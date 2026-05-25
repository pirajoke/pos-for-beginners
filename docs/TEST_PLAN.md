# Test Plan

## Local Tests

```bash
python3 -m unittest discover -s tests
```

## Demo Vault Test

```bash
rm -rf /tmp/sisi-demo-vault
python3 scripts/bootstrap_client.py --vault /tmp/sisi-demo-vault --allow-non-obsidian
python3 scripts/check_vault.py --vault /tmp/sisi-demo-vault
```

## Source Discovery Test

```bash
mkdir -p /tmp/sisi-source-sample
printf "Granola transcript" > /tmp/sisi-source-sample/granola-call.txt
python3 scripts/source_discovery.py --vault /tmp/sisi-demo-vault --scan-path /tmp/sisi-source-sample
```

## Manual QA

- Open `START HERE - Sisi Obsidian Setup.md`.
- Confirm the first prompt asks only one question.
- Confirm connector prompt requires approval before external access.
