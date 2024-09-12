import os
import h5py
import numpy as np
import geopandas as gpd
from downloadGEDI import Download
from ETL import ETL
from custom_logging import CustomLogging
from datetime import datetime

USBOUNDARY = gpd.GeoDataFrame.from_file("../boundaries/US.geojson")  # Import geojson as GeoDataFrame
INDIR = os.getcwd()
DATADIR = INDIR + "/data/sat/gedil2b"
AVGTIME = np.array()

downloadlinks = "earthdata_files/19-20-l2b.txt"

with open(downloadlinks, "r") as f:
    links = f.read()

clean_links = []
for link in links.split("\n"):
    clean_links.append(link)

print(f"[INFO] Starting with the {downloadlinks} file")
for i, link in enumerate(clean_links):
    starttime=datetime.now()
    filename = Download.gediFile(DATADIR, link, i)
    gediL2A_h5 = h5py.File(filename, 'r')
    beamNames = [g for g in gediL2A_h5.keys() if g.startswith('BEAM')]
    gediL2A_objs = []
    gediL2A_h5.visit(gediL2A_objs.append)

    # Retrieve list of datasets
    gediSDS = [o for o in gediL2A_objs if isinstance(gediL2A_h5[o], h5py.Dataset)] # search for relevant SDS inside data file

    df = ETL.extractDataFrame(beamNames, gediL2A_h5, gediL2AFlag=0)
    os.remove(filename)
    df = ETL.cleanDataFrame(df, USBOUNDARY, gediL2AFlag=0)

    print(f"[INFO] Saving DataFrame file")
    CustomLogging.logOutput(f"[INFO] Saved DataFrame file {i}")
    df.to_csv(DATADIR+f"/csv/GEDIL2B_{i}.csv", index=False)
    endtime = datetime.now()
    print(f"[INFO] Time taken: {endtime-starttime} seconds")
    AVGTIME = np.append(AVGTIME, endtime-starttime)
    print(f"[INFO] Time Remaining: {AVGTIME.mean()*len(clean_links)}")
