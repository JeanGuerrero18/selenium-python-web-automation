# Agent instructions

## Language

- Comments are written in **neutral Spanish** (no voseo): `#` comments, module/class/function docstrings, and
  comments in `config.ini`, `pyproject.toml`, `.gitignore` and GitHub workflows.
  This overrides the global "comments in English" rule for this project.
- Test function docstrings are also in Spanish. `conftest.py` copies them into the Description column of the
  pytest-html report, and they must match the Java project's `@Test(description = ...)` strings case by case.
- Identifiers, log messages, `step(...)` texts, assertion messages and commit messages stay in English.
- Keep technical terms that are normally used untranslated (driver, page object, frame, badge, timeout, CI).
- Comments must still fit ruff's `line-length = 110`.
