import numpy as np, pandas as pd
import requests
from io import BytesIO
from bs4 import BeautifulSoup as soup
from functools import reduce

dfs = reduce((lambda lst,page:lst+[pd.read_csv(BytesIO(requests.get("http://keplerebs.villanova.edu"+i["href"]).content), delimiter="\t") for i in soup(requests.get(page).content).find_all("a") if i.text == "data"]),map("http://keplerebs.villanova.edu/?page={}".format, range(1, 60)),[])
