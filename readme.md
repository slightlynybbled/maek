# Purpose

To replace makefiles with something easier to use.  Opinionated and slanted towards C/C++ workflow.

# Status: Experimental

All of this is likely to change as I begin to use the tool.  Don't count on consistency.

# Usage

All uses will assume that there is a file called `maekfile` within the directory being executed.  This file consists of a YML dictionary containing a default configuration along with other potential configurations which are variantes on the default.  You may specify a different `maekfile` on the command line using the `--file` or `-f` options.

## YML files

The YML file is best presented as an example.  Below is an example that will compile an arm-based processor.

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
    maek, version 0.0.3
    $> maek --help
    Usage: maek [OPTIONS] CONFIGURATION
    
    Options:
      --version        Show the version and exit.
      -c, --clean
      -f, --file TEXT  specifies the maekfile
      -v, --verbose    turn on verbose mode
      -q, --quiet      quiet output, only displays warnings and errors
      --version        Show the version and exit.
      --help           Show this message and exit.

      
## Building a Project

    $> maek release
    
## Cleaning a Project

    $> maek release --clean
    
# Configuration Options

Every `maekfile` file must contain a `default` configuration.  Each configuration is a level 1 within the YAML-based `maekfile`.  Each configuration may contain the following options:

## clean

Boolean `true` or `false`.  Will trigger a clean as part of every execution of this configuration.  Default: `false`.

## compile

Boolean.  Will trigger a compile as part of every execution of this configuration.  Default: `true`.

## link

Boolean.  Will trigger a link as part of every execution of this configuration.  Default: `true`.

## out

List of strings.  Specifies the extension of the output.  Default: `out`.  Other desired extensions might be `exe` or `elf`.

```yml
default:
  out:
    - hex
    - bin
```

## exports

List of strings.  Will trigger a copy operation of the output file into different formats.  Valid strings are `hex` and `bin`.

## scripts

List of `pre` and `post` scripts, which are themselves lists of strings.  These commands will be executed verbatim before and/or after the build operation.  Defaults to `null`.

```yml
default:
  scripts:
    pre:
      - rm -rf /path/to/somefile
    post:
      - /path/to/custom/script --script_param
```

## toolchain_path

String.  Specifies the path to the directory containg the toolchain.  Defaults to `null`.

## compiler

String.  Defaults to `gcc`.

## linker

String.  Defaults to `gcc`.

## objcopy

String.  Defaults to `objcopy`.

## size

String.  Defaults to `size`.

## flags

A list of strings, each containing flags that will be forwarded to, both, the `compiler` and the `linker`.

```yml
default:
  flags:
    - -O1
    - -fdata-sections
    - -ffunction-sections
```

## cflags

A list of strings, each containing flags that will be forwarded to the compiler only.  Very similar to `flags` above.

## lflags

A list of strings, each containing flags that will be forwarded to the linker only.  Very similar to `flags` above.

## sources

A list of strings, each of which is a source.  This is usually a list of your c files.

```yml
default:
  sources:
    - src/main.c
    - src/included_source.c
```

## includes

A list of strings, similar in format to `sources`, each element of which is an include file that will be passed to, both, the compiler and linker.

## lscripts

A list of strings, similar in format to `sources`, each element of which will be passed as a linker script into the linker.

