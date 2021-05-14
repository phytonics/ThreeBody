#%%

import pandas as pd
import matplotlib.pyplot as plt
import np
import scipy as sp

#%%

df = pd.read_csv("data/kepler_ktc_kic.csv")
print(df)

#%%

for i in df.columns:
    print(i)

#%%

df.summary()

"""
        ktc_investigation_id  ktc_kepler_id  ... sci_output  sci_dct_purp
0                         EX         757076  ...          4           NaN
1                         EX         757076  ...          4           NaN
2                         EX         757076  ...          4           NaN
3                         EX         757076  ...          4           NaN
4                         EX         757076  ...          4           NaN
...                      ...            ...  ...        ...           ...
2895752              GO40015      100004297  ...          2           NaN
2895753              GO40015      100004297  ...          2           NaN
2895754              GO40004      100004298  ...          1           NaN
2895755              GO40038      100004299  ...          1           NaN
2895756              GO40038      100004300  ...          1           NaN

[2895757 rows x 75 columns]
ktc_investigation_id
ktc_kepler_id
ktc_target_type
ktc_obsv_start_mjd
ktc_obsv_stop_mjd
ktc_obsv_start_time
ktc_obsv_stop_time
ktc_act_obsv_start_mjd
ktc_act_obsv_stop_mjd
ktc_act_obsv_start_time
ktc_act_obsv_stop_time
sci_ra
sci_dec
kic_pmra
kic_pmdec
kic_umag
kic_gmag
kic_rmag
kic_imag
kic_zmag
kic_gredmag
kic_d51mag
twoMass_jmag
twoMass_hmag
twoMass_kmag
kic_kepmag
twoMass_tmid
kic_scpid
kic_altid
kic_altsource
kic_galaxy
kic_blend
kic_variable
kic_teff
kic_logg
kic_feh
kic_ebminusv
kic_av
kic_radius
kic_cq
kic_pq
kic_aq
kic_catkey
kic_scpkey
kic_parallax
kic_glon
kic_glat
kic_pmtotal
kic_grcolor
twoMass_jkcolor
twoMass_gkcolor
twoMass_2mass_id
sci_archive_class
sci_data_set_name
refnum
sci_pep_id
sci_start_time
sci_end_time
sci_release_date
sci_generation_date
sci_data_quarter
condition_flag
sci_data_rel
twoMass_conflictFlag
sci_crowdsap
sci_flfrcsap
sci_Cdpp3_0
sci_Cdpp6_0
sci_Cdpp12_0
sci_contamination
sci_skygroup_id
sci_module
sci_channel
sci_output
sci_dct_purp
"""
