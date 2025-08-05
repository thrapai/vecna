# Contributing to Vecna

Thank you for considering contributing to this project! We welcome contributions of all kinds, including bug reports, feature requests, code, and documentation improvements.

## Table of Contents
- [Getting Started](#getting-started)
- [Contribution Guidelines](#contribution-guidelines)
- [Submitting Changes](#submitting-changes)

## Getting Started

1. **Fork the repository** and clone it locally:
    ```bash
    git clone https://github.com/your-username/vecna.git
    cd vecna
    ```

2. **Setup** the development environment:
    - Ensure you have Python 3.10 or later installed.
    - Create a virtual environment:
      ```bash
      python -m venv venv
      source venv/bin/activate
      ```
    - Install the development dependencies:
      ```bash
      pip install -e .[dev]
      ```

3. **Run tests** to ensure everything is working:
    ```bash
    ./run_tests.sh
    ```

## Contribution Guidelines

- Keep your changes focused. One feature or fix per pull request.
- Write clear commit messages.
- Follow existing code style.
- Add tests if applicable.
- Update documentation if you add or change functionality.

## Submitting Changes
1. **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/my-feature
    ```
2. **Make your changes** and commit them with a clear message:
    ```bash
    git commit -m "Add feature X"
    ```
3. **Ensure your code passes all tests**:
    ```bash
    ./run_tests.sh
    ```
4. **Push your changes** to your fork:
    ```bash
    git push origin feature/my-feature
    ```
5. **Create a pull request**:
    - Go to the original repository on GitHub.
    - Click on "Pull Requests" and then "New Pull Request".
    - Select your branch and provide a clear description of your changes.
