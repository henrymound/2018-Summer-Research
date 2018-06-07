package main

 import (
     "fmt"
     "os/exec"
     "time"
     "os"
     "gobot.io/x/gobot"
     "gobot.io/x/gobot/platforms/dji/tello"
 )

 func main() {
     drone := tello.NewDriver("0000")

     work := func() {
         mplayer := exec.Command("mplayer","-fps", "25", "-")
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
              //After 15 seconds in the air
              gobot.After(10*time.Second, func() {
                fmt.Println("Front Flip")
                drone.FrontFlip()

                gobot.After(5*time.Second, func() {
                  fmt.Println("Back Flip")
                  drone.BackFlip()

                  gobot.After(5*time.Second, func() {
                    fmt.Println("Right Flip")
                    drone.RightFlip()

                    gobot.After(5*time.Second, func() {
                      fmt.Println("Left Flip")
                      drone.LeftFlip()

                      gobot.After(5*time.Second, func() {

                        fmt.Println("Land")
                        drone.Land()
                        
                        fmt.Println("Loop complete, terminating program.")
                        os.Exit(3)
                      })
                    })
                  })
                })
              })
         })





     }

     robot := gobot.NewRobot("tello",
         []gobot.Connection{},
         []gobot.Device{drone},
         work,
     )

     robot.Start()
 }
