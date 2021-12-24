import os

import yaml


def openFile(rootDirectory, subDirectory, fileName, mode='r'):
    """Open instdata file given the path.

    Parameters
    ----------
    rootDirectory : `str`
        Root directory.
    subDirectory : `str`
       Sub directory.
    fileName : `str`
        File name.
    mode : `str`
        file opening mode.

    Returns
    -------
    IO : `IOFile`
        IO file.
    """

    varName = '$PFS_INSTDATA_DIR'
    rootPath = os.path.expandvars(varName)

    if rootPath == varName:
        raise RuntimeError(f'{varName} is not defined')

    path = os.path.join(rootPath, rootDirectory, subDirectory, f'{fileName}.yaml')
    return open(path, mode=mode)


def loadYaml(rootDirectory, fileName, subDirectory=''):
    """Load instdata yaml given the root directory (config/data), the file name and a optional subdirectory.

    Parameters
    ----------
    rootDirectory : `str`
        Root directory.
    fileName : `str`
        File name.
    subDirectory : `str`
       Optional subdirectory.

    Returns
    -------
    dict : `dict`
        yaml file as python dictionary.
    """
    with openFile(rootDirectory, subDirectory, fileName, mode='r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def dumpYaml(rootDirectory, fileName, data, subDirectory=''):
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
    """
    with openFile(rootDirectory, subDirectory, fileName, mode='w') as file:
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
