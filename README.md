# MechaPulse
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white"/></a>
<a href="https://isocpp.org/"><img src="https://img.shields.io/badge/C++-00599C?style=flat&logo=c%2B%2B&logoColor=white"/></a>
<a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white"/></a>
<a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white"/></a>
<a href="https://www.raspberrypi.org/"><img src="https://img.shields.io/badge/Raspberry%20Pi-A22846?style=flat&logo=raspberry-pi&logoColor=white"/></a>
<a href="https://www.espressif.com/en/products/socs/esp32"><img src="https://img.shields.io/badge/ESP32-000000?style=flat&logo=espressif&logoColor=white"/></a>
<a href="https://code.visualstudio.com/"><img src="https://img.shields.io/badge/VS%20Code-007ACC?style=flat&logo=visual-studio-code&logoColor=white"/></a> 
<a href="https://jupyter.org/"><img src="https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white"/></a>
# Project Overview
MechaPulse is an Industrial IoT project that uses sound analysis to detect faults in machinery. The proposed system consists of an array of embedded devices placed across machines, each monitoring sound and running a TinyML model to predict potential faults. Alerts are sent to a central dashboard for real-time monitoring. As a prototype, we have developed a system where an ESP32 module records and processes audio, sending data to a Raspberry Pi where the ML model identifies faults. Currently we are developing the next stage of the prototype, which will run the ML model directly on the ESP32, with the Raspberry Pi acting as a gateway to a cloud-based dashboard for remote monitoring.
