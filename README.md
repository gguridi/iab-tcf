# iab-tcf

![Testing](https://github.com/gguridi/iab-tcf/workflows/Testing/badge.svg)
[![codecov](https://codecov.io/gh/gguridi/iab-tcf/branch/master/graph/badge.svg)](https://codecov.io/gh/gguridi/iab-tcf)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/6e6a8a02a6b14c5998b29bbe06327c87)](https://www.codacy.com/gh/gguridi/iab-tcf/dashboard)
![Releasing](https://github.com/gguridi/iab-tcf/workflows/Releasing/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/iab-tcf/badge/?version=latest)](https://iab-tcf.readthedocs.io/en/latest/?badge=latest)

A Python implementation of the IAB consent strings (v1.1 and v2)

## Installing

Install and update using pip:

```bash
pip install -U iab-tcf
```

## Documentation

[Documentation](https://iab-tcf.readthedocs.io/en/stable/) of this package can be
found at [readthedocs.io](https://iab-tcf.readthedocs.io/en/stable/).

To generate the documentation locally:

```bash
uv sync --group docs
cd docs/
uv run sphinx-apidoc -f -o . ../iab_tcf/
uv run make html
```

## A Simple Example

In order to decode a v1.1 or v2 consent string automatically we can do:

```python
from iab_tcf import decode

consent = decode("CO5VTlWO5VTlWH1AAAENAwCwAIAAAAAAAIAAAAoAAAAA.YAAAAAAAAAA")

print(consent.version) # prints 2
```

If we want to improve performance and we already know it's going to
be a v2 consent string we can do:

```python
from iab_tcf import decode_v2

consent = decode_v2("CO5VTlWO5VTlWH1AAAENAwCwAIAAAAAAAIAAAAoAAAAA.YAAAAAAAAAA")

print(consent.version) # prints 2
```

## Tests

The project is managed with [uv](https://docs.astral.sh/uv/). In order to run
the tests locally we can do:

```bash
uv sync
uv run pytest -v .
```

## Thanks

Many thanks to [LiveRamp/iabconsent](https://github.com/LiveRamp/iabconsent)
which greatly inspired this project, and forms the basis and internal logic.
