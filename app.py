from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

DATA_PATH = os.path.join("data", "68544eadb00637051626.csv")

#  1. Define threshold value
MOISTURE_THRESHOLD = 40

@app.route('/')
def home():
    df = pd.read_csv(DATA_PATH)

    if df.empty:
        return "No sensor data found."

    # 2. Get latest sensor row
    latest = df.tail(1).to_dict(orient='records')[0]

    #  3. Determine irrigation status
    current_moisture = float(latest.get('Soil_Moisture', 0))
    irrigation_status = "ON" if current_moisture < MOISTURE_THRESHOLD else "OFF"

    #  4. Prepare trend chart data (optional)
    trend_data = df.tail(10)[['Timestamp', 'Soil_Moisture']].to_dict(orient='records')

    #  5. Pass new values to template
    return render_template(
        'index.html',
        data=latest,
        irrigation_status=irrigation_status,
        threshold=MOISTURE_THRESHOLD,
        trend=trend_data
    )

if __name__ == '__main__':
    app.run(debug=True)
