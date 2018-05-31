package main

 import (
     "fmt"
     "os/exec"
     "time"

     "gobot.io/x/gobot"
     "gobot.io/x/gobot/platforms/dji/tello"
 )

 func main() {
     drone := tello.NewDriver("8891")

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

         drone.TakeOff()
         fmt.Println("Take Off")

         gobot.After(5*time.Second, func() {
             drone.Land()
         })

         drone.On(tello.VideoFrameEvent, func(data interface{}) {
             pkt := data.([]byte)
             if _, err := mplayerIn.Write(pkt); err != nil {
                 fmt.Println(err)
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
