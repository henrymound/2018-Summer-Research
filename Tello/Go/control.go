package main

import (
	"bufio"
	"fmt"
	"gobot.io/x/gobot"
	"gobot.io/x/gobot/platforms/dji/tello"
	"os"
	"os/exec"
	"strings"
	"time"
)

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

		// After 5 seconds, drone should have opened up a video channel.
		gobot.After(5*time.Second, func() {
			fmt.Println("Starting trick loop.")
			drone.TakeOff()
			fmt.Println("Take Off")

			// Get User Input
			reader := bufio.NewReader(os.Stdin)

			// Continually ask what flip to do or quit
			for true {
				fmt.Print("\nWhat Would You Like to Do?\n")
				fmt.Print("(m) Move\n(r) Rotate\n(f) Flips\n(s) Stop Motion\n(q) Quit\n")
				text, _ := reader.ReadString('\n')
				text = strings.Replace(text, "\n", "", -1)

				if text == "s" {
					fmt.Print("Stopping Movement...\n")
					drone.Forward(0)
					drone.Backward(0)
					drone.Up(0)
					drone.Down(0)
					drone.Clockwise(0)
					drone.CounterClockwise(0)
				}

				if text == "m" {
					// Get User Input
					moveBool := true
					reader := bufio.NewReader(os.Stdin)

					// Continually ask what flip to do or quit
					for moveBool {
						fmt.Print("\nWhere should I go?\n")
						fmt.Print("(u) Up\n(d) Down\n(f) Forward\n(b) Backward\n(l) Left\n(r) Right\n(q) Quit\n")
						text, _ := reader.ReadString('\n')
						text = strings.Replace(text, "\n", "", -1)

						if text == "u" {
							fmt.Print("How fast up should I go? (0-100)\n")
							var i int
							fmt.Scan(&i)
							drone.Up(i)
							i = 0
						}

						if text == "d" {
							fmt.Print("How fast down should I go? (0-100)\n")
							var i int
							fmt.Scan(&i)
							drone.Down(i)
							i = 0
						}

						if text == "f" {
							fmt.Print("How fast forward should I go? (0-100)\n")
							var i int
							fmt.Scan(&i)
							drone.Forward(i)
							i = 0
						}

						if text == "b" {
							fmt.Print("How fast backward should I go? (0-100)\n")
							var i int
							fmt.Scan(&i)
							drone.Backward(i)
							i = 0
						}

						if text == "l" {
							fmt.Print("How fast left should I go? (0-100)\n")
							var i int
							fmt.Scan(&i)
							drone.Left(i)
							i = 0
						}

						if text == "r" {
							fmt.Print("How fast right should I go? (0-100)\n")
							var i int
							fmt.Scan(&i)
							drone.Right(i)
							i = 0
						}

						if text == "s" {
							fmt.Print("Stopping Movement...\n")
							drone.Forward(0)
							drone.Backward(0)
							drone.Up(0)
							drone.Down(0)

						}

						if text == "q" {
							fmt.Print("Stopping Movement...\n")
							drone.Forward(0)
							drone.Backward(0)
							drone.Up(0)
							drone.Down(0)
							drone.Clockwise(0)
							drone.CounterClockwise(0)
							moveBool = false
						}

					}
				}

				if text == "r" {
					// Get User Input
					rotateBool := true
					reader := bufio.NewReader(os.Stdin)

					// Continually ask what flip to do or quit
					for rotateBool {
						fmt.Print("\nHow should I rotate?\n")
						fmt.Print("(c) Clockwise\n(cc) Counter Clockwise\n(q) Quit\n")
						text, _ := reader.ReadString('\n')
						text = strings.Replace(text, "\n", "", -1)

						if text == "c" {
							fmt.Print("How fast clockwise should I rotate? (0-100)\n")
							var i int
							fmt.Scan(&i)
							drone.Clockwise(i)
							i = 0
						}

						if text == "cc" {
							fmt.Print("How fast counterclockwise should I rotate? (0-100)\n")
							var i int
							fmt.Scan(&i)
							drone.CounterClockwise(i)
							i = 0
						}

						if text == "q" {
							fmt.Print("Stopping Movement...\n")
							drone.Forward(0)
							drone.Backward(0)
							drone.Up(0)
							drone.Down(0)
							drone.Clockwise(0)
							drone.CounterClockwise(0)
							rotateBool = false
						}
					}

				}

				if text == "f" {
					// Get User Input
					reader := bufio.NewReader(os.Stdin)

					// Continually ask what flip to do or quit
					for true {
						fmt.Print("What Flip Should I do?")
						fmt.Print("(l) Left, (r) Right, (b) Back, (f) Front, (bb) Bounce, (q) Quit\n")
						text, _ := reader.ReadString('\n')
						text = strings.Replace(text, "\n", "", -1)

						if text == "f" {
							drone.FrontFlip()
						}

						if text == "b" {
							drone.BackFlip()
						}

						if text == "l" {
							drone.LeftFlip()
						}

						if text == "r" {
							drone.RightFlip()
						}

						if text == "bb" {
							drone.Bounce()
						}

						if text == "q" {
							fmt.Println("Land")
							drone.Land()

							fmt.Println("Loop complete, terminating program.")
							os.Exit(3)
						}

					}
				}

				if text == "q" {
					fmt.Println("Land")
					drone.Land()

					fmt.Println("Flight complete. Terminating program.")
					os.Exit(3)
				}

				if text == "pq" {
					fmt.Println("Palm Landing...")
					drone.PalmLand()

					fmt.Println("Flight complete. Terminating program.")
					os.Exit(3)
				}

			}

		})

	}

	robot := gobot.NewRobot("tello",
		[]gobot.Connection{},
		[]gobot.Device{drone},
		work,
	)

	robot.Start()
}
