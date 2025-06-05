{
    "name": "Ecole",
    "summary": "RedMed Capital",
    "version": "17.0",
    "license": "AGPL-3",
    "category": "Real Estate",
    "website": "http://psimaroc.com/",
    "depends": ["base", 'product', 'account'],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/ecole_menu_views.xml",
        "views/menu_views.xml",
        "views/account_move_line_views.xml",
        "views/res_pertner_form.xml",
        "views/res_users_views.xml",
        "views/product_school.xml",
        "reports/report_bulletin.xml",
        "reports/report_invoice_line_client.xml",


    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
