/** @odoo-module **/

import { PaymentForm } from '@payment/js/payment_form';
import { patch } from '@web/core/utils/patch';

patch(PaymentForm.prototype, {

    /**
     * Handle COD payment method selection
     */
    async _processPayment(code, providerId, processingValues) {
        if (code === 'cod') {
            return this._processDirectPayment(code, providerId, processingValues);
        }
        return super._processPayment(code, providerId, processingValues);
    },

    /**
     * Process COD payment directly
     */
    async _processDirectPayment(code, providerId, processingValues) {
        const formData = this._getFormData();

        // Add COD specific data
        formData.append('provider_code', code);
        formData.append('provider_id', providerId);

        try {
            const response = await this.rpc('/payment/cod/process', {
                'provider_id': providerId,
                'amount': processingValues.amount,
                'currency_id': processingValues.currency_id,
                'reference': processingValues.reference,
            });

            if (response.success) {
                window.location.href = response.redirect_url;
            } else {
                this._displayError(response.error);
            }
        } catch (error) {
            this._displayError("Payment processing failed. Please try again.");
        }
    }
});
