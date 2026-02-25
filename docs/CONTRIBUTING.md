# Contributing to MechaPulse

Thank you for your interest in contributing to MechaPulse! This document explains how to set up a development environment, submit changes, and follow the project's coding standards.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Branch Naming](#branch-naming)
- [Commit Messages](#commit-messages)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Coding Standards](#coding-standards)
  - [Python](#python)
  - [C++ (Firmware)](#c-firmware)
- [Testing](#testing)
- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)

---

## Code of Conduct

Please be respectful and constructive in all interactions. We welcome contributors of all experience levels.

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:

   ```bash
   git clone https://github.com/<your-username>/MechaPulse.git
   cd MechaPulse
   ```

3. **Add the upstream remote** so you can pull in future changes:

   ```bash
   git remote add upstream https://github.com/AkinduID/MechaPulse.git
   ```

4. Set up the relevant component following [`docs/SETUP_GUIDE.md`](SETUP_GUIDE.md).

---

## Development Workflow

```
main  ←  feature/your-feature  (PR)
      ←  fix/your-fix           (PR)
```

1. Create a new branch from `main`:

   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/your-descriptive-name
   ```

2. Make your changes in small, logical commits (see [Commit Messages](#commit-messages)).

3. Push your branch to your fork:

   ```bash
   git push origin feature/your-descriptive-name
   ```

4. Open a Pull Request against the `main` branch of the upstream repository.

---

## Branch Naming

| Prefix | Usage |
|--------|-------|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `docs/` | Documentation-only changes |
| `refactor/` | Code restructuring without behavior change |
| `test/` | Adding or updating tests |

---

## Commit Messages

Use concise, imperative-mood commit messages:

```
Add FFT feature extraction to firmware
Fix model path resolution on Windows
Update API reference for /predict endpoint
```

- Limit the first line to 72 characters.
- Add a blank line followed by a more detailed description when necessary.

---

## Pull Request Guidelines

- Keep PRs focused — one logical change per PR.
- Fill in the PR description template, including the motivation for the change.
- Reference any related issues with `Closes #<issue-number>` in the PR description.
- Ensure the code builds and tests pass before requesting review.
- Respond to review comments within a reasonable timeframe.

---

## Coding Standards

### Python

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines.
- Use type hints for function signatures where practical.
- Keep functions short and single-purpose.
- Document public functions and classes with docstrings.

```python
def extract_features(signal: np.ndarray, sample_rate: int) -> dict:
    """Extract time- and frequency-domain features from an audio signal.

    Args:
        signal: 1-D NumPy array of audio samples.
        sample_rate: Sample rate in Hz.

    Returns:
        Dictionary with keys RMS, Mean, MA1, MA2, MA3, F1, F2, F3.
    """
    ...
```

### C++ (Firmware)

- Follow the existing indentation style in `src/main.cpp` (2-space indent).
- Prefer `constexpr` / `const` over `#define` for constants.
- Add a comment for each configuration constant.
- Avoid blocking the main loop for extended periods; use `millis()`-based timing where possible.

---

## Testing

### Backend (Python)

Run the FastAPI server locally and exercise endpoints with `curl` or the Swagger UI at `http://localhost:8000/docs`.

Automated tests (if added):

```bash
cd desktop-app
pytest
```

### Firmware

Use the PlatformIO unit test framework:

```bash
cd device-firmware
pio test
```

### Notebooks

Re-run all notebook cells from top to bottom to verify they execute without errors:

```bash
jupyter nbconvert --to notebook --execute notebooks/*.ipynb
```

---

## Reporting Bugs

Open a GitHub Issue with:

1. A clear title describing the problem.
2. Steps to reproduce.
3. Expected vs. actual behavior.
4. Environment details (OS, Python version, hardware).

---

## Requesting Features

Open a GitHub Issue with the `enhancement` label and describe:

1. The use case or problem being solved.
2. A proposed solution or API design.
3. Any alternatives considered.
