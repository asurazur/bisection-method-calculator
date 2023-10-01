from pathlib import Path
import tkinter as tk
import pandas as pd
import re
from bisection import bisection
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, font, StringVar, filedialog, messagebox

OUTPUT_PATH = Path(__file__).parent
RELATIVE_PATH = "assets/frame0"
ASSETS_PATH = OUTPUT_PATH / RELATIVE_PATH


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def parse_fx(expression):
    # Replace "^" with "**"
    expression = expression.replace("^", "**")

    pattern = r"(\d)(x)"

    # Compile the regular expression
    regex = re.compile(pattern)

    # Replace all matches with "digit*x"
    return regex.sub(r"\1*\2", expression)

def change_entry(char):
    # Get the currently focused widget
    # if button entry, put char at cursor then put the cursor at the end
    focused_widget = window.focus_get()
    if isinstance(focused_widget, tk.Entry):
        cursor_position = focused_widget.index(tk.INSERT)
    else:
        return

    if char not in "sin()cos()x()%^*/" and focused_widget != fx_entry:
        if focused_widget in (x0_entry, x1_entry):
            if char in "-+":
                try:
                    first_char = focused_widget.get()[0]
                    # if negative, check if first char is negative. if negative do nothing else append
                    if char == "-" and first_char != "-" :
                        focused_widget.insert(0,char)
                    # if positive, check if the first char is negative. if negative remove negative
                    elif char == "+" and first_char == "-":
                        new_text = focused_widget.get()[1:]
                        focused_widget.delete(0, tk.END)  # Clear the current text
                        focused_widget.insert(0, new_text)

                except IndexError:
                    print("The string is empty, and there are no characters to access.")
                
            else:
                focused_widget.insert(cursor_position, char)
    elif focused_widget == fx_entry:
        current_equation = equation.get()
        try:
            if current_equation[-1] == char and char in "x()%^.*/+-" and len(current_equation):
                return  # Don't append the character if it's equal to the last character and in the specified set
        except:
            equation.set(current_equation + char)
        else:
            equation.set(current_equation + char)
    focused_widget.icursor(cursor_position + 1)
    print("{} key is pressed".format(char))

def validate_guess_input(P):
    # This function is called when the entry is being edited
    if P == "":
        return True

    if P.count('.') > 1:
        return False

    if not P[-1].isdigit() and P[-1] != '.':
        return False

    if any(char.isalpha() for char in P):
        return False

    return True

def validate_fx_input(P):
    valid_chars = "0123456789x^()%.*+-/"
    prev_char = None  # To keep track of the previous character
    for char in P:
        if char not in valid_chars:
            return False
        if char in "x()%^.*/+-" and char == prev_char:
            return False
        prev_char = char
    return True


def show_save_dialog(content_to_save):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w") as file:
                file.write(content_to_save)
            print(f"File saved as {file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")


def show_result(event=None):
    try:
        format_expression = parse_fx(equation.get())
        print(format_expression)
        expression = bisection(
            format_expression,
            float(guess1.get()),
            float(guess2.get()),
        )
        # print to r field the result and opens up a window which the user can export the interations
        if (expression.is_valid()):
            result = expression.solve()
            result_var.set(str(round(result, 6)))
            iterations = pd.DataFrame(expression.steps)
            iterations.index = iterations.index+1
            print(iterations)
            # Create the popup window
            popup_dialog = tk.Toplevel(window)
            popup_dialog.title("Iterations")
            try:
                popup_dialog.iconbitmap(
                    relative_to_assets("bisection_icon.ico"))
            except (FileNotFoundError, IOError):
                messagebox.showerror('FileNotFound', 'Icon File Missing')
            txt = "Iterations for: \n\nf(x) = {},\t x_0 = {},\t x_1 = {}\n\n{}\n\nRoot: {}".format(
                equation.get(), guess1.get(), guess2.get(), iterations, result)
            label = tk.Label(popup_dialog, text=txt)
            label.pack(padx=120, pady=40)
            export_button = tk.Button(
                popup_dialog, text="Export", command=lambda: show_save_dialog(txt)
            )
            export_button.pack(pady=10)
        else:
            result_var.set("Invalid Input")
    except:
        print("Invalid parameters")
        result_var.set("Invalid parameters")


def clear():
    guess1.set("")
    guess2.set("")
    result_var.set("")
    equation.set("")


