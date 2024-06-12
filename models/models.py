# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
from datetime import datetime
import pytz


class SdMomMoms(models.Model):
    _name = 'sd_mom.moms'
    _description = 'sd_mom.moms'
    _inherit = ['mail.thread', 'mail.activity.mixin']



    def _location_domain(self):
        domain = []
        partners = self.env['res.partner'].search([])
        partners = list([rec.id for rec in partners if rec.company_type == 'company'])
        if partners:
            domain = [('id', 'in', partners)]
        return domain

    def _default_project_id(self):
        project_id = self.env['project.project']

        # stage_id = self.sudo().stage_find(project_id.id, [('fold', '=', False), ('is_closed', '=', False)])
        print(f'============  \n {project_id}  \n {self.env.context}\n')
        return project_id
    logo_1 = fields.Many2many('res.partner', 'res_partner_sd_mom_moms_logo_1', domain=lambda self: self._location_domain())
    logo_2 = fields.Many2many('res.partner', 'res_partner_sd_mom_moms_logo_2', domain=lambda self: self._location_domain())
    # location = fields.Many2one('res.partner', 'res_partner_sd_mom_moms_location', domain="[('company_type', '=', 'company')]")
    location = fields.Many2one('res.partner', domain=lambda self: self._location_domain())
    project_id = fields.Many2one('project.project', required=True, tracking=True)
    name = fields.Char(required=True, translate=True, tracking=True)
    mom_no = fields.Char(required=True,  tracking=True)
    mom_date = fields.Date(required=True, tracking=True,
                             default=lambda self: datetime.now(pytz.timezone(self.env.context.get('tz', 'Asia/Tehran'))))
    active = fields.Boolean(default=True)
    # location = fields.Char()
    description = fields.Html()
    agenda = fields.Html()
    description_2 = fields.Html()
    def _list_title(self):
        return [('client', 'Client'),
                ('consultant', 'Consultant'),
                ('contractor', 'Contractor'),
                ('internal', 'Internal'),
                ('others', 'Others')]

    list_title_1 = fields.Selection(selection='_list_title', default='client')
    list_title_2 = fields.Selection(selection='_list_title', default='consultant')
    list_title_3 = fields.Selection(selection='_list_title', default='contractor')

    list_1 = fields.Html()
    list_2 = fields.Html()
    list_3 = fields.Html()
    state = fields.Selection([('ongoing', 'Ongoing'),
                              ('stopped', 'Stopped'),
                              ('canceled', 'Canceled'),
                              ('done', 'Done')], default='ongoing', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    # stage_id = fields.Many2one('')
    mom_id = fields.Many2one('sd_mom.moms', string='MOM',
        default=False, recursive=True, store=True, readonly=False,
        index=True, tracking=True, check_company=True, change_default=True)
    # project_id = fields.Many2one('project.project', default=lambda self: self._default_project_id())
    tasks = fields.One2many('project.task', 'mom_id', string="Task Activities",  tracking=True,)


    def write(self, vals):
        if vals.get('tasks'):
            # print(f'----------------------------------------\n'
            #       f'{vals.get("tasks")}')
            # tasks_sequence = list([rec[1] for rec in vals.get('tasks') if rec[0] and rec[2] and rec[2].get('sequence')])
            new_tasks = []
            new_task = []
            line_no = 1
            for task in vals.get("tasks"):
                new_task = task
                if task[0] == 0:
                    new_task[2]['mom_line_no'] = line_no
                elif task[0] == 1:
                    new_task[2]['mom_line_no'] = line_no
                elif task[0] == 4:
                    new_task[0] = 1
                    new_task[2] = {'mom_line_no': line_no}
                new_tasks.append(new_task)
                line_no += 1
            # print(f'---------------\n {new_tasks}')
            vals["tasks"] = new_tasks
        return super().write(vals)

    @api.model
    def create(self, vals):
        new_tasks = []
        line_no = 1
        for task in vals.get("tasks"):
            # print(f'===== CREATE =====\n {task}')
            new_task = task
            new_task[2]['mom_line_no'] = line_no
            new_task[2]['sequence'] = line_no
            new_tasks.append(new_task)
            line_no += 1
            # print(f'\n {new_task}\n')

        vals["tasks"] = new_tasks
        return super().create(vals)


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
    # date_deadline_j = fields.Char()
    mom_detail = fields.Html()
    mom_line_no = fields.Integer(string='No')

    @api.model
    def create(self, vals):
        if vals.get('mom_id'):
            # vals['project_id'] = self.env['project.project'].sudo().search([('name', '=', 'MOM')]).id
            vals['stage_id'] = self.sudo().stage_find(vals['project_id'], [
                    ('fold', '=', False), ('is_closed', '=', False)])
        return super().create(vals)

    # def write(self, vals):
    #     print(f'==========    TASK WRITE\n {vals}\n')
    #
    #     return super().write(vals)

