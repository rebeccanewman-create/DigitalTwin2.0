#-----------------------------------------------------------------------------
# Description: Extract laser scan vectors and save them as data + plots
#-----------------------------------------------------------------------------

import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# 1. Path to your actual Build 5 file
path_file = r'C:\Users\rpn\Downloads\2021-08-23 TCR Phase 1 Build 5.hdf5'
sample_layer = 100  # The layer scan path we want to extract

print(f"Opening HDF5 file to extract laser scan paths for Layer {sample_layer}...")

with h5py.File(path_file, 'r') as build:
    
    # Construct the internal path key for the requested layer
    scan_key = f'scans/{sample_layer}'
    
    if scan_key in build:
        # Load the raw 5-column scan vector array into memory
        scan_matrix = build[scan_key][:]
        
        # ---------------------------------------------------------------------
        # PART A: SAVE AS NUMERICAL CSV TEXT FILE
        # ---------------------------------------------------------------------
        csv_filename = f"layer_{sample_layer}_laser_vectors.csv"
        print(f"Saving raw vector coordinates to: {csv_filename}...")
        
        # Define readable headers matching the dataset specification
        headers = "X_Start,X_End,Y_Start,Y_End,Relative_Time_t"
        np.savetxt(csv_filename, scan_matrix, delimiter=",", header=headers, comments="")
        
        # ---------------------------------------------------------------------
        # PART B: GENERATE AND SAVE LASER VECTOR PLOT
        # ---------------------------------------------------------------------
        print("Generating 2D laser vector path plot...")
        
        # Split the matrix columns out based on the documentation specs
        x = scan_matrix[:, 0:2]  # Columns 0 and 1: Start/End X
        y = scan_matrix[:, 2:4]  # Columns 2 and 3: Start/End Y
        t = scan_matrix[:, 4]    # Column 4: Relative print timestamp
        
        # Setup a color mapping system to shade lines from early to late time
        colorizer = cm.ScalarMappable(norm=mcolors.Normalize(np.min(t), np.max(t)), cmap='jet')
        
        # Build a line collection bundle out of the coordinate pairs
        line_collection = collections.LineCollection(np.stack([x, y], axis=-1), colors=colorizer.to_rgba(t), linewidths=0.5)
        
        # Create the plot figure
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot()
        plt.axis('scaled')
        
        # Set bounds based on coordinates
        ax.set_xlim(x.min() - 5, x.max() + 5)
        ax.set_ylim(y.min() - 5, y.max() + 5)
        
        # Add vectors and labeling
        ax.add_collection(line_collection)
        plt.title(f"Laser Scan Vector Paths - Layer {sample_layer} (Colored by Timeline)")
        plt.xlabel("X Coordinate (mm)")
        plt.ylabel("Y Coordinate (mm)")
        
        plot_filename = f"layer_{sample_layer}_vector_plot.png"
        print(f"Saving visual plot to: {plot_filename}...")
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        plt.close()
        
    else:
        print(f"Error: Layer key '{scan_key}' was not found in this HDF5 build archive.")

print("\n🎉 Success! Check your workspace file explorer side panel.")