if __name__ == "__main__":
    window = Tk()
    window.resizable(False, False)
    window.title("Bisection Method Calculator")
    window.geometry("725x652")
    window.configure(bg="#000000")
    window.bind("<Return>", show_result)
    try:
        icon = PhotoImage(file=relative_to_assets("bisection_icon.png"))
        window.tk.call('wm', 'iconphoto', window, icon)
    except (FileNotFoundError, IOError):
        messagebox.showerror('FileNotFound', 'Icon File Missing')

    guess1 = StringVar()
    guess2 = StringVar()
    equation = StringVar()
    result_var = StringVar()

    
    validate_guess_input_cmd = window.register(validate_guess_input)
    validate_fx_input_cmd = window.register(validate_fx_input)

    canvas = Canvas(
        window,
        bg="#000000",
        height=652,
        width=725,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    equal_button = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=show_result,
        relief="flat"
    )
    equal_button.place(
        x=545.0,
        y=556.0,
        width=161.0,
        height=70.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    divide_button = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("/"),
        relief="flat"
    )
    divide_button.place(
        x=635.0,
        y=194.0,
        width=70.0,
        height=70.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    close_par_button = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry(")"),
        relief="flat"
    )
    close_par_button.place(
        x=455.0,
        y=194.0,
        width=70.0,
        height=70.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    x_button = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("x"),
        relief="flat"
    )
    x_button.place(
        x=545.0,
        y=194.0,
        width=70.0,
        height=70.0
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    sine_button = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("sin()"),
        relief="flat"
    )
    sine_button.place(
        x=545.0,
        y=374.0,
        width=70.0,
        height=70.0
    )

    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    exponent_button = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("^"),
        relief="flat"
    )
    exponent_button.place(
        x=545.0,
        y=284.0,
        width=70.0,
        height=70.0
    )

    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    cosine_button = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("cos()"),
        relief="flat"
    )
    cosine_button.place(
        x=545.0,
        y=464.0,
        width=70.0,
        height=70.0
    )

    button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    open_par_button = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("("),
        relief="flat"
    )
    open_par_button.place(
        x=365.0,
        y=194.0,
        width=70.0,
        height=70.0
    )

    button_image_9 = PhotoImage(
        file=relative_to_assets("button_9.png"))
    clear_button = Button(
        image=button_image_9,
        borderwidth=0,
        highlightthickness=0,
        command=clear,
        relief="flat"
    )
    clear_button.place(
        x=275.0,
        y=194.0,
        width=70.0,
        height=70.0
    )

    button_image_10 = PhotoImage(
        file=relative_to_assets("button_10.png"))
    minus_button = Button(
        image=button_image_10,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("-"),
        relief="flat"
    )
    minus_button.place(
        x=635.0,
        y=374.0,
        width=70.0,
        height=71.0
    )

    button_image_11 = PhotoImage(
        file=relative_to_assets("button_11.png"))
    six_button = Button(
        image=button_image_11,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("6"),
        relief="flat"
    )
    six_button.place(
        x=455.0,
        y=374.0,
        width=70.0,
        height=71.0
    )

    button_image_12 = PhotoImage(
        file=relative_to_assets("button_12.png"))
    five_button = Button(
        image=button_image_12,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("5"),
        relief="flat"
    )
    five_button.place(
        x=365.0,
        y=374.0,
        width=70.0,
        height=71.0
    )

    button_image_13 = PhotoImage(
        file=relative_to_assets("button_13.png"))
    four_button = Button(
        image=button_image_13,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("4"),
        relief="flat"
    )
    four_button.place(
        x=275.0,
        y=374.0,
        width=70.0,
        height=71.0
    )

    button_image_14 = PhotoImage(
        file=relative_to_assets("button_14.png"))
    multiply_button = Button(
        image=button_image_14,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("*"),
        relief="flat"
    )
    multiply_button.place(
        x=635.0,
        y=284.0,
        width=70.0,
        height=70.0
    )

    button_image_15 = PhotoImage(
        file=relative_to_assets("button_15.png"))
    nine_button = Button(
        image=button_image_15,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("9"),
        relief="flat"
    )
    nine_button.place(
        x=455.0,
        y=284.0,
        width=70.0,
        height=70.0
    )

    button_image_16 = PhotoImage(
        file=relative_to_assets("button_16.png"))
    eight_button = Button(
        image=button_image_16,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("8"),
        relief="flat"
    )
    eight_button.place(
        x=365.0,
        y=284.0,
        width=70.0,
        height=70.0
    )

    button_image_17 = PhotoImage(
        file=relative_to_assets("button_17.png"))
    seven_button = Button(
        image=button_image_17,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("7"),
        relief="flat"
    )
    seven_button.place(
        x=275.0,
        y=284.0,
        width=70.0,
        height=70.0
    )

    button_image_18 = PhotoImage(
        file=relative_to_assets("button_18.png"))
    plus_button = Button(
        image=button_image_18,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("+"),
        relief="flat"
    )
    plus_button.place(
        x=635.0,
        y=465.0,
        width=70.0,
        height=71.0
    )

    button_image_19 = PhotoImage(
        file=relative_to_assets("button_19.png"))
    three_button = Button(
        image=button_image_19,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("3"),
        relief="flat"
    )
    three_button.place(
        x=455.0,
        y=465.0,
        width=70.0,
        height=71.0
    )

    button_image_20 = PhotoImage(
        file=relative_to_assets("button_20.png"))
    two_button = Button(
        image=button_image_20,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("2"),
        relief="flat"
    )
    two_button.place(
        x=365.0,
        y=465.0,
        width=70.0,
        height=71.0
    )

    button_image_21 = PhotoImage(
        file=relative_to_assets("button_21.png"))
    zero_button = Button(
        image=button_image_21,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("0"),
        relief="flat"
    )
    zero_button.place(
        x=365.0,
        y=556.0,
        width=70.0,
        height=71.0
    )

    button_image_22 = PhotoImage(
        file=relative_to_assets("button_22.png"))
    decimal_point_button = Button(
        image=button_image_22,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("."),
        relief="flat"
    )
    decimal_point_button.place(
        x=455.0,
        y=556.0,
        width=70.0,
        height=71.0
    )

    button_image_23 = PhotoImage(
        file=relative_to_assets("button_23.png"))
    one_button = Button(
        image=button_image_23,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("1"),
        relief="flat"
    )
    one_button.place(
        x=275.0,
        y=465.0,
        width=70.0,
        height=71.0
    )

    button_image_24 = PhotoImage(
        file=relative_to_assets("button_24.png"))
    modulo_button = Button(
        image=button_image_24,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_entry("%"),
        relief="flat"
    )
    modulo_button.place(
        x=275.0,
        y=556.0,
        width=70.0,
        height=71.0
    )

    fx_entry_image = PhotoImage(
        file=relative_to_assets("entry_4.png")
    )
    fx_entry_bg = canvas.create_image(
        226.0,
        125.0,
        image=fx_entry_image
    )
    fx_entry = Entry(
        textvariable=equation,
        bd=0,
        bg="#313131",
        fg="#FFFFFF",
        insertbackground="white",
        highlightthickness=0,
        font=font.Font(family="Inter", size=16),
        justify="center",
        validate="key",
        validatecommand=(validate_fx_input_cmd, "%P")
    )
    fx_entry.place(
        x=52.0,
        y=85.0+35,
        width=348.0,
        height=78.0 - 35
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        136.0,
        225.0,
        image=entry_image_1
    )
    x0_entry = Entry(
        textvariable=guess1,
        bd=0,
        bg="#313131",
        fg="#FFFFFF",
        insertbackground="white",
        highlightthickness=0,
        font=font.Font(family="Inter", size=16),
        justify="center",
        validate="key",
        validatecommand=(validate_guess_input_cmd, "%P")
    )
    x0_entry.place(
        x=52.0,
        y=190.0+30,
        width=168.0,
        height=68.0 - 30
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        136.0,
        320.0,
        image=entry_image_2
    )
    x1_entry = Entry(
        textvariable=guess2,
        bd=0,
        bg="#313131",
        fg="#FFFFFF",
        insertbackground="white",
        highlightthickness=0,
        font=font.Font(family="Inter", size=16),
        justify="center",
        validate="key",
    )
    x1_entry.place(
        x=52.0,
        y=285.0+30,
        width=168.0,
        height=68.0-30
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        580.0,
        128.0,
        image=entry_image_3
    )
    result_entry = Entry(
        textvariable=result_var,
        bd=0,
        bg="#FF9B00",
        fg="#FFFFFF",
        disabledbackground="#FF9B00",
        disabledforeground="#FFFFFF",
        state="disabled",
        highlightthickness=0,
        insertbackground="white",
        font=font.Font(family="Inter", size=16),
        justify="center"
    )
    result_entry.place(
        x=490.0,
        y=88.0+30,
        width=180.0,
        height=78.0-30
    )

    canvas.create_text(
        53.0,
        92.0,
        anchor="nw",
        text="f(x)",
        fill="#FFFFFF",
        font=("PlayfairDisplayItalic SemiBold", 24 * -1)
    )

    canvas.create_text(
        53.0,
        191.0,
        anchor="nw",
        text="x",
        fill="#FFFFFF",
        font=("PlayfairDisplayItalic SemiBold", 24 * -1)
    )

    canvas.create_text(
        53.0,
        285.0,
        anchor="nw",
        text="x",
        fill="#FFFFFF",
        font=("PlayfairDisplayItalic SemiBold", 24 * -1)
    )

    canvas.create_text(
        502.0,
        95.0,
        anchor="nw",
        text="r",
        fill="#FFFFFF",
        font=("PlayfairDisplayItalic SemiBold", 24 * -1)
    )

    canvas.create_text(
        64.0,
        199.0+5,
        anchor="nw",
        text="0",
        fill="#FFFFFF",
        font=("PlayfairDisplayItalic SemiBold", 16 * -1)
    )

    canvas.create_text(
        64.0,
        293.0+5,
        anchor="nw",
        text="1",
        fill="#FFFFFF",
        font=("PlayfairDisplayItalic SemiBold", 16 * -1)
    )

    canvas.create_text(
        29.0,
        22.0,
        anchor="nw",
        text="Bisection Method Calculator",
        fill="#FFFFFF",
        font=("Inter Medium", 24 * -1)
    )

    window.mainloop()
