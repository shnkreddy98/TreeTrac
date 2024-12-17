import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
from shapely.geometry import Point, box
from matplotlib import colors
import numpy as np
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
import webbrowser

part1csv = "../Dataset/fia-part-1.csv"
part2csv = "../Dataset/fia-part-2.csv"
mergecsv = "../Dataset/fia-merged.csv"

def get_data(date):
    if int(date.split("-")[0])==2019:
        df = load_data(part1csv)
    else:
        df = load_data(part2csv)
    return df

def get_merge_data():
    df = load_data(mergecsv)
    return df

@st.cache_data  # 👈 Add the caching decorator
def load_data(filename):
    df = pd.read_csv(filename)
    return df

def normalize_array(values):
    max_value = max(values)
    min_value = min(values)
    normalized_values = [0.2 + (0.8 - 0.2) * ((v - min_value) / (max_value - min_value)) for v in values]
    return normalized_values

def draw_two(col1, col2, dataset_option, current_data, lat, lon):
    # Display plots in columns
    with col1:
        st.subheader(f"{dataset_option} Ground Truth")
        fig_left = create_map(current_data['sat'], f"{dataset_option} Values", lat, lon)
        st.pyplot(fig_left)
                
    with col2:
        st.subheader(f"{dataset_option} Satellite Data")
        fig_right = create_map(current_data['ground'], f"{dataset_option} Values", lat, lon)
        st.pyplot(fig_right)

# Define function to create interactive graph
def create_interactive_graph(df_agg, title, y_axes, var, color = 1, date='Date'):
    if color:
        colors = {'Predicted': 'blue', 'Actual': 'green'}
        line_colors = [colors.get(col, None) for col in y_axes]

        fig = px.line(
            df_agg,
            x=date,
            y=y_axes,
            labels={'value': f'{var}', 'variable': 'Source'},
            title=title,
            color_discrete_sequence=line_colors
        )
    else:
        fig = px.line(
            df_agg,
            x=date,
            y=y_axes,
            labels={'value': f'{var}', 'variable': 'Source'},
            title=title
        )
    fig.update_layout(
        xaxis_title=date,
        yaxis_title=f'{var}',
        legend_title='Source',
        template='plotly_white'
    )
    # Apply individual opacities
    if color:
        opacities = {'Predicted': 0.25, 'Actual': 1}
        for trace in fig.data:
            col_name = trace.name
            if col_name in opacities:
                trace.opacity = opacities[col_name]

    return fig

