require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const axios = require('axios');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.static('public'));
app.use(bodyParser.json());

app.get('/api/mapbox', async (req, res) => {
    try {
        const mapboxAPI = process.env.MAPBOX_API_KEY;

        res.json(mapboxAPI);
    } catch (error) {
        console.error('Error fetching Mapbox data:', error);
        res.status(500).send('Error fetching Mapbox data');
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});
