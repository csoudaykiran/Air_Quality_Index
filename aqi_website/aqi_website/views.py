from django.shortcuts import render
import pandas as pd
import joblib

# Load the saved model
model = joblib.load('models/aqi_model')



def predict_aqi(request):
    if request.method == 'POST':
        lat = float(request.POST.get('latitude'))
        lng = float(request.POST.get('longitude'))

        co_aqi = float(request.POST.get('co_aqi'))
        ozone_aqi = float(request.POST.get('ozone_aqi'))
        no2_aqi = float(request.POST.get('no2_aqi'))
        pm25_aqi = float(request.POST.get('pm25_aqi'))

        new_data = pd.DataFrame({
            'lat': [lat],
            'lng': [lng],
            'CO AQI Value': [co_aqi],
            'Ozone AQI Value': [ozone_aqi],
            'NO2 AQI Value': [no2_aqi],
            'PM2.5 AQI Value': [pm25_aqi]
        })

        predicted_aqi_value = model.predict(new_data)[0]
        predicted_category = ""

        # Define AQI category thresholds
        good_threshold = 50
        moderate_threshold = 100

        # Categorize the predicted AQI value
        if predicted_aqi_value <= good_threshold:
            predicted_category = "Good"
        elif predicted_aqi_value <= moderate_threshold:
            predicted_category = "Moderate"
        else:
            predicted_category = "Bad"

        

        context = {
            'predicted_aqi_value': predicted_aqi_value,
            'predicted_category': predicted_category
            
        }

        return render(request, 'result.html', context)

    return render(request, 'input.html')
