def font_properties():
    from matplotlib.font_manager import FontProperties

    font_props = FontProperties()
    # font_props.set_name('sans_serif')
    font_props.set_size(15)
    font_props.set_weight('bold')

    return font_props

import matplotlib.pyplot as plt

def axis_to_depth_profile(ax):
    # Move x-axis to the top
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    # Invert the y-axis to increase downwards
    ax.invert_yaxis()

    ax.set_box_aspect(2)  # Makes the plot 2 times taller than wide
    # Optionally, add grid lines for reference
    ax.grid(False)

    return ax
