from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from python_backend.load_downloaded_data import load_data
from io import StringIO
import pandas as pd
from python_backend.make_map import MapGenerator, Map
from python_backend.model_classes import *
import pickle
from datetime import datetime, timezone

class ModelUnpickler(pickle.Unpickler): # Assigns models to the right class
    def find_class(self, module, name):
        if module == "__main__":
            module = "python_backend.model_classes"
        return super().find_class(module, name)

def load_model(path: Path):
    with path.open("rb") as f:
        return ModelUnpickler(f).load()



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

last_upload_time: datetime | None = None
PUBLIC_DIR = Path("/app/public")

@app.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...)
):
    csv_text = (await file.read()).decode("utf-8")
    global last_upload_time
    last_upload_time = datetime.now(timezone.utc)
    unprocessed = pd.read_csv(StringIO(csv_text))

    df = load_data(unprocessed)

    MODEL_DIR = Path(__file__).resolve().parent / "models"

    # Load all models
    moisture_model = load_model(MODEL_DIR / "moisture_model.pkl")
    salinity_model = load_model(MODEL_DIR / "salinity_model.pkl")
    water_model = load_model(MODEL_DIR / "water_model.pkl")

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

    return f"CSV successfully uploaded to website. Maps {[map.filename for map in maps]} succesfully generated."

@app.get("/last-upload")
def last_upload():
    return {
        "last_upload": last_upload_time.isoformat() if last_upload_time else None
    }