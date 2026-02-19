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


from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np

@api_view(['POST'])
def predict(request):
    try:
        data = request.data  # ✅ VERY IMPORTANT (NOT json.loads)

        name = data.get("name")
        time = data.get("time")
        amount = data.get("amount")

        if name is None or time is None or amount is None:
            return Response({"error": "Missing fields"}, status=400)

        time = float(time)
        amount = float(amount)

        # dummy PCA features
        random_pca = np.random.normal(0, 1, 28)
        features = [time] + list(random_pca) + [amount]
        input_data = np.array(features).reshape(1, -1)

        prediction = model.predict(input_data)[0]

        return Response({"prediction": int(prediction)})

    except Exception as e:
        print("ERROR:", str(e))
        return Response({"error": str(e)}, status=500)

