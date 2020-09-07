# iab-tcf

[![Build Status](https://travis-ci.org/gguridi/iab-tcf.svg?branch=master)](https://travis-ci.org/gguridi/iab-tcf)
[![codecov](https://codecov.io/gh/gguridi/iab-tcf/branch/master/graph/badge.svg)](https://codecov.io/gh/gguridi/iab-tcf)
![Releasing](https://github.com/gguridi/iab-tcf/workflows/Releasing/badge.svg)

A Python implementation of the IAB consent strings (v1.1 and v2)

# Installing

Install and update using pip:

```bash
pip install -U iab-tcf
```

# A Simple Example

In order to decode a v1.1 or v2 consent string automatically we can do:

```python
from iab_tcf import decode

consent = decode("CO5VTlWO5VTlWH1AAAENAwCwAIAAAAAAAIAAAAoAAAAA.YAAAAAAAAAA")

print(consent.version) # prints 2
```

If we want to improve performance and we already know it's going to be a v2 consent 
string we can do:

```python
from iab_tcf import decode_v2

consent = decode_v2("CO5VTlWO5VTlWH1AAAENAwCwAIAAAAAAAIAAAAoAAAAA.YAAAAAAAAAA")

print(consent.version) # prints 2
```

# Tests

In order to run the tests locally we can do:

```bash
pip install -r requirements-test.txt
pytest -v .
```

# Thanks

Many thanks to [LiveRamp/iabconsent](https://github.com/LiveRamp/iabconsent) which greatly inspired this project, and forms the basis and internal logic.
