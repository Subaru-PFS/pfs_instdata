import os

import yaml


def toAbsFilepath(rootDirectory, subDirectory, fileName, isRelative=True):
    """Return yaml absolute filepath.

    Parameters
    ----------
    rootDirectory : `str`
        Root directory.
    subDirectory : `str`
       Sub directory.
    fileName : `str`
        File name.

    Returns
    -------
    abspath : `str`
        Absolute filepath.
    """

    varName = '$PFS_INSTDATA_DIR'
    rootPath = os.path.expandvars(varName)

    if rootPath == varName:
        raise RuntimeError(f'{varName} is not defined')

    # construct full path if provided one is declared as relative to instdata path.
    rootDirectory = os.path.join(rootPath, rootDirectory) if isRelative else rootDirectory

    return os.path.join(rootDirectory, subDirectory, f'{fileName}.yaml')


def loadYaml(rootDirectory, fileName, subDirectory='', isRelative=True):
    """Load instdata yaml given the root directory (config/data), the file name and a optional subdirectory.

    Parameters
    ----------
    rootDirectory : `str`
        Root directory.
    fileName : `str`
        File name.
    subDirectory : `str`
       Optional subdirectory.
    isRelative : `bool`
       Is the provided rootDirectory relative to instdata path or not.

    Returns
    -------
    dict : `dict`
        yaml file as python dictionary.
    """
    with open(toAbsFilepath(rootDirectory, subDirectory, fileName, isRelative=isRelative), mode='r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def dumpYaml(rootDirectory, fileName, data, subDirectory='', isRelative=True):
    """Dump data to instdata yaml file.

    Parameters
    ----------
    rootDirectory : `str`
        Root directory.
    fileName : `str`
        File name.
    data : `dict`
        dictionary to dump.
    subDirectory : `str`
       Optional subdirectory.
    isRelative : `bool`
       Is the provided rootDirectory relative to instdata path or not.
    """
    with open(toAbsFilepath(rootDirectory, subDirectory, fileName, isRelative=isRelative), mode='w') as file:
        return yaml.dump(data, file)


def loadConfig(fileName, subDirectory=''):
    """Load instdata configuration file.

    Parameters
    ----------
    fileName : `str`
        File name.
    subDirectory : `str`
       Optional subdirectory.

    Returns
    -------
    dict : `dict`
        config dictionary.
    """
    return loadYaml('config', fileName, subDirectory=subDirectory)


def loadData(fileName, subDirectory=''):
    """Load instdata data file.

    Parameters
    ----------
    fileName : `str`
        File name.
    subDirectory : `str`
       Optional subdirectory.

    Returns
    -------
    dict : `dict`
        data dictionary.
    """
    return loadYaml('data', fileName, subDirectory=subDirectory)


def dumpData(fileName, data, subDirectory=''):
    """Load instdata data file.

    Parameters
    ----------
    fileName : `str`
        File name.
    data : `dict`
        Dictionary to dump.
    subDirectory : `str`
       Optional subdirectory.
    """
    return dumpYaml('data', fileName, data, subDirectory=subDirectory)
