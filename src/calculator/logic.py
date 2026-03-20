import ast
import math

class CalculatorLogic:
    def __init__(self):
        self.expression = ""
        self.result = ""
        self.memory = 0

    def on_button_press(self, value: str) -> None:
        if value == "AC":
            self.expression = ""
            self.result = ""
        elif value == "C":
            self.expression = self.expression[:-1]
        elif value == "=":
            try:
                self.result = str(self._evaluate_expression(self.expression))
            except (SyntaxError, ZeroDivisionError, ValueError) as e:
                self.result = "Error"
        elif value == "+/-":
            if self.expression:
                if self.expression.startswith('-'):
                    self.expression = self.expression[1:]
                else:
                    self.expression = '-' + self.expression
        elif value == "%":
            if self.expression:
                try:
                    self.expression = str(float(self.expression) / 100)
                except ValueError:
                    self.result = "Error"
        elif value in ("M+", "M-", "MR", "MC"):
            self._handle_memory(value)
        else:
            if self.result and value not in "+-*/^":
                self.expression = ""
            self.result = ""
            self.expression += value

    def _handle_memory(self, value: str):
        try:
            current_val = float(self.get_display_text())
        except ValueError:
            current_val = 0

        if value == "MC":
            self.memory = 0
        elif value == "MR":
            self.expression = str(self.memory)
        elif value == "M+":
            self.memory += current_val
        elif value == "M-":
            self.memory -= current_val

    def _evaluate_expression(self, expression: str) -> float:
        try:
            # Replace user-friendly symbols with Python operators
            expression = expression.replace("√", "sqrt")
            expression = expression.replace("x", "*")
            expression = expression.replace("÷", "/")
            expression = expression.replace("^", "**")
            
            # Safely parse the expression
            node = ast.parse(expression, mode='eval')
            return self._eval_node(node.body)
        except Exception as e:
            raise ValueError("Invalid expression") from e

    def _eval_node(self, node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            elif isinstance(node.op, ast.Sub):
                return left - right
            elif isinstance(node.op, ast.Mult):
                return left * right
            elif isinstance(node.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                return left / right
            elif isinstance(node.op, ast.Pow):
                return left ** right
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            if isinstance(node.op, ast.USub):
                return -operand
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in self._get_safe_functions():
                args = [self._eval_node(arg) for arg in node.args]
                return self._get_safe_functions()[node.func.id](*args)
        
        raise ValueError(f"Unsupported node type: {type(node)}")

    def _get_safe_functions(self):
        return {
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log10,
            'ln': math.log,
        }

    def get_display_text(self) -> str:
        return self.result or self.expression or "0"

