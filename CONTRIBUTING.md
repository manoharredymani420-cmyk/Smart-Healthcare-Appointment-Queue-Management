# Contributing to MediCare

Thank you for contributing.

## Development setup

1. Fork or clone the repository.
2. Create a Python virtual environment.
3. Install dependencies.
4. Configure `.env`.
5. Start PostgreSQL.
6. Run migrations.
7. Start the Flask application.
8. Run tests.

## Branch naming

Use:

```text
feature/<name>
fix/<name>
docs/<name>
test/<name>
refactor/<name>
```

## Commit messages

Examples:

```text
feat: add appointment booking API
fix: prevent duplicate appointment slots
test: add queue service tests
docs: update API documentation
```

## Pull Requests

A PR should include:

- Clear description
- Reason for the change
- Tests
- Screenshots for UI changes
- Documentation updates when needed

## Healthcare data rule

Do not submit real patient information, medical records, passwords, tokens, or other private information.

Use synthetic/demo data only.
