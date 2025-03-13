# -*- coding: utf-8 -*-
{
    'name': 'Employee Tracking',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Seguimiento de horas de trabajo y eficiencia de los empleados',
    'description': 'Permite registrar las horas trabajadas de los empleados y calcular su eficiencia.',
    'author': 'Michael Patricio Cumbicus Yaguana, Irene Jurado Castillo',
    'depends': ['hr'],
    'data': [
        'views/employee_ranking_views.xml', 
        'views/employee_worklog_views.xml',
        'views/employee_tracking_menu.xml',  
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
