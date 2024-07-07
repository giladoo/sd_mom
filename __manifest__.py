# -*- coding: utf-8 -*-
{
    'name': "Minute Of Meeting",

    'summary': """
        """,

    'description': """
        
    """,

    'author': "Arash Homayounfar",
    'website': "https://gilaneh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Service Desk/Service Desk',
    'application': True,
    'version': '17.0.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail', 'project'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'views/control_panel.xml',
        'views/project.xml',
        'views/views.xml',
        'report/mom_print.xml',
        'report/mom_print_template.xml',
        # 'views/templates.xml',
        # 'views/hr_employee_views.xml',
        # 'data/home_data.xml'
    ],
    'assets': {
        # 'website.assets_editor': [
        #     'static/src/**/*',
        # ],

        'web.assets_frontend': [

             # 'sd_mom/static/src/css/my-style.scss',
            # 'sd_mom/static/src/js/website_form_sd_mom.js'
        ],
        'web.assets_common': [
            # 'sd_mom/static/src/xml/control_panel.xml',
            'sd_mom/static/src/css/styles.css',

        ],
        'web.report_assets_common': [
            # 'sd_mom/static/src/xml/control_panel.xml',
            'sd_mom/static/src/css/styles.css',

        ],
        'web.assets_qweb': [
            # 'sd_mom/static/src/components/**/*.xml',
            # 'sd_mom/static/src/web/**/*.xml',
            # 'sd_mom/static/src/xml/**/*.xml',
            'sd_mom/static/src/components/**/*.xml',
        ],
        'web.assets_backend': [

            'sd_mom/static/src/components/**/*.js',
            'sd_mom/static/src/components/**/*.scss',
            'sd_mom/static/src/css/styles.css',
            # 'sd_mom/static/src/web/**/*.scss',
            # 'sd_mom/static/src/web/**/*.js',

            # 'sd_mom/static/src/js/website_form_sd_mom.js'
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/theme_screenshot.png'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'license': 'LGPL-3',

}
