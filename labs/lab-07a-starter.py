from satpy.scene import Scene
from satpy.resample import get_area_def
from satpy import find_files_and_readers
from datetime import datetime
import glob
import warnings

# Check if files exist
fnames = glob.glob('/kaggle/input/meteosat-11-l1b-hrit-201802281500/H*201802281500-__')
print(f"Found {len(fnames)} files")
if fnames:
  print(f"First few files: {fnames[:3]}")
else:
  print("No files found! Check your path.")

# Create scene
scn = Scene(reader='seviri_l1b_hrit', filenames=fnames)

composite = 'natural_color'
print(f"Loading composite: {composite}")
scn.load([composite], upper_right_corner="NE")

print(f"Available datasets: {list(scn.keys())}")

# For Jupyter notebook, use:
scn.show(composite)

# OR save to file:
scn.save_dataset(composite, filename='output.png')
print("Image saved to output.png")
