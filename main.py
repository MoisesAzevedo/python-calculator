from tkinter import *
from tkinter import font, messagebox
from services.history_manager import HistoryManager
from ui.history_window import HistoryWindow
from utils.formatters import ExpressionValidator, NumberFormatter

# Configuration constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 580  # Adjusted for toolbar
MARGIN_SIZE = 12
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
        bd=2, 
        bg=bg_color, 
        cursor="hand2",
        font=('Segoe UI', FONT_SIZE, 'bold'), 
        activebackground=active_color, 
        activeforeground=COLORS['fg_text'],
        relief='raised',  # Use raised relief for rounded appearance
        command=command
    ).grid(row=row, column=column, columnspan=columnspan, padx=BUTTON_SPACING, pady=BUTTON_SPACING, sticky='nsew')

# Create main window
# Create root window
win = Tk()
win.title("Modern Calculator")
# Make the root background white for visible margin around the calculator
win.configure(bg='white')
win.resizable(1, 1)
win.minsize(350 + MARGIN_SIZE * 2, 500 + MARGIN_SIZE * 2)

# Set initial size but don't center yet
win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

# Container frame to create a visible margin around the calculator
container = Frame(
    win,
    bg=COLORS['bg_main'],
    padx=MARGIN_SIZE,
    pady=MARGIN_SIZE,
    # draw a visible border around the calculator so the margin stands out
    highlightthickness=2,
    highlightbackground='#cccccc'
)
container.pack(fill=BOTH, expand=True)

# Initialize history manager
history_manager = HistoryManager()

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
    try:
        # Validate expression before evaluation
        if not ExpressionValidator.is_valid_expression(expression):
            messagebox.showerror("Erro", "Expressão inválida!")
            return
        
        # Sanitize expression for evaluation
        sanitized_expr = ExpressionValidator.sanitize_expression(expression)
        
        # Calculate result
        result = eval(sanitized_expr)
        formatted_result = NumberFormatter.format_result(result)
        
        # Add to history before clearing
        display_expr = ExpressionValidator.format_for_display(expression)
        history_manager.add_calculation(display_expr, formatted_result)
        
        # Update display
        input_text.set(formatted_result)
        expression = ""
        
    except ZeroDivisionError:
        messagebox.showerror("Erro", "Divisão por zero!")
        bt_clear()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
        bt_clear()

def show_history():
    """Show the calculation history window."""
    history_entries = history_manager.get_history()
    
    def on_select_result(result):
        """Callback when a history result is selected."""
        global expression
        expression = result
        input_text.set(result)
    
    def on_clear_history():
        """Callback when history is cleared."""
        history_manager.clear_history()
    
    history_window = HistoryWindow(
        win, 
        history_entries, 
        on_select_result, 
        on_clear_history
    )
    history_window.show()

def insert_from_history():
    """Insert the last calculation result into current expression."""
    last_calculation = history_manager.get_last_calculation()
    if last_calculation:
        btn_click(last_calculation.result)
    else:
        messagebox.showinfo("Informação", "Não há histórico disponível.")
 
expression = ""
 
# 'StringVar()' :It is used to get the instance of input field
 
input_text = StringVar()

# Create toolbar frame for history buttons
toolbar_frame = Frame(container, bg=COLORS['bg_main'], width=WINDOW_WIDTH)
# Set toolbar to WINDOW_WIDTH and buttons will fill this width
toolbar_frame.pack(side=TOP, pady=(5, 0), fill=X)

# Create history buttons in toolbar with consistent styling and proper width
history_btn = Button(
    toolbar_frame,
    text="📚 Histórico",
    command=show_history,
    bg=COLORS['bg_clear'],
    fg=COLORS['fg_text'],
    font=('Segoe UI', 10, 'bold'),
    relief='raised',
    cursor='hand2',
    activebackground=COLORS['active_clear'],
    activeforeground=COLORS['fg_text'],
    bd=2,
    height=1,
    width=18
)
history_btn.pack(side=LEFT, fill=X, expand=True, padx=(10, BUTTON_SPACING//2), pady=2)

last_btn = Button(
    toolbar_frame,
    text="⏮️ Último",
    command=insert_from_history,
    bg=COLORS['bg_clear'],
    fg=COLORS['fg_text'],
    font=('Segoe UI', 10, 'bold'),
    relief='raised',
    cursor='hand2',
    activebackground=COLORS['active_clear'],
    activeforeground=COLORS['fg_text'],
    bd=2,
    height=1,
    width=18
)
last_btn.pack(side=RIGHT, fill=X, expand=True, padx=(BUTTON_SPACING//2, 10), pady=2)
 
# Let us creating a frame for the input field
 
input_frame = Frame(container, width=WINDOW_WIDTH, height=80, bd=0, highlightbackground="#333333",
 highlightcolor=COLORS['border_input'], highlightthickness=2, bg=COLORS['bg_input'])
 
input_frame.pack(side=TOP, pady=5, fill=X)
 
#Let us create a input field inside the 'Frame'
 
input_field = Entry(input_frame, font=('Segoe UI', 20, 'bold'), 
textvariable=input_text, width=WINDOW_WIDTH,bg=COLORS['bg_input'], bd=0, justify=RIGHT,
fg=COLORS['fg_text'], insertbackground=COLORS['border_input'])
 
input_field.grid(row=0, column=0)
 
input_field.pack(ipady=15, padx=10)

 
btns_frame = Frame(container, width=WINDOW_WIDTH, height=400, bg=COLORS['bg_frame'])
 
btns_frame.pack(pady=5, fill=X)

# Configure grid weights for responsive design
for i in range(4):
    btns_frame.grid_columnconfigure(i, weight=1)
for i in range(5):  # Back to 5 rows for standard calculator layout
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

# Update the window to calculate final size, then center it
win.update_idletasks()
center_window(win, WINDOW_WIDTH, WINDOW_HEIGHT)
 
win.mainloop()
