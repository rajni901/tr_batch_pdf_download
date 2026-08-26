{
    'name': 'Batch PDF Download',
    'version': '19.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Download multiple Invoices, Sale Orders, Purchase Orders and Delivery Orders as a single ZIP file.',
    'description': """
Batch PDF Download — by Vayu Sharma
========================================
Select multiple records and download all PDFs as a single ZIP file in one click.

Features:
- Batch download Invoices as ZIP
- Batch download Sale Orders as ZIP
- Batch download Purchase Orders as ZIP
- Batch download Delivery Orders as ZIP
- Auto-named PDF files (Invoice_INV001.pdf, Order_SO001.pdf etc.)
- Works from list view — select any number of records
    """,
    'author': 'Vayu Sharma',
    'website': '',
    'license': 'OPL-1',
    'depends': ['account', 'sale_management', 'purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/batch_pdf_wizard_views.xml',
        'views/action_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 15.00,
    'currency': 'USD',
}
