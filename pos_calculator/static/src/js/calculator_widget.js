/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

export class CalculatorDialog extends ConfirmationDialog {
    static template = "calculator_in_pos.CalculatorDialog";

    setup() {
        super.setup();
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
            if (!this.state.expression.trim()) {
                return;
            }
            let expression = this.state.expression
                .replace(/×/g, '*')
                .replace(/÷/g, '/');
            const result = eval(expression);

            if (!isFinite(result)) {
                this.state.display = "Invalid";
                this.state.expression = "";
            } else {
                const rounded = parseFloat(result.toFixed(8));
                this.state.display = String(rounded);
                this.state.expression = String(rounded);
            }

            this.state.showResult = true;
        } catch (e) {
            this.state.display = "Invalid";
            this.state.expression = "";
            this.state.showResult = true;
        }
    }

    onConfirm() {
        this.props.close();
    }

}

patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
    },

    onClickCalculator() {
        this.dialog.add(CalculatorDialog, {
            title: ("Calculator"),
            body: ("Use the calculator below:"),
            confirm: () => {},
            cancel: () => {},
        });
    }
});

ControlButtons.components = {
    ...ControlButtons.components,
    CalculatorDialog
};