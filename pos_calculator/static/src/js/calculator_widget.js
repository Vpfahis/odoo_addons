/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";

export class CalculatorWidget extends Component {
    static template = "calculator_in_pos.CalculatorWidget";

    setup() {
        this.pos = usePos();
        this.state = useState({
            display: "0",
            expression: "",
            showResult: false
        });
    }

    inputNumber(num) {
        if (this.state.showResult) {
            this.state.expression = String(num);
            this.state.display = this.state.expression;
            this.state.showResult = false;
        } else {
            this.state.expression += String(num);
            this.state.display = this.state.expression;
        }
    }

    inputDecimal() {
        if (this.state.showResult) {
            this.state.expression = "0.";
            this.state.display = this.state.expression;
            this.state.showResult = false;
        } else {
            this.state.expression += ".";
            this.state.display = this.state.expression;
        }
    }

    clear() {
        this.state.display = "0";
        this.state.expression = "";
        this.state.showResult = false;
    }

    backspace() {
        if (this.state.showResult) {
            this.clear();
        } else {
            this.state.expression = this.state.expression.slice(0, -1);
            this.state.display = this.state.expression || "0";
        }
    }

    performOperation(op) {
        if (this.state.showResult) {
            this.state.expression = this.state.display + op;
            this.state.display = this.state.expression;
            this.state.showResult = false;
        } else {
            // Only add operator if last character isn't already one
            const lastChar = this.state.expression.slice(-1);
            if ("+-*/".includes(lastChar)) {
                this.state.expression = this.state.expression.slice(0, -1) + op;
            } else {
                this.state.expression += op;
            }
            this.state.display = this.state.expression;
        }
    }

    equals() {
        try {
            let expression = this.state.expression
                .replace(/×/g, '*')
                .replace(/÷/g, '/');
            const result = eval(expression);

            if (!isFinite(result)) {
                this.state.display = "ERROR";
                this.state.expression = "";
            } else {
                // Round to 8 decimal places max, and remove trailing zeros
                const rounded = parseFloat(result.toFixed(8));
                this.state.display = String(rounded);
                this.state.expression = String(rounded);
            }

            this.state.showResult = true;
        } catch (e) {
            this.state.display = "ERROR";
            this.state.expression = "";
            this.state.showResult = true;
        }
    }

    copyToClipboard() {
        navigator.clipboard.writeText(this.state.display);
    }

    closeCalculator() {
        this.props.onClose();
    }
}

// Patch the ControlButtons to include the calculator button
patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        this.calculatorState = useState({
            showCalculator: false
        });
    },

    onClickCalculator() {
        this.calculatorState.showCalculator = !this.calculatorState.showCalculator;
    },

    onCloseCalculator() {
        this.calculatorState.showCalculator = false;
    }
});

// Add the calculator component to ControlButtons
ControlButtons.components = {
    ...ControlButtons.components,
    CalculatorWidget
};