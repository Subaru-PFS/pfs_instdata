"""PFS Instrument Data Package

This package provides access to instrument characteristics files for PFS.
"""

import os
from importlib.resources import files
from pathlib import Path


def get_data_path():
    """
    Get the path to the data directory.

    Returns
    -------
    Path
        Path object pointing to the data directory
    """
    package_path = Path(__file__).parent

    # Try package-bundled data first (for installed packages)
    bundled_data = package_path / "data"
    if bundled_data.exists() and bundled_data.is_dir():
        return bundled_data

    # Fallback to repository structure (for editable installs)
    repo_data = package_path.parent.parent.parent / "data"
    return repo_data


def get_config_path():
    """
    Get the path to the config directory.

    Returns
    -------
    Path
        Path object pointing to the config directory
    """
    package_path = Path(__file__).parent

    # Try package-bundled config first (for installed packages)
    bundled_config = package_path / "config"
    if bundled_config.exists() and bundled_config.is_dir():
        return bundled_config

    # Fallback to repository structure (for editable installs)
    repo_config = package_path.parent.parent.parent / "config"
    return repo_config


def get_root_path():
    """
    Get the path to the package root directory.

    For editable installs, returns the repository root.
    For regular installs, returns a path that can be used with /data and /config
    appended (which points to the bundled data/config directories).

    Returns
    -------
    Path
        Path object pointing to the root directory
    """
    package_path = Path(__file__).parent

    # Check if we're in development mode (editable install)
    repo_root = package_path.parent.parent.parent
    if (repo_root / "data").exists() and (repo_root / "config").exists():
        # Development/editable install: return repository root
        return repo_root

    # Regular install: return package directory itself
    # (data and config are bundled inside it)
    return package_path


def setup_envvar():
    """
    Setup environment variables for PFS instrument data.

    This function sets the PFS_INSTDATA_DIR environment variable to point to
    the package root directory. This is useful for compatibility with legacy code that
    expects this environment variable to be set.

    Returns
    -------
    dict
        Dictionary of environment variables that were set
    """
    root_path = get_root_path()
    env_vars = {"PFS_INSTDATA_DIR": str(root_path)}

    for key, value in env_vars.items():
        os.environ[key] = value

    return env_vars


__all__ = ["get_data_path", "get_config_path", "get_root_path", "setup_envvar"]
