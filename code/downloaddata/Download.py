import os
import h5py
import numpy as np
import geopandas as gpd
from datetime import datetime
from code.download_data.download_gedi import DownloadGEDI
from code.download_data.ETL import ETL
from code.download_data.custom_logging import CustomLogging

def process_links_in_batches(links, batch_size=10):
    for i in range(0, len(links), batch_size):
        yield links[i:i + batch_size]

def download(BASE_DIR, RAW_DIR):
    resume_idx = f"{BASE_DIR}/txtfiles/resume.txt"
    if not os.path.exists(resume_idx):
        print(f"[INFO] Starting download for the first time")
        resume = 0
        with open(resume_idx, 'w') as file:
            file.write(str(resume))
        
    else:
        with open(resume_idx, 'r') as file:
            resume = int(file.read())
        print(f"[INFO] Resuming download at \
                link_no: {resume}")

    BOUNDARYFILE = f"{BASE_DIR}/txtfiles/boundaries/US.geojson"
    USBOUNDARY = gpd.GeoDataFrame.from_file(BOUNDARYFILE)
    
    DOWNLOADLINKS = f"{BASE_DIR}/txtfiles/earthdata_files/19-20-l2a.txt"

    batch_size = 10

    CustomLogging.logOutput(f"[INFO] Starting with the {DOWNLOADLINKS} file", gediL2AFlag=1)

    with open(DOWNLOADLINKS) as f:
        links = [line.rstrip('\n') for line in f]

    if resume>0:
        links = links[resume:]
    
    for batch_no, batch in enumerate(process_links_in_batches(links, batch_size)):
        print(f"[INFO] Processing batch:{batch_no} of {len(links)//batch_size}")
        for link in batch:
            if link.split("/")[4].startswith("GEDI02_A"):
                print(f"[INFO] Processing GEDIL2A link \n", end='\r')
                gediL2AFlag = 1
            else:
                print(f"[INFO] Processing GEDIL2B link \n", end='\r')
                gediL2AFlag = 0

            try:
                starttime=datetime.now()
                filename = DownloadGEDI.gediFile(BASE_DIR, RAW_DIR, link, resume, gediL2AFlag)
                gediL2A_h5 = h5py.File(filename, 'r')
                beamNames = [g for g in gediL2A_h5.keys() if g.startswith('BEAM')]
                gediL2A_objs = []
                gediL2A_h5.visit(gediL2A_objs.append)

                df = ETL.extractDataFrame(beamNames, gediL2A_h5, USBOUNDARY, gediL2AFlag)
                os.remove(filename)

                CustomLogging.logOutput(f"[INFO] Saved DataFrame file {resume}", gediL2AFlag)
                endtime = datetime.now()
                if df.shape[0] != 0:
                    if not os.path.exists(RAW_DIR+"csv"):
                        os.mkdir(RAW_DIR+"csv")
                    df.to_csv(f"{RAW_DIR}csv/GEDIL2A_{resume}.csv", index=False)
                    CustomLogging.logOutput(f"{RAW_DIR}csv/GEDIL2A_{resume}.csv", gediL2AFlag)
                    CustomLogging.logOutput(f"[INFO] Time taken: {endtime-starttime} seconds", gediL2AFlag)

                resume += 1
                
                with open(resume_idx, "w+") as f:
                    f.write(str(resume))
            
            except Exception as e:
                if gediL2AFlag:
                    CustomLogging.logOutput(f"[ERR] {e}", gediL2AFlag)
                else:
                    CustomLogging.logOutput(f"[ERR] {e}", gediL2AFlag)


