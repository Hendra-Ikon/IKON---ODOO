
from datetime import datetime, timedelta
from odoo import models, api, fields

class YourModel(models.Model):
    _name = 'ikon.date'

    @api.model
    def get_dates_within_one_week(self, ids=None, prefetch_ids=None, context=None):
        today = fields.Date.today()
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        end_of_current_week = today + timedelta(days=6)

        dates_within_one_week = []

        current_date = monday
        while current_date <= min(sunday, end_of_current_week):
            dates_within_one_week.append(current_date)
            current_date += timedelta(days=1)

        return dates_within_one_week

    def print_dates_within_one_week(self, ids=None, prefetch_ids=None, context=None):
        dates_within_one_week = self.get_dates_within_one_week()
        for date in dates_within_one_week:
            print(date)
#
# your_model_instance = YourModel()
#
# # Call the print_dates_within_one_week method on the instance
# your_model_instance.print_dates_within_one_week()
