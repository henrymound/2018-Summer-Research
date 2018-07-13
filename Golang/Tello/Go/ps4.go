package main

import (
	"fmt"
	term "github.com/nsf/termbox-go"
	"gobot.io/x/gobot"
	"gobot.io/x/gobot/platforms/dji/tello"
	"os"
	"os/exec"
	"strconv"
	"time"
	"image"
  "image/png"
	"bytes"
)

func reset() {
	term.Sync() // cosmestic purpose
}

var GLOBAL_SPEED = 100

var forward = 0
var backward = 0
var left = 0
var right = 0
var up = 0
var down = 0
var clockwise = 0
var counterclockwise = 0

func main() {

	drone := tello.NewDriver("0000")

	work := func() {
		mplayer := exec.Command("mplayer", "-fps", "25", "-")
		mplayerIn, _ := mplayer.StdinPipe()
		if err := mplayer.Start(); err != nil {
			fmt.Println(err)
			return
		}

		drone.On(tello.ConnectedEvent, func(data interface{}) {
			fmt.Println("Connected")
			drone.StartVideo()
			drone.SetVideoEncoderRate(5)
			gobot.Every(100*time.Millisecond, func() {
				drone.StartVideo()
			})
		})

		drone.On(tello.VideoFrameEvent, func(data interface{}) {
			pkt := data.([]byte)


			if _, err := mplayerIn.Write(pkt); err != nil {
				fmt.Println(err)
			}
		})
	}

	gobot.After(5*time.Second, func() {
		drone.TakeOff()
		fmt.Println("Take Off")
		loopBool := true
		fmt.Println("Enter any key to see their ASCII code or press ESC button to quit")

		err := term.Init()
		if err != nil {
			panic(err)
		}

		defer term.Close()

		for loopBool {
			switch ev := term.PollEvent(); ev.Type {
			case term.EventKey:
				switch ev.Key {
				case term.KeyEsc:
					loopBool = false
				case term.KeyArrowUp: // Move drone forward
					//fmt.Println("Forward")
					up = 0
					down = 0
					forward = 0
					backward = 0
					left = 0
					right = 0
					clockwise = 0
					counterclockwise = 0
					forward = GLOBAL_SPEED
				case term.KeyArrowDown: // Move drone backward
					//fmt.Println("Backward")
					up = 0
					down = 0
					forward = 0
					backward = 0
					left = 0
					right = 0
					clockwise = 0
					counterclockwise = 0
					backward = GLOBAL_SPEED
				case term.KeyArrowLeft: // Move drone left
					//fmt.Println("Left")
					up = 0
					down = 0
					forward = 0
					backward = 0
					left = 0
					right = 0
					clockwise = 0
					counterclockwise = 0
					left = GLOBAL_SPEED
				case term.KeyArrowRight: // Move drone right
					//fmt.Println("Right")
					up = 0
					down = 0
					forward = 0
					backward = 0
					left = 0
					right = 0
					right = GLOBAL_SPEED
				case term.KeySpace: // Move drone up
					//fmt.Println("Up")
					up = 0
					down = 0
					forward = 0
					backward = 0
					left = 0
					right = 0
					clockwise = 0
					counterclockwise = 0
					up = GLOBAL_SPEED
				case term.KeyF1: // Move drone down
					//fmt.Println("Down")
					up = 0
					down = 0
					forward = 0
					backward = 0
					left = 0
					right = 0
					clockwise = 0
					counterclockwise = 0
					down = GLOBAL_SPEED
				case term.KeyEnter:
					fmt.Println("Halt") // Stop drone movement
					up = 0
					down = 0
					forward = 0
					backward = 0
					left = 0
					right = 0
					clockwise = 0
					counterclockwise = 0
					drone.Forward(forward)
					drone.Backward(backward)
					drone.Left(left)
					drone.Right(right)
					drone.Up(up)
					drone.Down(down)
					drone.Clockwise(clockwise)
					drone.CounterClockwise(counterclockwise)
				case term.KeyTab: // Land drone
					fmt.Println("Halting and Landing...")
					up = 0
					down = 0
					forward = 0
					backward = 0
					left = 0
					right = 0
					clockwise = 0
					counterclockwise = 0
					loopBool = false
					drone.Land()
					os.Exit(3)
				case term.KeyF2: // Rotate drone clockwise
					//fmt.Println("Down")
					up = 0
					down = 0
					forward = 0
					backward = 0
					left = 0
					right = 0
					clockwise = 100
					counterclockwise = 0
				case term.KeyF3: // Rotate drone counterclockwise
					//fmt.Println("Down")
					up = 0
					down = 0
					forward = 0
					backward = 0
					left = 0
					right = 0
					clockwise = 0
					counterclockwise = 100
				default:
					// we only want to read a single character or one key pressed event
					fmt.Println("ASCII : ", ev.Ch)
				}

				reset() // Clear terminal
				fmt.Println("Forward: " + strconv.Itoa(forward))
				fmt.Println("Backward: " + strconv.Itoa(backward))
				fmt.Println("Left: " + strconv.Itoa(left))
				fmt.Println("Right: " + strconv.Itoa(right))
				fmt.Println("Up: " + strconv.Itoa(up))
				fmt.Println("Down: " + strconv.Itoa(down))
				fmt.Println("Clockwise: " + strconv.Itoa(clockwise))
				fmt.Println("CounterClockwise: " + strconv.Itoa(counterclockwise))

				if forward != 0{
					drone.Forward(forward)
				}
				if backward != 0{
					drone.Backward(backward)
				}
				if left != 0{
					drone.Left(left)
				}
				if right != 0{
					drone.Right(right)
				}
				if up != 0{
					drone.Up(up)
				}
				if down != 0{
					drone.Down(down)
				}
				if clockwise != 0{
					drone.Clockwise(clockwise)
				}
				if counterclockwise != 0{
					drone.CounterClockwise(counterclockwise)
				}

			case term.EventError:
				panic(ev.Err)

			}
		}
	})

	robot := gobot.NewRobot("tello",
		[]gobot.Connection{},
		[]gobot.Device{drone},
		work,
	)

	robot.Start()

}
