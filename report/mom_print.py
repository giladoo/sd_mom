# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http
import re

class DictToObject:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class ReportHrExtendIpacResumeEn(models.AbstractModel):
    _name = 'report.sd_mom.mom_print_template'
    # _name = 'report.hr_employee.resume_en_report'
    _description = 'MOM Print'

    # ########################################################################################
    def get_report_values(self, docids=None, data=None):
        return self._get_report_values(docids, data)

    # ########################################################################################
    @api.model
    def _get_report_values(self, docids=None, data=None):
        errors = []
        doc_data_list = []
        PAGE_LINES = 25
        CLEANR = re.compile('<.*?>')
        context = self.env.context
        time_z = pytz.timezone(context.get('tz'))
        date_time = datetime.now(time_z)
        calendar = context.get('lang')
        date_time1 = self.date_converter(date_time, context.get('lang'))
        docs = self.env['sd_mom.moms'].browse(docids)
        data = dict({rec.id: DictToObject(**{'name': rec.name,
                                             'project_name': rec.project_id.name,
                                             'location': rec.location.name,
                                             'location_des': rec.location_des,
                                             'description': rec.description,
                                             'description_2': rec.description_2,
                                             'logo_block_1': list([partner.id for partner in rec.logo_1 ]),
                                             'logo_block_2': list([partner.id for partner in rec.logo_2 ]),
                                             'is_attendees': True if len(re.sub(CLEANR, "", rec.list_1)) > 0 or len(re.sub(CLEANR, "", rec.list_1)) > 0 else False ,
                                             'is_list_1': True if len(re.sub(CLEANR, "", rec.list_1)) > 0 else False,
                                             'is_list_2': True if len(re.sub(CLEANR, "", rec.list_2)) > 0 else False,
                                             'is_list_3': True if len(re.sub(CLEANR, "", rec.list_3)) > 0 else False,
                                             'list_title_1': rec.list_title_1,
                                             'list_title_2': rec.list_title_2,
                                             'list_title_3': rec.list_title_3,
                                             'list_1': rec.list_1,
                                             'list_2': rec.list_2,
                                             'list_3': rec.list_3,
                                             # 'is_agenda': True if len(re.sub(CLEANR, "", rec.agenda)) > 0 else False,
                                             'agenda': rec.agenda,
                                             'mom_date': self.date_converter(rec.mom_date, calendar)['date'],
                                             'start_time_hour': rec.start_time_hour,
                                             'start_time_minute': rec.start_time_minute,
                                             'end_time_hour': rec.end_time_hour,
                                             'end_time_minute': rec.end_time_minute,
                                             'assistant': rec.assistant,
                                             'page_count': rec.page_count,
                                             'mom_no': rec.mom_no,
                                             'tasks': [DictToObject(**{'mom_line_no': task_rec.mom_line_no,
                                                                       'name': task_rec.name,
                                                                       'mom_detail': task_rec.mom_detail if len(re.sub(CLEANR, "", task_rec.mom_detail)) > 0 else '',
                                                                       'date_deadline': self.date_converter(task_rec.date_deadline, calendar)['date'],
                                                                       'mom_responsible': task_rec.mom_responsible.split('\n') if task_rec.mom_responsible else [],
                                                                       'stage_id': task_rec.stage_id.name,
                                                                       'is_closed': task_rec.is_closed,
                                                                       }) for task_rec in rec.tasks]})
                     for rec in docs})

        # for rec_id, rec_value in data.items():
            # print(f'==============\n {rec_id}   {rec_value}')
            # for task in rec_value.tasks:
            #     print(f'           {task.mom_line_no} {task.name} {task.mom_detail} [{re.sub(CLEANR, "", task.mom_detail)}] len detail:{len(task.mom_detail)} ')


        return {
            'docs': docs,
            'data': data,
            'doc_ids': docids,

        }



    # ########################################################################################
    def date_converter(self, date_time, lang):
        if date_time:
            if lang == 'fa_IR':
                date_time = jdatetime.datetime.fromgregorian(datetime=date_time)
                date_time = {'date': date_time.strftime("%Y/%m/%d"),
                      'time': date_time.strftime("%H:%M:%S")}
            else:
                date_time = {'date': date_time.strftime("%Y-%m-%d"),
                            'time': date_time.strftime("%H:%M:%S")}
        else:
            date_time = {'date': '',
                         'time': ''}
        return date_time

    # ########################################################################################
    def _table_record(self, items, start_date, first_day, last_day, record_type=False):
        day = len(list([item for item in items
                        if (not record_type or item.record_type.name == record_type)
                        and item.record_date == start_date]))

        month = len(list([item for item in items
                          if (not record_type or item.record_type.name == record_type)
                          and item.record_date <= start_date
                          and item.record_date >= first_day ]))

        total = len(list([item for item in items if (not record_type or item.record_type.name == record_type)]))
        return day, month, total

    # ########################################################################################
    def _table_record_sum_of_records(self, items, start_date, first_day, last_day, record_type=False):
        day = sum(list([item.man_hours for item in items
                        if (not record_type or item.record_type.name == record_type)
                        and item.record_date == start_date]))

        month = sum(list([item.man_hours for item in items
                          if (not record_type or item.record_type.name == record_type)
                          and item.record_date <= start_date
                          and item.record_date >= first_day ]))

        total = sum(list([item.man_hours for item in items if (not record_type or item.record_type.name == record_type)]))
        day = int(round(day, 0))
        month = int(round(month, 0))
        total = int(round(total, 0))
        return day, month, total

