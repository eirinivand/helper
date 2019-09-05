def open_file(file_to_open):
    try:
        my_file = open(file_to_open, "r")
        return print(my_file.read())
    except Exception as ex:
        return print(ex)
