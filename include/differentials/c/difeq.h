#pragma once

#include <valarray>

class Difeq
{
public:
    virtual std::valarray<double> differentiate(double time, const std::valarray<double>& current) = 0;
};
