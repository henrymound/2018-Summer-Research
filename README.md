# Tello
*All Go files that give live video require mplayer.*

**To Install mplayer:**
- Mac: ``` brew install mplayer ```
- Linux: ``` apt install mplayer ``` (may require sudo)

## Tello Programs
**TakeoffAndLand.go**: Establishes a video connection and performs a simple takeoff and landing.


**control.go**: Gives full drone control via keyboard input commands. The controls are as follows:
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
