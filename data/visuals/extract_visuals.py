#-----------------------------------------------------------------------------
# Description: Extract layer images and the build text log from Peregrine HDF5
#-----------------------------------------------------------------------------

import h5py
import matplotlib.pyplot as plt

# 1. Path to your actual Build 5 file
path_file = r'C:\Users\rpn\Downloads\2021-08-23 TCR Phase 1 Build 5.hdf5'

print("Opening HDF5 file to extract images and text logs...")

with h5py.File(path_file, 'r') as build:
    
    # -------------------------------------------------------------------------
    # PART A: EXTRACT THE PRINTER TEXT LOG
    # -------------------------------------------------------------------------
    print("\nReading printer log file...")
    # Read the text block from metadata attributes 
    if 'log_file/' in build.attrs:
        log_text = build.attrs['log_file/'] [cite: 45]
        
        # Write it out as a normal text document in your folder
        log_filename = "printer_build_log.txt"
        with open(log_filename, "w", encoding="utf-8") as text_file:
            text_file.write(str(log_text))
        print(f" Successfully saved: {log_filename}")
    else:
        print(" No log_file text found in global attributes.")

    # -------------------------------------------------------------------------
    # PART B: EXTRACT VISUAL LAYER IMAGES
    # -------------------------------------------------------------------------
    print("\nExtracting camera images...")
    
    # Grab pointers to the layer camera sets [cite: 70, 71]
    # post_melt: camera images taken right after laser melting [cite: 70]
    # post_powder: camera images taken right after fresh powder spreading 
    # Fix Line 39 & 40 by making sure they look exactly like this:
    post_melt_dataset = build['slices/camera_data/visible/0']
    post_powder_dataset = build['slices/camera_data/visible/1']
    
    # Let's extract a sample layer midway through the build
    sample_layer = 100 
    
    print(f"Extracting Layer {sample_layer} visual images...")
    
    # Read the individual 2D arrays into memory [cite: 61]
    img_melt = post_melt_dataset[sample_layer, ...]
    # Ensure lines 49 and 50 look exactly like this with NO extra brackets:
    img_melt = post_melt_dataset[sample_layer, ...]
    img_powder = post_powder_dataset[sample_layer, ...]
    
    # Save the matrices directly to high-quality PNG image files
    melt_filename = f"layer_{sample_layer}_post_melt.png"
    powder_filename = f"layer_{sample_layer}_post_powder.png"
    
    # Save using a grayscale colormap (or use 'jet' if you want a heat map style)
    plt.imsave(melt_filename, img_melt, cmap='gray')
    plt.imsave(powder_filename, img_powder, cmap='gray')
    
    print(f" Successfully saved: {melt_filename}")
    print(f" Successfully saved: {powder_filename}")

print("\n🎉 Done! Check your file explorer panel for your text and image files.")