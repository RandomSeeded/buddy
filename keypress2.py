from showkey import ShowKey

def key_pressed(kc):
    print "Key pressed - keycode: %d" % kc

def key_released(kc):
    print "Key released - keycode: %d" % kc

def alt_q(arg):
    print "Alt Q was pressed"

sk = ShowKey()
sk.addKeyAction("*p", key_pressed)  # adds handler for all key press
sk.addKeyAction("*r", key_released) # adds handler for all key release
sk.addKeyAction([16, 56], alt_q)    # adds handler for Alt-Q comb.
sk.run()

