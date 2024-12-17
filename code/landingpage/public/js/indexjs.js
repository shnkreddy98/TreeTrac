// Ensure your server is running and /api/mapbox endpoint is accessible
async function fetchMapboxAPIKey() {
    try {
        // Fetch the Mapbox API key from the server endpoint
        const response = await fetch('/api/mapbox');

        // Check if the response is successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the response as JSON
        const apiKey = await response.json();

        mapboxgl.accessToken = apiKey;

        const map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/satellite-v9',
            center: [-98, 38.88],
            minZoom: 3,
            zoom: 2
        });
    } catch (error) {
        // Handle any errors
        console.error('Error fetching Mapbox API key:', error);
    }
}

// Call the function
fetchMapboxAPIKey();


year2019 = document.getElementById("2019");
year2020 = document.getElementById("2020");

let yearSelected, mapbox_url, mapbox_layer;

const urlParams = new URLSearchParams(window.location.search);

year2019.addEventListener("click", () => {
    mapbox_url = "mapbox://shnkreddy.2hv20ojb";
    mapbox_layer = "fiapart1";
    year=2019
    year2019.style.backgroundColor = '#ffffff';
    year2020.style.backgroundColor = '#ffffff';
    year2019.style.backgroundColor = '#add8e6';
    document.getElementById("")
    getMap(mapbox_url, mapbox_layer)
});
year2020.addEventListener("click", () => {
    mapbox_url = "mapbox://shnkreddy.5gy1hfqc"
    mapbox_layer = "fiapart2"
    year=2020
    year2019.style.backgroundColor = '#ffffff';
    year2020.style.backgroundColor = '#ffffff';
    year2020.style.backgroundColor = '#add8e6';
    getMap(mapbox_url, mapbox_layer)
});


