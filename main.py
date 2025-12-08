import tkinter


def main():

    button_values = [
    [ "AC", "+/-", "%", "/" ],
    [ "7", "8", "9", "*" ],
    [ "4", "5", "6", "-" ],
    [ "1", "2", "3", "+" ],
    [ "0", ".", "√", "="]
    ]

    right_symbol = ["/", "*", "-", "+"]
    top_symbol = ["AC", "+/-", "%"]

    row_count = len(button_values)
    column_count = len(button_values[0])

    light_grey = "#D4D4D2"
    color_black = "#1C1C1C"
    color_dark_grey = "#505050"
    color_orange = "#FF9500"
    color_white = "#FFFFFF"

    window = tkinter.Tk()
    window.title("Calculator")
    window.geometry("350x560")
    window.resizable(False,False)

    frame = tkinter.Frame(window)
    label = tkinter.Label(frame,text="0",font=('Calibri',30),background=color_black,
                          foreground=color_white,anchor="e",height=8)
    label.grid(row=0,column=0,columnspan=column_count,sticky="we")


    for row in range(row_count):
        for column in range(column_count):
            value = button_values[row][column]
            button = tkinter.Button(frame, text=value,font=("Helvetica",5),
                                    height=6,
                                    width=10,
                                    command= lambda value=value: button_clicked(value))
            button.grid(row=row+1,column=column)

            if value in right_symbol:
                button.configure(background=color_orange)
            elif value in top_symbol:
                button.configure(background=light_grey)
            else:
                button.configure(background=color_dark_grey,foreground=color_white)

    frame.pack()
    

    def button_clicked(value):
        pass

    window.update()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_x = int((screen_width / 2) - (window_width / 2))
    window_y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    window.mainloop()




if __name__ == "__main__":
    main()
