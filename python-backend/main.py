from fastapi import FastAPI, UploadFile, File, Form
from pathlib import Path
from load_downloaded_data import load_data
from io import StringIO
import pandas as pd
from make_map import MapGenerator, Map
from model_classes import *
import pickle

app = FastAPI()
PUBLIC_DIR = Path("/app/public")

@app.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...)
):
    csv_text = (await file.read()).decode("utf-8")
    unprocessed = pd.read_csv(StringIO(csv_text))

    df = load_data(unprocessed)

    # Load all models
    moisture_model = pickle.load(open('models/moisture_model.pkl', 'rb'))
    salinity_model = pickle.load(open('models/salinity_model.pkl', 'rb'))
    water_model = pickle.load(open('models/water_model.pkl', 'rb'))

    # Perform all predictions
    x = df[['temperature (C)', 'Volumetric Water Content (%)', 'Electrical Conductivity (uS/cm)']]
    df['moisture'] = moisture_model.predict(x)
    df['salinity'] = salinity_model.predict(x)
    df['water_to_give_L_per_m2'] = water_model.predict(x)
    
    generator = MapGenerator(df)

    # All maps that have to be generated:
    maps = [Map('moisture',                         'Moisturemap.html',     'plasma'),
            Map('salinity',                         'Salinitymap.html',     'copper'),
            Map('water_to_give_L_per_m2',           'Watermap.html',        'viridis',  categorical=False),
            Map('temperature (C)',                  'Temperaturemap.html',  'coolwarm', categorical=False),
            Map('Volumetric Water Content (%)',     'Watercontentmap.html', 'Blues',    categorical=False),
            Map('Electrical Conductivity (uS/cm)',  'Conductivitymap.html', 'summer',   categorical=False)]

    # Generate all maps
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    for map in maps:
        generator.points_to_fields(map.datapoint)
        map_obj = generator.save_map(map.cmap, map.categorical)
        map_obj.save(str(PUBLIC_DIR / map.filename))

    return {"status": "ok", "filenames": [map.filename for map in maps]}