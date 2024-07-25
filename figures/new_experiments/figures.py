def initialise():
    import sys
    import pathlib as pl

    pickle = 'new_exp_12-05-23.pkl'

    home = pl.Path.home()
    path = home / 'work' / 'data' / 'hydrothermal_alteration' /'new_hydrothermal' / pickle

    omph_path = home / 'work' / 'Omphalos'
    tope_path = home / 'work' / 'topepan'

    sys.path.append(str(omph_path))
    sys.path.append(str(tope_path))

    return home, path, pickle


def import_data(smalls_cats):
    set1 = hp.quick_import(path, smalls_cats=smalls_cats)
    datasets = [set1]

    return set1, datasets


def font_properties():
    from matplotlib.font_manager import FontProperties

    font_props = FontProperties()
    #font_props.set_name('sans_serif')
    font_props.set_size(24)
    font_props.set_weight('bold')

    return font_props


def synthetic_vars(data):
    clays = ['Hsaponite(Mg)', 'Clinochlore', 'Chamosite(Daph', 'Celadonite']
    basalt = ['Forsterite', 'Fayalite', 'Microcline', 'Ferrosilite(al', 'Enstatite(alph', 'Diopside', 'Anorthite',
              'Albite(low)', 'Ilmenite']
    serp = ['Chrysotile', 'Talc']
    amph = ['Actinolite', 'Tremolite']
    epidote = ['Epidote', 'Clinozoisite']
    calcite_components = ['Ca++', 'HCO3-']

    min_groups = [clays, basalt, serp, amph, epidote]
    group_names = ['Clays', 'Basalt', 'serp', 'amph', 'epidote']

    for group, name in zip(min_groups, group_names):
        for file in set1:
            plots.sum_vars(set1[file], 'volume', group, name)
            plots.sum_vars(set1[file], 'rate', group, name)

    for file in set1:
        plots.prod_vars(set1[file], 'totcon', calcite_components, 'CaDIC')


def moles_to_flux(x):
    # Independent of model duration
    mor_length = 65000e3  # m
    spread_rate = 40e-3  # m/yr
    mm_sulfur = 32.06  # g/mol

    conversion = spread_rate * mor_length * mm_sulfur / 1e12
    return x * conversion


def flux_to_moles(x):
    # Independent of model duration
    mor_length = 65000e3  # m
    spread_rate = 40e-3  # m/yr
    mm_sulfur = 32.06  # g/mol

    conversion = spread_rate * mor_length * mm_sulfur / 1e12
    return x / conversion


if __name__ == '__main__':
    # Initialise directories
    home, path, pickle = initialise()

    # Import modules
    import copy
    import omphalos
    import topepan as tp
    from topepan import plot as tpp
    from omphalos import file_methods as fm
    from coeus import helper as hp
    from coeus import plots
    import xarray as xr
    import numpy as np

    # Import data
    smalls_cats = ['volume', 'rate']
    set1, datasets = import_data(smalls_cats)

    # Generate new quanitites
    synthetic_vars(set1)

    font_props = font_properties()