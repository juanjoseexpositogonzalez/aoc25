# Advent of Code 2025

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![Advent of Code](https://img.shields.io/badge/Advent%20of%20Code-2025-brightgreen.svg)](https://adventofcode.com/2025)

This repository contains my solutions to the [Advent of Code 2025](https://adventofcode.com/2025) programming challenges. Advent of Code is an annual event featuring daily programming puzzles released throughout December.

## Table of Contents

- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Progress](#progress)
- [About](#about)

## Project Structure

The repository is organized by day, with each challenge in its own directory:

```
2025/
├── day01/
│   ├── main.py      # Solution implementation
│   ├── input.txt    # Challenge input data
│   └── test.txt     # Test cases (when available)
├── day02/
│   ├── main.py
│   └── input.txt
├── day03/
│   ├── main.py
│   ├── input.txt
│   └── test.txt
├── day04/
│   ├── main.py
│   └── input.txt
├── day05/
│   ├── main.py
│   ├── input.txt
│   └── test.txt
├── day06/
│   ├── main.py
│   ├── input.txt
│   └── test.txt
├── day07/
│   ├── main.py
│   ├── input.txt
│   └── test.txt
├── pyproject.toml   # Project configuration
├── uv.lock          # Dependency lock file
└── README.md        # This file
```

Each day's directory contains:
- **`main.py`**: The Python solution implementation for that day's challenge
- **`input.txt`**: The input data provided for the challenge
- **`test.txt`**: Test cases or example inputs (when available)

## Requirements

- **Python 3.14+**: As specified in `pyproject.toml`
- **uv**: Fast Python package installer and resolver (inferred from `uv.lock`)

## Installation

### Installing uv

If you don't have `uv` installed, you can install it using one of the following methods:

**Using pip:**
```bash
pip install uv
```

**Using curl (Linux/macOS):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Using PowerShell (Windows):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For more installation options, visit the [uv documentation](https://github.com/astral-sh/uv).

### Setting up the project

Once `uv` is installed, you can sync the project dependencies:

```bash
uv sync
```

## Usage

To run a solution for a specific day, navigate to that day's directory and execute the `main.py` file:

```bash
cd day01
python main.py
```

Or using Python directly from the root directory:

```bash
python day01/main.py
```

### Example

```bash
# Run Day 1 solution
cd day01 && python main.py

# Run Day 2 solution
cd day02 && python main.py

# Run Day 3 solution
cd day03 && python main.py

# Run Day 4 solution
cd day04 && python main.py

# Run Day 5 solution
cd day05 && python main.py

# Run Day 6 solution
cd day06 && python main.py

# Run Day 7 solution
cd day07 && python main.py
```

### Adding New Challenges

When starting a new day's challenge:

1. Create a new directory: `mkdir dayXX` (where XX is the day number)
2. Create `main.py` with your solution
3. Add `input.txt` with the challenge input
4. Optionally add `test.txt` with test cases
5. Update the progress table in this README

## Progress

| Day | Part 1 | Part 2 | Notes |
|-----|:------:|:------:|-------|
| [Day 1](day01/) | ✅ | ✅ | |
| [Day 2](day02/) | ✅ | ✅ | |
| [Day 3](day03/) | ✅ | ✅ | |
| [Day 4](day04/) | ✅ | ✅ | |
| [Day 5](day05/) | ✅ | ✅ | |
| [Day 6](day06/) | ✅ | ✅ | |
| [Day 7](day07/) | ✅ | ✅ | |
| Day 8 | ⬜ | ⬜ | |
| Day 9 | ⬜ | ⬜ | |
| Day 10 | ⬜ | ⬜ | |
| Day 11 | ⬜ | ⬜ | |
| Day 12 | ⬜ | ⬜ | |

**Legend:**
- ✅ Completed
- ⬜ Not started

## About

[Advent of Code](https://adventofcode.com/) is created by [Eric Wastl](http://was.tl/). Each December, participants solve programming puzzles to save Christmas. The challenges are designed to be solved in any programming language, and each day's puzzle has two parts.

---

**Note**: This repository contains my personal solutions. If you're participating in Advent of Code, I encourage you to solve the challenges yourself before looking at these solutions!

