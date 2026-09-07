# Contributing to Distributed Content Management

Thank you for your interest in contributing! We welcome contributions to market signal collectors, monetization adapters, decision algorithms, and pipeline stages.

## Code of Conduct
Please ensure all discussions, code reviews, and interactions remain constructive, respectful, and focused on technical excellence.

## How to Contribute

1. **Fork & Clone**
   ```bash
   git clone https://github.com/<your-username>/distributed-content-management.git
   cd distributed-content-management
   ```

2. **Branching Strategy**
   Create a descriptive feature or fix branch from `main`:
   ```bash
   git checkout -b feature/dynamic-serp-adapter
   ```

3. **Development Guidelines**
   - Maintain pure Python 3.10+ standard library compatibility where possible, minimizing heavy external dependencies.
   - Use strict type annotations (`typing`, `dataclasses`, `enum`).
   - Every new feature or decision rule must include unit tests in `tests/`.

4. **Running Tests**
   Before submitting, ensure all tests pass:
   ```bash
   python -m unittest discover tests
   python examples/run_portfolio_simulation.py
   ```

5. **Submitting a Pull Request**
   - Reference any relevant issues.
   - Describe the problem solved and provide a test summary.
   - We review pull requests promptly!
