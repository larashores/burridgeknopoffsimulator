#pragma once

double get_position(double* array, int num_cols, int row, int col);
double get_position(double* array, int col);

void set_velocity(double* array, int num_cols, int row, int col, double value);
void set_velocity(double* array, int col, double value);