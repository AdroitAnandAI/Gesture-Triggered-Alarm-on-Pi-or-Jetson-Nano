# Gesture Triggered Alarm on Pi or Jetson Nano
_Gesture Triggered Cam Alarm for Women Security based on Computer Vision, Mathematical Concavity Estimation, MQTT, OpenVINO and Pimoroni Blinkt! on RPi or Jetson Nano_

**Imagine a lady who is sitting alone in a clinic, shop, company, or isolated elsewhere needs urgent rescue.** She may not have the opportunity or liberty to make a call. The surveillance camera should be smart enough to understand her gestures, be it with hand or objects, as an SOS signal. We can **use image processing, deep learning, or arithmetic algorithms to analyze the incoming video frames from an SoC with a camera, to trigger an alert.**

## Watch the project demo video:

[![Watch Project Demo](images/preview.png)](https://youtu.be/NzQqCbhVgbs)

There are **3 main modules** for this project,
a) **Localize the object**, used to trigger the event.
b) **Analyze the motion** of the object to recognize the signal
c) **Deployment on an SoC** to install the gadget in the environment.

This is a tricky problem, as **we need a cheap solution for easy adoption, but not at the cost of accuracy**, as we deal with emergencies here. Similarly, it is **easier to detect a custom object but it is more useful to use your own body** to signal the emergency.


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

### Solution Idea

- **Object Localization: Object Color Masking using Computer Vision**
 
It is very **compute-efficient to create a mask for a particular color** to identify the object based on its color. We can then **check the size and shape of the contour** to confirm the find. It would be prudent to **use an object with a distinct color** to avoid false positives.

This method is **not only highly efficient and accurate but it also paves the way to do gesture recognition using pure mathematical models, making it an ideal solution on the Edge.**

- **Concavity Estimation using Vector Algebra**

If all the vectors in point cloud are concave, then it represents circular motion.

-    **Compute the vectors** by differencing adjacent points.
-    Compute vector length using np.linalg.norm
-    Exclude the outlier vectors by defining  boundary distribution

-    If the distance between points < threshold, then ignore the motion
-    **Take the cross product of vectors to detect left or right turns.**
-    **If any consecutive value has a different sign, then the direction is changing. Hence, compute a rolling multiplication.**

-    **Find out the location of direction change** (where ever indices are negative)
-    Compute the variance of negative indices
-    **If all rolling multiplication values > 0, then motion is circular**
-    If the variance of negative indices > threshold, then motion is non-circular
-    If % of negative values > threshold, then motion is non-circular
-    **Based on the 3 conditions above, the circular gesture is detected.**

Thus, **we can use Object Color Masking (to detect an object) and use efficient algebra-based concavity estimation (to detect a gesture).** For the purpose of the demo, we will deploy these algorithms on an RPi with a camera and see how it performs.

**If a circular motion is detected, then messages are pushed to people concerned and an alarm is triggered. Event trigger is demonstrated by flashing 'red' light on a Pimoroni Blinkt! signalled using  MQTT messages.**

**This is an efficient and practical solution for gesture detection on edge devices.** Probably the only downside may be the sensitivity to extreme lighting conditions or the need for an external object other than your body, to trigger the alarm.

To address the above drawback, we can also use gesture recognition models optimized by OpenVINO to recognize sign languages and trigger alerts. If you want to use a custom gesture then you can train your own and convert to intermediate representation using model optimizer.


https://user-images.githubusercontent.com/39004869/134632745-53bbf2fd-3a46-4b23-a51e-dd390fdc1972.mp4


However, some layers of such OpenVINO models are not supported by MYRIAD device as given in the table here. Hence, this module need to be hosted on a remote server as an API. Alternatively, we can train hand gesture classification model and convert to OpenVINO IR format to deploy on an SoC. **To conclude, we can consider the vector algebra model to be an efficient, cheap and generic solution to detect gestures.**


## References

1. https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
2. https://docs.openvinotoolkit.org/latest/omz_demos_face_recognition_demo_python.html
