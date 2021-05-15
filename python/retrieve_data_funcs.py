import lightkurve as lk

def getIds():
    ids_file = open("../data/kepler_ids.txt")
    ids = list(map(int, ids_file.readlines()))
    ids_file.close()
    return ids

def retrieveCollection(kplrId):
    search_result = lk.search_lightcurve(f'KIC {kplrId}', mission='Kepler')
    # Download and stitch the data together
    klc = search_result.download_all().stitch()
    ax = klc.plot(column='pdcsap_flux', label='PDCSAP Flux', normalize=True)
    klc.plot(column='sap_flux', label='SAP Flux', normalize=True, ax=ax)
    klc.plot(ax=ax, label="Actual Data")
    ax.set_title(f"Light curve of {kplrId}")
    ax.figure.savefig(f'..plots/{kplrId}.png')
    return klc

def getId(index=0):
    return getIds()[index]

def retrieveLightCurve(index=0):
    return retrieveCollection(getIds()[index])

