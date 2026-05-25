# GitHub Handoff

## What To Send The Client

Copy this message:

```
Привет! Вот твоя персональная операционная система.

Открой терминал и вставь одну строку:

bash <(curl -fsSL https://raw.githubusercontent.com/pirajoke/pos-for-beginners/main/install.sh)

Скрипт:
1. Проверит что git и python3 установлены
2. Скачает проект
3. Найдёт твой Obsidian vault (или спросит путь)
4. Запустит wizard — 8 шагов, по одному за раз

Можно остановиться на любом шаге и продолжить потом.
Прогресс сохраняется автоматически.

Если что-то непонятно — пиши, разберёмся.
```

## Alternative For Non-Technical Clients

If the client cannot use Terminal:

1. Download the repo as ZIP from GitHub
2. Extract to Desktop
3. Double-click `install.command` (macOS only)
4. Drag Obsidian vault folder into Terminal window

## Requirements

- macOS / Linux (Windows: use WSL)
- Python 3.8+
- Git
- Obsidian (installed, vault created)

## Do Not Include

- Raw client source files
- Secrets or API tokens
- Exported mail, Notion data, Granola/Crisp transcripts
