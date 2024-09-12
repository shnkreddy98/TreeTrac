import os
import h5py
import numpy as np
import geopandas as gpd
from downloadGEDI import Download
from ETL import ETL
from custom_logging import CustomLogging
from datetime import datetime
import argparse

USBOUNDARY = gpd.GeoDataFrame.from_file("boundaries/US.geojson")  # Import geojson as GeoDataFrame
INDIR = os.getcwd() + os.sep
AVGTIME = []

def parse_arguments():
    parser = argparse.ArgumentParser(description='Collect GEDI data for the level mentioned in the arguments and Earthdata list.')
    parser.add_argument('--dataDir', help='path to directory to store the data')
    parser.add_argument('--links', help='path to the directory containing links list')
    parser.add_argument('--resume', help='link no. to start from')


    return parser.parse_args()

def main(gediL2AFlag, idx):
    global AVGTIME
    with open(DOWNLOADLINKS, "r") as f:
        links = f.read()

    clean_links = []
    for link in links.split("\n"):
        clean_links.append(link)

    CustomLogging.logOutput(f"[INFO] Starting with the {DOWNLOADLINKS} file", gediL2AFlag)
    try:
        for i in range(int(idx), len(clean_links)):
            link = clean_links[i]
            starttime=datetime.now()
            filename = Download.gediFile(DATADIR, link, i, gediL2AFlag)
            gediL2A_h5 = h5py.File(filename, 'r')
            beamNames = [g for g in gediL2A_h5.keys() if g.startswith('BEAM')]
            gediL2A_objs = []
            gediL2A_h5.visit(gediL2A_objs.append)

            df = ETL.extractDataFrame(beamNames, gediL2A_h5, USBOUNDARY, gediL2AFlag)
            os.remove(filename)

            CustomLogging.logOutput(f"[INFO] Saved DataFrame file {i}", gediL2AFlag)
            endtime = datetime.now()
            if df.shape[0] != 0:
                df.to_csv(DATADIR+f"/csv/GEDIL2A_{i}.csv", index=False)
                CustomLogging.logOutput(f"[INFO] Time taken: {endtime-starttime} seconds", gediL2AFlag)
            AVGTIME = np.append(AVGTIME, endtime-starttime)
            CustomLogging.logOutput(f"[INFO] Time Remaining: {AVGTIME.mean()*len(clean_links[i:])}", gediL2AFlag)
            if gediL2AFlag:
                with open("resumel2a.txt", "w+") as f:
                    f.write(str(i))
            else:
                with open("resumel2b.txt", "w+") as f:
                    f.write(str(i))
    
    except Exception as e:
        if gediL2AFlag:
            CustomLogging.logOutput(f"[ERR] {e}", gediL2AFlag)
        else:
            CustomLogging.logOutput(f"[ERR] {e}", gediL2AFlag)



if __name__=="__main__":
    parsed_args = parse_arguments()
    DATADIR = INDIR + parsed_args.dataDir
    DOWNLOADLINKS = parsed_args.links
    resume_idx = parsed_args.resume
    if parsed_args.dataDir.endswith("l2a"):
        gediL2AFlag = 1
    else:
        gediL2AFlag = 0
    main(gediL2AFlag, resume_idx)

