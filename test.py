from rankine import rankine


def main():
    '''
    A test program for rankine power cycles.
    R1 is a rankine cycle object that is instantiated for turbine inlet of saturated vapor.
    R2 is a rankine cycle object that is instantiated for turbine inlet of superheated vapor.
    :return: none
    '''
    R1 = rankine(p_high=8000, p_low=8, name='Rankine cycle - saturated steam inlet')
    #This line creates an instance of the rankine class with the specified parameters for a turbine inlet of saturated vapor.
    R1.calc_efficiency()
    #This line calculates the efficiency of the rankine cycle represented by the R1 object.

    Tsat = R1.state1.T
    # This line assigns the temperature of the saturated vapor at the turbine inlet to the variable Tsat
    R2 = rankine(p_high=8000, p_low=8, t_high=1.7 * Tsat, name='Rankine cycle - superheated steam inlet')
    R2.calc_efficiency()
    #This line calculates the efficiency of the rankine cycle represented by the R2 object.

    R1.print_summary()
    R2.print_summary()


if __name__ == "__main__":
    main()
