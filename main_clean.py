from tkinter import *
from tkinter import font

# Configuration constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 550
BUTTON_SPACING = 3
BUTTON_HEIGHT = 2
FONT_SIZE = 14

# Color scheme - Gray and Blue only
COLORS = {
    'bg_main': '#1e1e1e',
    'bg_input': '#2d2d2d',
    'bg_frame': '#1e1e1e',
    'bg_number': '#424242',
    'bg_operator': '#2196F3',  # Blue for operators
    'bg_clear': '#607D8B',     # Blue-gray for clear
    'bg_equals': '#1976D2',    # Darker blue for equals
    'fg_text': '#ffffff',
    'border_input': '#2196F3',
    'active_number': '#616161',
    'active_operator': '#1976D2',
    'active_clear': '#546E7A',
    'active_equals': '#1565C0'
}

def center_window(window, width, height):
    """Center the window on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def create_button(parent, text, bg_color, active_color, command, row, column, columnspan=1, width=7):
    """Create a standardized button with consistent styling"""
    return Button(
        parent, 
        text=text, 
        fg=COLORS['fg_text'],
        width=width, 
        height=BUTTON_HEIGHT, 
        bd=0, 
        bg=bg_color, 
        cursor="hand2",
        font=('Segoe UI', FONT_SIZE, 'bold'), 
        activebackground=active_color, 
        activeforeground=COLORS['fg_text'],
        relief='flat',
        command=command
    ).grid(row=row, column=column, columnspan=columnspan, padx=BUTTON_SPACING, pady=BUTTON_SPACING, sticky='nsew')

# Create main window
win = Tk()
win.title("Modern Calculator")
win.configure(bg=COLORS['bg_main'])
win.resizable(1, 1)
win.minsize(350, 500)

# Center the window on screen
center_window(win, WINDOW_WIDTH, WINDOW_HEIGHT)

###################Starting with functions ####################
# 'btn_click' function : 
# This Function continuously updates the 
# input field whenever you enter a number

def btn_click(item):
    global expression
    expression = expression + str(item)
    input_text.set(expression)

# 'bt_clear' function :This is used to clear 
# the input field

def bt_clear(): 
    global expression 
    expression = "" 
    input_text.set("")
 
# 'bt_equal':This method calculates the expression 
# present in input field
 
def bt_equal():
    global expression
    result = str(eval(expression)) 
    input_text.set(result)
    expression = ""
 
expression = ""
 
# 'StringVar()' :It is used to get the instance of input field
 
input_text = StringVar()
 
# Let us creating a frame for the input field
 
input_frame = Frame(win, width=WINDOW_WIDTH, height=80, bd=0, highlightbackground="#333333",
 highlightcolor=COLORS['border_input'], highlightthickness=2, bg=COLORS['bg_input'])
 
input_frame.pack(side=TOP, pady=5)
 
#Let us create a input field inside the 'Frame'
 
input_field = Entry(input_frame, font=('Segoe UI', 20, 'bold'), 
textvariable=input_text, width=20, bg=COLORS['bg_input'], bd=0, justify=RIGHT,
fg=COLORS['fg_text'], insertbackground=COLORS['border_input'])
 
input_field.grid(row=0, column=0)
 
input_field.pack(ipady=15, padx=10)

 
btns_frame = Frame(win, width=WINDOW_WIDTH, height=400, bg=COLORS['bg_frame'])
 
btns_frame.pack(pady=5)

# Configure grid weights for responsive design
for i in range(4):
    btns_frame.grid_columnconfigure(i, weight=1)
for i in range(5):
    btns_frame.grid_rowconfigure(i, weight=1)
 
# Create all buttons using the standardized function
# Row 0
create_button(btns_frame, "C", COLORS['bg_clear'], COLORS['active_clear'], 
              lambda: bt_clear(), 0, 0, columnspan=3, width=23)
create_button(btns_frame, "÷", COLORS['bg_operator'], COLORS['active_operator'], 
              lambda: btn_click("/"), 0, 3)

# Row 1  
create_button(btns_frame, "7", COLORS['bg_number'], COLORS['active_number'], 
              lambda: btn_click(7), 1, 0)
create_button(btns_frame, "8", COLORS['bg_number'], COLORS['active_number'], 
              lambda: btn_click(8), 1, 1)
create_button(btns_frame, "9", COLORS['bg_number'], COLORS['active_number'], 
              lambda: btn_click(9), 1, 2)
create_button(btns_frame, "×", COLORS['bg_operator'], COLORS['active_operator'], 
              lambda: btn_click("*"), 1, 3)

# Row 2
create_button(btns_frame, "4", COLORS['bg_number'], COLORS['active_number'], 
              lambda: btn_click(4), 2, 0)
create_button(btns_frame, "5", COLORS['bg_number'], COLORS['active_number'], 
              lambda: btn_click(5), 2, 1)
create_button(btns_frame, "6", COLORS['bg_number'], COLORS['active_number'], 
              lambda: btn_click(6), 2, 2)
create_button(btns_frame, "−", COLORS['bg_operator'], COLORS['active_operator'], 
              lambda: btn_click("-"), 2, 3)

# Row 3
create_button(btns_frame, "1", COLORS['bg_number'], COLORS['active_number'], 
              lambda: btn_click(1), 3, 0)
create_button(btns_frame, "2", COLORS['bg_number'], COLORS['active_number'], 
              lambda: btn_click(2), 3, 1)
create_button(btns_frame, "3", COLORS['bg_number'], COLORS['active_number'], 
              lambda: btn_click(3), 3, 2)
create_button(btns_frame, "+", COLORS['bg_operator'], COLORS['active_operator'], 
              lambda: btn_click("+"), 3, 3)

# Row 4
create_button(btns_frame, "0", COLORS['bg_number'], COLORS['active_number'], 
              lambda: btn_click(0), 4, 0, columnspan=2, width=16)
create_button(btns_frame, ".", COLORS['bg_number'], COLORS['active_number'], 
              lambda: btn_click("."), 4, 2)
create_button(btns_frame, "=", COLORS['bg_equals'], COLORS['active_equals'], 
              lambda: bt_equal(), 4, 3)
 
win.mainloop()
