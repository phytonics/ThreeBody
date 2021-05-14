from astropy.io import fits
import pandas as pd
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style

plt.style.use(astropy_mpl_style)

data = fits.open('../data/kplr000757099/kplr000757099.fits')
data.info()

tce1Columns = [
    "timeId",
    "time",
    "timecorr",
    "cadenceno",
    "phase",
    "lc_init",
    "lc_init_err",
    "lc_white",
    "lc_detrend",
    "model_init",
    "model_white"
]


statsColumns = [
    "timeId",
    "time",
    "timecorr",
    "cadenceno",
    "pdcsap_flux",
    "pdcsap_flux_err",
    "residual_lc",
    "deweights",
    "quality",
    "ses_corr_1_5",
    "ses_corr_2_0",
    "ses_corr_2_5",
    "ses_corr_3_0",
    "ses_corr_3_5",
    "ses_corr_4_5",
    "ses_corr_5_0",
    "ses_corr_6_0",
    "ses_corr_7_5",
    "ses_corr_9_0",
    "ses_corr_10_5",
    "ses_corr_12_0",
    "ses_corr_12_5",
    "ses_corr_15_0",
    "ses_norm_1_5",
    "ses_norm_2_0",
    "ses_norm_2_5",
    "ses_norm_3_0",
    "ses_norm_3_5",
    "ses_norm_4_5",
    "ses_norm_5_0",
    "ses_norm_6_0",
    "ses_norm_7_5",
    "ses_norm_9_0",
    "ses_norm_10_5",
    "ses_norm_12_0",
    "ses_norm_12_5",
    "ses_norm_15_0",
    "cdpp_1_5",
    "cdpp_2_0",
    "cdpp_2_5",
    "cdpp_3_0",
    "cdpp_3_5",
    "cdpp_4_5",
    "cdpp_5_0",
    "cdpp_6_0",
    "cdpp_7_5",
    "cdpp_9_0",
    "cdpp_10_5",
    "cdpp_12_0",
    "cdpp_12_5",
    "cdpp_15_0"
]

tce1 = pd.DataFrame(data[1].data)
stats = pd.DataFrame(data[2].data)

kplr000757099 = pd.merge(tce1, stats, on="TIME", how="outer")

kplr000757099.to_csv("../data/kplr000757099/kplr000757099.csv")
print("saved data")

data.close()
