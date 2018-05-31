package main

  import (
      "time"
      "math/rand"
      "gobot.io/x/gobot"
      "gobot.io/x/gobot/platforms/dji/tello"
      "strconv"
  )

  func main() {
      drone := tello.NewDriver(strconv.Itoa(rand.Intn(10000)))

      work := func() {
          drone.TakeOff()

          gobot.After(5*time.Second, func() {
              drone.FrontFlip()
          })

          gobot.After(10*time.Second, func() {
              drone.BackFlip()
          })

          gobot.After(15*time.Second, func() {
              drone.Land()
          })
      }

      robot := gobot.NewRobot("tello",
          []gobot.Connection{},
          []gobot.Device{drone},
          work,
      )

      robot.Start()
  }
