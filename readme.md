# Purpose

To replace makefiles with something easier to use.  Opinionated and slanted towards C/C++ workflow.

# Usage

## YML files

The YML file is best presented as an example.  Below is an example that will compile an arm-based processor.

Each configuration is given a name.  Each configuration name is directly callable from the command line.

```yml
configuration_name:
  path: C:/_code/test
  out: elf
  exports:
    - hex
    - bin

  scripts:
    pre:
    post:
      - python reference/hex_combiner.py boot="bootloader/bootloader.hex" app="release/release.hex" dest="release/combined.hex"

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
    - ldscripts/mem-bootload.ld
    - ldscripts/sections.ld
```

## Information and Help

    $> maek
    maek version 0.0.1
    $> maek --help
    Usage: maek [OPTIONS]

    Options:
      --version           Show the version and exit.
      -p, --project TEXT  path to the project file (yml)  [required]
      -n, --name TEXT     the name to build from the project file  [required]
      -c, --clean         when specified, will clean the project
      -b, --build         when specified, build the project (default)
      --help              Show this message and exit.
      
## Cleaning a project

    $> maek --project path/to/maekfile.yml --clean
    
