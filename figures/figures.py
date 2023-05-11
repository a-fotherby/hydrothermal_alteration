def initialise():
    import sys
    import pathlib as pl

    pickle = '21-04-23.pkl'

    home = pl.Path.home()
    path = home / 'work' / 'data' / 'hydrothermal_alteration' / pickle

    omph_path = home / 'work' / 'Omphalos'
    tope_path = home / 'work' / 'topepan'

    sys.path.append(str(omph_path))
    sys.path.append(str(tope_path))

    return home, path, pickle


def import_data(smalls_cats):
    set1 = hp.quick_import(path, smalls_cats=smalls_cats)
    datasets = [set1]

    return set1, datasets


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
