package main

import (
	"image"
	"image/color"
	"image/draw"
	"sync"

	"golang.org/x/exp/shiny/driver"
	"golang.org/x/exp/shiny/screen"
	"golang.org/x/mobile/event/key"
	"golang.org/x/mobile/event/lifecycle"
	"golang.org/x/mobile/event/mouse"
	"golang.org/x/mobile/event/paint"
	"golang.org/x/mobile/event/size"
)

var wg sync.WaitGroup
var winSize = image.Pt(1920, 1080)

var cache []image.Rectangle

func init() {
	cache = make([]image.Rectangle, 0, 1024)
}
func flushcache() {
	cache = cache[:0]
}

func Draw(dst draw.Image, r image.Rectangle, src image.Image, sp image.Point) {
	cache = append(cache, r)
	draw.Draw(dst, r, src, sp, draw.Src)
}

func main() {
	driver.Main(func(src screen.Screen) {
		win, _ := src.NewWindow(&screen.NewWindowOptions{winSize.X, winSize.Y})
		focused := false
		focused = focused
		buf, err := src.NewBuffer(winSize)
		if err != nil {
			panic(err)
		}
		draw.Draw(buf.RGBA(), buf.RGBA().Bounds(), Yellow, image.ZP, draw.Src)
		tx, err := src.NewTexture(winSize)
		if err != nil {
			panic(err)
		}
		paintfn := func() {
			tx.Upload(image.ZP, buf, buf.Bounds())
			win.Copy(buf.Bounds().Min, tx, tx.Bounds(), screen.Src, nil)
			win.Publish()
		}
		// lambda to paint only rectangles changed during a sweep of the mouse
		paintcache := func() {
			wg.Add(len(cache))
			for _, r := range cache {
				go func(r image.Rectangle) {
					tx.Upload(r.Min, buf, r)
					wg.Done()
				}(r)
			}
			wg.Wait()
			wg.Add(len(cache))
			for _, r := range cache {
				go func(r image.Rectangle) {
					pt := r.Min

					// Uncomment the following two statements and it works
					// pt.X *= 2
					// pt.Y *= 2

					win.Copy(pt, tx, r, screen.Src, nil)
					wg.Done()
				}(r)
			}
			wg.Wait()
			win.Publish()
			flushcache()
		}
		var drawdot bool
		for {
			switch e := win.NextEvent().(type) {
			case mouse.Event:
				pt := image.Pt(int(e.X), int(e.Y))
				if e.Button == 1 || drawdot {
					if e.Direction == mouse.DirRelease {
						drawdot = false
					} else {
						drawdot = true
						Draw(buf.RGBA(), image.Rect(0, 0, 5, 5).Add(pt), Mauve, image.ZP)
						win.Send(paint.Event{})
					}
				}
			case key.Event:
			case size.Event:
				paintfn()
				flushcache()
			case paint.Event:
				paintcache()
			case lifecycle.Event:
				if e.To == lifecycle.StageDead {
					return
				}
				// NT doesn't repaint the window if another window covers it
				if e.Crosses(lifecycle.StageFocused) == lifecycle.CrossOff {
					focused = false
				} else if e.Crosses(lifecycle.StageFocused) == lifecycle.CrossOn {
					focused = true
				}
			}
		}
	})
}

var (
	Red    = image.NewUniform(color.RGBA{255, 0, 0, 255})
	Green  = image.NewUniform(color.RGBA{0, 255, 0, 255})
	Blue   = image.NewUniform(color.RGBA{0, 192, 192, 255})
	Cyan   = image.NewUniform(color.RGBA{0xAA, 0xAA, 0xFF, 255})
	White  = image.NewUniform(color.RGBA{255, 255, 255, 255})
	Yellow = image.NewUniform(color.RGBA{255, 255, 224, 255})
	Gray   = image.NewUniform(color.RGBA{66, 66, 66, 255})
	Mauve  = image.NewUniform(color.RGBA{128, 66, 193, 255})
)
