from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception:
        return "Could not calculate the expression."


if __name__ == "__main__":
    print(calculator.invoke("3500 * 1.1"))