package main

import (
	"fmt"
	term "github.com/nsf/termbox-go"
	"gobot.io/x/gobot"
	"gobot.io/x/gobot/platforms/dji/tello"
	"os"
	"os/exec"
	"time"
)

func reset() {
	term.Sync() // cosmestic purpose
}

var forwardPressed = false
var backwardPressed = false
var leftPressed = false
var rightPressed = false
var upPressed = false
var downPressed = false

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
					//fmt.Println("Up")
					forwardPressed = true
					backwardPressed = false
				case term.KeyArrowDown: // Move drone backward
					//fmt.Println("Down")
					backwardPressed = true
					forwardPressed = false
				case term.KeyArrowLeft: // Move drone left
					//fmt.Println("Left")
					leftPressed = true
					rightPressed = false
				case term.KeyArrowRight: // Move drone right
					//fmt.Println("Right")
					rightPressed = true
					leftPressed = false
				case term.KeySpace: // Move drone up
					//fmt.Println("Space")
					upPressed = true
					downPressed = false
				case term.KeyF1: // Move drone down
					//fmt.Println("Backspace")
					downPressed = true
					upPressed = false
				case term.KeyEnter:
					//fmt.Println("Enter") // Stop drone movement
					upPressed = false
					downPressed = false
					forwardPressed = false
					backwardPressed = false
					leftPressed = false
					rightPressed = false
				case term.KeyTab: // Land drone
					fmt.Println("Landing...")
					drone.Land()
					os.Exit(3)
				default:
					// we only want to read a single character or one key pressed event
					fmt.Println("ASCII : ", ev.Ch)
				}

				// Move drone based on boolean values
				if forwardPressed{
					drone.Forward(100)
					fmt.Println("Forward")
				}else{
					drone.Forward(0)
				}

				if backwardPressed{
					drone.Backward(100)
					fmt.Println("Backward")
				}else{
					drone.Backward(0)
				}

				if leftPressed{
					drone.Left(100)
					fmt.Println("Left")
				}else{
					drone.Left(0)
				}

				if rightPressed{
					drone.Right(100)
					fmt.Println("Right")
				}else{
					drone.Right(0)
				}

				if upPressed{
					drone.Up(100)
					fmt.Println("Up")
				}else{
					drone.Up(0)
				}

				if downPressed{
					drone.Down(100)
					fmt.Println("Down")
				}else{
					drone.Down(0)
				}

				if !downPressed &&
						!upPressed &&
						!forwardPressed &&
						!backwardPressed &&
						!leftPressed &&
						!rightPressed{
							print("Halt")
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
