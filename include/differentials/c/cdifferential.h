#pragma once

#include "differentials/c/cfrictionalforce.h"
#include "differentials/c/cplateforce.h"
#include "differentials/c/cpositionupdater.h"
#include "differentials/c/cspringforce.h"
#include "differentials/c/difeq.h"

#include <valarray>

class CDifferential : public Difeq
{
public:
    CDifferential(int num_rows, int num_cols,
                  double scaled_spring_length,
                  double scaled_plate_velocity,
                  double alpha, double l);

    std::valarray<double> differentiate(double time, const std::valarray<double>& values) const override;
private:
    CPositionUpdater m_position_updater;
    CSpringForce m_spring_force;
    CPlateForce m_plate_force;
    CFrictionalForce m_frictional_force;
    const int m_rows;
    const int m_cols;
};
