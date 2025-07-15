{
    "name": "Razorpay Payment Provider",
    "version": "1.0",
    "category": "My Category",
    "summary": "Integrate Razorpay into Odoo 18 Website Checkout",
    "description": "Provides Razorpay as a payment method in the website cart flow.",
    "depends": ["payment", "website_sale"],
    "data": [
        "views/payment_razorpay_views.xml",
        "views/payment_razorpay_templates.xml",
        "data/payment_provider_data.xml"
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3"
}
