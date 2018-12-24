#include "utilities.h"


double get_position(const std::valarray<double>& array, int num_cols, int row, int col)
{
    return array[2*num_cols*row + 2*col];
}

double get_position(const std::valarray<double>& array, int col)
{
    return array[2*col];
}

void set_position(std::valarray<double>& array, int num_cols, int row, int col, double value)
{
    array[2*num_cols*row + 2*col] = value;
}

void set_position(std::valarray<double>& array, int col, double value)
{
    array[2*col] = value;
}

void add_position(std::valarray<double>& array, int num_cols, int row, int col, double value)
{
    array[2*num_cols*row + 2*col] += value;
}

void add_position(std::valarray<double>& array, int col, double value)
{
    array[2*col] += value;
}

double get_velocity(const std::valarray<double>& array, int num_cols, int row, int col)
{
    return array[2*num_cols*row + 2*col + 1];
}

double get_velocity(const std::valarray<double>& array, int col)
{
    return array[2*col + 1];
}

void set_velocity(std::valarray<double>& array, int num_cols, int row, int col, double value)
{
    array[2*num_cols*row + 2*col + 1] = value;
}

void set_velocity(std::valarray<double>& array, int col, double value)
{
    array[2*col + 1] = value;
}

void add_velocity(std::valarray<double>& array, int num_cols, int row, int col, double value)
{
    array[2*num_cols*row + 2*col + 1] += value;
}

void add_velocity(std::valarray<double>& array, int col, double value)
{
    array[2*col + 1] += value;
}