package main

import (
  "github.com/azul3d/keyboard"
)

func main() {

	watcher := keyboard.NewWatcher()
  for true{
	   // Query for the map containing information about all keys
	    status := watcher.States()

      left := status[keyboard.ArrowLeft]
  	  if left == keyboard.Down {
         print("Left down")
  		     // The arrow to left is being held down
  		       // Do something!
  	  }
  }

}
