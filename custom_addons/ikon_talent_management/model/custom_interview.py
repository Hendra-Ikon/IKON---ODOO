import requests
from odoo import models, fields, api
from odoo.tools import is_html_empty
from datetime import datetime
import time

class CustomInterviewOne(models.Model):
    _inherit = "hr.applicant"

    applicant_id = fields.Many2one(
        comodel_name='hr.applicant', 
        string='Applicant')

    is_summarizing = fields.Boolean(default=False)
    
    # Field for first interview
    interviewer_one_ids = fields.Many2many('res.users', 'hr_applicant_res_users_interviewers_one_rel',
        string='First Interviewers', index=True, tracking=True,
        domain="[('share', '=', False), ('company_ids', 'in', company_id)]")
    interview_one_date = fields.Date(
        string="First Interview Date")
    interview_one_link = fields.Char(
        string="First Interview Link")
    is_first_link_valid = fields.Boolean(compute='_compute_is_first_link_valid', store=False)
    interview_one_decision = fields.Selection(
        string="First Interview Decision", 
        selection=[
            ('hire', 'Hire'), 
            ('do_not_hire', 'Do Not Hire'), 
            ('second_interview', 'Refer for 2nd Interview')])
    interview_one_summary = fields.Html(string="First Interview Summary")

    # Field for second interview
    interviewer_two_ids = fields.Many2many('res.users', 'hr_applicant_res_users_interviewers_two_rel',
        string='Second Interviewers', index=True, tracking=True,
        domain="[('share', '=', False), ('company_ids', 'in', company_id)]")
    interview_two_date = fields.Date(
        string="Second Interview Date")
    interview_two_link = fields.Char(
        string="Second Interview Link")
    is_second_link_valid = fields.Boolean(compute='_compute_is_second_link_valid', store=False)
    interview_two_decision = fields.Selection(
        string="Second Interview Decision", 
        selection=[
            ('hire', 'Hire'), 
            ('do_not_hire', 'Do Not Hire')])
    interview_two_summary = fields.Html(string="Second Interview Summary")
    
    def _compute_is_first_link_valid(self):
        for record in self:
            link = record.interview_one_link or ''
            record.is_first_link_valid = 'https://ikonsultancoid-my.sharepoint.com/' in link
    
    def _compute_is_second_link_valid(self):
        for record in self:
            link = record.interview_two_link or ''
            record.is_second_link_valid = 'https://ikonsultancoid-my.sharepoint.com/' in link    
    
    def notify(self, title, message):
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'sticky': True,
            }
        }

        return notification
    
    def write_interview_summary(self, summary, interview_num):
        if interview_num == 1:
            self.interview_one_summary = summary
        elif interview_num == 2:
            self.interview_two_summary = summary

    def action_summarize_interview(self):
        start_time = time.time()
       
        model = self.env['hr.job'].sudo()
        applied_position = self.job_id
        job = model.sudo().search([('id', '=', applied_position.id)], limit=1)
      
        interview_num = self.env.context.get('interview_num')

        if interview_num == 1:
            prompt_list = job.first_interview_summary_prompt
            interview_link = self.interview_one_link
        elif interview_num == 2:
            prompt_list = job.second_interview_summary_prompt
            interview_link = self.interview_two_link
        
        prompts = []

        for prompt in prompt_list:
            if prompt.dependency_field:
                dependency_name = prompt.dependency_field.name
                field = model._fields[dependency_name]
                field_value = getattr(job, dependency_name, False)

                dependency_value = str(field_value).replace('<ul>', '').replace('</ul>', '').replace('&nbsp;','').replace('</p>','').replace('<p>','\n-')
                requirement = f"{field.string}:\n{dependency_value}"
                
                prompt_template = f"Based on the previously provided interview transcript, please make detailed list, and each point mentions and explains {prompt.prompt.strip(' .')} with the following requirements in html format (e.g. <h2>Title</h2> <ul> <li> <strong>Point 1:</strong> <p> Explanation </p> </li> </ul>):\n{requirement}"
                
                prompts.append(prompt_template)
            else:
                prompt_template = f"Based on the previously provided interview transcript, please make detailed list, and each point mentions and explains {prompt.prompt.strip(' .')} in Bahasa Indonesia in html format (e.g. <h2>Title</h2> <ul> <li> <strong>Point 1:</strong> <p> Explanation </p> </li> </ul>)."
                
                prompts.append(prompt_template)

        try:
            response = requests.post('http://undetected-selenium:5000/summarize', json={
                'name': self.partner_name,
                'interview_link': interview_link,
                'prompts': prompts,
                'applied_job': job.name
            })

            if response.json().get('error'):
                raise Exception(response.json().get('error'))

            summary = response.json().get('summary')

            self.write_interview_summary(summary, interview_num)
            
            elapsed_time = time.time() - start_time
            message = f"Succesfully summarized interview, please refresh this page.\nTime elapsed {elapsed_time} seconds."
            title = "Success"
            return self.notify(title, message)
        
        except Exception as e:
            title = "ERROR"
            message = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: [ERROR] {e}\nCopy this message and send to your administrator.'
            return self.notify(title, message)

    def summarize_interview(self):
        # Check if already running
        if self.env['hr.applicant'].search_count([('is_summarizing', '=', True)]) > 0:
            return  # Exit if another instance is running
        
        # Set the flag to indicate the job is running
        self.env['hr.applicant'].update({'is_summarizing': True})

        try:
            first_interviewed_applicants = self.search([
                ('interview_one_summary', '=', False),
                ('interview_one_link', 'ilike', 'https://ikonsultancoid-my.sharepoint.com')
            ])

            first_interviewed_applicants += self.search([
                ('interview_one_summary', '=', '<p><br></p>'),
                ('interview_one_link', 'ilike', 'https://ikonsultancoid-my.sharepoint.com')
            ])

            second_interviewed_applicants = self.search([
                ('interview_two_summary', '=', False),
                ('interview_two_link', 'ilike', 'https://ikonsultancoid-my.sharepoint.com')
            ])

            second_interviewed_applicants += self.search([
                ('interview_two_summary', '=', '<p><br></p>'),
                ('interview_two_link', 'ilike', 'https://ikonsultancoid-my.sharepoint.com')
            ])

            for applicant in first_interviewed_applicants:
                applicant.with_context(interview_num=1).action_summarize_interview()

            for applicant in second_interviewed_applicants:
                applicant.with_context(interview_num=2).action_summarize_interview()
        finally:
            # Reset the flag when done
            self.env['hr.applicant'].update({'is_summarizing': False})