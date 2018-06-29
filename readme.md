# Purpose

To replace makefiles with something easier to use.  Opinionated and slanted towards C/C++ workflow.

# Status: Experimental

All of this is likely to change as I begin to use the tool.  Don't count on consistency.

# Usage

## YML files

The YML file is best presented as an example.  Below is an example that will compile an arm-based processor.

Each file must contain a `default` configuration.  All other configurations will inherit from the default configuration.

```yml
default:
  clean: false
  compile: true
  link: true

  path: C:/_code/test
  out: elf
  exports:
    - hex
    - bin

  scripts:
    pre: null
    post: null

  toolchain_path: C:/Program Files (x86)/GNU Tools ARM Embedded/6 2017-q2-update/bin
  compiler: arm-none-eabi-gcc
  linker: arm-none-eabi-gcc
  objcopy: arm-none-eabi-objcopy
  size: arm-none-eabi-size

  flags:
    - -O1
    - -mcpu=cortex-m3
    - -mthumb
    - -fsigned-char
    - -ffunction-sections
    - -fdata-sections
    - -ffreestanding
    - -flto
    - -fno-move-loop-invariants

  cflags:
    - -DSTM32F10X_LD
    - -DHSE_VALUE=8000
    - -DNDEBUG

  lflags:
    - -Xlinker --gc-sections
    - -nostartfiles
    - -Xlinker -Map=_project/map

  sources:
    -  source/main.c
    -  source/my-lib.c

  includes:
    - source/inc
    - source/my-includes

  lscripts:
    - ldscripts/libs.ld
    - ldscripts/mem.ld
    - ldscripts/sections.ld
    
# the difference between the release and default is that the 
# release will combine two text files using a post-build script
release:
  scripts:
    pre:
    post:
      - python reference/hex_combiner.py boot="bootloader/bootloader.hex" app="release/release.hex" dest="release/combined.hex"
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
    
