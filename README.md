# Coinoxr - Open Exchange Rates

[![Build Status](https://travis-ci.org/luisfmcalado/coinoxr.svg?branch=master)](https://travis-ci.org/luisfmcalado/coinoxr)
[![Coverage Status](https://coveralls.io/repos/github/luisfmcalado/coinoxr/badge.svg?branch=master)](https://coveralls.io/github/luisfmcalado/coinoxr?branch=master)

Python library for Open Exchange Rates API.

## Installation

Install dependency
```bash
$ pip install coinoxr
```

Install dependency from source code
```bash
$ python setup.py install
```

### Requirements
- Python 3.7+


## Usage

```python
import coinoxr
coinoxr.app_id = "c01ed21da6424fd3b0ac68f9e63a3d29"

coinoxr.Latest().get(base="EUR")
```

## Development

Run all the tests for every environment:

```bash
$ make test
```

The code can be formatted with black:

```bash
$ make fmt
```