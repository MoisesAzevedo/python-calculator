"""
History Window UI Component - handles the history display interface.
Following Single Responsibility Principle - only manages history window UI.
"""
from tkinter import *
from tkinter import ttk, messagebox
from typing import List, Callable, Optional
from models.calculation_entry import CalculationEntry


class HistoryWindow:
    """Manages the history window interface."""
    
    def __init__(self, parent: Tk, history_entries: List[CalculationEntry], 
                 on_select_callback: Optional[Callable[[str], None]] = None,
                 on_clear_callback: Optional[Callable[[], None]] = None):
        """
        Initialize the history window.
        
        Args:
            parent: Parent window
            history_entries: List of calculation entries to display
            on_select_callback: Callback when a history item is selected
            on_clear_callback: Callback when clear history is requested
        """
        self.parent = parent
        self.history_entries = history_entries
        self.on_select_callback = on_select_callback
        self.on_clear_callback = on_clear_callback
        self.window = None
        self.search_var = StringVar()
        self.filtered_entries = history_entries.copy()
        
    def show(self) -> None:
        """Display the history window."""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
            
        self._create_window()
        self._setup_ui()
        self._populate_history()
    
    def _create_window(self) -> None:
        """Create the history window."""
        self.window = Toplevel(self.parent)
        self.window.title("Histórico de Cálculos")
        self.window.geometry("450x500")
        self.window.configure(bg='#1e1e1e')
        self.window.resizable(True, True)
        
        # Center the window
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Center on parent
        self.window.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (450 // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (500 // 2)
        self.window.geometry(f"450x500+{x}+{y}")
    
    def _setup_ui(self) -> None:
        """Setup the user interface components."""
        # Title
        title_label = Label(
            self.window,
            text="Histórico de Cálculos",
            font=('Segoe UI', 16, 'bold'),
            bg='#1e1e1e',
            fg='#ffffff'
        )
        title_label.pack(pady=10)
        
        # Search frame
        search_frame = Frame(self.window, bg='#1e1e1e')
        search_frame.pack(fill=X, padx=10, pady=5)
        
        Label(
            search_frame,
            text="Buscar:",
            font=('Segoe UI', 10),
            bg='#1e1e1e',
            fg='#ffffff'
        ).pack(side=LEFT)
        
        search_entry = Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 10),
            bg='#2d2d2d',
            fg='#ffffff',
            insertbackground='#2196F3',
            bd=1,
            relief='solid'
        )
        search_entry.pack(side=LEFT, fill=X, expand=True, padx=(5, 0))
        search_entry.bind('<KeyRelease>', self._on_search)
        
        # Buttons frame
        buttons_frame = Frame(self.window, bg='#1e1e1e')
        buttons_frame.pack(fill=X, padx=10, pady=5)
        
        Button(
            buttons_frame,
            text="Limpar Histórico",
            command=self._clear_history,
            bg='#607D8B',
            fg='#ffffff',
            font=('Segoe UI', 10),
            relief='flat',
            cursor='hand2'
        ).pack(side=LEFT)
        
        Button(
            buttons_frame,
            text="Atualizar",
            command=self._refresh_history,
            bg='#2196F3',
            fg='#ffffff',
            font=('Segoe UI', 10),
            relief='flat',
            cursor='hand2'
        ).pack(side=LEFT, padx=(5, 0))
        
        # History listbox with scrollbar
        list_frame = Frame(self.window, bg='#1e1e1e')
        list_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Create listbox with scrollbar
        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.history_listbox = Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=('Consolas', 10),
            bg='#2d2d2d',
            fg='#ffffff',
            selectbackground='#2196F3',
            selectforeground='#ffffff',
            bd=0,
            relief='flat',
            activestyle='none'
        )
        self.history_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        self.history_listbox.bind('<Double-Button-1>', self._on_item_double_click)
        
        scrollbar.config(command=self.history_listbox.yview)
        
        # Info label
        self.info_label = Label(
            self.window,
            text="Duplo clique em um item para usar o resultado",
            font=('Segoe UI', 9),
            bg='#1e1e1e',
            fg='#888888'
        )
        self.info_label.pack(pady=5)
    
    def _populate_history(self) -> None:
        """Populate the history listbox with entries."""
        self.history_listbox.delete(0, END)
        
        if not self.filtered_entries:
            self.history_listbox.insert(END, "Nenhum cálculo encontrado")
            self.info_label.config(text="Histórico vazio")
            return
        
        # Show most recent first
        for entry in reversed(self.filtered_entries):
            time_str = entry.get_formatted_time()
            display_text = f"[{time_str}] {entry.expression} = {entry.result}"
            self.history_listbox.insert(END, display_text)
        
        count = len(self.filtered_entries)
        self.info_label.config(
            text=f"{count} cálculo(s) encontrado(s). Duplo clique para usar o resultado."
        )
    
    def _on_search(self, event=None) -> None:
        """Handle search input."""
        query = self.search_var.get().strip()
        
        if not query:
            self.filtered_entries = self.history_entries.copy()
        else:
            query_lower = query.lower()
            self.filtered_entries = [
                entry for entry in self.history_entries
                if (query_lower in entry.expression.lower() or 
                    query_lower in entry.result.lower())
            ]
        
        self._populate_history()
    
    def _on_item_double_click(self, event=None) -> None:
        """Handle double-click on history item."""
        selection = self.history_listbox.curselection()
        if not selection or not self.filtered_entries:
            return
        
        # Get the selected entry (reverse index since we show most recent first)
        index = len(self.filtered_entries) - 1 - selection[0]
        selected_entry = self.filtered_entries[index]
        
        if self.on_select_callback:
            self.on_select_callback(selected_entry.result)
        
        self.window.destroy()
    
    def _clear_history(self) -> None:
        """Handle clear history request."""
        if not self.history_entries:
            messagebox.showinfo("Informação", "O histórico já está vazio.")
            return
        
        result = messagebox.askyesno(
            "Confirmar",
            "Tem certeza que deseja limpar todo o histórico?",
            parent=self.window
        )
        
        if result and self.on_clear_callback:
            self.on_clear_callback()
            self.history_entries.clear()
            self.filtered_entries.clear()
            self._populate_history()
    
    def _refresh_history(self) -> None:
        """Refresh the history display."""
        self.search_var.set("")
        self.filtered_entries = self.history_entries.copy()
        self._populate_history()
    
    def update_history(self, new_entries: List[CalculationEntry]) -> None:
        """Update the history entries and refresh display."""
        self.history_entries = new_entries
        self._refresh_history()
