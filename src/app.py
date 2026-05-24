from flask import Flask, jsonify, render_template, request
from src.calculator import Calculator


app = Flask(__name__)
calculator = Calculator()


@app.route("/")
def index():
    """Render the main calculator interactive web application page."""
    return render_template("index.html")


@app.route("/api/calculate", methods=["POST"])
def calculate():
    """
    API endpoint to perform calculations.
    Expects a JSON payload with:
      - 'operation': The math operation to execute
                     (add, subtract, multiply, divide, power, square_root)
      - 'a': The first number (or input value for square root)
      - 'b': The second number (optional for square_root)
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "success": False,
            "error": "Request body must be valid JSON."
        }), 400

    operation = data.get("operation")
    if not operation:
        return jsonify({
            "success": False,
            "error": "Missing 'operation' in request data."
        }), 400

    # Retrieve parameters
    a_val = data.get("a")
    b_val = data.get("b")

    # Validate operation
    valid_ops = {
        "add", "subtract", "multiply", "divide", "power", "square_root"
    }
    if operation not in valid_ops:
        allowed = ", ".join(valid_ops)
        return jsonify({
            "success": False,
            "error": f"Invalid operation. Must be one of: {allowed}"
        }), 400

    # Helper validation function
    def parse_number(val, name):
        if val is None:
            raise ValueError(
                f"Missing parameter '{name}' for operation '{operation}'."
            )
        try:
            val_str = str(val)
            if '.' in val_str or 'e' in val_str.lower():
                return float(val)
            return int(val)
        except (ValueError, TypeError):
            raise ValueError(f"Parameter '{name}' must be a valid number.")

    try:
        if operation == "square_root":
            a = parse_number(a_val, "a")
            result = calculator.square_root(a)
        else:
            a = parse_number(a_val, "a")
            b = parse_number(b_val, "b")

            if operation == "add":
                result = calculator.add(a, b)
            elif operation == "subtract":
                result = calculator.subtract(a, b)
            elif operation == "multiply":
                result = calculator.multiply(a, b)
            elif operation == "divide":
                result = calculator.divide(a, b)
            elif operation == "power":
                result = calculator.power(a, b)
            else:
                return jsonify({
                    "success": False,
                    "error": "Unsupported operation."
                }), 400

        return jsonify({"success": True, "result": result})

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
