from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style

plt.style.use(astropy_mpl_style)

data = fits.open('../../data/kplr000757099.fits')
data.info()

data[1].dump("../../data/kplr000757099_tce1.txt")
data[2].dump("../../data/kplr000757099_stats.txt")

print("saved data")

data.close()