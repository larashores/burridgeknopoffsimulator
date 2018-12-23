#pragma once

#include <valarray>

double get_position(const std::valarray<double>& array, int num_cols, int row, int col);
double get_position(const std::valarray<double>& array, int col);
void set_position(std::valarray<double>& array, int num_cols, int row, int col, double value);
void set_position(std::valarray<double>& array, int col, double value);
void add_position(std::valarray<double>& array, int num_cols, int row, int col, double value);
void add_position(std::valarray<double>& array, int col, double value);

double get_velocity(const std::valarray<double>& array, int num_cols, int row, int col);
double get_velocity(const std::valarray<double>& array, int col);
void set_velocity(std::valarray<double>& array, int num_cols, int row, int col, double value);
void set_velocity(std::valarray<double>& array, int col, double value);
void add_velocity(std::valarray<double>& array, int num_cols, int row, int col, double value);
void add_velocity(std::valarray<double>& array, int col, double value);