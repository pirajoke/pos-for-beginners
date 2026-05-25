# Test Plan

## Local Tests

```bash
python3 -m unittest discover -s tests
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
