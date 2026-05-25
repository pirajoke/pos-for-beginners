# GitHub Handoff

## Ссылка для клиента

```
https://github.com/pirajoke/pos-for-beginners
```

## Сообщение клиенту (скопировать)

```
Привет! Вот твоя персональная операционная система.

https://github.com/pirajoke/pos-for-beginners

Открой терминал и вставь 3 строки:

git clone https://github.com/pirajoke/pos-for-beginners.git
cd pos-for-beginners
python3 scripts/setup_pos.py --vault ~/ObsidianVault

Wizard проведёт тебя через 8 шагов — по одному за раз.
Можно остановиться и продолжить потом. Прогресс сохраняется.

Если что-то непонятно — пиши.
```

## Если repo private

Сначала дай доступ:

```bash
gh repo edit pirajoke/pos-for-beginners --visibility public
```

Или добавь клиента как collaborator:

```bash
gh repo add-collaborator pirajoke/pos-for-beginners CLIENT_GITHUB_USERNAME
```

## Требования у клиента

- macOS / Linux (Windows: WSL)
- Python 3
- Git
- Obsidian
