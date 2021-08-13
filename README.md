# Gesture Triggered Alarm on Pi or Jetson Nano
_Gesture Triggered Cam Alarm for Women Security based on Computer Vision, Mathematical Concavity Estimation, MQTT, OpenVINO and Pimoroni Blinkt! on RPi or Jetson Nano_


## Preparing to Run


To run the object tracking and gesture recognition code,
```sh
python3 ball_tracking.py
```

**Note:**The twilio account details need to be filled in correctly in `sendsms.py` file in order to get alert messages on mobile.

To enable alarm simulation with Pimoroni Blinkt! execute
```sh
python3 mqtt-blinkt.py
```

To run Gesture (American Sign Language - ASL) Recognition models using OpenVINO

```sh
python3 gesture_recognition_demo.py -m_a OV2021_models/asl-recognition-0004.xml -m_d OV2021_models/person-detection-asl-0001.xml -i 0 -c <omz_dir>/data/dataset_classes/msasl100.json
```

### Supported Models

* asl-recognition-0004
* common-sign-language-0001
* common-sign-language-0002
* person-detection-asl-0001

if you get an error on module import, then add this path: <omz_dir>/demos/common/python to the system path.

## References

1. https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
2. https://docs.openvinotoolkit.org/latest/omz_demos_face_recognition_demo_python.html