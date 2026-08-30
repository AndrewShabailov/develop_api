# develop_api

![UI Tests](https://github.com/AndrewShabailov/develop_api/actions/workflows/ui-tests.yml/badge.svg)

Daily updated repository to improve framework structure from basic to senior.

## Стек

- pytest + requests + pydantic — API-слой
- Playwright — UI-слой
- SQLAlchemy — проверки в БД
- GitHub Actions — CI

## Запуск локально

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
pytest src/main/ui/tests -v
```