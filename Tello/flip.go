package main

 import (
     "fmt"
     "os/exec"
     "time"
     "os"
     "bufio"
     "strings"
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

              // Get User Input
              reader := bufio.NewReader(os.Stdin)

              // Continually ask what flip to do or quit
              for(true){
                fmt.Print("What Would You Like to Do??")
                fmt.Print("(m) Move, (r) Rotate, (f) Flips, (q) Quit\n")
                text, _ := reader.ReadString('\n')
                text = strings.Replace(text, "\n", "", -1)

                if(text == "m"){

                }

                if(text == "r"){

                }

                if(text == "f"){
                  flips()
                }

                if(text == "q"){
                  fmt.Println("Land")
                  drone.Land()

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

 func flips(){
   // Get User Input
   reader := bufio.NewReader(os.Stdin)

   // Continually ask what flip to do or quit
   for(true){
     fmt.Print("What Flip Should I do?")
     fmt.Print("(l) Left, (r) Right, (b) Back, (f) Front, (bb) Bounce, (q) Quit\n")
     text, _ := reader.ReadString('\n')
     text = strings.Replace(text, "\n", "", -1)

     if(text == "f"){
       drone.FrontFlip()
     }

     if(text == "b"){
       drone.BackFlip()
     }

     if(text == "l"){
       drone.LeftFlip()
     }

     if(text == "r"){
       drone.RightFlip()
     }

     if(text == "bb"){
       drone.Bounce()
     }

     if(text == "q"){
       fmt.Println("Land")
       drone.Land()

       fmt.Println("Loop complete, terminating program.")
       os.Exit(3)
     }

   }
 }

 func move(){
   // Get User Input
   reader := bufio.NewReader(os.Stdin)

   // Continually ask what flip to do or quit
   for(true){
     fmt.Print("Where should I go, master?")
     fmt.Print("(u) Up, (d) Down, (f) Forward, (b) Backward, (l) Left, (r) Right, (q) Quit\n")
     text, _ := reader.ReadString('\n')
     text = strings.Replace(text, "\n", "", -1)

     if(text == "f"){
       drone.FrontFlip()
     }

     if(text == "b"){
       drone.BackFlip()
     }

     if(text == "l"){
       drone.LeftFlip()
     }

     if(text == "r"){
       drone.RightFlip()
     }

     if(text == "q"){
       fmt.Println("Land")
       drone.Land()

       fmt.Println("Loop complete, terminating program.")
       os.Exit(3)
     }

   }
 }