function getMap(mapbox_url, mapbox_layer) {
    
    // Initialize the map here
    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/satellite-v9',
        center: [-98, 38.88],
        minZoom: 3,
        zoom: 2
    });
    map.on('load', () => {
        map.loadImage(
            'assets/img/tower.png',
            (error, image) => {
                if (error) throw error;
                // Add the image to the map style.
                map.addImage('tower-icon', image);
                // Add forest polygons source
                map.addSource('forests', {
                    'type': 'vector',
                    'url': 'mapbox://shnkreddy.binp7ock'
                });
                // Add towers source
                map.addSource('towers', {
                    'type': 'vector',
                    'url': 'mapbox://shnkreddy.68g4qc2w'
                });
                // Add data points source
                map.addSource('data', {
                    'type': 'vector',
                        'url': mapbox_url
                });
        
                // Add forest polygons layer
                map.addLayer({
                    'id': 'forests',
                    'type': 'fill',
                    'source': 'forests',
                    'source-layer': 'ca_forest-8q0k9m',
                    'paint': {
                        'fill-outline-color': 'rgba(255,255,255,1)',
                        'fill-color': 'rgba(0,0,0,0.1)',
                    }
                });
        
                // Add highlighted forest layer
                map.addLayer({
                    'id': 'forest-highlighted',
                    'type': 'fill',
                    'source': 'forests',
                    'source-layer': 'ca_forest-8q0k9m',
                    'paint': {
                        'fill-outline-color': '#484896',
                        'fill-color': '#228B22',
                        'fill-opacity': 0.25
                    },
                    'filter': ['in', 'GIS_ACRES', '']
                });
        
                // Add tower points layer
                map.addLayer({
                    'id': 'towers',
                    'type': 'symbol',
                    'source': 'towers',
                    'source-layer': 'fia-towers-6b41q8',
                    'layout': {
                                'icon-image': 'tower-icon', // reference the image
                                'icon-size': 0.025
                            },
                    'filter': ['all', 
                            ['in', 'ForestName', ''], 
                            ['in', 'TowersID', '']]
                });
        
                // Add data points layer
                map.addLayer({
                    'id': 'data',
                    'type': 'circle',
                    'source': 'data',
                    'source-layer': mapbox_layer,
                    'paint': {
                        'circle-radius': 5,
                        'circle-color': '#FF0000'
                    },
                    'filter': ['all', 
                            ['in', 'ForestName', ''], 
                            ['in', 'TowersID', '']]
                });
    
                const uniqueForestNames = new Set(); // Using a Set to ensure uniqueness
    
                // --------------------------------------------------------------------------------------------------------------------------------------------
                // Function to extract coordinates dynamically
                function getCoordinates(geometry) {
                    if (!geometry || !geometry.type || !geometry.coordinates) {
                        console.warn("Invalid geometry structure:", geometry);
                        return null;
                    }
    
                    switch (geometry.type) {
                        case "Point":
                            return geometry.coordinates; // Single [lng, lat] pair
                        case "MultiPoint":
                        case "LineString":
                            return geometry.coordinates[0]; // First point
                        case "Polygon":
                            return geometry.coordinates[0][0]; // First coordinate in the outer ring
                        case "MultiPolygon":
                            return geometry.coordinates[0][0][0]; // First coordinate in the first ring of the first polygon
                        default:
                            console.warn("Unhandled geometry type:", geometry.type);
                            return null;
                    }
                }
                    
                // Mapbox interaction function
                function highlightForest(forestName) {
                    forestNameDisplay = document.getElementById("forest-name");
                    forestNameDisplay.innerText= `Selected Forest: ${forestName}`;
                    if (!forestName) return;
                    // Query features based on the forest name
                    const selectedFeatures = map.queryRenderedFeatures({
                        layers: ['forests'], // Specify the layer to query
                        filter: ['==', 'FORESTNAME', forestName] // Filter by forest name
                    });
                    if (selectedFeatures.length > 0) {
                        const gis = selectedFeatures.map(
                            (feature) => feature.properties.GIS_ACRES
                        );
                        // Highlight the forest on the map
                        map.setFilter('forest-highlighted', ['in', 'GIS_ACRES', ...gis]);
                        // Highlight towers in the forest
                        map.setFilter('towers', ['==', 'ForestName', forestName]);
                        const coordinates = getCoordinates(selectedFeatures[0].geometry);
                        map.flyTo({
                                    center: coordinates,
                                    zoom: 7 // Use current zoom level
                                    });
                    } else {
                            console.log(`No features found for forest: ${forestName}`);
                        }
                }
                var wasLoaded = false;
                map.on('render', function() {
                    if (!map.loaded() || wasLoaded) return;
                    const forestFeatures = map.querySourceFeatures('forests', {
                        sourceLayer: 'ca_forest-8q0k9m'
                    });
                    wasLoaded = true;
                    forestFeatures.forEach((feature) => {
                        if (feature.properties && feature.properties.FORESTNAME) {
                            uniqueForestNames.add(feature.properties.FORESTNAME);
                        }
                    }); 
                    const forestNameArray = Array.from(uniqueForestNames);
                    // Function to populate table
                    function populateTable(array) {
                        // Get the table element
                        const table = document.querySelector("table");
                        // Clear existing rows (except the header)
                        table.querySelectorAll("tr:not(:first-child)").forEach(row => row.remove());
                        // Loop through the array and create rows
                        array.forEach(item => {
                            // Create a table row
                            const row = document.createElement("tr");
                            // Create a table cell and set the content
                            const cell = document.createElement("td");
                            cell.textContent = item;
                            // Append the cell to the row
                            row.appendChild(cell);
                            // Attach a hover event listener to the row
                            row.addEventListener("click", () => {
                                highlightForest(item); // Function to run your query or action
                            });
                            // Append the row to the table
                            table.appendChild(row);
                        });
                    }
                    // Populate the dropdown with unique forest names
                    populateTable(forestNameArray)
                });
            });
        });
        map.on('click', (e) =>{
            const bbox = [
                [e.point.x - 5, e.point.y - 5],
                [e.point.x + 5, e.point.y + 5]
            ];
            const selectedFeatures = map.queryRenderedFeatures(bbox, {
                layers: ['forests']
            });
            if (selectedFeatures.length > 0) {
                const gis = selectedFeatures.map(
                    (feature) => feature.properties.GIS_ACRES
                );
                const forestName = selectedFeatures[0].properties.FORESTNAME || 'Unknown Forest';
                map.setFilter('forest-highlighted', ['in', 'GIS_ACRES', ...gis]);
                // Set filter for towers based on the selected forest name
                map.setFilter('towers', ['==', 'ForestName', forestName]);
                
                forestNameDisplay = document.getElementById("forest-name");
                forestNameDisplay.innerText= `Selected Forest: ${forestName}`;
                const coordinates = e.lngLat
                map.flyTo({
                    center: coordinates,
                    zoom: 7 // Use current zoom level
                });
            }
        });
            
        // Event to handle clicks on towers
        map.on('click', 'towers', (e) => {
            console.log('clicked')
            const point = e.features[0].properties;
            const coordinates = e.features[0].geometry.coordinates;
            const forestName = point.ForestName || 'Unknown Forest';
            const towersID = point.TowersID || 'Unknown Tower';
            // Set filter for towers based on the selected forest name
            map.setFilter('data', ['all',
                            ['==', 'ForestName', forestName],
                            ['==', 'TowersID', towersID]]);
            
            // Center map on the clicked point with current zoom level
            map.flyTo({
                center: coordinates,
                zoom: map.getZoom() // Use current zoom level
            });
        });
                
        // Event to handle clicks on points
        map.on('click', 'data', (e) => {
            const point = e.features[0].properties;
            const coordinates = e.features[0].geometry.coordinates;
            const forestName = point.ForestName || 'Unknown Forest';
            const popupContent = `
                <strong>Forest Name:</strong> ${forestName}<br>
                <strong>Tree Height:</strong> ${point.Height || 'N/A'}<br>
                <strong>Carbon:</strong> ${point.Carbon || 'N/A'}<br>
                <strong>Diameter:</strong> ${point.Diameter || 'N/A'}<br>
                <strong>Measurement Date:</strong> ${point.Date || 'N/A'}<br>
                <button onclick='redirectToBreakdown(${JSON.stringify(point)})'>Breakdown</button>`;
            new mapboxgl.Popup()
                .setLngLat(coordinates)
                .setHTML(popupContent)
                .addTo(map);
            // Center map on the clicked point with current zoom level
            map.flyTo({
                center: coordinates,
                zoom: map.getZoom() // Use current zoom level
            });
        });
                
        window.redirectToBreakdown = (point) => {
            const lat = point.Latitude
            const lon = point.Longitude
            const date = point.Date
            const forestname = point.ForestName
            const breakdownPageURL = `http://www.localhost:8501/?lat=${lat}&lon=${lon}&date=${date}&forestname=${forestname}`;
            window.location.href = breakdownPageURL;
        };
                
        // Change cursor to pointer when hovering over points
        map.on('mouseenter', 'towers', () => {
            map.getCanvas().style.cursor = 'pointer';
        });
                
        map.on('mouseleave', 'towers', () => {
            map.getCanvas().style.cursor = '';
        });
        
    
    
}