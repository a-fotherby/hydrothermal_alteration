import paraview.simple as pvs

# Function to set custom color map centered at time 0 with max/min based on all times
def set_custom_colormap_centered_at_time_0():
    # Get the active source
    source = pvs.GetActiveSource()

    # Get the time range and set the time to 0
    time_keeper = pvs.GetTimeKeeper()
    time_keeper.Time = time_keeper.TimestepValues[0]
    pvs.UpdatePipeline(time_keeper.Time, source)

    # Get the display properties
    display = pvs.GetDisplayProperties(source)

    # Get the currently visible variable
    color_array_info = display.ColorArrayName
    if color_array_info[1] == '':
        print("No active variable found for coloring.")
        return

    array_name = color_array_info[1]

    # Get the data range for the current array at time 0
    data_info = source.GetCellDataInformation().GetArray(array_name)
    initial_data_range = data_info.GetRange()
    initial_value = (initial_data_range[0] + initial_data_range[1]) / 2

    # Find the overall data range across all time steps
    overall_min = float('inf')
    overall_max = float('-inf')

    for time_step in time_keeper.TimestepValues:
        time_keeper.Time = time_step
        pvs.UpdatePipeline(time_keeper.Time, source)
        data_info = source.GetCellDataInformation().GetArray(array_name)
        data_range = data_info.GetRange()
        overall_min = min(overall_min, data_range[0])
        overall_max = max(overall_max, data_range[1])

    # Calculate the symmetric range around the initial value at time 0
    max_extent = max(abs(initial_value - overall_min), abs(initial_value - overall_max))
    custom_range = [initial_value - max_extent, initial_value + max_extent]

    # Set the scalar color map
    pvs.ColorBy(display, ('CELLS', array_name))

    # Rescale the color map to the custom range
    lut = pvs.GetColorTransferFunction(array_name)
    lut.RescaleTransferFunction(custom_range[0], custom_range[1])

    # Rescale the opacity map to the custom range
    pwf = pvs.GetOpacityTransferFunction(array_name)
    pwf.RescaleTransferFunction(custom_range[0], custom_range[1])

    # Render the view
    pvs.Render()

# Call the function to apply the custom color map
set_custom_colormap_centered_at_time_0()

