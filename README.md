# PFS Instrument Data Config Repository - pfs_instdata

## Overview

Instrument characteristics and configuration data for the Subaru Prime Focus Spectrograph (PFS).

This repository stores the versioned data files (e.g., fiber maps, PFI geometry, actor configs) used by the PFS software stack, mostly for the Instrument Control Software (ICS) components. It includes a small Python helper package (`pfs.instdata`) to locate these resources at runtime whether the package is installed normally or used in an editable checkout.

## Directory layout

- Data lives under `data/`
- Configuration lives under `config/`
- Python helpers live under `python/pfs/instdata/`

## Installation

pfs-instdata is published as a standard Python package (Python 3.12+).

- From PyPI:

  ```bash
  pip install pfs-instdata
  ```

- From source (editable/development install):

  ```bash
  git clone https://github.com/Subaru-PFS/pfs_instdata.git
  cd pfs_instdata
  pip install -e .
  ```

Optional: to set a legacy environment variable used by some tools, you can run in Python:

```python
from pfs.instdata import setup_envvar
setup_envvar()  # sets PFS_INSTDATA_DIR to the package root
```

## Usage

This repository is used for looking up configuration data stored mostly in YAML files and CSV files,
which are stored in the `config/` and `data/` directories respectively.

If you are using the Python package, import `pfs.instdata` and call its helpers to find the data/config directories without hard-coding paths.

```python
from pfs.instdata import get_data_path, get_config_path, get_root_path

print("root path:", get_root_path())
print("data path:", get_data_path())
print("config path:", get_config_path())
```
