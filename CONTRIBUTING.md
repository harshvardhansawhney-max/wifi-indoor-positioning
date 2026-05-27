# Contributing Guidelines

## Welcome!

Thank you for interest in contributing to the WiFi Indoor Positioning project. We welcome:

- Bug reports
- Feature requests
- Code contributions
- Documentation improvements
- Research papers/references
- Dataset contributions
- Performance optimizations

## Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/wifi-indoor-positioning.git
cd wifi-indoor-positioning
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

Follow the code style guide below.

### 4. Test Locally

```bash
# Backend tests
cd backend && pytest tests/ -v

# Frontend tests
cd frontend && npm test
```

### 5. Commit & Push

```bash
git add .
git commit -m "Brief description of changes"
git push origin feature/your-feature-name
```

### 6. Create Pull Request

On GitHub, create PR with:
- Clear description
- Related issue number
- Screenshot (if UI change)
- Test results

## Code Style

### Python

```bash
# Format with Black
black backend/

# Lint with Flake8
flake8 backend/

# Type check
mypy backend/
```

**Style Guide**:
- PEP 8 compliant
- Docstrings for all functions
- Type hints where practical
- Max line length: 100 characters

### JavaScript/TypeScript

```bash
# Format
npm run format

# Lint
npm run lint
```

**Style Guide**:
- Prettier formatting
- ESLint rules
- TypeScript strict mode
- Component naming: PascalCase

## Pull Request Process

1. **Description**
   - What problem does it solve?
   - How does it work?
   - Any breaking changes?

2. **Testing**
   - Unit tests included?
   - Integration tests?
   - Manual testing done?

3. **Documentation**
   - README updated?
   - Docstrings added?
   - Comments where needed?

4. **Reviews**
   - Address reviewer comments
   - Re-request review after changes
   - No force pushes after review

## Issue Reporting

### Bug Report Template

```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. ...
2. ...

## Expected Behavior

## Actual Behavior

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11]
- Node.js: [e.g., 18]

## Logs
```
[Paste relevant logs]
```
```

### Feature Request Template

```markdown
## Description
Clear description of desired feature

## Motivation
Why is this needed?

## Proposed Solution
How should it work?

## Alternatives Considered
```

## Development Setup

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .[dev]  # Install dev dependencies
```

### Frontend Development

```bash
cd frontend
npm install
npm start  # Development server with hot reload
```

### Running Tests

```bash
# All tests
make test

# Specific test file
pytest tests/backend/test_signal_processing.py -v

# Coverage
pytest --cov=backend tests/
```

## Project Structure

```
wifi-indoor-positioning/
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── models/           # ML models
├── datasets/         # Training data
├── tests/            # Test suites
├── scripts/          # Utility scripts
├── docs/             # Documentation
└── docker/           # Docker setup
```

## Coding Standards

### Backend (Python)

**Imports**: Group into sections
```python
# Standard library
import os
from pathlib import Path

# Third-party
import numpy as np
from fastapi import FastAPI

# Local
from config import settings
from database.models import User
```

**Functions**: Include docstrings
```python
def process_signals(signals: List[Dict]) -> np.ndarray:
    """Process and extract features from signals.
    
    Args:
        signals: List of signal measurements
        
    Returns:
        Feature array of shape (n_samples, n_features)
        
    Raises:
        ValueError: If signals format is invalid
    """
    pass
```

### Frontend (React/TypeScript)

**Components**:
```typescript
interface ComponentProps {
  title: string;
  onAction?: () => void;
}

const MyComponent: React.FC<ComponentProps> = ({ title, onAction }) => {
  return <div>{title}</div>;
};

export default MyComponent;
```

## Documentation

When adding features:

1. Update relevant README sections
2. Add to API documentation
3. Include usage examples
4. Update architecture diagram if major change
5. Add to changelog

## Performance Guidelines

- Inference latency: < 100ms
- Position update: < 500ms
- API response: < 1s
- Frontend render: < 60fps
- CPU usage: < 15%
- Memory usage: < 500MB

## Security Guidelines

- No hardcoded credentials
- Input validation on all APIs
- SQL injection prevention
- XSS protection in frontend
- HTTPS/TLS in production
- Regular dependency updates

## Release Process

1. Update version in code
2. Update CHANGELOG.md
3. Create release notes
4. Tag release: `git tag v0.2.0`
5. Push tag: `git push origin v0.2.0`
6. Create GitHub release
7. Upload artifacts

## Community

- **Discussions**: GitHub Discussions
- **Issues**: Bug reports and features
- **Pulls**: Code contributions
- **Wiki**: Community documentation

## Code of Conduct

- Be respectful and inclusive
- No harassment or discrimination
- Assume good intent
- Report violations to maintainers

## Questions?

Open an issue or start a discussion on GitHub!

---

**Thank you for contributing!** 🚀
