from astropy.io import fits
import pandas as pd
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style

plt.style.use(astropy_mpl_style)

data = fits.open('../../data/kplr000757099/kplr000757099.fits')
data.info()

df = pd.DataFrame(data[2].data)

data.close()