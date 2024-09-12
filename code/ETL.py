import pandas as pd
import numpy as np
import geopandas as gpd
from custom_logging import CustomLogging

class ETL():

    def extractDataFrame(beamNames, gediL2A, USBOUNDARY, gediL2AFlag):
        CustomLogging.logOutput(f"[INFO] Extracting data...", gediL2AFlag)
        latslons_df = pd.DataFrame()
        for beam in beamNames:
            lonSample, latSample, shotSample, qualitySample, elevSample = [], [], [], [], []  # Set up lists to store data
            modis_nonvegetatedSample, modis_treecoverSample, dateSample = [], [], []
            if gediL2AFlag:
                rhSample, pft_classSample = [], []
            else:
                coverSample, paiSample = [], []

            # Open the SDS
            shots = gediL2A[f'{beam}/shot_number'][()]
            modis_nonvegetated = gediL2A[f'{beam}/land_cover_data/modis_treecover'][()]
            modis_treecover = gediL2A[f'{beam}/land_cover_data/modis_treecover'][()]
            date = gediL2A['METADATA']['DatasetIdentification'].attrs['creationDate']

            if gediL2AFlag:
                lons = gediL2A[f'{beam}/lon_lowestmode'][()]
                lats = gediL2A[f'{beam}/lat_lowestmode'][()]
                elev = gediL2A[f'{beam}/elev_lowestmode'][()]
                quality = gediL2A[f'{beam}/quality_flag'][()]
                pft_class = gediL2A[f'{beam}/land_cover_data/pft_class'][()]
                rh = gediL2A[f'{beam}/rh'][()]

            else:
                lons = gediL2A[f'{beam}/geolocation/lon_lowestmode'][()]
                lats = gediL2A[f'{beam}/geolocation/lat_lowestmode'][()]
                elev = gediL2A[f'{beam}/geolocation/elev_lowestmode'][()]
                quality = gediL2A[f'{beam}/l2b_quality_flag'][()]
                cover = gediL2A[f'{beam}/pai'][()]
                pai = gediL2A[f'{beam}/cover'][()]

            for i in range(len(shots)):
                shotSample.append(str(shots[i]))
                lonSample.append(lons[i])
                latSample.append(lats[i])
                qualitySample.append(quality[i])
                elevSample.append(elev[i])
                modis_nonvegetatedSample.append(modis_nonvegetated[i])
                modis_treecoverSample.append(modis_treecover[i])
                dateSample.append(date)
                if gediL2AFlag:
                    rhSample.append(rh[i][100])
                    pft_classSample.append(pft_class[i])
                else:
                    coverSample.append(cover[i])
                    paiSample.append(pai[i])
                        
            if gediL2AFlag:
                # Write all of the sample shots to a dataframe
                latslons = pd.DataFrame({'Beam': beam, 'ShotNumber': shotSample, 
                                         'Longitude': lonSample, 'Latitude': latSample,
                                         'QualityFlag': qualitySample, 'rh': rhSample,
                                         'Elevation': elevSample, 'NonVegetated': modis_nonvegetatedSample,
                                         'TreeCover': modis_treecoverSample, 'PFTClass': pft_classSample,
                                         'Date': dateSample})
            else:
                latslons = pd.DataFrame({'Beam': beam, 'ShotNumber': shotSample, 
                                         'Longitude': lonSample, 'Latitude': latSample,
                                         'QualityFlag': qualitySample, 'cover': coverSample, 
                                         'pai': paiSample, 'Elevation': elevSample, 
                                         'NonVegetated': modis_nonvegetatedSample,
                                         'TreeCover': modis_treecoverSample, 'Date': dateSample})


            latslons_df = pd.concat([latslons_df, latslons], ignore_index=True)
        latslons_df.dropna(inplace=True)

        if gediL2AFlag:
            latslons_df[["NonVegetated", "TreeCover"]] = latslons_df[["NonVegetated", "TreeCover"]].replace(-9999, np.nan)
        else:
            latslons_df[["NonVegetated", "TreeCover", "cover", "pai"]] = latslons_df[["NonVegetated", "TreeCover", 
                                                                                      "cover", "pai"]].replace(-9999, np.nan)
                
        # Take the lat/lon dataframe and convert each lat/lon to a shapely point
        latslons_df['geometry'] = gpd.points_from_xy(latslons_df.Longitude, latslons_df.Latitude)
        # Convert to a Geodataframe
        gdf = gpd.GeoDataFrame(latslons_df, geometry='geometry', crs=4326)

        joined_gdf = gpd.sjoin(gdf,USBOUNDARY,how='inner',predicate='within')
        CustomLogging.logOutput(f"After clean: {joined_gdf.shape}", gediL2AFlag)

        df = pd.DataFrame(joined_gdf.drop('geometry', axis=1))
        return df
