import lightkurve as lk

def retrieveCollection(kplrId):
    search_result = lk.search_lightcurve(f'KIC {kplrId}', mission='Kepler')
    # Download and stitch the data together
    klc = search_result.download_all().stitch()
    ax = klc.plot(column='pdcsap_flux', label='PDCSAP Flux', normalize=True)
    klc.plot(column='sap_flux', label='SAP Flux', normalize=True, ax=ax)
    klc.plot(ax=ax, label="Actual Data")
    ax.set_title(f"Light curve of {kplrId}")
    ax.figure.savefig(f'..plots/{kplrId}.png')
    return lc


lcs = []

with open("../data/kepler_ids.txt") as ids_file:
    lc = retrieveCollection(int(float(ids_file.readline())))
    lcs.append(lcs)