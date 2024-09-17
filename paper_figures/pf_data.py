def initialise(file_name):
    import sys
    import pathlib as pl

    home = pl.Path.home()
    path = home / 'work' / 'hydrothermal_alteration' / 'pflotran_model' / file_name

    omph_path = home / 'work' / 'Omphalos'
    tope_path = home / 'work' / 'topepan'

    sys.path.append(str(omph_path))
    sys.path.append(str(tope_path))

    return home, path

def syntheric_vars(primary_mineral_groups, secondary_mineral_groups, data): 
    for group, minerals in primary_mineral_groups.items():
        minerals = [string + "_VF" for string in minerals]
        data = sum_variables(data, minerals, group + "_VF")

    for group, minerals in secondary_mineral_groups.items():
        minerals = [string + "_VF" for string in minerals]
        data = sum_variables(data, minerals, group + "_VF")


    primary_minerals_VF = [string + "_VF" for string in primary_minerals]
    secondary_minerals_VF = [string + "_VF" for string in secondary_minerals]

    data = sum_variables(data, primary_minerals_VF, 'primary_minerals_VF')
    data = sum_variables(data, secondary_minerals_VF, 'secondary_minerals_VF')
    data['percentage_alteration'] = data['secondary_minerals_VF'] / data['primary_minerals_VF'].isel(time=0) * 100

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


def mineral_groups():
    primary_minerals = ['Anorthite', 'Albite', 'Diopside', 'Hedenbergite', 'Forsterite', 'Fayalite']
    secondary_minerals = ['Tremolite', 'Talc', 'Quartz', 'Saponite_Mg', 
                        'Epidote', 'Zoisite', 'Chamosite-7A', 'Clinochlore-7A', 'Analcime', 
                        'Anhydrite', 'Calcite']

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
    import os
    from pathlib import Path
    import sys

    module_path = Path('/home/angus/work/Omphalos')

    if module_path not in sys.path:
        sys.path.append(module_path)

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str, help='Name of .h5 file.')

    args = parser.parse_args()
    # Initialise directories
    home, path = initialise(args.file_name)

    # Import modules
    from coeus import pflotran as pfl
    import h5py

    # Open the HDF5 file in read mode
    with h5py.File(path, 'r') as hdf:
        data = pfl.h5_to_xarray(hdf)

    primary_minerals, secondary_minerals, primary_mineral_groups, secondary_mineral_groups = mineral_groups()
    pf_data = syntheric_vars(primary_mineral_groups, secondary_mineral_groups, data)

    print(f'Primary minerals: {primary_minerals}')
    print(f'Secondary minerals: {secondary_minerals}')
    print(f'Primary mineral groups: {primary_mineral_groups}')
    print(f'Secondary mineral groups: {secondary_mineral_groups}')
