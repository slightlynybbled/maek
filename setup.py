from setuptools import setup
import os

requirements = [
    'tqdm >= 4.2', 'click >= 6.7', 'pyyaml >= 4.1'
]

# these are generally only used by devs
setup_requirements = [
    'flake8 >= 3.5.0'
]

# provide correct path for version
__version__ = None
here = os.path.dirname(os.path.dirname(__file__))

try:
    exec(open(os.path.join(here, 'maek/version.py')).read())
except FileNotFoundError:
    # this is the path when installing into venv through pycharm
    exec(open(os.path.join(here, 'maek/maek/version.py')).read())

with open('readme.md', 'r') as f:
    readme = f.read()

setup(
    name='maek',
    version=__version__,
    description='Command-line makefile replacement',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Jason R. Jones',
    author_email='slightlynybbled@gmail.com',
    url='https://github.com/slightlynybbled/maek',
    packages=['maek'],
    install_requires=requirements,
    setup_requires=setup_requirements,
    zip_safe=True,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English'
    ],
    keywords='c build make',
    entry_points={
        'console_scripts': ['maek = maek.__main__: main']
    }
)
