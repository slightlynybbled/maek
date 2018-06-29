import os
from shutil import rmtree
import subprocess

from tqdm import tqdm
import logging


class Builder:
    def __init__(self, name, path=None,
                 toolchain_path=None, compiler='gcc', linker='gcc', objcopy='objcopy', size='size',
                 flags: list=None, cflags: list=None, lflags: list=None,
                 sources: list=None, includes: list=None, lscripts: list=None,
                 out: str=None, exports: list=None, scripts: dict=None,
                 compile: bool=True, link: bool=True,
                 clean: bool=False, force: bool=False,
                 loglevel=logging.INFO):

        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)
        self._logger.info('building...')

        toolchain_path = toolchain_path if toolchain_path else ''
        flags = flags if flags else []
        cflags = cflags if cflags else []
        lflags = lflags if lflags else []
        sources = sources if sources else []
        includes = includes if includes else []
        lscripts = lscripts if lscripts else []
        if not path:
            path = os.getcwd()
        else:
            os.chdir(f'{path}')

        out = f'{path}/{name}/{name}.{out}' if out else f'{path}/{name}/{name}.out'
        self._logger.debug(f'out file path: {out}')

        exports = [f'{name}.{e}' for e in exports] if exports else []
        if exports:
            self._logger.debug(f'exports: {exports}')

        os.makedirs(f'{path}', exist_ok=True)

        if scripts and not clean:
            pre_compile_scripts = scripts.get('pre')
            if pre_compile_scripts:
                self._logger.info('executing pre-build scripts...')
                ExecScripts(pre_compile_scripts, loglevel=loglevel+10)

        if clean:
            self._logger.info('cleaning...')
            try:
                rmtree(f'{name}')
            except FileNotFoundError:
                pass

            if not compile or not link:
                return

        os.makedirs(f'{path}/{name}', exist_ok=True)

        compiler = Compiler(
            name,
            compiler=f'{toolchain_path}/{compiler}' if toolchain_path else f'{compiler}',
            sources=sources,
            includes=includes,
            flags=flags + cflags,
            force=force,
            loglevel=loglevel
        )
        if compile:
            compiler.compile()

        print('out file', out)
        linker = Linker(
            name,
            path=path,
            linker=f'{toolchain_path}/{linker}' if toolchain_path else f'{linker}',
            sources=compiler.output_files,
            scripts=lscripts,
            flags=flags + lflags,
            out=f'{out}',
            loglevel=loglevel
        )
        if link:
            linker.link()

        # copiers will operate exclusively within the build directory, but only after a successful link operation
        if compile or link:
            copier = Copier(
                in_file=os.path.basename(linker.out_file),
                path=f'{path}/{name}',
                out_files=exports,
                objcopy=objcopy,
                loglevel=loglevel
            )
            copier.copy()

            sizer = Sizer(
                in_file=os.path.basename(linker.out_file),
                path=f'{path}/{name}',
                size=size,
                loglevel=loglevel
            )
            sizer.size()

        if scripts and not clean:
            post_compile_scripts = scripts.get('post')
            if post_compile_scripts:
                ExecScripts(post_compile_scripts, loglevel=loglevel+10)


class Compiler:
    def __init__(self, name: str, compiler='gcc',
                 sources=None, includes=None, flags=None, force=False,
                 loglevel=logging.INFO):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        build_path = f'{name}'

        base_names = [f'{os.path.splitext(s)[0]}' for s in sources]
        source_files = []
        object_files = []
        to_compile = []

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
                to_compile.append(o)
            object_files.append(o)

        flag_string = ' '.join(flags)
        include_string = ' '.join([f'-I"{i}"' for i in includes])

        compile_scripts = [f'"{compiler}" -c {sf} -o {of} {flag_string} {include_string}' for sf, of in zip(source_files, to_compile)]

        self.output_files = object_files
        self._compile_scripts = compile_scripts

    def compile(self):
        self._logger.info('compiling...')
        # build the project directory as GCC will not create subdirectories for you
        for o in self.output_files:
            d = os.path.dirname(o)
            os.makedirs(d, exist_ok=True)

        # compile all of the .o files
        ExecScripts(self._compile_scripts, loglevel=self._logger.getEffectiveLevel())


class Linker:
    def __init__(self, name: str, path: str, linker: str='gcc',
                 sources: list=None, scripts: list=None, flags=None,
                 out: str=None,
                 loglevel=logging.INFO):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        self._name = name

        sources = sources if sources else []
        scripts = scripts if scripts else []
        flags = flags if flags else []
        out = out if out else f'{path}/{name}.out'

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
        ExecScripts([self._link_script], loglevel=self._logger.getEffectiveLevel())


class Copier:
    def __init__(self, in_file, path, out_files: list, objcopy='objcopy', loglevel=logging.INFO):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        self._scripts = []

        for out_file in out_files:
            if 'hex' in out_file.lower():
                self._scripts.append(
                    f'{objcopy} -O ihex {path}/{in_file} {path}/{out_file}'
                )
            elif 'bin' in out_file.lower():
                self._scripts.append(
                    f'{objcopy} -O binary {path}/{in_file} {path}/{out_file}'
                )

    def copy(self):
        if self._scripts:
            self._logger.info('copying...')
            ExecScripts(self._scripts, loglevel=logging.DEBUG)


class Sizer:
    def __init__(self, in_file, path, format='dec', size='size', loglevel=logging.INFO):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        self._script = ''

        if 'dec' in format.lower():
            self._script = f'{size} {path}/{in_file}'
        elif 'hex' in format.lower():
            self._script = f'{size} -x {path}/{in_file}'
        else:
            self._script = None

    def size(self):
        if self._script:
            self._logger.info('sizing...')
            ExecScripts([self._script], loglevel=self._logger.getEffectiveLevel())


# todo: parallel builds
class ExecScripts:
    def __init__(self, scripts: list, working_directory=None, loglevel=logging.INFO):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        if working_directory:
            os.chdir(working_directory)

        for script in tqdm(scripts):
            self._logger.debug(f'{script}')

            p = subprocess.Popen(script, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output, error = p.communicate()
            status = p.wait()

            if output:
                self._logger.info(f"\n{output.decode('utf-8')}")

            if error:
                self._logger.warning(f"\n{error.decode('utf-8')}")

            if status != 0:
                self._logger.error('failed')
            else:
                self._logger.debug('success')
