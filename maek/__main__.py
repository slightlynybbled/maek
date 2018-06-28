import logging
import yaml
import click

from maek.maek import Builder
from maek.version import __version__


@click.command()
@click.version_option()
@click.option('--project', '-p', type=str, default='maek', required=True, help='path to the project file (yml)')
@click.option('--name', '-n', type=str, default='build', required=True, help='the name to build from the project file')
@click.option('--clean', '-c', is_flag=True, default=False, help='when specified, will clean the project')
@click.option('--build', '-b', is_flag=True, default=False, help='when specified, build the project (default)')
def main(project, name, clean, build):
    try:
        with open(project, 'r') as f:
            string = f.read()
            bd = yaml.load(string)
    except (FileNotFoundError, PermissionError):
        print(f'maek version {__version__}')
        return

    project_found = False
    for project_name in bd.keys():
        if project_name == name:
            project_found = True

            pd = {'name': project_name}
            for k, v in bd[project_name].items():
                pd[k] = v

            Builder(compile=build, link=build, clean=clean, **pd)

    if not project_found:
        print(f'name "{name}" not found within {project}, exiting')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    main()


