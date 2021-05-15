import pandas as pd
import np

df = pd.read_csv("../data/kepler_ktc_kic.csv", low_memory=False)
print(df)

ids = np.unique(df.ktc_kepler_id.to_numpy())
print(ids)

with open("../data/kepler_ids.txt", "w+") as ids_file:
    np.savetxt(ids_file, ids, fmt='%i')

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
[   757076    757099    757137 ... 100004298 100004299 100004300]
"""
