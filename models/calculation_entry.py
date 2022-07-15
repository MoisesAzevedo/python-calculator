"""
Model for representing a calculation entry in the history.
Following Single Responsibility Principle - only handles calculation data.
"""
from datetime import datetime
from typing import Optional


class CalculationEntry:
    """Represents a single calculation entry in the history."""
    
    def __init__(self, expression: str, result: str, timestamp: Optional[datetime] = None):
        """
        Initialize a calculation entry.
        
        Args:
            expression: The mathematical expression that was calculated
            result: The result of the calculation
            timestamp: When the calculation was performed (defaults to now)
        """
        self.expression = expression
        self.result = result
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> dict:
        """Convert the entry to a dictionary for serialization."""
        return {
            'expression': self.expression,
            'result': self.result,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CalculationEntry':
        """Create a CalculationEntry from a dictionary."""
        return cls(
            expression=data['expression'],
            result=data['result'],
            timestamp=datetime.fromisoformat(data['timestamp'])
        )
    
    def __str__(self) -> str:
        """String representation of the calculation entry."""
        return f"{self.expression} = {self.result}"
    
    def get_formatted_time(self) -> str:
        """Get formatted timestamp for display."""
        return self.timestamp.strftime("%H:%M:%S")
    
    def get_formatted_date(self) -> str:
        """Get formatted date for display."""
        return self.timestamp.strftime("%d/%m/%Y")
