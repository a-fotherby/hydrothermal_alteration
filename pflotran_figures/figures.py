def font_properties():
    from matplotlib.font_manager import FontProperties

    font_props = FontProperties()
    # font_props.set_name('sans_serif')
    font_props.set_size(28)
    font_props.set_weight('bold')

    return font_props


def s_moles_to_flux(x):
    import numpy as np
    # Cast to float
    x = np.array(x)
    # Independent of model duration
    mor_length = 65000e3  # m
    spread_rate = 40e-3  # m/yr
    mm_sulfur = 32.06  # g/mol

    conversion = spread_rate * mor_length / 1e12

    return x * conversion


def s_flux_to_moles(x):
    import numpy as np
    # Cast to float
    x = np.array(x)
    # Independent of model duration
    mor_length = 65000e3  # m
    spread_rate = 40e-3  # m/yr
    mm_sulfur = 32.06  # g/mol

    conversion = spread_rate * mor_length / 1e12
    return x / conversion


def c_moles_to_flux(x):
    # Independent of model duration
    mor_length = 65000e3  # m
    spread_rate = 40e-3  # m/yr
    molar_mass = 12  # g/mol

    conversion = spread_rate * mor_length * molar_mass / 1e12
    return x * conversion


def c_flux_to_moles(x):
    # Independent of model duration
    mor_length = 65000e3  # m
    spread_rate = 40e-3  # m/yr
    molar_mass = 12  # g/mol

    conversion = spread_rate * mor_length * molar_mass / 1e12
    return x / conversion


if __name__ == '__main__':
    font_props = font_properties()

