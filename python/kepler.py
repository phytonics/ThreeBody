import lightkurve as lk

def getIds():
    """
    :returns: A list containing all the certified Kepler Ids.
    """
    ids_file = open("../data/kepler_ids.txt")
    ids = list(map(int, ids_file.readlines()))
    ids_file.close()
    return ids

def retrieveKeplerCollection(kplrId):
    """
    :param kplrId: The Kepler Id, as an Integer, String or Float
    :returns: A Tuple containing the kplrId as an Integer and a LightCurve object
    """
    kplrId = int(kplrId)
    search_result = lk.search_lightcurve(f'KIC {kplrId}', mission='Kepler')
    klc = search_result.download_all().stitch()
    return kplrId, klc

def getId(index=0):
    return getIds()[index]

def retrieveLightCurve(index=0):
    return retrieveKeplerCollection(getIds()[index])

def plotLightCurve(kplrId, klc):
    ax = klc.plot(column='pdcsap_flux', label='PDCSAP Flux', normalize=True)
    klc.plot(column='sap_flux', label='SAP Flux', normalize=True, ax=ax)
    klc.plot(ax=ax, label="Actual Data")
    ax.set_title(f"Light curve of {kplrId}")
    # ax.figure.savefig(f'..plots/{kplrId}.png')

