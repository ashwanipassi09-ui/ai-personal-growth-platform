# Документация по Git Flow и Conventional Commits

#Ветвление (Branching Strategy)

Мы используем *Git Flow* для управления версиями и параллельной разработки.

# Основные ветки:

| Ветка | Назначение | Пример |
|-------|------------|--------|
| `main` | Production-ready код, релизные версии | `main` |
| `develop` | Интеграционная ветка для разработки | `develop` |
| `feature/*` | Новые функции | `feature/user-auth` |
| `bugfix/*` | Исправление багов | `bugfix/login-error` |
| `hotfix/*` | Срочные исправления production | `hotfix/critical-bug` |

### Правила работы с ветками:
