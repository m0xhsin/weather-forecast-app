import numpy as np
from sklearn.linear_model import LinearRegression

def predict_temperature(temps):
    X = np.array(range(len(temps))).reshape(-1, 1)
    y = np.array(temps)

    model = LinearRegression()
    model.fit(X, y)

    next_hour = np.array([[len(temps)]])
    prediction = model.predict(next_hour)

    return prediction[0]
