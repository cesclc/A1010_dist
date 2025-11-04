# codeSample/ex7_solution04.py - Jupyter Notebook to show available attributes
from satpy import Scene
from satpy.demo import get_us_midlatitude_cyclone_abi
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np

# Download ABI demo data
print("Downloading ABI demo data...")
filenames = get_us_midlatitude_cyclone_abi()
print(f"Got {len(filenames)} ABI files")

# Open Band 2 (Red channel)
ds = xr.open_dataset(filenames[1])  # Usually Band 2

# Get radiance data
radiance = ds['Rad'].values

print(f"Radiance shape: {radiance.shape}")
print(f"Radiance range: {np.nanmin(radiance):.4f} to {np.nanmax(radiance):.4f}")

# Check what attributes are actually available
print("\nAvailable attributes:")
print(list(ds.attrs.keys())[:20])  # Show first 20 attributes

# Try different possible attribute names
band_id = ds.attrs.get('band_id') or ds.attrs.get('band_number') or 'Unknown'
time_start = ds.attrs.get('time_coverage_start') or ds.attrs.get('date_created') or 'Unknown time'

# Plot raw radiance
plt.figure(figsize=(12, 10))
plt.imshow(radiance, cmap='gray', vmin=0, vmax=np.nanpercentile(radiance, 99))
plt.colorbar(label='Radiance (W/m²/sr/µm)')
plt.title(f"Band {band_id} Raw Radiance\n{time_start}")
plt.axis('off')
plt.tight_layout()
plt.show()

ds.close()

# Or to see ALL attributes first:

# Open and explore attributes
ds = xr.open_dataset(filenames[1])

print("All global attributes:")
print("=" * 60)
for key, value in ds.attrs.items():
    print(f"{key}: {value}")

ds.close()
