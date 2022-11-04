def hi():
    # other code...
    hi.bye = 42  # Create function attribute.
    sigh = 10

hi()
print(hi.bye)  # -> 42