def analysis(data, dataset_option):
    heightsat_arr = [float(data.HeightSat1.values[0]), float(data.HeightSat2.values[0]), float(data.HeightSat3.values[0]), float(data.HeightSat4.values[0])]
    treecoversat_arr = [float(data.TreeCoverSat1.values[0]), float(data.TreeCoverSat2.values[0]), float(data.TreeCoverSat3.values[0]), float(data.TreeCoverSat4.values[0])]
    diametersat_arr = [float(data.DiameterSat1.values[0]), float(data.DiameterSat2.values[0]), float(data.DiameterSat3.values[0]), float(data.DiameterSat4.values[0])]
    ndvisat_arr = [float(data.NDVISat1.values[0]), float(data.NDVISat2.values[0]), float(data.NDVISat3.values[0]), float(data.NDVISat4.values[0])]
    carbonsat_arr = [float(data.CarbonSat1.values[0]), float(data.CarbonSat2.values[0]), float(data.CarbonSat3.values[0]), float(data.CarbonSat4.values[0])]

    heightground_arr = [float(data.HeightGround1.values[0]), float(data.HeightGround2.values[0]), float(data.HeightGround3.values[0]), float(data.HeightGround4.values[0])]
    treecoverground_arr = [float(data.TreeCoverGround1.values[0]), float(data.TreeCoverGround2.values[0]), float(data.TreeCoverGround3.values[0]), float(data.TreeCoverGround4.values[0])]
    diameterground_arr = [float(data.DiameterGround1.values[0]), float(data.DiameterGround2.values[0]), float(data.DiameterGround3.values[0]), float(data.DiameterGround4.values[0])]
    ndviground_arr = [float(data.NDVIGround1.values[0]), float(data.NDVIGround2.values[0]), float(data.NDVIGround3.values[0]), float(data.NDVIGround4.values[0])]
    carbonground_arr = [float(data.CarbonGround1.values[0]), float(data.CarbonGround2.values[0]), float(data.CarbonGround3.values[0]), float(data.CarbonGround4.values[0])]

    carbonmodel_arr = [float(data.CarbonModel1.values[0]), float(data.CarbonModel2.values[0]), float(data.CarbonModel3.values[0]), float(data.CarbonModel4.values[0])]

    heightsat_arr_normalized = normalize_array(heightsat_arr)
    treecoversat_arr_normalized = normalize_array(treecoversat_arr)
    diametersat_arr_normalized = normalize_array(diametersat_arr)
    ndvisat_arr_normalized = normalize_array(ndvisat_arr)
    carbonsat_arr_normalized = normalize_array(carbonsat_arr)

    heightground_arr_normalized = normalize_array(heightground_arr)
    treecoverground_arr_normalized = normalize_array(treecoverground_arr)
    diameterground_arr_normalized = normalize_array(diameterground_arr)
    ndviground_arr_normalized = normalize_array(ndviground_arr)
    carbonground_arr_normalized = normalize_array(carbonground_arr)

    carbonmodel_arr_nornmalized = normalize_array(carbonmodel_arr)
        
    # Define different datasets
    datasets = {
        'Height': {
            'sat': np.array(heightsat_arr_normalized),
            'ground': np.array(heightground_arr_normalized)
        },
        'TreeCover': {
            'sat': np.array(treecoversat_arr_normalized),
            'ground': np.array(treecoverground_arr_normalized)
        },
        'Diameter': {
            'sat': np.array(diametersat_arr_normalized),
            'ground': np.array(diameterground_arr_normalized)
        },
        'NDVI': {
            'sat': np.array(ndvisat_arr_normalized),
            'ground': np.array(ndviground_arr_normalized)
        },
        'Carbon': {
            'sat': np.array(carbonsat_arr_normalized),
            'ground': np.array(carbonground_arr_normalized),
            'model': np.array(carbonmodel_arr_nornmalized)
        }
    }

    # Get selected dataset
    current_data = datasets[dataset_option]

    if dataset_option!='Carbon':
        # Create two columns for side-by-side plots
        col1, col2 = st.columns(2)
        draw_two(col1, col2, dataset_option, current_data, lat, lon)

    else:
        # Create two columns for side-by-side plots
        col1, col2, col3 = st.columns(3)
        draw_two(col1, col2, dataset_option, current_data, lat, lon)

        with col3:
            st.subheader(f"{dataset_option} Model Data")
            fig_right = create_map(current_data['model'], f"{dataset_option} Values", lat, lon)
            st.pyplot(fig_right)


def ground_vs_satellite(df, lat, lon, var):
    # date = pd.to_datetime(date)

    df_draw = df[(df['Latitude'] == lat) & (df['Longitude'] == lon)]

    # Set Date as index
    df_draw = df_draw.set_index('Date')

    # Select numeric columns only
    numeric_columns = df_draw.select_dtypes(include=['float', 'int']).columns
    df_draw_numeric = df_draw[numeric_columns]

    # Resample for daily, weekly, and monthly data
    df_draw_daily = df_draw_numeric.resample('D').mean().reset_index()
    df_draw_weekly = df_draw_numeric.resample('W').mean().reset_index()
    df_draw_monthly = df_draw_numeric.resample('ME').mean().reset_index()

    if var=='Carbon':
        y_axes = [f'{var}Sat', f'{var}Ground', f'{var}Model']
    else:
        y_axes = [f'{var}Sat', f'{var}Ground']

    # Create graphs
    st.subheader(f"{var} values over the years (Daily)")
    daily_graph = create_interactive_graph(df_draw_daily, "Daily Graph", y_axes, var)
    st.plotly_chart(daily_graph)
    
    st.subheader(f"{var} values over the years (Weekly)")
    weekly_graph = create_interactive_graph(df_draw_weekly, "Weekly Graph", y_axes, var)
    st.plotly_chart(weekly_graph)
    
    st.subheader(f"{var} values over the years (Monthly)")
    monthly_graph = create_interactive_graph(df_draw_monthly, "Monthly Graph", y_axes, var)
    st.plotly_chart(monthly_graph)

