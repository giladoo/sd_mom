# -*- coding: utf-8 -*-
import datetime
import json
from datetime import  timedelta
# import random

from odoo import models, fields, api, tools

from colorama import Fore


class SdMomMoms(models.Model):
    _name = 'sd_mom.moms'
    _description = 'sd_mom.moms'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, translate=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    mom_id = fields.Many2one('sd_mom.moms', string='MOM',
        default=False, recursive=True, store=True, readonly=False,
        index=True, tracking=True, check_company=True, change_default=True)
    tasks = fields.One2many('project.task', 'mom_id', string="Task Activities")


    # @api.onchange('tasks')
    # def tasks_changed(self):
    #     print(f'=========>>>> tasks_changed, self: {self}')
        # self.write({'tasks': self.tasks})
        # return {'type': 'ir.actions.client', 'tag': 'reload'}

    # def write(self, vals):
    #     print(f'=========>>>> write, vals: {vals}')
    #     return super().write(vals)

class SdMomTask(models.Model):
    _inherit = 'project.task'

    mom_id = fields.Many2one('sd_mom.moms')
    date_deadline_j = fields.Char()

    @api.model
    def create(self, vals):
        if vals.get('mom_id'):
            vals['project_id'] = self.env['project.project'].sudo().search([('name', '=', 'MOM')]).id
            vals['stage_id'] = self.sudo().stage_find(vals['project_id'], [
                    ('fold', '=', False), ('is_closed', '=', False)])
        return super().create(vals)

    # def write(self, vals):
    #     print(f'==========    TASK WRITE\n {vals}\n')
    #
    #     return super().write(vals)

