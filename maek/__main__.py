import logging
import yaml
import click

from maek.maek import Builder
from maek.version import __version__

logging.basicConfig(format='%(asctime)s: %(message)s')


@click.command()
@click.version_option()
@click.argument('configuration')
@click.option('--clean', '-c', is_flag=True, default=False)
@click.option('--file', '-f', type=str, default='maekfile', help='specifies the maekfile')
@click.option('--verbose', '-v', is_flag=True, default=False, help='turn on verbose mode')
@click.option('--quiet', '-q', is_flag=True, default=False, help='quiet output, only displays warnings and errors')
@click.version_option()
def main(configuration, clean, file, verbose, quiet):
    logger = logging.getLogger()
    if verbose:
        logger.setLevel(logging.DEBUG)

    try:
        with open(file, 'r') as f:
            string = f.read()
            bd = yaml.load(string)
    except (FileNotFoundError, PermissionError):
        logger.error(f'cannot find configuration file {file}')
        return

    # first, load the 'default' configuration
    project = bd.get('default')
    if project is None:
        logger.error('default configuration not found, exiting')
        return

    config_found = False

    for project_name in bd.keys():
        if project_name == configuration:
            config_found = True

            new_project = bd['default'].copy()
            new_project['name'] = configuration

            # overwrite the defaults
            for k, v in bd[configuration].items():
                new_project[k] = v

            if clean:
                new_project['clean'] = True
                new_project['compile'] = False
                new_project['link'] = False

            loglevel = logging.DEBUG if verbose else logging.INFO
            loglevel = logging.WARNING if quiet else loglevel

            Builder(loglevel=loglevel, **new_project)

    if not config_found:
        logger.error(f'configuration {configuration} not found within {file}')


if __name__ == '__main__':
    main()


