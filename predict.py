from datetime import datetime

import joblib
import numpy as np

start = datetime.now()
model = joblib.load("trainer/model_pipeline.pkl")
end = datetime.now()
print(f"time to load model: {end-start}")

x = np.array(
    [
        [8.3252, 41.0, 6.98412698, 1.02380952, 322.0, 2.55555556, 37.88, -122.23],
        [8.3252, 41.0, 6.98412698, 1.02380952, 322.0, 2.55555556, 37.88, -122.23],
        [8.3252, 41.0, 6.98412698, 1.02380952, 322.0, 2.55555556, 37.88, -122.23],
        [8.3252, 41.0, 6.98412698, 1.02380952, 322.0, 2.55555556, 37.88, -122.23],
        [58.3252, 414.0, 66.8412698, 10.02380952, 112.0, 33.555355556, 7.88, -12.23],
    ]
)

print(f"shape of input data: {x.shape}")
start = datetime.now()
p = model.predict(x)
end = datetime.now()
print(f"time to perform vectorized predictions: {end-start}")

start = datetime.now()
for item in x:
    model.predict(item.reshape(-1, 8))
end = datetime.now()
print(f"time to perform for-loop iterated predictions: {end-start}")
print(p)
# target: 4.526
