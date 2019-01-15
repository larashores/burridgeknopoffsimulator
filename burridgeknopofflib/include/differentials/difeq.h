#pragma once

#include <valarray>


namespace differentials {

class Difeq
{
public:
    virtual std::valarray<double> differentiate(double time, const std::valarray<double>& current) const = 0;
};

}  // differentials
