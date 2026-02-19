# Using  DJango Rest Famework i am doing this prject
import os
import joblib 
import json
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR,"model.pkl")
model = joblib.load(model_path)


@api_view(['POST'])
def predict(request):
    if request.method=='POST':
        try:
            #data = json.loads(request.body)
            data = request.data
            name = str(data.get("name"))
            time = float(data.get("time"))
            amount = float(data.get("amount"))
            if name and time and amount:
                random_pca = np.random.normal(0, 1, 28)
                feauters = [time] + list(random_pca)+ [amount]
                input_data = np.array(feauters).reshape(1,-1)
                prediction = model.predict(input_data)[0]
                #print("Prediction is:",prediction)
                return Response({"prediction":int(prediction)})

        except Exception as e:
            return Response({"error": str(e)}, status=500)
