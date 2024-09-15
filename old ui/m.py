import streamlit as st
import requests
import threading
def main():
    # Creating Streamlit buttons
    record_button = st.button('Record', key='record_button')
    stop_button = st.button('Stop', key='stop_button')

    # Function to send record command to the backend
    def start_recording():
        # Send HTTP POST request to start recording
        response = requests.post("http://127.0.0.1:8000/start-recording")
        if response.status_code == 200:
            st.success("Recording started successfully")
            st.write("Prediction:", response.json()["prediction"])
            if response.json()["prediction"] == 1.0:
                st.markdown("**Machine ID: Off condition with noise**")
                # st.image("D:\\Documents\\SLIoT\\ML App\\ui\\off.png", caption="Off condition with noise", width=200)
                # send_error_request("Off condition")
            elif response.json()["prediction"] == 2.0:
                st.markdown("**Machine ID: Healthy condition**")
                # st.image("D:\\Documents\\SLIoT\\ML App\\ui\\good_.png", caption="Healthy condition", width=200)
                # send_error_request("Healthy condition")
            elif response.json()["prediction"] == 3.0:
                st.markdown("**Machine ID: Bearing Fault**")
                # st.image("D:\\Documents\\SLIoT\\ML App\\ui\\mfault1_.png", caption="Bearing Fault", width=200)
                # send_error_request("Bearing Fault")
            else:
                st.markdown("**Machine ID: Fan Fault**")
                # st.image("D:\\Documents\\SLIoT\\ML App\\ui\\mfault2.png", caption="Fan Fault", width=200)
                # send_error_request("Fan Fault")
        else:
            st.error("Failed to start recording")

    # Function to send stop command to the backend
    def stop_recording():
        # Send HTTP POST request to stop recording
        response = requests.post("http://127.0.0.1:8000/stop-recording")
        if response.status_code == 200:
            st.success("Recording stopped successfully")
            # Display prediction received from backend
        else:
            st.error("Failed to stop recording")

    # Handling button clicks
    if record_button:
        start_recording()

    if stop_button:
        stop_recording()

    x= threading.Thread(target=start_recording)
    y= threading.Thread(target=stop_recording)
    x.start()
    y.start()
    x.join()
    y.join()

if __name__ == "__main__":
    main()
