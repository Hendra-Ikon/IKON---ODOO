from odoo import api, models

class TalentManagementTalentInheritXLSX(models.AbstractModel):
    _name = 'report.talent_management_talent_inherit.talent_management_talent_inherit_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):
        report_name = 'Talent Management Talent Inherit Report'
        worksheet = workbook.add_worksheet(report_name)
        bold = workbook.add_format({'bold': True})

        # Define your report header
        worksheet.write(0, 0, 'Name', bold)
        worksheet.write(0, 1, 'Phone Number', bold)
        worksheet.write(0, 2, 'Headline', bold)
        worksheet.write(0, 3, 'URL Linkedin', bold)
        worksheet.write(0, 4, 'Experience', bold)

        row = 1

        for record in records:
            # Populate the Excel rows with data
            worksheet.write(row, 0, record.name)
            worksheet.write(row, 1, record.no_tlp)
            worksheet.write(row, 2, record.skill)
            worksheet.write(row, 3, record.url)
            worksheet.write(row, 4, record.experience)

            row += 1