def create_map(data_values, title, lat, lon):

    # Define Mapbox API key
    MAPBOX_API_KEY = os.getenv("MAPBOXAPI")

    # Create a point and convert to GeoDataFrame
    point = Point(lon, lat)
    gdf = gpd.GeoDataFrame(geometry=[point], crs="EPSG:4326")

    # Convert to Web Mercator for consistent distance measurements
    gdf = gdf.to_crs(epsg=3857)

    # Get the point coordinates in meters
    center_x, center_y = gdf.geometry.iloc[0].x, gdf.geometry.iloc[0].y

    # Create a grid around the center point
    grid_size = 250
    n_cells = 2  # number of cells in each direction

    # Calculate grid boundaries
    x_min = center_x - grid_size
    x_max = center_x + grid_size
    y_min = center_y - grid_size
    y_max = center_y + grid_size

    # Create grid cells
    grid_cells = []
    cell_size = (2 * grid_size) / n_cells

    for i in range(n_cells):
        for j in range(n_cells):
            cell_x_min = x_min + i * cell_size
            cell_x_max = x_min + (i + 1) * cell_size
            cell_y_min = y_min + j * cell_size
            cell_y_max = y_min + (j + 1) * cell_size
            cell = box(cell_x_min, cell_y_min, cell_x_max, cell_y_max)
            grid_cells.append(cell)

    # Create GeoDataFrame for grid
    grid_gdf = gpd.GeoDataFrame(geometry=grid_cells, crs="EPSG:3857")

    # Assign the data values
    grid_gdf['value'] = data_values

    # Create a custom green colormap
    green_colors = [(0, 'lightgreen'), (1, 'darkgreen')]
    green_cmap = colors.LinearSegmentedColormap.from_list('custom_green', green_colors)

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot grid with green colors and data-based opacity
    grid_gdf.plot(ax=ax, 
                  column='value',
                  cmap=green_cmap,
                  alpha=data_values,
                  edgecolor='black',
                  linewidth=1,
                  legend=True,
                  legend_kwds={'label': 'Intensity'})

    # Set map extent
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])

    # Add Mapbox satellite basemap
    ctx.add_basemap(
        ax,
        source=f"https://api.mapbox.com/v4/mapbox.satellite/{{z}}/{{x}}/{{y}}@2x.png?access_token={MAPBOX_API_KEY}",
        attribution='© Mapbox',
        zoom=16
    )

    # Add title
    ax.set_title(title, fontsize=14)
    
    return fig

# Function for ARIMA model on training and testing data
def train_test_arima(data, forest_name, start_date, end_date, column='Carbon'):
    
    filtered_data = data[data['ForestName'] == forest_name]
    
    if filtered_data.empty:
        print("No data available for the given ForestName and TowersID.")
        return

    # Group data by 'Date' to calculate daily averages
    daily_avg = filtered_data.groupby('Date').agg({column: 'mean'}).reset_index()

    # Set the 'Date' column as the index
    daily_avg.set_index('Date', inplace=True)
    
    # Generate the requested out-of-range dates
    out_of_range_dates = pd.date_range(start=start_date, end=end_date, freq='D')

    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    
    # Check if start date is out of range
    if start_date > daily_avg.index.max() or start_date < daily_avg.index.min():
        # Calculate the daily averages for the available years
        repeated_avg = daily_avg.groupby(daily_avg.index.dayofyear).mean().reset_index()
        
        # Map daily averages to the new date range
        day_of_year_mapping = out_of_range_dates.dayofyear
        repeated_avg = pd.DataFrame({
            'Date': out_of_range_dates,
            column: repeated_avg[column].values.take(day_of_year_mapping - 1, mode='wrap')
        })

        fig = px.line(
            repeated_avg,
            x='Date',
            y=column,
            title=f'Carbon Values for {forest_name}'
        )
        fig.update_layout(
            xaxis_title=date,
            yaxis_title=f'{column}',
            legend_title='Source',
            template='plotly_white'
        )
        st.plotly_chart(fig)

def season_plots(df, variable, which):
    fig = px.histogram(df, x=variable+which, y="Season",
                       color='Year', barmode='group',
                       histfunc='avg', height=400)
    
    st.plotly_chart(fig)

def seasonwise(variable, lat, lon):
    df = get_merge_data()
    df = df[(df.Latitude==lat)&(df.Longitude==lon)]
    st.subheader(f'Satellite {variable} values over the season')
    season_plots(df, variable, 'Sat')
    st.subheader(f'Ground Truth {variable} values over the season')
    season_plots(df, variable, 'Ground')

