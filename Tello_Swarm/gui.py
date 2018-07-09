from tkinter import *

root = Tk()

#wifiInterface, port, videoPort, conReqPort
wifiInterfaceLabel = Label(root, text="Wifi Interface: ")
wifiInterfaceLabel.grid(row=1, column=0, sticky=E)
wifiInterfaceText = Text(root, height=1, width=10)
wifiInterfaceText.grid(row=1, column=1, sticky=W)
wifiInterfaceText.insert(END, "wlp1s0")

#port
portLabel = Label(root, text="Port: ")
portLabel.grid(row=2, column=0, sticky=E)
portText = Text(root, height=1, width=10)
portText.grid(row=2, column=1, sticky=W)
portText.insert(END, "9000")

#videoPort
videoPortLabel = Label(root, text="Video Port: ")
videoPortLabel.grid(row=3, column=0, sticky=E)
videoPortText = Text(root, height=1, width=10)
videoPortText.grid(row=3, column=1, sticky=W)
videoPortText.insert(END, "6038")
mainloop()
