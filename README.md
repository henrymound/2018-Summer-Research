# 2018 Summer Research
This summer Professor Jason Grant and his research assistant, Henry Mound, are exploring the application of drone-based computer vision for crowd behavior analysis. Specifically, they are analyzing holistic motion of crowds to detect regions of dominant flow and to detect abnormal motion within a scene. By using a technique called optical flow, they are able to analyze the apparent motion of objects in a scene by calculating the displacement vectors between points in consecutive frames of video.

The team is working with various hardware configurations and computer vision platforms. Their findings will help inform what technologies Professor Grant will teach in his new robotics class, which will be offered beginning in the Spring semester of 2019.

|                               | C# | Python | Go | Java |
|-------------------------------|----|--------|----|------|
| Uncompressed Video Stream     | ✓  | ✗      | ✓  | ✗    |
| Facial Tracking               | ✘  | ✗      | ✓  | ✗    |
| Optical Flow & Edge Detection | ✗  | ✓      | ✗  | ✗    |
| Multiple Tello Control        | ✗  | ✓      | ✗  | ✓    |
| Game Controller Support       | ✓  | ✓      | ✓  | ✗    |

## Tello Swarm
Check out [Adventures with DJI Ryze Tello: Controlling a Tello Swarm](https://medium.com/@henrymound/adventures-with-dji-ryze-tello-controlling-a-tello-swarm-1bce7d4e045d)

## Tello
*All Go files that give live video require mplayer.*

**To Install mplayer:**
- Mac: ``` brew install mplayer ```
- Linux: ``` apt install mplayer ``` (may require sudo)

### Tello Programs
**TakeoffAndLand.go**: Establishes a video connection and performs a simple takeoff and landing.


**control.go**: Gives full drone control via keyboard input commands. Each command must be typed via the command line followed by pressing enter. The controls are as follows:
  - **(m) Move**
    - ```(u) Up```
    - ```(d) Down```
    - ```(f) Forward```
    - ```(b) Backward```
    - ```(l) Left```
    - ```(r) Right```
    - ```(q) Quit```
  - **(r) Rotate**
    - ```(c) Clockwise```
    - ```(cc) Counter Clockwise```
    - ```(q) Quit```
  - **(f) Flips**
    - ```(l) Left```
    - ```(r) Right```
    - ```(b) Back```
    - ```(f) Front```
    - ```(bb) Bounce```
    - ```(q) Quit```
  - **(s) Stop Motion**
  - **(q) Quit**

**ps4.go**: Gives full driving drone control via keyboard input. The keyboard input can be mapped to a game controller if desired. **GLOBAL_SPEED** should be set before running. GLOBAL_SPEED is the speed at which the drone will move (between 0 and 100) when given input. The button mapping is as follows:
- **Up Arrow:** Moves drone forward
- **Down Arrow:** Moves drone backward
- **Left Arrow:** Moves drone left
- **Right Arrow:** Moves drone right
- **Space:** Moves drone up
- **F1:** Moves drone down
- **F2:** Rotates drone clockwise
- **F3:** Rotates drone counterclockwise
- **Enter:** Halts drone movement
- **Tab:** Halts drone movement and lands
