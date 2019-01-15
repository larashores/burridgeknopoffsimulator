#include "differentials/springforce.h"
#include "utilities.h"


namespace differentials {

SpringForce::SpringForce(int rows, int cols, double spring_length, double l) :
        m_rows{rows},
        m_cols{cols},
        m_spring_length{spring_length},
        m_l_squared{l*l}
{
    if (rows == 1 and cols >= 2)
    {
        m_diff_func = [this](auto& current, auto& results){return diff_one_dim(current, results);};
    } else
    {
        m_diff_func = [this](auto& current, auto& results){return diff_full(current, results);};
    }
}

void SpringForce::differentiate(const std::valarray<double>& current,
                                 std::valarray<double>& results) const
{
    return m_diff_func(current, results);
}

void SpringForce::diff_full(const std::valarray<double>& current,
                             std::valarray<double>& results) const
{
    for(int i=0; i < m_rows; i++)
    {
        for(int j=0; j < m_cols; j++)
        {
            double cur {get_position(current, m_cols, i, j)};

            double force {0};
            if(i >= 1) {
                force += get_position(current, m_cols, i - 1, j) - cur;
            } if(i < m_rows - 1) {
                force += get_position(current, m_cols, i + 1, j) - cur;
            } if(j >= 1) {
                force += get_position(current, m_cols, i, j - 1) - cur + m_spring_length;
            } if(j < m_cols - 1) {
                force += get_position(current, m_cols, i, j + 1) - cur - m_spring_length;
            }
            add_velocity(results, m_cols, i, j, force * m_l_squared);
        }
    }
}

void SpringForce::diff_one_dim(const std::valarray<double>& current,
                                std::valarray<double>& results) const
{
    set_velocity(results, 0,
                 m_l_squared * (get_position(current, 1) - get_position(current, 0) - m_spring_length));
    set_velocity(results, m_cols - 1, m_l_squared *
                                      (get_position(current, m_cols-2) - get_position(current, m_cols-1) + m_spring_length));
    for(int j=1; j < m_cols - 1; j++)
    {
        double force {m_l_squared * (get_position(current, j - 1)
                                     + get_position(current, j + 1)
                                     - 2 * get_position(current, j))};
        add_velocity(results, j, force);
    }
}

}  // differentials
