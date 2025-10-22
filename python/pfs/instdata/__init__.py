"""PFS Instrument Data Package

This package provides access to instrument characteristics files for PFS.
"""

import os
from pathlib import Path
from importlib.resources import files as _res_files


def _package_root_traversable():
    """Return an importlib.resources Traversable for this package root."""
    return _res_files(__package__)


def _package_root_path_or_none():
    """Return a filesystem Path to the package root if available, else None.

    When the package is installed as a normal directory on disk (including
    editable installs), importlib.resources.files returns a path-like object
    that supports os.fspath(). If the package is inside a zip file, this
    will return None.
    """
    pkg_trav = _package_root_traversable()
    try:
        return Path(os.fspath(pkg_trav))
    except TypeError:
        return None


def get_data_path() -> os.PathLike:
    """
    Get a path-like object pointing to the data directory.

    The returned object is a pathlib.Path when the resources live on the
    filesystem (e.g., editable install), otherwise an importlib.resources
    Traversable when packaged in a non-filesystem container.

    Returns
    -------
    os.PathLike
        Path-like object pointing to the data directory

    Examples
    --------
    >>> from pfs.instdata import get_data_path
    >>> dp = get_data_path()
    >>> import os
    >>> os.fspath(dp)  # doctest: +ELLIPSIS
    '.../data'
    >>> # List available subdirectories/files
    >>> getattr(dp, 'iterdir', lambda: [])()  # doctest: +ELLIPSIS
    ...
    """
    # Prefer repository structure (for editable installs)
    package_path = _package_root_path_or_none()
    if package_path is not None:
        repo_data = package_path.parent.parent.parent / "data"
        if repo_data.exists() and repo_data.is_dir():
            return repo_data

    # Fallback to package-bundled data (for installed packages)
    bundled_data = _package_root_traversable().joinpath("data")
    return bundled_data


def get_config_path() -> os.PathLike:
    """
    Get a path-like object pointing to the config directory.

    The returned object is a pathlib.Path when the resources live on the
    filesystem (e.g., editable install), otherwise an importlib.resources
    Traversable when packaged in a non-filesystem container.

    Returns
    -------
    os.PathLike
        Path-like object pointing to the config directory

    Examples
    --------
    >>> from pfs.instdata import get_config_path
    >>> cp = get_config_path()
    >>> import os
    >>> os.fspath(cp)  # doctest: +ELLIPSIS
    '.../config'
    >>> # Access a known config file (path presence may vary by install)
    >>> hasattr(cp, 'joinpath')
    True
    """
    # Prefer repository structure (for editable installs)
    package_path = _package_root_path_or_none()
    if package_path is not None:
        repo_config = package_path.parent.parent.parent / "config"
        if repo_config.exists() and repo_config.is_dir():
            return repo_config

    # Fallback to package-bundled config (for installed packages)
    bundled_config = _package_root_traversable().joinpath("config")
    return bundled_config


def get_root_path() -> os.PathLike:
    """
    Get a path-like object to the package root directory.

    For editable installs, returns the repository root. For regular installs,
    returns a Traversable pointing to the installed package directory.

    Returns
    -------
    os.PathLike
        Path-like object pointing to the root directory

    Examples
    --------
    >>> from pfs.instdata import get_root_path
    >>> rp = get_root_path()
    >>> import os
    >>> os.fspath(rp)  # doctest: +ELLIPSIS
    '...'
    >>> # In an editable checkout, the root contains 'data' and 'config'
    >>> hasattr(rp, 'joinpath') and all((rp / n).exists() for n in ('data', 'config'))  # doctest: +ELLIPSIS
    True
    """
    package_path = _package_root_path_or_none()

    # Check if we're in development mode (editable install)
    if package_path is not None:
        repo_root = package_path.parent.parent.parent
        if (repo_root / "data").exists() and (repo_root / "config").exists():
            # Development/editable install: return repository root
            return repo_root

    # Regular install: return package directory itself (as Traversable)
    return _package_root_traversable()


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

    Examples
    --------
    >>> import os
    >>> from pfs.instdata import setup_envvar, get_root_path
    >>> env = setup_envvar()
    >>> 'PFS_INSTDATA_DIR' in env and env['PFS_INSTDATA_DIR'] == os.fspath(get_root_path())
    True
    >>> os.environ['PFS_INSTDATA_DIR'] == env['PFS_INSTDATA_DIR']
    True
    """
    root_path = get_root_path()
    try:
        root_str = os.fspath(root_path)
    except TypeError:
        root_str = str(root_path)

    env_vars = {"PFS_INSTDATA_DIR": root_str}

    for key, value in env_vars.items():
        os.environ[key] = value

    return env_vars


__all__ = ["get_data_path", "get_config_path", "get_root_path", "setup_envvar"]
