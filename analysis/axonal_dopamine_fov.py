# Zahra
# visualize mean images of axonal-gcamp images

import os, numpy as np, tifffile, matplotlib.pyplot as plt

dy = 3
animal = 'e193'
src = r'X:\dopamine_imaging'

imgfld = os.path.join(src, animal, str(dy))
imgfl = [os.path.join(imgfld, xx) for xx in os.listdir(imgfld) if "ZD" in xx][0]
tifs = [os.path.join(imgfl, xx) for xx in os.listdir(imgfl) if "tif" in xx]
plane1 = [xx for xx in tifs if "plane01" in xx]
img_pln1 = tifffile.imread(plane1[0])
meanimg_pln1 = np.mean(img_pln1, axis=0)

plane1 = [xx for xx in tifs if "plane01" in xx]
img_pln1 = tifffile.imread(plane1[0])
meanimg_pln1 = np.mean(img_pln1, axis=0)

plane2 = [xx for xx in tifs if "plane02" in xx]
img_pln2 = tifffile.imread(plane2[0])
meanimg_pln2 = np.mean(img_pln2, axis=0)

plane3 = [xx for xx in tifs if "plane03" in xx]
img_pln3 = tifffile.imread(plane3[0])
meanimg_pln3 = np.mean(img_pln3, axis=0)

fig, axes = plt.subplots(1,3, figsize=(15,5))
ax = axes[0]
ax.imshow(meanimg, cmap="Greys_r")
ax.axis("off")
