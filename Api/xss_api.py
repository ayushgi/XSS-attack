import numpy as np
from fastapi import FastAPI, Form
from pydantic import BaseModel
import tensorflow as tf

app = FastAPI()

model = tf.keras.models.load_model('xss_detection_model.h5')

def convert_to_ascii(input_data):
    input_data_to_char = [ord(i) for i in input_data]
    Zero_array = np.zeros((400))
    indexs = min(len(input_data_to_char), 400)
    for i in range(indexs):
        Zero_array[i] = input_data_to_char[i]
    Zero_array.shape = (20, 20)
    return Zero_array

# POST endpoint for checking XSS payload
@app.post("/check-xss/")
async def check_xss(payload: str = Form(...)):
    ascii_input = convert_to_ascii(payload)
    ascii_input = np.expand_dims(ascii_input, axis=(0, -1)) 
    prediction = model.predict(ascii_input)[0][0]  
    
    is_malicious = True if prediction > 0.5 else False
    return {"payload": payload, "is_malicious": is_malicious, "prediction_score": float(prediction)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
