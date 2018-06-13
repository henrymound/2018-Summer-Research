package main

import (
	"fmt"
	term "github.com/nsf/termbox-go"
	"gobot.io/x/gobot"
	"gobot.io/x/gobot/platforms/dji/tello"
	"os/exec"
  "os"
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
        drone.Forward(0)
        drone.Backward(0)
        drone.Left(0)
        drone.Right(0)
        drone.Clockwise(0)
        drone.CounterClockwise(0)
        drone.Up(0)
        drone.Down(0)
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
      case term.KeyF1:
        reset()
        fmt.Println("F1 pressed")
        drone.Forward(0)
        drone.Backward(0)
        drone.Left(0)
        drone.Right(0)
        drone.Up(0)
        drone.Down(0)
        drone.Clockwise(0)
        drone.CounterClockwise(0)
        fmt.Println("Stopping movement.")
			case term.KeyArrowUp:
				reset()
				fmt.Println("Arrow Up pressed")
        drone.Forward(100)
			case term.KeyArrowDown:
				reset()
				fmt.Println("Arrow Down pressed")
        drone.Backward(100)
			case term.KeyArrowLeft:
				reset()
				fmt.Println("Arrow Left pressed")
        drone.Left(100)
			case term.KeyArrowRight:
				reset()
				fmt.Println("Arrow Right pressed")
        drone.Right(100)
			case term.KeySpace:
				reset()
        fmt.Println("Space pressed")
        drone.Forward(0)
        drone.Backward(0)
        drone.Left(0)
        drone.Right(0)
        drone.Up(0)
        drone.Down(0)
        drone.Clockwise(0)
        drone.CounterClockwise(0)
        drone.Land()
        fmt.Println("Loop complete, terminating program.")
        os.Exit(3)
			case term.KeyBackspace:
				reset()
				fmt.Println("Backspace pressed")
			case term.KeyEnter:
				reset()
				fmt.Println("Enter pressed")
			case term.KeyTab:
				reset()
				fmt.Println("Tab pressed")
      case term.KeyPgup:
        reset()
        fmt.Println("Page Up pressed")
        drone.Up(100)
      case term.KeyPgdn:
        reset()
        fmt.Println("Page Down pressed")
        drone.Down(100)
      case term.KeyF11:
        reset()
        fmt.Println("F11 pressed (CounterClockwise Rotate)")
        drone.CounterClockwise(100)
      case term.KeyF12:
        reset()
        fmt.Println("F12 pressed (Clockwise Rotate)")
        drone.Clockwise(100)
			default:
				// we only want to read a single character or one key pressed event
				reset()
				fmt.Println("ASCII : ", ev.Ch)

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
