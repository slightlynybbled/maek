#include <stdio.h>
#include "example.h"

int returnInteger(void){
    int i = 0;
    while(i++ < 10)
        printf("%d\n", i);

    return i;
}

