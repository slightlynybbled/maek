import os
from shutil import rmtree
import subprocess

from tqdm import tqdm
import logging


class Builder:
    def __init__(self, name, path,
                 toolchain_path, compiler, linker, objcopy, size,
                 flags: list=None, cflags: list=None, lflags: list=None,
                 sources: list=None, includes: list=None, lscripts: list=None,
                 out: str=None, exports: list=None, scripts: dict=None,
                 compile: bool=True, link: bool=True,
                 clean: bool=False, force: bool=False):

        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.DEBUG)

        self._logger.info('building...')

        os.chdir(path)

        flags = flags if flags else []
        cflags = cflags if cflags else []
        lflags = lflags if lflags else []
        sources = sources if sources else []
        includes = includes if includes else []
        lscripts = lscripts if lscripts else []
        out = out if out else f'{path}/{name}/{name}.{out}'
        exports = [f'{name}.{e}' for e in exports] if exports else []

        if scripts:
            pre_compile_scripts = scripts.get('pre')
            if pre_compile_scripts:
                ExecScripts(pre_compile_scripts)

        if clean:
            self._logger.info('cleaning...')
            try:
                rmtree(f'{path}/{name}')
            except FileNotFoundError:
                pass
            os.makedirs(f'{path}/{name}', exist_ok=True)

        compiler = Compiler(
            name,
            compiler=f'{toolchain_path}/{compiler}',
            sources=sources,
            includes=includes,
            flags=flags + cflags,
            force=force
        )
        if compile:
            compiler.compile()

        linker = Linker(
            name,
            linker=f'{toolchain_path}/{linker}',
            sources=compiler.output_files,
            scripts=lscripts,
            flags=flags + lflags,
            out=f'{name}/{name}.{out}'
        )
        if link:
            linker.link()

        # copyiers will operate exclusively within the build directory
        os.chdir(f'{path}/{name}')
        copier = Copier(
            in_file=os.path.basename(linker.out_file),
            out_files=exports,
            objcopy=objcopy
        )
        copier.copy()

        sizer = Sizer(
            in_file=os.path.basename(linker.out_file),
            size=size
        )
        sizer.size()
        os.chdir(path)

        if scripts:
            post_compile_scripts = scripts.get('post')
            if post_compile_scripts:
                ExecScripts(post_compile_scripts)


class Compiler:
    def __init__(self, name: str, compiler='gcc',
                 sources=None, includes=None, flags=None, force=False):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)

        self._name = name
        self._compiler = compiler

        build_path = f'{self._name}'

        base_names = [f'{os.path.splitext(s)[0]}' for s in sources]
        source_files = []
        object_files = []

        # if the object file is older than the source, then re-compile
        for fname in base_names:
            s = f'{fname}.c'
            o = f'{build_path}/{fname}.o'

            s_mtime = os.stat(s).st_mtime

            try:
                o_mtime = os.stat(o).st_mtime
            except FileNotFoundError:
                o_mtime = 0.0

            if s_mtime > o_mtime or force:
                source_files.append(s)
                object_files.append(o)

        flag_string = ' '.join(flags)
        include_string = ' '.join([f'-I"{i}"' for i in includes])

        compile_scripts = [f'"{self._compiler}" -c {sf} -o {of} {flag_string} {include_string}' for sf, of in zip(source_files, object_files)]

        self.output_files = object_files
        self._compile_scripts = compile_scripts

    def compile(self):
        self._logger.info('compiling...')
        # build the project directory as GCC will not create subdirectories for you
        for o in self.output_files:
            d = os.path.dirname(o)
            os.makedirs(d, exist_ok=True)

        # compile all of the .o files
        ExecScripts(self._compile_scripts)


class Linker:
    def __init__(self, name: str, str=None, linker: str='gcc',
                 sources: list=None, scripts: list=None, flags=None,
                 out: str=None):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)

        self._name = name

        sources = sources if sources else []
        scripts = scripts if scripts else []
        flags = flags if flags else []
        out = out if out else f'{name}/{name}'

        for s in scripts:
            _, extension = os.path.splitext(s)
            if extension != '.ld':
                raise ValueError(f'linker script extension not valid: {extension}')

        flags_string = ' '.join(flags)
        linker_scripts_string = ' '.join([f'-T "{s}"' for s in scripts])
        sources_string = ' '.join([f'"{s}"' for s in sources])

        self._link_script = f'"{linker}" -o {out} {flags_string} {linker_scripts_string} {sources_string}'
        self.out_file = out

    def link(self):
        self._logger.info('linking...')
        ExecScripts([self._link_script])


class Copier:
    def __init__(self, in_file, out_files: list, objcopy='objcopy'):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)

        self._scripts = []

        for out_file in out_files:
            if 'hex' in out_file.lower():
                self._scripts.append(
                    f'{objcopy} -O ihex {in_file} {out_file}'
                )
            elif 'bin' in out_file.lower():
                self._scripts.append(
                    f'{objcopy} -O binary {in_file} {out_file}'
                )

    def copy(self):
        self._logger.info('copying...')
        ExecScripts(self._scripts)


class Sizer:
    def __init__(self, in_file, format='dec', size='size'):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)

        self._script = ''

        if 'dec' in format.lower():
            self._script = f'{size} {in_file}'
        elif 'hex' in format.lower():
            self._script = f'{size} -x {in_file}'
        else:
            self._script = None

    def size(self):
        if self._script:
            self._logger.info('sizing...')
            ExecScripts([self._script], loglevel=logging.DEBUG)


# todo: parallel builds
class ExecScripts:
    def __init__(self, scripts: list, working_directory=None, loglevel=logging.INFO):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        self.success = True

        if working_directory:
            os.chdir(working_directory)

        for script in tqdm(scripts):
            self._logger.debug(f'{script}')

            p = subprocess.Popen(script, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output, error = p.communicate()
            status = p.wait()

            if output:
                self._logger.debug(output.decode('utf-8'))

            if error:
                self._logger.warning(error.decode('utf-8'))

            if status != 0:
                self._logger.error(f'failed')
