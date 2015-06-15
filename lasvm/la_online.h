#ifndef LA_ONLINE_H
#define LA_ONLINE_H
#include "classification_types.h"

using namespace std;
#include <stdio.h>
#include <vector>
#include <cmath>
#include <ctime>
#include <cstring>
#include <iostream>
#include <fstream>
#include <algorithm>

#include "vector.h"
#include "lasvm.h"

namespace online 
{

extern int m,msv;                         
extern vector <double> alpha_sv;            // alpha_i, SV weights
extern double b0;                        // threshold

void parse_command_line(int argc, char **argv);

void load_data_file();

//This function is modified from libsvm_load_data(char *filename)
void libsvm_load_data(const std::vector<LabelData> &trainingdata);

//double kernel(lasvm_sparsevector_t* sv, double x_sq, int j, void *kparam);
double kernel(int i, double x_sq, lasvm_sparsevector_t* testvector, void *kparam);

void train_online();

int libsvm_save_model(std::string model_file_name);

int libsvm_load_model(std::string model_file_name);

void test();

}
#endif
