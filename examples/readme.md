# Sample `maekfile`

In the maekfile, there are various configurations defined, all of which inherit from the `default`.

To build these configurations:

    $> maek debug
    2018-06-29 13:38:00,288: building...
    2018-06-29 13:38:00,288: compiling...
    0it [00:00, ?it/s]
    out file:  debug/debug.exe
    2018-06-29 13:38:00,289: linking...
    100%|███████████████████| 1/1 [00:00<00:00, 13.54it/s]
    2018-06-29 13:38:00,364: copying...
    0it [00:00, ?it/s]
    2018-06-29 13:38:00,365: sizing...
      0%|                                                                                                                                                               | 0/1 [00:00<?, ?it/s]
    2018-06-29 13:38:00,453:
      text    data     bss     dec     hex filename
      10080    2388    2448   14916    3a44 debug.exe
    
    100%|███████████████████| 1/1 [00:00<00:00, 11.52it/s]
    
    $>maek release
    


