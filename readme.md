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
    
