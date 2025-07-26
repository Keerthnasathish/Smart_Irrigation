from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

DATA_PATH = os.path.join('data', '68544eadb00637051626.csv')

@app.route('/')
def home():
    try:
        df = pd.read_csv(DATA_PATH)

        if df.empty:
            return "Sensor data not available"

        latest = df.tail(1).to_dict(orient='records')[0]

        # Select last 10 rows for trend chart
        trend_data = df.tail(10)[['Timestamp', 'Soil_Moisture']].to_dict(orient='records')

        return render_template('index.html', data=latest, trend=trend_data)

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
