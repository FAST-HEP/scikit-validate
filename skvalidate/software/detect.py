import sys

from plumbum import local


def __get_root_version__():
    root_config = local['root-config']
    return root_config('--version').strip()


def __get_geant4_version__():
    g4_config = local['geant4-config']
    return g4_config('--version').strip()


def __get_python_version__():
    return '{}.{}.{}'.format(
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro,
    )


def __get_gcc_version__():
    gcc = local['gcc']
    version = gcc('--version').split()[2]
    if '-' in version:
        version = version.split('-')[0]
    return version


software_versions = {
    'python': __get_python_version__,
    'root': __get_root_version__,
    'geant4': __get_geant4_version__,
    'gcc': __get_gcc_version__,
}


def get_software_version(software):
    if software.lower() not in software_versions:
        msg = 'Do not know how to detect version for: {}.\n'.format(software)
        msg += 'Known software: {}'.format(', '.join(software_versions.keys()))

        raise KeyError(msg)
    return software_versions[software.lower()]()
