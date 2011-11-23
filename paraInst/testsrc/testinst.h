/*
  My own instrumental tool header.
*/

#ifndef _TEST_INST_H
#define _TEST_INST_H


#include <string.h>
#include <stdlib.h>

/* create or open a file in the given place with the same name as the funName 
   and write the value of the monitoring variable into that file. Each line is
   a single call.
*/
/*
  type: 0: unsigned, 1: singed
*/
int instout_i(char * funName, char * varName, int value);
  
int instout_l(char * funName, char * varName, long value);

int instout_ll(char * funName, char * varName, long long value);

int instout_u(char * funName, char * varName, unsigned value);

int instout_lu(char * funName, char * varName, unsigned long value);

int instout_f(char * funName, char * varName, float value);

int instout_d(char * funName, char * varName, double value);

#endif /* _TEST_INST_H */
