## Overview

mortar is a set of tools for evaluating OCR results for games. The purpose of
the project is to improve upon the OCR path that MORT offers. Some of mortar's
features toward this end include:

- Reproduce the Tesseract/OCR path used in MORT precisely. This allows for
  evaluating data as MORT does, in an automated, reproducible way.
- Host a comprehensive set of test cases for Japanese to English translation of
  pixel fonts using scenes from 8 and 16-bit era games.

## Requirements

The package is intended to run on a WSL system. It creates a Windows Tesseract
process to perform OCR function.

## Installation

### Clone the repository

```
git clone https://github.com/spectrumbranch/mortar.git
cd mortar
```

### Installing with pip

It is recommended to use [pdm](#installing-with-pdm-recommended-over-pip)
instead.

To install the package using pip:

```
python -m venv .venv
. .venv/bin/activate

pip install .[dev]
```

### Installing with pdm (recommended over pip)

- Install pdm using your package manager.
- Run `pdm install`. The command creates a virtualenv with the mortar package
  and its dependencies installed inside it.

With the package installed, the `pdm run` command runs a command from within
the package environment. `pdm run nox` runs development checks, for example.

### Activating the virtualenv

It may be convenient to activate the virtualenv by running
`. .venv/bin/activate`. With the virtualenv activated, all commands supported by
the package are placed on the path and can be run directly (e.g. by running
`nox` instead of `pdm run nox`).

### Set the required environment variables

The package requires these variables be set. Actual values vary between
configurations.

Path to the Tesseract executable:

```
export TESSERACT="$VCPKG_INSTALLED/x64-windows-static-md/x64-windows-static-md/tools/tesseract/tesseract.exe"
```

Path to the `tessdata` directory installed with MORT:

```
export TESSERACT_DATA="C:/MORT/MORT/bin/x64/Release/net7.0-windows10.0.22621.0/tessdata"
```

### Automatically activating the virtualenv and setting environment variables

[direnv](https://direnv.net/) can be used to automatically set required
environment variables upon entering the project directory. See the direnv
documentation and [Python](https://github.com/direnv/direnv/wiki/Python)
section of the direnv wiki for details.

## Usage

### Run the tests

#### OCR tests

OCR tests perform OCR on a collection of images from various games. The
results are compared against correct reference data (not yet implemented).
Because this is a long running procedure, the OCR tests are not included in the
project's test suite by default. To run them, tell pytest about them explicitly:

```
pytest test/test_jp.py
```

#### Development

To run all development checks, including linting and type checks, use nox.

```
nox
```

### Use the command line interface

The `mortess` command generates an OCR string from an image on demand. The
result is the same as MORT's Tesseract path. Paths must be absolute paths on a
WSL filesystem (i.e. begin with `/mnt`).

```
mortess /mnt/c/path/to/some/mort_capture.png
```

### Configuration

mortar loads its configuration in `$HOME/.config/mortar/config.toml`, creating
the file if it is not present.

#### log_level

The value of this key controls the logging level. The log levels are `"DEBUG"`,
`"INFO"`, `"WARNING"`, and `"ERROR"`.

#### ssh

When the `use_ssh` key is `true`, mortar executes its processes over ssh
instead of locally. The ssh connection is controlled by the values of the `host`
and `port` keys. This feature is useful for running mortar on a non-Windows
system that then does its OCR work on a Windows system, for example.
