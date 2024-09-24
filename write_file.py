def add_new_line(filename, text):
    with open(filename, 'a') as f:
        f.write(text)
