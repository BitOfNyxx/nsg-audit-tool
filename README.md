# nsg-audit-tool

![Status](https://img.shields.io/badge/status-Week%201%20%E2%80%94%20skeleton%20only-orange)

A Python CLI for auditing Azure Network Security Group (NSG) rules for risky
configurations — things like overly permissive source ranges (`0.0.0.0/0` on
sensitive ports), unused or shadowed rules, management-plane exposure, and
other common misconfigurations that drift into NSGs over time. The goal is to
give operators a fast, scriptable second opinion on their network posture.

## Installation

Install in editable mode with the dev extras:

```bash
pip install -e ".[dev]"
```

Run the tests:

```bash
pytest
```

## Usage

Show the built-in help:

```bash
nsg-audit --help
```

Print the version (sourced from package metadata):

```bash
nsg-audit --version
```

Pick an output format (`json` is the default; `csv` and `markdown` are also accepted):

```bash
nsg-audit --output-format markdown
```
