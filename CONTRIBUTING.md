# Contributing to quant-portfolio

Thank you for your interest in contributing to this quantitative trading portfolio project!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/quant-portfolio.git`
3. Set up your development environment (see README.md)
4. Create a new branch for your feature

## Development Workflow

### Branch Strategy

We follow a feature-branch workflow:

- **`main`**: Production-ready code
- **`dev`**: Development branch for integration
- **`track-a`**: Custom event engine implementation
- **`track-b`**: NautilusTrader integration (current focus)
- **`feature/*`**: Feature branches (e.g., `feature/new-strategy`)
- **`fix/*`**: Bug fix branches (e.g., `fix/data-loader`)

### Creating a Branch

```bash
# For new features
git checkout -b feature/your-feature-name

# For bug fixes
git checkout -b fix/issue-description
```

### Making Changes

1. Write clean, documented code
2. Follow PEP 8 style guidelines
3. Add tests for new functionality
4. Update documentation as needed
5. Commit with clear, descriptive messages

### Commit Messages

Follow conventional commit format:

```
<type>: <description>

[optional body]
[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
- `feat: Add momentum strategy implementation`
- `fix: Correct data alignment in backtest engine`
- `docs: Update README with installation steps`

## Code Quality

### Testing

Run tests before submitting:

```bash
pytest tests/
```

### Linting

Ensure code passes linting:

```bash
flake8 .
black --check .
```

## Submitting Changes

1. Push your branch to your fork
2. Open a Pull Request against the appropriate target branch
3. Describe your changes clearly
4. Link any related issues
5. Wait for code review and address feedback

## Code Review Process

- At least one approval required
- All CI checks must pass
- Maintainers will review within 48 hours
- Address feedback promptly

## Questions?

Feel free to open an issue for discussion or reach out to maintainers.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
