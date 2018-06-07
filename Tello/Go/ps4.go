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

var forwardPressed = false
var backwardPressed = false
var leftPressed = false
var rightPressed = false
var upPressed = false
var downPressed = false

func reset() {
	term.Sync() // cosmestic purpose
}

func checkKeys() {
	switch ev := term.PollEvent(); ev.Type {
	case term.EventKey:
		switch ev.Key {
		case term.KeyEsc:
			loopBool = false
		case term.KeyF1:
			fmt.Println("F1")
		case term.KeyArrowUp:
			fmt.Println("Arrow Up pressed")
		case term.KeyArrowDown:
			fmt.Println("Arrow Down pressed")
		case term.KeyArrowLeft:
			fmt.Println("Arrow Left pressed")
		case term.KeyArrowRight:
			fmt.Println("Arrow Right pressed")
		case term.KeySpace:
			fmt.Println("Space pressed")
		case term.KeyBackspace:
			fmt.Println("Backspace pressed")
		case term.KeyEnter:
			fmt.Println("Enter pressed")
		default:
			// we only want to read a single character or one key pressed event
			fmt.Println("ASCII : ", ev.Ch)
		}
	case term.EventError:
		panic(ev.Err)
	}
}

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
				checkKeys()
			})
		})

		drone.On(tello.VideoFrameEvent, func(data interface{}) {
			pkt := data.([]byte)
			if _, err := mplayerIn.Write(pkt); err != nil {
				fmt.Println(err)
			}
		})
	}

	//Run the main control

	gobot.After(5*time.Second, func() {
		drone.TakeOff()
		fmt.Println("Take Off")

	})

	robot := gobot.NewRobot("tello",
		[]gobot.Connection{},
		[]gobot.Device{drone},
		work,
	)

	robot.Start()

}
