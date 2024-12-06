import graphene
from odoo.addons.graphql_base import OdooObjectType

class TimesheetType(OdooObjectType):
    class Meta:
        name = 'Timesheet'
        description = 'Timesheet entry type'
    
    id = graphene.Int()
    state = graphene.String()
    status = graphene.String()
    employee_id = graphene.Int()
    unit_amount = graphene.Float()
    name = graphene.String()
    date = graphene.Date()
    approved_date = graphene.Date()
    rejected_date = graphene.Date()
    rejected_reason = graphene.String()
    approved_id = graphene.Int()
    rejected_id = graphene.Int()

class CreateTimesheetInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    project_id = graphene.Int(required=True)
    task_id = graphene.Int()
    unit_amount = graphene.Float(required=True)
    employee_id = graphene.Int(required=True)
    date = graphene.Date(required=True)

class CreateTimesheet(graphene.Mutation):
    class Arguments:
        input = CreateTimesheetInput(required=True)

    timesheet = graphene.Field(TimesheetType)
    success = graphene.Boolean()

    def mutate(self, info, input):
        env = info.context["env"]
        vals = {
            'name': input.name,
            'project_id': input.project_id,
            'task_id': input.task_id,
            'unit_amount': input.unit_amount,
            'employee_id': input.employee_id,
            'date': input.date
        }
        timesheet = env['account.analytic.line'].create(vals)
        return CreateTimesheet(timesheet=timesheet, success=True)

class TimesheetMutation(graphene.Mutation):
    class Arguments:
        timesheet_id = graphene.Int(required=True)
        action = graphene.String(required=True)
        reason = graphene.String(required=False)

    success = graphene.Boolean()
    timesheet = graphene.Field(TimesheetType)

    def mutate(self, info, timesheet_id, action, reason=None):
        env = info.context["env"]
        timesheet = env['account.analytic.line'].browse(timesheet_id)
        
        if action == 'approve':
            timesheet.Action_Approve()
        elif action == 'reject':
            timesheet.Action_Reject()
            if reason:
                timesheet.rejected_reason = reason
        elif action == 'resubmit':
            timesheet.Action_Resubmit()
        
        return TimesheetMutation(success=True, timesheet=timesheet)

class Query(graphene.ObjectType):
    # GET all timesheets
    timesheets = graphene.List(TimesheetType)
    # GET timesheet by ID
    timesheet_byID = graphene.Field(TimesheetType, id=graphene.Int(required=True))
    
    def resolve_timesheets(self, info):
        return info.context["env"]['account.analytic.line'].search([])
    
    def resolve_timesheet(self, info, id):
        return info.context["env"]['account.analytic.line'].browse(id)

class Mutation(graphene.ObjectType):
    create_timesheet = CreateTimesheet.Field()
    update_timesheet = TimesheetMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)