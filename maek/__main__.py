import logging
import yaml
import click
import os

import coloredlogs

from maek.maek import Builder
from maek.util import dict_replace
from maek.version import __version__


@click.command()
@click.version_option()
@click.argument('configuration', default='default')
@click.option('--clean', '-c', is_flag=True, default=False)
@click.option('--file', '-f', type=str, default='maekfile.yml',
              help='specifies the maekfile')
@click.option('--verbose', '-v', is_flag=True, default=False,
              help='turn on verbose mode')
@click.option('--quiet', '-q', is_flag=True, default=False,
              help='quiet output, only displays warnings and errors')
@click.option('--list_configs', '-l', is_flag=True, default=False,
              help='shows the available configurations')
@click.version_option()
def main(configuration, clean, file, verbose, quiet, list_configs):
    logger = logging.getLogger()
    if verbose:
        coloredlogs.install(level=logging.DEBUG, fmt='%(asctime)s: %(message)s')
    else:
        coloredlogs.install(level=logging.INFO, fmt='%(asctime)s: %(message)s')

    # if there is no extension, then append 'yml' to it
    if os.path.splitext(file)[1] == '':
        file += '.yml'

    try:
        with open(file, 'r') as f:
            string = f.read()
            bd = yaml.load(string)
    except FileNotFoundError:
        logger.error(f'cannot find configuration file {file}')
        return
    except PermissionError:
        logger.error(f'user does not have permission to access {file}')
        return

    # if the '--list' option is specified, then
    # list the available configurations
    if list_configs:
        print(f'maek v{__version__} available configurations:')
        for config, _ in bd.items():
            print(f' - {config}')
        return

    # first, load the 'default' configuration
    project = bd.get('default')
    if project is None:
        logger.error('default configuration not found, exiting')
        return

    config_found = False

    # look for the configuration that was specified on the command line
    for project_name in bd.keys():
        if project_name == configuration:
            config_found = True

            new_project = bd['default'].copy()
            new_project['name'] = configuration

            # overwrite the defaults
            for k, v in bd[configuration].items():
                if isinstance(v, dict):
                    if 'add' in v.keys():
                        new_project[k] += v['add']
                    else:
                        new_project[k] = v
                else:
                    new_project[k] = v

            # replace certain strings
            new_project = dict_replace(new_project,
                                       '{{ BUILD_PATH }}',
                                       new_project['name'])

            if clean:
                new_project['clean'] = True
                new_project['compile'] = False
                new_project['link'] = False

            loglevel = logging.DEBUG if verbose else logging.INFO
            loglevel = logging.WARNING if quiet else loglevel

            Builder(loglevel=loglevel, **new_project)
            break  # the configuration was executed, now break out of the loop

    if not config_found:
        logger.error(f'configuration "{configuration}" '
                     f'not found within "{file}"')


if __name__ == '__main__':
    main()
