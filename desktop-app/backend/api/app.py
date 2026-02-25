# Import required libraries
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn 
import pickle
import numpy as np
import pandas as pd
import sounddevice as sd
import soundfile as sf
import scipy.io.wavfile as wavfile
import scipy.fftpack as fftpk

# Load the saved model
import os
_model_path = os.path.join(os.path.dirname(__file__), "..", "..", "models", "machine_failure_detection_model3.pkl")
model = pickle.load(open(_model_path, 'rb'))

app = FastAPI()

# Flag to control recording state
is_recording = False

class Input(BaseModel):
    RMS: float
    Mean: float
    MA1: float
    MA2: float
    MA3: float
    F1: float
    F2: float
    F3: float

# Endpoint to start recording
@app.post("/start-recording")
def start_recording():
    global is_recording
    is_recording = True
    while is_recording:
        # is_recording = False
        # Recording the audio
        samplerate = 48000  
        duration = 5 # seconds
        audio = 'test.wav'
        mydata = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, blocking=True)
        sd.wait()
        sf.write(audio, mydata, samplerate)

        # Reading the audio
        s_rate, signal = wavfile.read(audio)

        # Extracting the features
        mean = abs(signal).mean()
        rms = np.sqrt(abs(signal**2).mean())
        FFT_ = abs(fftpk.fft(signal))
        FFT = FFT_[range(len(FFT_)//2)]
        freqs = fftpk.fftfreq(len(FFT), 1.0/s_rate)[range(len(FFT_)//2)]
        sorted = np.sort(FFT)[::-1]
        ma1, ma2 , ma3 = sorted[[0,1,2]]
        max_amp_index = [np.where(FFT == sorted[0])[0], np.where(FFT == sorted[1])[0], np.where(FFT == sorted[2])[0]]
        f1, f2, f3 = np.concatenate(freqs[max_amp_index])

        # Storing the features in a list
        features = [rms, mean, ma1, ma2, ma3, f1, f2, f3]

        # Creating a dataframe
        input_data = pd.DataFrame([features])
        input_data.columns = ["RMS","Mean","MA1","MA2","MA3","F1","F2","F3"]

        # Making a prediction
        prediction = model.predict(input_data)[0]
        return {"status": "success", "prediction": prediction}
    

# Endpoint to stop recording, extract features, make prediction, and return the result
@app.post("/stop-recording")
def stop_recording():
    global is_recording
    is_recording = False
    
    # else:
        # return {"status": "error", "message": "Recording is not started"}

if __name__ == "__main__":
    uvicorn.run(app,port=8000)
