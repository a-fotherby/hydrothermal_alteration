def initialise(file_name):
    import sys
    import pathlib as pl

    home = pl.Path.home()
    path = home / 'work' / 'data' / 'hydrothermal_alteration' / file_name

    omph_path = home / 'work' / 'Omphalos'
    tope_path = home / 'work' / 'topepan'

    sys.path.append(str(omph_path))
    sys.path.append(str(tope_path))

    return home, path

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

def import_data(path, smalls_cats):
    set1 = hp.quick_import(path, smalls_cats=smalls_cats)
    datasets = [set1]

    return set1, datasets


def syntheric_vars(primary_mineral_groups, secondary_mineral_groups, data): 
    for group, minerals in primary_mineral_groups.items():
        data = sum_variables(data, minerals, group)

    for group, minerals in secondary_mineral_groups.items():
        data = sum_variables(data, minerals, group)

    data = sum_variables(data, primary_minerals, 'primary_minerals')
    data = sum_variables(data, secondary_minerals, 'secondary_minerals')
    data['percentage_alteration'] = data['secondary_minerals'] / data['primary_minerals'].isel(time=0) * 100

    return data


def sum_variables(xarray_obj, var_names, new_var_name):
    """
    Sums specified variables in an xarray object element-wise and adds the result as a new variable.
    
    Parameters:
    xarray_obj (xr.Dataset): The xarray Dataset containing the variables.
    var_names (list of str): A list of variable names to sum.
    new_var_name (str): The name of the new variable to store the sum.
    
    Returns:
    xr.Dataset: The modified xarray Dataset with the new summed variable.
    """

    import xarray as xr
    # Check if all variable names exist in the xarray object
    missing_vars = [var for var in var_names if var not in xarray_obj.data_vars]
    if missing_vars:
        raise ValueError(f"The following variables are not in the xarray object: {missing_vars}")
    
    # Initialize a zero-filled DataArray based on the first variable's shape and coordinates
    sum_var = xr.zeros_like(xarray_obj[var_names[0]])
    
    # Sum the variables element-wise
    for var_name in var_names:
        sum_var += xarray_obj[var_name]
    
    # Add the summed variable to the xarray object
    xarray_obj[new_var_name] = sum_var
    
    return xarray_obj

def old_mineral_groups():
    primary_minerals = ['Forsterite', 'Fayalite', 'Microcline', 'Ferrosilite(al', 'Enstatite(alph', 'Diopside', 'Anorthite', 'Albite(low)', 'Ilmenite']
    secondary_minerals = ['Hsaponite(Mg)', 'Clinochlore', 'Chamosite(Daph', 'Celadonite', 'Chrysotile', 'Talc', 'Actinolite', 'Tremolite', 'Epidote', 'Clinozoisite', 'Anhydrite', 'Calcite']

    olivine = ['Forsterite', 'Fayalite']
    feldspars = ['Microcline', 'Anorthite', 'Albite(low)']
    clinopyroxenes = ['Diopside', 'Ferrosilite(al', 'Enstatite(alph']
    clays = ['Hsaponite(Mg)', 'Clinochlore', 'Chamosite(Daph', 'Celadonite']
    serpentinites = ['Chrysotile', 'Talc']
    amphiboles = ['Actinolite', 'Tremolite']
    epidote = ['Epidote', 'Clinozoisite']
    sulfates = ['Anhydrite']
    carbonates = ['Calcite']

    primary_mineral_groups = {
        'olivine': olivine,
        'feldspars': feldspars,
        'clinopyroxenes': clinopyroxenes
    }

    secondary_mineral_groups = {
        'clays': clays,
        'serpentinites': serpentinites,
        'amphiboles': amphiboles,
        'epidote': epidote,
        'sulfates': sulfates,
        'carbonates': carbonates
    }

    return primary_minerals, secondary_minerals, primary_mineral_groups, secondary_mineral_groups

def new_mineral_groups():
    primary_minerals = ['Anorthite', 'Albite', 'Diopside', 'Hedenbergite', 'Forsterite', 'Fayalite']
    secondary_minerals = ['Tremolite', 'Epidote', 'Zoisite', 'Chamosite-7A', 'Clinochlore-7A', 'Analcime', 'Anhydrite', 'Calcite']

    clays = ['Saponite_Mg', 'Chamosite-7A', 'Clinochlore-7A']
    zeolites = ['Analcime']
    amphiboles = ['Tremolite']
    serpentinites = ['Talc']
    epidotes = ['Epidote', 'Zoisite']
    olivine = ['Forsterite', 'Fayalite']
    clinopyroxenes = ['Diopside', 'Hedenbergite']
    plagioclases = ['Anorthite', 'Albite']
    sulfates = ['Anhydrite']
    carbonates = ['Calcite']

    secondary_mineral_groups = {
        'clays': clays,
        'zeolites': zeolites,
        'amphiboles': amphiboles,
        'serpentinites': serpentinites,
        'epidotes': epidotes,
        'sulfates': sulfates,
        'carbonates': carbonates,
    }

    primary_mineral_groups = {
        'olivine': olivine,
        'clinopyroxenes': clinopyroxenes,
        'plagioclases': plagioclases
    }

    return primary_minerals, secondary_minerals, primary_mineral_groups, secondary_mineral_groups


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str, help='Name of netCDF4 file.')
    parser.add_argument('-c', '--categories', nargs='+', default=[])
    args = parser.parse_args()
    # Initialise directories
    home, path = initialise(args.file_name)

    # Import modules
    from coeus import helper as hp
    import xarray as xr

    # Import data
    ct_data = {}
    for category in args.categories:
        ct_data.update({category: xr.open_dataset(args.file_name, group=category)})

    if 'volume' in args.categories:
        primary_minerals, secondary_minerals, primary_mineral_groups, secondary_mineral_groups = new_mineral_groups()

        ct_data['volume'] = syntheric_vars(primary_mineral_groups, secondary_mineral_groups, ct_data['volume'])

        print(f'Primary minerals: {primary_minerals}')
        print(f'Secondary minerals: {secondary_minerals}')
        print(f'Primary mineral groups: {primary_mineral_groups}')
        print(f'Secondary mineral groups: {secondary_mineral_groups}')
