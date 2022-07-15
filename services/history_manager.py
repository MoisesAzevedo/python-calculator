"""
History Manager Service - handles all history-related operations.
Following Single Responsibility Principle - only manages calculation history.
"""
import json
import os
from typing import List, Optional
from models.calculation_entry import CalculationEntry


class HistoryManager:
    """Manages the calculation history with persistence capabilities."""
    
    def __init__(self, history_file: str = "calculator_history.json"):
        """
        Initialize the history manager.
        
        Args:
            history_file: Path to the file where history will be stored
        """
        self.history_file = history_file
        self._history: List[CalculationEntry] = []
        self._max_entries = 100  # Limit history to prevent excessive memory usage
        self.load_history()
    
    def add_calculation(self, expression: str, result: str) -> None:
        """
        Add a new calculation to the history.
        
        Args:
            expression: The mathematical expression
            result: The calculated result
        """
        entry = CalculationEntry(expression, result)
        self._history.append(entry)
        
        # Keep only the last max_entries calculations
        if len(self._history) > self._max_entries:
            self._history = self._history[-self._max_entries:]
        
        self.save_history()
    
    def get_history(self) -> List[CalculationEntry]:
        """Get all calculation entries in chronological order."""
        return self._history.copy()
    
    def get_recent_history(self, count: int = 10) -> List[CalculationEntry]:
        """
        Get the most recent calculations.
        
        Args:
            count: Number of recent entries to return
            
        Returns:
            List of recent calculation entries
        """
        return self._history[-count:] if self._history else []
    
    def clear_history(self) -> None:
        """Clear all history entries."""
        self._history.clear()
        self.save_history()
    
    def get_last_calculation(self) -> Optional[CalculationEntry]:
        """Get the most recent calculation entry."""
        return self._history[-1] if self._history else None
    
    def save_history(self) -> None:
        """Save the history to a file."""
        try:
            history_data = [entry.to_dict() for entry in self._history]
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def load_history(self) -> None:
        """Load the history from a file."""
        if not os.path.exists(self.history_file):
            return
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
                self._history = [CalculationEntry.from_dict(data) for data in history_data]
        except Exception as e:
            print(f"Error loading history: {e}")
            self._history = []
    
    def search_history(self, query: str) -> List[CalculationEntry]:
        """
        Search for calculations containing the query string.
        
        Args:
            query: String to search for in expressions or results
            
        Returns:
            List of matching calculation entries
        """
        query_lower = query.lower()
        return [
            entry for entry in self._history
            if query_lower in entry.expression.lower() or query_lower in entry.result.lower()
        ]
    
    def get_history_count(self) -> int:
        """Get the total number of entries in history."""
        return len(self._history)
