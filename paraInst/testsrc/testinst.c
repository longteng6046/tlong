#include "testinst.h"

int instout_i(char * funName, char * varName, int value){
  char * prefix="/home/tlong/tmp/apr_inst/";
  FILE * file;
  char fileName[100];
  strcpy(fileName, prefix);
  strcat(fileName, funName);
  strcat(fileName, "_");
  strcat(fileName, varName);
  strcat(fileName, ".txt");
  /* printf("%s\n", fileName); */

  file = fopen(fileName, "a");
  if (file == NULL){
    fprintf(stderr, "error creating/opening the file.\n");
    exit(1);
  }
  fprintf(file, "%d\n", value);
  fclose(file);
}

int instout_l(char * funName, char * varName, long value){
  char * prefix="/home/tlong/tmp/apr_inst/";
  FILE * file;
  char fileName[100];
  strcpy(fileName, prefix);
  strcat(fileName, funName);
  strcat(fileName, "_");
  strcat(fileName, varName);
  strcat(fileName, ".txt");
  /* printf("%s\n", fileName); */

  file = fopen(fileName, "a");
  if (file == NULL){
    fprintf(stderr, "error creating/opening the file.\n");
    exit(1);
  }
  fprintf(file, "%ld\n", value);
  fclose(file);
}

int instout_ll(char * funName, char * varName, long long value){
  char * prefix="/home/tlong/tmp/apr_inst/";
  FILE * file;
  char fileName[100];
  strcpy(fileName, prefix);
  strcat(fileName, funName);
  strcat(fileName, "_");
  strcat(fileName, varName);
  strcat(fileName, ".txt");
  /* printf("%s\n", fileName); */

  file = fopen(fileName, "a");
  if (file == NULL){
    fprintf(stderr, "error creating/opening the file.\n");
    exit(1);
  }
  fprintf(file, "%lld\n", value);
  fclose(file);
}


int instout_u(char * funName, char * varName, unsigned value){
  char * prefix="/home/tlong/tmp/apr_inst/";
  FILE * file;
  char fileName[100];
  strcpy(fileName, prefix);
  strcat(fileName, funName);
  strcat(fileName, "_");
  strcat(fileName, varName);
  strcat(fileName, ".txt");
  /* printf("%s\n", fileName); */

  file = fopen(fileName, "a");
  if (file == NULL){
    fprintf(stderr, "error creating/opening the file.\n");
    exit(1);
  }
  fprintf(file, "%u\n", value);
  fclose(file);
}

int instout_lu(char * funName, char * varName, unsigned long value){
  char * prefix="/home/tlong/tmp/apr_inst/";
  FILE * file;
  char fileName[100];
  strcpy(fileName, prefix);
  strcat(fileName, funName);
  strcat(fileName, "_");
  strcat(fileName, varName);
  strcat(fileName, ".txt");
  /* printf("%s\n", fileName); */

  file = fopen(fileName, "a");
  if (file == NULL){
    fprintf(stderr, "error creating/opening the file.\n");
    exit(1);
  }
  fprintf(file, "%lu\n", value);
  fclose(file);
}

int instout_f(char * funName, char * varName, float value){
  char * prefix="/home/tlong/tmp/apr_inst/";
  FILE * file;
  char fileName[100];
  strcpy(fileName, prefix);
  strcat(fileName, funName);
  strcat(fileName, "_");
  strcat(fileName, varName);
  strcat(fileName, ".txt");
  /* printf("%s\n", fileName); */

  file = fopen(fileName, "a");
  if (file == NULL){
    fprintf(stderr, "error creating/opening the file.\n");
    exit(1);
  }
  fprintf(file, "%f\n", value);
  fclose(file);
}

int instout_d(char * funName, char * varName, double value){
  char * prefix="/home/tlong/tmp/apr_inst/";
  FILE * file;
  char fileName[100];
  strcpy(fileName, prefix);
  strcat(fileName, funName);
  strcat(fileName, "_");
  strcat(fileName, varName);
  strcat(fileName, ".txt");
  /* printf("%s\n", fileName); */

  file = fopen(fileName, "a");
  if (file == NULL){
    fprintf(stderr, "error creating/opening the file.\n");
    exit(1);
  }
  fprintf(file, "%f\n", value);
  fclose(file);
}
