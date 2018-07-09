# Sample `maekfile`

In the maekfile, there are four configurations defined: `default`, `debug`, `release`, and `run`.  The `debug`, `release`, and `run` configurations inherit all attributes from the `default` configuration except where they overwrite the default.

All executions assume that the user has navigated to a directory containing a valid `maekfile`.

# Building the `default` configuration

To build the default configuration, simply execute `maek` or `maek default` on the command line.

# Building other configurations

Building other configurations involves specifying the desired configuration on the command line.  For instance, to build the `debug` configuration, simply execute `maek debug`.

A sample `maek debug`:

    $> maek debug
    2018-06-29 15:30:52,869: beginning...
    2018-06-29 15:30:52,870: compiling...
    100%|████████████████████| 2/2 [00:00<00:00, 18.75it/s]
    out file E:\maek\examples/debug/debug.exe
    2018-06-29 15:30:52,981: linking...
    100%|████████████████████| 1/1 [00:00<00:00, 14.50it/s]
    2018-06-29 15:30:53,051: sizing...
      0%|                               | 0/1 [00:00<?, ?it/s]2
    018-06-29 15:30:53,230:
       text    data     bss     dec     hex filename
      10080    2388    2448   14916    3a44 E:\maek\examples/debug/debug.exe
    
    100%|████████████████████| 1/1 [00:00<00:00,  5.58it/s]

# Running the application

A `run` configuration was added just to make running the output file easier and to demonstrate the flexibility of `maek`.

    $> maek run
    2018-07-09 11:18:18,864: beginning...
    2018-07-09 11:18:18,864: executing post-build scripts...
    100%|████████████████████| 1/1 [00:00<00:00, 91.64it/s]

Note that the program output is not being displayed here.  Only errors and warnings from the program will be displayed unless one of the `--verbose` or `-v` options are specified.
