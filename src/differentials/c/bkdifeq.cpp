#include "differentials/c/bkdifeq.h"

BkDifeq::BkDifeq(int num_rows, int num_cols,
                             double scaled_spring_length,
                             double scaled_plate_velocity,
                             double alpha, double l) :
        m_position_updater{num_rows, num_cols},
        m_spring_force{num_rows, num_cols, scaled_spring_length, l},
        m_plate_force{num_rows, num_cols, scaled_spring_length},
        m_frictional_force{num_rows, num_cols, scaled_plate_velocity, alpha},
        m_rows{num_rows},
        m_cols{num_cols}
{

}

std::valarray<double> BkDifeq::differentiate(double /*time*/, const std::valarray<double>& current) const
{
    std::valarray<double> results (static_cast<std::size_t>(m_rows * m_cols * 2));
    m_spring_force.differentiate(current, results);
    m_frictional_force.differentiate(current, results);
    m_plate_force.differentiate(current, results);
    m_position_updater.differentiate(current, results);
    return results;
}
