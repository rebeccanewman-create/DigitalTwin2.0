#-----------------------------------------------------------------------------
# Description: Extract Peregrine HDF5 data and export to an Excel spreadsheet
#-----------------------------------------------------------------------------

import h5py
import pandas as pd
import numpy as np

# 1. Using the 'r' prefix so Windows paths work flawlessly
path_file = r'C:\Users\rpn\Downloads\2021-08-23 TCR Phase 1 Build 5.hdf5'

print("Opening HDF5 file and reading data...")

with h5py.File(path_file, 'r') as build:
    
    # -------------------------------------------------------------------------
    # EXTRACT TEMPORAL SENSOR LOG DATA
    # -------------------------------------------------------------------------
    print("Extracting layer-wise temporal sensor log...")
    
    temporal_data = {
        "Build Time (s)": build['temporal/build_time'][:],
        "Layer Time (s)": build['temporal/layer_times'][:],
        "Top Flow Rate (m3/h)": build['temporal/top_flow_rate'][:],
        "Bottom Chamber Temp (C)": build['temporal/bottom_chamber_temperature'][:],
        "Gas Loop Oxygen (%)": build['temporal/gas_loop_oxygen'][:],
        "Build Plate Temp (C)": build['temporal/build_plate_temperature'][:]
    }
    
    df_temporal = pd.DataFrame(temporal_data)
    df_temporal.index.name = 'Layer'
    
    # -------------------------------------------------------------------------
    # EXTRACT SPECIMEN MECHANICAL TEST PROPERTIES
    # -------------------------------------------------------------------------
    print("Extracting mechanical specimen properties...")
    
    # Updated to point to 'samples/test_results/...' as required by the dataset structure
    specimen_data = {
        "Ultimate Tensile Strength (MPa)": build['samples/test_results/ultimate_tensile_strength'][:],
        "Yield Strength (MPa)": build['samples/test_results/yield_strength'][:],
        "Total Elongation (%)": build['samples/test_results/total_elongation'][:]
    }
    
    df_specimens = pd.DataFrame(specimen_data)
    df_specimens.index.name = 'Sample/Part ID'
    
    if 0 in df_specimens.index:
        df_specimens = df_specimens.drop(index=0)

    # -------------------------------------------------------------------------
    # EXPORT EVERYTHING TO AN EXCEL WORKBOOK
    # -------------------------------------------------------------------------
    excel_filename = 'Peregrine_Dataset_Export.xlsx'
    print(f"Writing data out to Excel sheet: {excel_filename}...")
    
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        df_temporal.to_excel(writer, sheet_name='Temporal Log')
        df_specimens.to_excel(writer, sheet_name='Specimen Properties')

print("\n🎉 Success! Check your workspace folder for 'Peregrine_Dataset_Export.xlsx'.")
