import h5py
import numpy as np
from skimage import measure

# 1. Path to your actual Build 5 file
path_file = r'C:\Users\rpn\Downloads\2021-08-23 TCR Phase 1 Build 5.hdf5'

print("Opening HDF5 file in streaming mode...")

with h5py.File(path_file, 'r') as build:
    # Access the dataset pointer WITHOUT loading it into memory (no [:] at the end)
    part_dataset = build['slices/part_ids']
    total_layers, height, width = part_dataset.shape
    
    print(f"Dataset has {total_layers} layers ({height}x{width} pixels each).")
    print("Scanning layers to identify unique Part IDs (this saves RAM)...")
    
    # Track which unique Part IDs exist by sampling layers cleanly
    unique_parts = set()
    # Step through every 50th layer just to grab the ID tags present in the build
    for layer_idx in range(0, total_layers, 50):
        layer_data = part_dataset[layer_idx, :, :]
        unique_parts.update(np.unique(layer_data))
    
    # Remove 0 (empty background space)
    if 0 in unique_parts:
        unique_parts.remove(0)
        
    print(f"Found active 3D Model IDs: {list(unique_parts)}")
    
    # Process each identified part one by one
    for part_id in unique_parts:
        print(f"\nProcessing Part ID: {part_id}...")
        
        # Stream layers one-by-one to build a minimal bounding box array for just this part
        layer_tracker = []
        for layer_idx in range(total_layers):
            # Read just ONE 2D layer slice into memory at a time
            layer_mask = (part_dataset[layer_idx, :, :] == part_id)
            layer_tracker.append(layer_mask)
            
        # Convert list of 2D slices into a compact boolean 3D array (takes very little RAM)
        binary_mask = np.stack(layer_tracker, axis=0)
        del layer_tracker # Immediately clear memory list
        
        if not np.any(binary_mask):
            print(f"Part {part_id} is empty in this slice block. Skipping.")
            continue
            
        print(f"Generating 3D mesh surface for Part {part_id}...")
        # Marching cubes to generate the skin around pixels
        verts, faces, normals, values = measure.marching_cubes(binary_mask, level=0.5)
        
        obj_filename = f"Peregrine_Part_{part_id}.obj"
        print(f"Saving mesh to file Explorer: {obj_filename}...")
        
        # Write to OBJ file
        with open(obj_filename, 'w') as f:
            f.write(f"# Peregrine Dataset Extracted 3D Mesh - Part {part_id}\n")
            for v in verts:
                f.write(f"v {v[2]} {v[1]} {v[0]}\n") # Coordinate re-mapping for standard CAD viewers
            for face in faces:
                f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
                
        print(f"Finished saving Part {part_id}!")

print("\n🎉 Success! All available 3D models extracted without crashing your RAM.")