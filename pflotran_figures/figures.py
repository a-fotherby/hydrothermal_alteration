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


def import_data(path, smalls_cats):
    set1 = hp.quick_import(path, smalls_cats=smalls_cats)
    datasets = [set1]

    return set1, datasets


def font_properties():
    from matplotlib.font_manager import FontProperties

    font_props = FontProperties()
    # font_props.set_name('sans_serif')
    font_props.set_size(28)
    font_props.set_weight('bold')

    return font_props


def synthetic_vars_ben_mins(data):
    clays = ['Hsaponite(Mg)', 'Clinochlore', 'Chamosite(Daph', 'Celadonite']
    basalt = ['Forsterite', 'Fayalite', 'Diopside', 'Hedenbergite', 'Anorthite', 'Albite(low)']
    serp = ['Chrysotile', 'Talc']
    amph = ['Actinolite', 'Tremolite']
    epidote = ['Epidote', 'Clinozoisite']
    calcite_components = ('Ca++', 'HCO3-')

    min_groups = [clays, basalt, serp, amph, epidote]
    group_names = ['Clays', 'Basalt', 'serp', 'amph', 'epidote']

    for group, name in zip(min_groups, group_names):
        ds2 = sum(data['volume'][var] for var in group)
        data['volume'] = data['volume'].assign({name: ds2})

    return data


def synthetic_vars(data):
    clays = ('Hsaponite(Mg)', 'Clinochlore', 'Chamosite(Daph', 'Celadonite')
    basalt = ('Forsterite', 'Fayalite', 'Microcline', 'Ferrosilite(al', 'Enstatite(alph', 'Diopside', 'Anorthite',
              'Albite(low)', 'Ilmenite')
    serp = ('Chrysotile', 'Talc')
    amph = ('Actinolite', 'Tremolite')
    epidote = ('Epidote', 'Clinozoisite')
    calcite_components = ('Ca++', 'HCO3-')

    min_groups = [clays, basalt, serp, amph, epidote]
    group_names = ['Clays', 'Basalt', 'serp', 'amph', 'epidote']

    for group, name in zip(min_groups, group_names):
        ds2 = sum(data['volume'][var] for var in group)
        data['volume'] = data['volume'].assign({name: ds2})

    return data


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
    from coeus import plots
    import xarray as xr
    import numpy as np

    import h5py

    # Open the HDF5 file in read mode
    with h5py.File(path, 'r') as hdf:
        data = pfl.h5_to_xarray(hdf)


    font_props = font_properties()
