#pragma once

#include "frictionalforce.h"
#include "plateforce.h"
#include "positionupdater.h"
#include "springforce.h"
#include "difeq.h"

#include <valarray>

class BkDifeq : public Difeq
{
public:
    BkDifeq(int num_rows, int num_cols,
                  double scaled_spring_length,
                  double scaled_plate_velocity,
                  double alpha, double l);

    std::valarray<double> differentiate(double time, const std::valarray<double>& values) const override;
private:
    PositionUpdater m_position_updater;
    SpringForce m_spring_force;
    PlateForce m_plate_force;
    FrictionalForce m_frictional_force;
    const int m_rows;
    const int m_cols;
};
