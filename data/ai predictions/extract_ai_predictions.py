#-----------------------------------------------------------------------------
# Description: Extract AI anomaly prediction masks and generate visual overlays
#-----------------------------------------------------------------------------

import h5py
import numpy as np
import matplotlib.pyplot as plt

# 1. Path to your actual Build 5 file
path_file = r'C:\Users\rpn\Downloads\2021-08-23 TCR Phase 1 Build 5.hdf5'
sample_layer = 100  # The layer we want to check for AI predictions

# Enumerate the class names exactly as specified in the Peregrine handbook
CLASS_NAMES = {
    0: "Powder (Normal)", 1: "Printed (Normal)", 2: "Recoater Hopping", 
    3: "Recoater Streaking", 4: "Incomplete Spreading", 5: "Swelling", 
    6: "Debris", 7: "Super-Elevation", 8: "Spatter", 
    9: "Misprint", 10: "Over Melting", 11: "Under Melting"
}

print(f"Opening HDF5 file to extract AI anomaly segmentations for Layer {sample_layer}...")

with h5py.File(path_file, 'r') as build:
    
    # Grab the underlying post-melt camera image to use as a background blueprint
    camera_dataset = build['slices/camera_data/visible/0']
    bg_image = camera_dataset[sample_layer, ...]
    
    # Setup a plot window to overlay our findings
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(bg_image, cmap='gray')
    
    anomalies_found = False
    
    # Loop through anomaly classes 2 to 11 (skipping 0 and 1 since they are 'normal' regions)
    for class_id in range(2, 12):
        segmentation_key = f'slices/segmentation_results/{class_id}'
        
        if segmentation_key in build:
            # Load the binary matrix for this specific anomaly class on this layer
            anomaly_mask = build[segmentation_key][sample_layer, ...]
            
            # If the AI detected this anomaly type on this layer (at least one pixel is True)
            if np.any(anomaly_mask):
                anomalies_found = True
                class_name = CLASS_NAMES.get(class_id, f"Class {class_id}")
                print(f" Detected anomaly class: [{class_id}] {class_name}")
                
                # Mask out the background (make False pixels transparent)
                masked_anomaly = np.ma.masked_where(anomaly_mask == 0, anomaly_mask)
                
                # Draw the AI highlighted anomaly area over the photograph
                # Using an alpha level to make the overlay semi-transparent
                ax.imshow(masked_anomaly, cmap='autumn', alpha=0.6, label=class_name)
                
    if not anomalies_found:
        print(" No severe print anomalies were flagged by the DSCNN model on this layer.")
        plt.text(50, 50, "AI Prediction: Layer Clean", color='green', fontsize=14, weight='bold')
    
    plt.title(f"AI DSCNN Anomaly Predictions Overlay - Layer {sample_layer}")
    plt.axis('off')
    
    # Save the visual mapping
    output_filename = f"layer_{sample_layer}_ai_predictions.png"
    print(f"Saving prediction overlay to: {output_filename}...")
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()

print("\n🎉 Success! Check your workspace file explorer side panel.")