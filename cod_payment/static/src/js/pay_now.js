/** @odoo-module **/
import paymentForm from '@payment/js/payment_form';
import { rpc } from '@web/core/network/rpc';

paymentForm.include({
    async _selectPaymentOption(ev) {
        await this._super(...arguments);
        const providerId = ev.target.getAttribute('data-provider-id');
        const providerCode = ev.target.getAttribute('data-provider-code');
        const paymentMethodCode = ev.target.getAttribute('data-payment-method-code');
        this._addDeliveryCharge(providerId, paymentMethodCode);
    },

    async _prepareInlineForm(providerId, providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (providerCode !== 'cash_on_delivery') {
            return this._super(...arguments);
        }
        if (flow === 'token') {
            return;
        }
        this._setPaymentFlow('direct');
    },

    async _processDirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues) {
        if (providerCode !== 'cash_on_delivery') {
            return this._super(...arguments);
        }
        window.location = '/payment/status';
    },

    async _addDeliveryCharge(providerId, paymentMethodCode) {
        const response = await rpc('/shop/payment/cod_charges', {
            provider_id: providerId,
            payment_method_code: paymentMethodCode
        });
        const codChargeRow = document.querySelector('.cod-charges-row');
        const codChargeElement = document.querySelector('#cart_cod_charges');
        const codMonetaryElement = document.querySelector('#cart_cod_monetary');
        const totalElement = document.querySelector(`#${'order_total'} .${'text-end'}`);
        if (response && response.cod_charges > 0) {
            if (codChargeElement) {
                codChargeRow.style = '';
                codChargeElement.innerText = 'COD charges';
                codMonetaryElement.innerText = `${response.currency_symbol} ${response.cod_charges}.00`;
                totalElement.innerHTML = `<strong>${response.currency_symbol} ${response.amount_total}.00</strong>`;
                this.paymentContext.amount = response.amount_total;
            }
        } else if (response && response.cod_charges == 0) {
            if (codChargeElement) {
                codChargeElement.innerHTML = '';
                codMonetaryElement.innerHTML = '';
                totalElement.innerHTML = `<strong>${response.currency_symbol} ${response.amount_total}.00</strong>`;
                this.paymentContext.amount = response.amount_total;
            }
        }
    }
});
