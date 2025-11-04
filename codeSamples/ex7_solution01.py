# codeSample/ex7_solution01.py - Jupyter Notebook to show cloud and airmass
from satpy import Scene
from satpy.demo import get_us_midlatitude_cyclone_abi
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np

# Download ABI demo data
print("Downloading ABI demo data...")
filenames = get_us_midlatitude_cyclone_abi()
print(f"Got {len(filenames)} ABI files")

# Create scene
scn = Scene(reader='abi_l1b', filenames=filenames)
print(f"Available datasets : {list(scn.keys())}")

# Load both composites
print("Loading composites...")
scn.load(['true_color', 'airmass'])
print("Loading composites(2)...")
scn.load(['natural_color'])

# Resample to common area
print("Resampling...")
scn = scn.resample(resampler='native')
print(f"Available datasets after resampling: {list(scn.keys())}")

# Save both images
scn.save_dataset('true_color', filename='true_color_output.png')
scn.save_dataset('airmass', filename='airmass_output.png')
print("Images saved")

# Load images
img_true_color = Image.open('true_color_output.png')
img_airmass = Image.open('airmass_output.png')

# Add red border to airmass image
border_width = 20
img_airmass_bordered = Image.new('RGB',
    (img_airmass.width + 2*border_width, img_airmass.height + 2*border_width),
    color='red')
img_airmass_bordered.paste(img_airmass, (border_width, border_width))

# Display side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

ax1.imshow(img_true_color)
ax1.set_title('True Color Composite', fontsize=16, fontweight='bold')
ax1.axis('off')

ax2.imshow(img_airmass_bordered)
ax2.set_title('Airmass RGB Composite', fontsize=16, fontweight='bold', color='red')
ax2.axis('off')

plt.tight_layout()
plt.savefig('combined_display.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nAirmass RGB shows:")
print("- Red: Dry descending air (stratospheric intrusions)")
print("- Blue/Green: Moist tropical air masses")
print("- Boundaries between colors: Frontal zones")
