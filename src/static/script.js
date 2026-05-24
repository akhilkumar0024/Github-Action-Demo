document.addEventListener("DOMContentLoaded", () => {
    // State Variables
    let currentInput = "";
    let previousInput = "";
    let activeOperation = null;
    let isCalculated = false;
    let history = [];

    // DOM Elements
    const expressionLine = document.getElementById("expression-line");
    const resultLine = document.getElementById("result-line");
    const numButtons = document.querySelectorAll(".btn-num");
    const opButtons = document.querySelectorAll(".btn-operator");
    const btnClear = document.getElementById("btn-clear");
    const btnBackspace = document.getElementById("btn-backspace");
    const btnEquals = document.getElementById("btn-equals");
    const historyToggle = document.getElementById("history-toggle");
    const historyPanel = document.getElementById("history-panel");
    const historyList = document.getElementById("history-list");
    const historyChevron = document.getElementById("history-chevron");
    const btnClearHistory = document.getElementById("btn-clear-history");

    // Mapping operator symbols for displaying
    const opSymbols = {
        add: "+",
        subtract: "-",
        multiply: "×",
        divide: "÷",
        power: "^",
        square_root: "√"
    };

    // Initialize display
    updateDisplay();

    // --- Core Display Functions ---
    function updateDisplay() {
        // Build the expression line representation
        if (activeOperation && activeOperation !== "square_root") {
            expressionLine.textContent = `${previousInput} ${opSymbols[activeOperation]} ${currentInput}`;
        } else if (activeOperation === "square_root") {
            expressionLine.textContent = `√(${previousInput || currentInput})`;
        } else {
            expressionLine.textContent = currentInput || previousInput || "0";
        }

        // Build result line representation
        if (isCalculated) {
            // Highlight result line when calculation just finished
            resultLine.classList.add("calculated");
        } else {
            resultLine.classList.remove("calculated");
        }
    }

    function showResult(value) {
        resultLine.textContent = formatResult(value);
        isCalculated = true;
        updateDisplay();
    }

    function showError(errMessage) {
        resultLine.textContent = "Error";
        expressionLine.textContent = errMessage;
        isCalculated = false;
    }

    function formatResult(value) {
        if (value === null || value === undefined) return "0";
        const num = Number(value);
        if (isNaN(num)) return "Error";
        // Handle floating points neatly
        if (num % 1 !== 0) {
            const str = num.toString();
            return str.length > 10 ? num.toPrecision(8) : str;
        }
        return num.toString();
    }

    // --- API Calculations Request ---
    async function executeCalculation(operation, a, b = null) {
        resultLine.textContent = "..."; // loading state
        try {
            const response = await fetch("/api/calculate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ operation, a, b })
            });
            const data = await response.json();

            if (data.success) {
                const finalResult = data.result;
                const calculationStr = b !== null
                    ? `${a} ${opSymbols[operation]} ${b}`
                    : `${opSymbols[operation]}(${a})`;

                addToHistory(calculationStr, formatResult(finalResult));

                previousInput = finalResult.toString();
                currentInput = "";
                activeOperation = null;
                showResult(finalResult);
            } else {
                showError(data.error);
            }
        } catch (error) {
            showError("Network Error");
            console.error("API Error:", error);
        }
    }

    // --- Input Handlers ---
    function handleNumber(val) {
        if (isCalculated) {
            // Reset input if typing fresh after a previous calculation
            previousInput = "";
            currentInput = "";
            isCalculated = false;
        }

        // Prevent multiple decimal points
        if (val === "." && currentInput.includes(".")) return;

        // Prevent multiple leading zeros
        if (val === "0" && currentInput === "0") return;

        // Replace leading zero if typing a digit
        if (currentInput === "0" && val !== ".") {
            currentInput = val;
        } else {
            currentInput += val;
        }

        resultLine.textContent = currentInput;
        updateDisplay();
    }

    function handleOperator(op) {
        isCalculated = false;

        if (op === "square_root") {
            const valToSquare = currentInput || previousInput || "0";
            executeCalculation("square_root", Number(valToSquare));
            return;
        }

        // For binary operators:
        if (currentInput) {
            if (previousInput && activeOperation) {
                // Chain calculations: execute previous first
                executeCalculation(activeOperation, Number(previousInput), Number(currentInput)).then(() => {
                    activeOperation = op;
                    updateDisplay();
                });
            } else {
                previousInput = currentInput;
                currentInput = "";
                activeOperation = op;
                updateDisplay();
            }
        } else if (previousInput) {
            activeOperation = op;
            updateDisplay();
        }
    }

    function handleEquals() {
        if (activeOperation && currentInput && previousInput) {
            executeCalculation(activeOperation, Number(previousInput), Number(currentInput));
        }
    }

    function handleClear() {
        currentInput = "";
        previousInput = "";
        activeOperation = null;
        isCalculated = false;
        resultLine.textContent = "0";
        expressionLine.textContent = "0";
    }

    function handleBackspace() {
        if (isCalculated) {
            handleClear();
            return;
        }
        if (currentInput.length > 0) {
            currentInput = currentInput.slice(0, -1);
            resultLine.textContent = currentInput || "0";
            updateDisplay();
        }
    }

    // --- History Management ---
    function addToHistory(exp, res) {
        history.unshift({ exp, res });
        if (history.length > 10) history.pop(); // keep last 10 entries
        renderHistory();

        // Automatically expand history panel on the first calculation
        if (history.length === 1 && historyPanel.classList.contains("collapsed")) {
            historyPanel.classList.remove("collapsed");
            historyChevron.style.transform = "rotate(180deg)";
        }
    }

    //clear recent history 
    function clearRecentHistory() {
        history = [];
        renderHistory();
    }
    function renderHistory() {
        if (history.length === 0) {
            historyList.innerHTML = `<div class="empty-history">No calculations yet</div>`;
            return;
        }

        historyList.innerHTML = history.map(item => `
            <div class="history-item">
                <span class="history-item-exp">${item.exp} =</span>
                <span class="history-item-res">${item.res}</span>
            </div>
        `).join("");
    }

    // --- Event Listeners ---
    numButtons.forEach(btn => {
        btn.addEventListener("click", () => handleNumber(btn.getAttribute("data-val")));
    });

    opButtons.forEach(btn => {
        btn.addEventListener("click", () => handleOperator(btn.getAttribute("data-op")));
    });

    btnClear.addEventListener("click", handleClear);
    btnBackspace.addEventListener("click", handleBackspace);
    btnEquals.addEventListener("click", handleEquals);

    // Toggle history panel dropdown
    historyToggle.addEventListener("click", () => {
        const isCollapsed = historyPanel.classList.toggle("collapsed");
        historyChevron.style.transform = isCollapsed ? "rotate(0deg)" : "rotate(180deg)";
    });

    btnClearHistory.addEventListener("click", (e) => {
        e.stopPropagation(); // Prevent toggling the history panel
        clearRecentHistory();
    });

    // --- Physical Keyboard Integration ---
    document.addEventListener("keydown", (e) => {
        const key = e.key;

        // Number and decimal keys
        if (/^[0-9.]$/.test(key)) {
            e.preventDefault();
            handleNumber(key);
        }
        // Operator mappings
        else if (key === "+") {
            e.preventDefault();
            handleOperator("add");
        } else if (key === "-") {
            e.preventDefault();
            handleOperator("subtract");
        } else if (key === "*") {
            e.preventDefault();
            handleOperator("multiply");
        } else if (key === "/") {
            e.preventDefault();
            handleOperator("divide");
        } else if (key === "^") {
            e.preventDefault();
            handleOperator("power");
        }
        // Enter / Equals keys
        else if (key === "Enter" || key === "=") {
            e.preventDefault();
            handleEquals();
        }
        // Backspace
        else if (key === "Backspace") {
            e.preventDefault();
            handleBackspace();
        }
        // Escape / Clear
        else if (key === "Escape") {
            e.preventDefault();
            handleClear();
        }
    });
});
