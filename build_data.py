import requests
import datetime
import time
while True:
    url = "https://heartican.pythonanywhere.com/getval"

    # Send GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        ecg_value = data.get("ecgVal")

        with open("labels.txt","a") as f:
            f.write(str(datetime.datetime.now().strftime("%H:%M:%S"))+",")
        with open("values.txt","a") as f1:
            f1.write(str(ecg_value)+",")
        print("value Written", str(datetime.datetime.now().strftime("%H:%M:%S"))+",",ecg_value)

    else:
        print("Connect The Heartician Device To Internet")
    time.sleep(5)
