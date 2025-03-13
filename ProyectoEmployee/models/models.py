# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EmployeeWorkLog(models.Model):
    _name = 'tracking.employee.worklog'
    _description = 'Registro de Horas de Trabajo'
    
    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    date = fields.Date(string='Fecha', required=True)
    hours_worked = fields.Float(string='Horas Trabajadas', required=True)
    tasks_completed = fields.Integer(string='Tareas Completadas', default=0)

    @api.model
    def create(self, vals):
        record = super(EmployeeWorkLog, self).create(vals)
        record.update_employee_efficiency()  # Actualizamos la eficiencia al crear el registro de trabajo
        return record

    def write(self, vals):
        result = super(EmployeeWorkLog, self).write(vals)
        self.update_employee_efficiency()  # Actualizamos la eficiencia al modificar el registro de trabajo
        return result

    def update_employee_efficiency(self):
        for log in self:
            logs = self.env['tracking.employee.worklog'].search([('employee_id', '=', log.employee_id.id)])
            total_hours = sum(logs.mapped('hours_worked'))
            total_tasks = sum(logs.mapped('tasks_completed'))
            efficiency = (total_tasks / total_hours) if total_hours else 0
            log.employee_id.efficiency = efficiency
        
        # Llamamos al método para actualizar el ranking después de cada actualización de eficiencia
        self.env['tracking.employee.ranking'].update_ranking()

class Employee(models.Model):
    _inherit = 'hr.employee'
    
    # Relación inversa de trabajo: un empleado puede tener muchos registros de trabajo
    worklog_ids = fields.One2many('tracking.employee.worklog', 'employee_id', string='Registros de Trabajo')

    efficiency = fields.Float(string='Eficiencia', compute='_compute_efficiency', store=True)

    @api.depends('worklog_ids')
    def _compute_efficiency(self):
        for employee in self:
            # Obtenemos todos los registros de trabajo asociados al empleado
            logs = employee.worklog_ids
            total_hours = sum(logs.mapped('hours_worked'))
            total_tasks = sum(logs.mapped('tasks_completed'))
            employee.efficiency = (total_tasks / total_hours) if total_hours else 0

class EmployeeRanking(models.Model):
    _name = 'tracking.employee.ranking'
    _description = 'Ranking de Empleados'
    
    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    efficiency = fields.Float(string='Eficiencia', related='employee_id.efficiency', store=True)

    @api.model
    def update_ranking(self):
        # Eliminamos todos los registros previos del ranking
        self.env['tracking.employee.ranking'].search([]).unlink()
        
        # Obtenemos a todos los empleados ordenados por eficiencia
        employees = self.env['hr.employee'].search([], order='efficiency desc')
        
        # Creamos un registro en el ranking por cada empleado
        for employee in employees:
            self.create({'employee_id': employee.id})

