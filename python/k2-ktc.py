import pandas as pd
import np

df = pd.read_csv("../data/k2_ktc_epic.csv", low_memory=False)
print(df)

ids = np.unique(df.ktc_k2_id.to_numpy())
print(ids)

with open("../data/k2_ids.txt", "w+") as ids_file:
    np.savetxt(ids_file, ids, fmt='%i')

"""
       ktc_investigation_id  ktc_k2_id  ... sci_dct_purp  k2_hlsp
0                       NaN  200000811  ...          NaN      NaN
1                       NaN  200000812  ...          NaN      NaN
2                       NaN  200000813  ...          NaN      NaN
3                       NaN  200000814  ...          NaN      NaN
4                       NaN  200000815  ...          NaN      NaN
                     ...        ...  ...          ...      ...
665732              GO19059  251816807  ...          NaN      8.0
665733              GO19063  251816808  ...          NaN      8.0
665734              GO19903  251816809  ...          NaN      8.0
665735              GO19903  251816810  ...          NaN      8.0
665736              GO19903  251816811  ...          NaN      8.0
[665737 rows x 72 columns]
[200000811 200000812 200000813 ... 251816809 251816810 251816811]
"""
