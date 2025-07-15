/** @odoo-module **/
import paymentForm from '@payment/js/payment_form'
import { loadJS } from '@web/core/assets';
import { rpc } from '@web/core/network/rpc';

paymentForm.include({
    async _selectPaymentOption(ev) {
        await this._super(...arguments);
        await this._updateCodDisplay();
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
        await rpc('/payment/cash_on_delivery/verify_payment', {
            reference: processingValues.reference,
        });
        window.location = '/payment/status'
    },

    async _initiatePaymentFlow(providerCode, paymentOptionId, paymentMethodCode, flow) {
        await this._super(...arguments);
        if (providerCode === 'cash_on_delivery') {
            const selectedRadio = document.querySelector('input[name="o_payment_radio"]:checked');
            if (selectedRadio) {
                const providerId = selectedRadio.getAttribute('data-provider-id');
                if (providerId) {
                    await rpc('/shop/payment/cod_charges', {
                        provider_id: providerId,
                        payment_method_code: providerCode
                    });
                }
            }
        }
    },

    async _updateCodDisplay() {
        const selectedRadio = document.querySelector('input[name="o_payment_radio"]:checked');
        if (!selectedRadio) {
            const codRow = document.querySelector('.cod-charges-row');
            if (codRow) {
                codRow.style.display = 'none';
            }
            return;
        }

        const providerId = selectedRadio.getAttribute('data-provider-id');
        const providerCode = selectedRadio.getAttribute('data-provider-code');

        try {
            const response = await rpc('/shop/payment/cod_charges', {
                provider_id: providerId,
                payment_method_code: providerCode
            });

            const codRow = document.querySelector('.cod-charges-row');
            const monetaryField = codRow?.querySelector('.monetary_field');

            if (providerCode === 'cash_on_delivery' && response.cod_charges > 0) {
                if (codRow && monetaryField) {
                    codRow.style.display = '';
                    monetaryField.textContent = `${response.currency_symbol}${response.cod_charges.toFixed(2)}`;
                }
            } else {
                if (codRow) {
                    codRow.style.display = 'none';
                }
            }

            const totalEl = document.getElementById('cart_total');
            if (totalEl) {
                const totalField = totalEl.querySelector('#order_total .text-end');
                if (totalField) {
                    totalField.innerHTML = `<strong>${response.currency_symbol}${response.amount_total.toFixed(2)}</strong>`;
                }
            }

            if (this.paymentContext) {
                this.paymentContext['amount'] = response.amount_total;
            }

        } catch (error) {
            console.error('Error updating COD charges:', error);
            const codRow = document.querySelector('.cod-charges-row');
            if (codRow) {
                codRow.style.display = 'none';
            }
        }
    },
})