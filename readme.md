# Purpose

To replace makefiles with something easier to use and with faster compile times.  In today's PC market, we have routine access to machines with multiple threads.  This package will check the number of threads that your machine will support and will create that many threads for the compile stage.   

This package is opinionated and slanted towards C/C++ workflow using gcc-like commands.

# Installation

If you are already using python and are familiar with a python workflow, then you can simply `pip install meak` and maek will be added to your python installation.

If you would rather just try it out, then you can download a windows binary from the releases directory and execute it directly.  The package is portable and may be executed on the command line.  Should work as well as the python package!

# Usage

All uses will assume that there is a file called `maekfile` within the directory being executed.  This file consists of a YML dictionary containing a default configuration along with other potential configurations which are variantes on the default.  You may specify a different `maekfile` on the command line using the `--file` or `-f` options.

The `/example` directory contains a gcc-oriented example, but I have been successfully using this package to cross-compile an ARM Cortex-M3 package for months.

## YML files

The YML file is best presented as an example.  Below is an example that will compile an generic 'hello-world' type of application that may be found in the `examples` directory.

Each file must contain a `default` configuration.  All other configurations will inherit from the default configuration.

```yml
default:
  clean: false
  compile: true
  link: true

  sources:
    - gcc/src/main.c
    - gcc/src/example.c

  includes:
    - gcc/inc

debug:
  out: exe
  flags:
    - -O0
    - -g

release:
  clean: true
  flags:
    - -O1
```

## Information and Help

The `maek` command generally expects to find a `maekfile` in the current directory.  If not found, then the file may be specified using the `-f` or `--file` options on the command line.

    $> maek --version
    maek, version 0.1.2
    $> maek --help
    Usage: maek.exe [OPTIONS] [CONFIGURATION]
    
    Options:
      --version           Show the version and exit.
      -c, --clean
      -f, --file TEXT     specifies the maekfile
      -v, --verbose       turn on verbose mode
      -q, --quiet         quiet output, only displays warnings and errors
      -l, --list_configs  shows the available configurations
      --help              Show this message and exit.

## Building a Project

Assuming that a configuration called `release` is available within the yml file, a suitable build command would be

    $> maek release
    
## Cleaning a Project

Need to clean up a project directory in order to do a re-build?  Simply call up the configuration name with the `--clean` parameter.

    $> maek release --clean

It is also possible to use the `clean` option shown in `configuration options` in order to execute a clean on every build.
    
# Configuration Options

Every `maekfile` file must contain a `default` configuration.  Each configuration is a level 1 within the YAML-based `maekfile`.  Each configuration may contain the following options:

## Configuration Options

### clean

Boolean `true` or `false`.  Will trigger a clean as part of every execution of this configuration.  Default: `false`.

### compile

Boolean.  Will trigger a compile as part of every execution of this configuration.  Default: `true`.

### link

Boolean.  Will trigger a link as part of every execution of this configuration.  Default: `true`.

### out

List of strings.  Specifies the extension of the output.  Default: `out`.  Other desired extensions might be `exe` or `elf`.

```yml
default:
  out:
    - hex
    - bin
```

### exports

List of strings.  Will trigger a copy operation of the output file into different formats.  Valid strings are `hex` and `bin`.

### scripts

List of `pre` and `post` scripts, which are themselves lists of strings.  These commands will be executed verbatim before and/or after the build operation.  Defaults to `null`.

```yml
default:
  scripts:
    pre:
      - rm -rf /path/to/somefile
    post:
      - /path/to/custom/script --script_param
```

### toolchain_path

String.  Specifies the path to the directory containg the toolchain.  Defaults to `null`.

### compiler

String.  Defaults to `gcc`.

### linker

String.  Defaults to `gcc`.

### objcopy

String.  Defaults to `objcopy`.

### size

String.  Defaults to `size`.

### flags

A list of strings, each containing flags that will be forwarded to, both, the `compiler` and the `linker`.

```yml
default:
  flags:
    - -O1
    - -fdata-sections
    - -ffunction-sections
```

### cflags

A list of strings, each containing flags that will be forwarded to the compiler only.  Very similar to `flags` above.

### lflags

A list of strings, each containing flags that will be forwarded to the linker only.  Very similar to `flags` above.

### sources

A list of strings, each of which is a source.  This is usually a list of your c files.

```yml
default:
  sources:
    - src/main.c
    - src/included_source.c
```

### includes

A list of strings, similar in format to `sources`, each element of which is an include file that will be passed to, both, the compiler and linker.

### lscripts

A list of strings, similar in format to `sources`, each element of which will be passed as a linker script into the linker.

## Special Strings

Some special strings will be automatically replaced wherever encountered in the `maekfile`.

`{{ BUILD_PATH }}` will be replaced by the configuration name.  This is useful in some places, particularly in pre and post-build scripts which apply to multiple configurations or for options that require a path (such as generating a map file below).

```yml
default:
  lflags:
    - -Xlinker -Map={{ BUILD_PATH }}/map
```
