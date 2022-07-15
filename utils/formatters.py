"""
Utility functions for the calculator application.
Following Single Responsibility Principle - only handles utility operations.
"""
import re
from typing import Union


class ExpressionValidator:
    """Validates and sanitizes mathematical expressions."""
    
    @staticmethod
    def is_valid_expression(expression: str) -> bool:
        """
        Check if an expression is valid for evaluation.
        
        Args:
            expression: The mathematical expression to validate
            
        Returns:
            True if the expression is valid, False otherwise
        """
        if not expression or expression.isspace():
            return False
        
        # Check for dangerous functions or imports
        dangerous_patterns = [
            r'\b(import|exec|eval|open|file|input|raw_input)\b',
            r'__\w+__',
            r'\bos\b',
            r'\bsys\b'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, expression, re.IGNORECASE):
                return False
        
        # Allow only basic mathematical operations and numbers
        allowed_pattern = r'^[\d\+\-\*\/\.\(\)\s]+$'
        return bool(re.match(allowed_pattern, expression))
    
    @staticmethod
    def sanitize_expression(expression: str) -> str:
        """
        Sanitize and format an expression for display.
        
        Args:
            expression: The expression to sanitize
            
        Returns:
            Sanitized expression
        """
        if not expression:
            return ""
        
        # Replace display symbols with evaluation symbols
        replacements = {
            '×': '*',
            '÷': '/',
            '−': '-'
        }
        
        sanitized = expression
        for display_symbol, eval_symbol in replacements.items():
            sanitized = sanitized.replace(display_symbol, eval_symbol)
        
        return sanitized
    
    @staticmethod
    def format_for_display(expression: str) -> str:
        """
        Format an expression for display with proper symbols.
        
        Args:
            expression: The expression to format
            
        Returns:
            Formatted expression for display
        """
        if not expression:
            return ""
        
        # Replace evaluation symbols with display symbols
        replacements = {
            '*': '×',
            '/': '÷',
            # Keep - as is since it's used for both minus and negative
        }
        
        formatted = expression
        for eval_symbol, display_symbol in replacements.items():
            formatted = formatted.replace(eval_symbol, display_symbol)
        
        return formatted


class NumberFormatter:
    """Handles number formatting for display purposes."""
    
    @staticmethod
    def format_result(result: Union[int, float, str]) -> str:
        """
        Format a calculation result for display.
        
        Args:
            result: The result to format
            
        Returns:
            Formatted result string
        """
        try:
            # Convert to float first to handle string numbers
            num_result = float(result)
            
            # If it's a whole number, display as integer
            if num_result.is_integer():
                return str(int(num_result))
            
            # For decimal numbers, limit precision
            return f"{num_result:.10g}"  # Remove trailing zeros
            
        except (ValueError, TypeError):
            return str(result)
    
    @staticmethod
    def truncate_long_number(number_str: str, max_length: int = 15) -> str:
        """
        Truncate very long numbers for display.
        
        Args:
            number_str: The number string to truncate
            max_length: Maximum length allowed
            
        Returns:
            Truncated number string
        """
        if len(number_str) <= max_length:
            return number_str
        
        # Try to use scientific notation for very long numbers
        try:
            num = float(number_str)
            return f"{num:.6e}"
        except ValueError:
            return number_str[:max_length] + "..."