# Streamlit app
def main(lat, lon, date, forestName):

    st.header(f"Breakdown of the point in {forestName}")
    
    df = get_data(date)
    df['Date'] = pd.to_datetime(df.Date)
    data = df[(df.Date==date)&(df.Latitude==lat)&(df.Longitude==lon)]

    # Display information about the selected point
    st.markdown(f"""
                ##### <b>ForestName:</b> <i style='font-weight:normal'>{forestName}</i>
                ##### <b>Location:</b> <i style='font-weight:normal'>[{lon}, {lat}]</i>
                ##### <b>Date:</b> <i style='font-weight:normal'>{date}</i>
                ##### <b>Carbon Stored:</b> <i style='font-weight:normal'>{data.Carbon.sum():.2f} pounds</i>
                """,
                unsafe_allow_html=True)

    # Dropdown for selecting dataset
    dataset_option = st.selectbox(
        'Select a Variable',
        ('Height', 'TreeCover', 'Diameter', 'NDVI', 'Carbon')
    )

    tab1, tab2, tab3, tab4 = st.tabs(["Analysis", "Ground Truth vs Satellite Data", "Actual Vs Predicted", "Predict"])

    with tab1:
        data = data[['Latitude', 'Longitude', 'Date', 'ForestName', 'TowersID', 
                 'HeightSat1', 'HeightSat2', 'HeightSat3', 'HeightSat4', 
                 'HeightGround1', 'HeightGround2', 'HeightGround3', 'HeightGround4', 
                 'TreeCoverSat1', 'TreeCoverSat2', 'TreeCoverSat3', 'TreeCoverSat4', 
                 'TreeCoverGround1', 'TreeCoverGround2', 'TreeCoverGround3', 'TreeCoverGround4', 
                 'DiameterSat1', 'DiameterSat2', 'DiameterSat3', 'DiameterSat4', 
                 'DiameterGround1', 'DiameterGround2', 'DiameterGround3', 'DiameterGround4', 
                 'NDVISat1', 'NDVISat2', 'NDVISat3', 'NDVISat4', 
                 'NDVIGround1', 'NDVIGround2', 'NDVIGround3', 'NDVIGround4', 
                 'CarbonSat1', 'CarbonSat2', 'CarbonSat3', 'CarbonSat4', 
                 'CarbonGround1', 'CarbonGround2', 'CarbonGround3', 'CarbonGround4', 
                 'CarbonModel1', 'CarbonModel2', 'CarbonModel3', 'CarbonModel4']]
        
        analysis(data, dataset_option)

    with tab2:
        ground_vs_satellite(df, lat, lon, dataset_option)
        seasonwise(dataset_option, lat, lon)
        # season_plots(df, dataset_option, lat, lon)

    with tab3:
        model = st.selectbox(
            'Select a Variable',
            ('Opti-CarboNet Model', 'Adaptive TabNet Model', 'Eco-CNN Model', 'CFR-Eco Ensemble Model', 'DeepGreen-DNN Model'))

        path = "../Dataset/"
        results = pd.read_csv(f"{path}{model}.csv")
        results = results[results['Actual']<40000]

        y_axes = ['Actual', 'Predicted']
        
        # Create graphs
        st.subheader("Daily Graph")
        daily_graph = create_interactive_graph(results, "Daily Graph", y_axes, model, 'Date')
        st.plotly_chart(daily_graph)

        
    with tab4:
        col1, col2, col3 = st.columns(3)

        with col1:
            forest_name = st.selectbox(
            'Select a ForestName for Analysis',
            list(df.ForestName.unique()))

        with col2:
            start_date = st.date_input("Enter the start date: ")

        with col3:
            end_date = st.date_input("Enter the end date: ")

        train_test_arima(df, forest_name, start_date, end_date)
    
    if st.button('Back'):
        webbrowser.open(f'http://localhost:3000/?lat={lat}&lon={lon}')


if __name__ == "__main__":
    st.set_page_config(page_title="Map Visualization", layout="wide")
    
    try:
        lat = float(st.query_params['lat'])
        lon = float(st.query_params['lon'])
        date = st.query_params['date']
        forestname = st.query_params['forestname']
    except:
        lat=39.761058
        lon=-121.407603
        date='2019-01-01'
        forestname='Plumas National Forest'

    main(lat, lon, date, forestname)

