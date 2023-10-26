# from odoo import models, fields, api
#
#
# class CrmTeam(models.Model):
#     _inherit = 'crm.team'
#
#     opportunities_amount_formatted = fields.Char(
#         string='Opportunities Amount (Formatted)',
#         compute='_compute_opportunities_amount_formatted',
#         store=True
#     )
#
#     @api.depends('opportunities_amount')
#     def _compute_opportunities_amount_formatted(self):
#         for team in self:
#             if team.opportunities_amount >= 1000000:
#                 formatted_amount = "{:.0f} M".format(team.opportunities_amount / 1000000)
#             else:
#                 formatted_amount = "{:,.2f}".format(team.opportunities_amount)
#
#             team.opportunities_amount_formatted = formatted_amount
#
#     def _compute_opportunities_data(self):
#         opportunity_data = self.env['crm.lead']._read_group([
#             ('team_id', 'in', self.ids),
#             ('probability', '<', 100),
#             ('type', '=', 'opportunity'),
#         ], ['expected_revenue:sum', 'team_id'], ['team_id'])
#         counts = {datum['team_id'][0]: datum['team_id_count'] for datum in opportunity_data}
#         amounts = {datum['team_id'][0]: datum['expected_revenue'] for datum in opportunity_data}
#
#         for team in self:
#             team.opportunities_count = counts.get(team.id, 0)
#             team.opportunities_amount = amounts.get(team.id, 0)
#             # Update the formatted amount here
#             team._compute_opportunities_amount_formatted()
#
#     # def _compute_opportunities_data(self):
#     #     opportunity_data = self.env['crm.lead']._read_group([
#     #         ('team_id', 'in', self.ids),
#     #         ('probability', '<', 100),
#     #         ('type', '=', 'opportunity'),
#     #     ], ['expected_revenue:sum', 'team_id'], ['team_id'])
#     #     counts = {datum['team_id'][0]: datum['team_id_count'] for datum in opportunity_data}
#     #     amounts = {datum['team_id'][0]: datum['expected_revenue'] for datum in opportunity_data}
#     #     for team in self:
#     #         team.opportunities_count = counts.get(team.id, 0)
#     #         amount = amounts.get(team.id, 0)
#     #
#     #         if amount >= 1000000:
#     #             # Convert to millions (1 M)
#     #             # formatted_amount = str(round(amount / 1000000)) + ' M'
#     #             formatted_amount = str(round(amount / 1000000)) + 'M'
#     #
#     #         else:
#     #             formatted_amount = str(amount)
#     #
#     #         team.opportunities_amount = formatted_amount
#
#     # def _compute_opportunities_data(self):
#     #     opportunity_data = self.env['crm.lead']._read_group([
#     #         ('team_id', 'in', self.ids),
#     #         ('probability', '<', 100),
#     #         ('type', '=', 'opportunity'),
#     #     ], ['expected_revenue:sum', 'team_id'], ['team_id'])
#     #     counts = {datum['team_id'][0]: datum['team_id_count'] for datum in opportunity_data}
#     #     amounts = {datum['team_id'][0]: datum['expected_revenue'] for datum in opportunity_data}
#     #     for team in self:
#     #         team.opportunities_count = counts.get(team.id, 0)
#     #         amount = amounts.get(team.id, 0)
#     #
#     #         if amount >= 1000000:
#     #             # Convert to millions (1M, 10M, 100M)
#     #             millions_amount = amount / 1000000
#     #             if millions_amount.is_integer():
#     #                 team.opportunities_amount = "{:.0f} M".format(millions_amount)
#     #             else:
#     #                 team.opportunities_amount = "{:.2f} M".format(millions_amount)
#     #         else:
#     #             team.opportunities_amount = amount
#
#     # opportunities_amount_formatted = fields.Char(
#     #     string='Opportunities Amount (Formatted)',
#     #     compute='_compute_opportunities_amount_formatted',
#     #     store=True
#     # )
#     #
#     # @api.depends('opportunities_amount')
#     # def _compute_opportunities_amount_formatted(self):
#     #     for team in self:
#     #         if team.opportunities_amount >= 1000000:
#     #             formatted_amount = "{:.0f} M".format(team.opportunities_amount / 1000000)
#     #         else:
#     #             formatted_amount = "{:,.2f}".format(team.opportunities_amount)
#     #
#     #         team.opportunities_amount_formatted = formatted_amount
#     #
#     # def _compute_opportunities_data(self):
#     #     opportunity_data = self.env['crm.lead']._read_group([
#     #         ('team_id', 'in', self.ids),
#     #         ('probability', '<', 100),
#     #         ('type', '=', 'opportunity'),
#     #     ], ['expected_revenue:sum', 'team_id'], ['team_id'])
#     #     counts = {datum['team_id'][0]: datum['team_id_count'] for datum in opportunity_data}
#     #     amounts = {datum['team_id'][0]: datum['expected_revenue'] for datum in opportunity_data}
#     #
#     #     for team in self:
#     #         team.opportunities_count = counts.get(team.id, 0)
#     #         team.opportunities_amount = amounts.get(team.id, 0)
#     #         # Update the formatted amount here
#     #         team._compute_opportunities_amount_formatted()
