import pandas as pd
import numpy as np
import requests
from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


def downloadFile(url, 
                 file, 
                 download_path):
    r = requests.get(url.format(file), 
                     allow_redirects=True)
    open(download_path.format(file), 'wb').write(r.content)

if __name__ == "__main__":
    url  = "https://apps.fs.usda.gov/fia/datamart/CSV/{}"

    files = ["CA_COND.csv",  "CA_COND_DWM_CALC.csv",  "CA_COUNTY.csv", 
            "CA_DWM_COARSE_WOODY_DEBRIS.csv",  "CA_DWM_DUFF_LITTER_FUEL.csv",  
            "CA_DWM_FINE_WOODY_DEBRIS.csv",  "CA_DWM_MICROPLOT_FUEL.csv",  
            "CA_DWM_RESIDUAL_PILE.csv",  "CA_DWM_TRANSECT_SEGMENT.csv",  
            "CA_DWM_VISIT.csv",  "CA_GRND_CVR.csv",  "CA_INVASIVE_SUBPLOT_SPP.csv",  
            "CA_LICHEN_LAB.csv",  "CA_LICHEN_PLOT_SUMMARY.csv", 
            "CA_LICHEN_VISIT.csv",  "CA_OZONE_BIOSITE_SUMMARY.csv",  
            "CA_OZONE_PLOT.csv",  "CA_OZONE_PLOT_SUMMARY.csv",  
            "CA_OZONE_SPECIES_SUMMARY.csv",  "CA_OZONE_VALIDATION.csv",  
            "CA_OZONE_VISIT.csv",  "CA_P2VEG_SUBPLOT_SPP.csv",  
            "CA_P2VEG_SUBP_STRUCTURE.csv",  "CA_PLOT.csv",  
            "CA_PLOTGEOM.csv",  "CA_PLOTSNAP.csv",  
            "CA_PLOT_REGEN.csv",  "CA_POP_ESTN_UNIT.csv",  "CA_POP_EVAL.csv",  
            "CA_POP_EVAL_ATTRIBUTE.csv",  "CA_POP_EVAL_GRP.csv",  
            "CA_POP_EVAL_TYP.csv",  "CA_POP_PLOT_STRATUM_ASSGN.csv",  
            "CA_POP_STRATUM.csv",  "CA_SEEDLING.csv",  "CA_SEEDLING_REGEN.csv", 
            "CA_SITETREE.csv",  "CA_SOILS_EROSION.csv",  "CA_SOILS_LAB.csv",  
            "CA_SOILS_SAMPLE_LOC.csv",  "CA_SOILS_VISIT.csv",  "CA_SUBPLOT.csv", 
            "CA_SUBPLOT_REGEN.csv",  "CA_SUBP_COND.csv",  "CA_SUBP_COND_CHNG_MTRX.csv",  
            "CA_SURVEY.csv",  "CA_TREE.csv",  "CA_TREE_GRM_BEGIN.csv",  
            "CA_TREE_GRM_COMPONENT.csv",  "CA_TREE_GRM_ESTN.csv",  
            "CA_TREE_GRM_MIDPT.csv",  "CA_TREE_GRM_THRESHOLD.csv",  
            "CA_TREE_REGIONAL_BIOMASS.csv",  "CA_TREE_WOODLAND_STEMS.csv",  
            "CA_VEG_PLOT_SPECIES.csv",  "CA_VEG_QUADRAT.csv",  
            "CA_VEG_SUBPLOT.csv",  "CA_VEG_SUBPLOT_SPP.csv",  "CA_VEG_VISIT.csv",]

    workingDir = "/Users/shnkreddy/SJSU/sem4/298B/"
    download_path = workingDir+"data/california/{}"
    for file in tqdm(files):
        print(f'Downloading {file.split(".")[0]}', end = '\r')
        downloadFile(url, 
                     file, 
                     download_path)