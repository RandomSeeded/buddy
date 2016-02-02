import Tkinter as tk
def keypress(event):
    if event.keysym == 'Escape':
        root.destroy()
    x = event.char
    if x == "w":
        print "blaw blaw blaw"
    elif x == "a":
        print "blaha blaha blaha"
    elif x == "s":
        print "blash blash blash"
    elif x == "d":
        print "blad blad blad"
    else:
        print x
root = tk.Tk()
print "Press a key (Escape key to exit):"
root.bind_all('<Key>', keypress)
# don't show the tk window
root.withdraw()
root.mainloop()
