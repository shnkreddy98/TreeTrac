import os
import h5py
import numpy as np
import geopandas as gpd
from downloadGEDI import Download
from ETL import ETL
from custom_logging import CustomLogging
from datetime import datetime
import sys

gedil2a = sys.argv[1]
linksfile = sys.argv[2]

USBOUNDARY = gpd.GeoDataFrame.from_file("boundaries/US.geojson")  # Import geojson as GeoDataFrame
INDIR = os.getcwd()
DATADIR = INDIR + f"/data/sat/{gedil2a}"
AVGTIME = []
DOWNLOADLINKS = f"earthdata_files/{linksfile}"

if __name__=="__main__":
    with open(DOWNLOADLINKS, "r") as f:
        links = f.read()

    clean_links = []
    for link in links.split("\n"):
        clean_links.append(link)

    print(f"[INFO] Starting with the {DOWNLOADLINKS} file")
    for i, link in enumerate(clean_links):
        starttime=datetime.now()
        filename = Download.gediFile(DATADIR, link, i)
        gediL2A_h5 = h5py.File(filename, 'r')
        beamNames = [g for g in gediL2A_h5.keys() if g.startswith('BEAM')]
        gediL2A_objs = []
        gediL2A_h5.visit(gediL2A_objs.append)

        # Retrieve list of datasets
        gediSDS = [o for o in gediL2A_objs if isinstance(gediL2A_h5[o], h5py.Dataset)] # search for relevant SDS inside data file

        df = ETL.extractDataFrame(beamNames, gediL2A_h5, USBOUNDARY, gediL2AFlag=1)
        os.remove(filename)

        print(f"[INFO] Saving DataFrame file")
        CustomLogging.logOutput(f"[INFO] Saved DataFrame file {i}")
        if df.shape[0] != 0:
            df.to_csv(DATADIR+f"/csv/GEDIL2A_{i}.csv", index=False)
            print(f"[INFO] Time taken: {endtime-starttime} seconds")
        endtime = datetime.now()
        AVGTIME = np.append(AVGTIME, endtime-starttime)
        print(f"[INFO] Time Remaining: {AVGTIME.mean()*len(clean_links)}")
