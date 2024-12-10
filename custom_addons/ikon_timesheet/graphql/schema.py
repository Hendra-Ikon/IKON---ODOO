import graphene
from odoo.addons.graphql_base import OdooObjectType

# Defines timesheet data structure and field
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

# Defines input structure for creating timesheets
class CreateTimesheetInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    project_id = graphene.Int(required=True)
    task_id = graphene.Int()
    unit_amount = graphene.Float(required=True)
    employee_id = graphene.Int(required=True)
    date = graphene.Date(required=True)

# Handles timesheet creation mutation
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

# Handles timesheet delete mutation
class DeleteTimesheet(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        env = info.context["env"]
        timesheet = env['account.analytic.line'].browse(id)
        if timesheet:
            timesheet.unlink()
            return DeleteTimesheet(success=True, message="Timesheet deleted successfully")
        return DeleteTimesheet(success=False, message="Timesheet not found")

# Handles timesheet state changes (approve/reject/resubmit)
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

# Defines available queries for timesheet operations
class Query(graphene.ObjectType):
    timesheets = graphene.List(TimesheetType)
    timesheet = graphene.Field(TimesheetType, id=graphene.Int(required=True))

    def resolve_timesheets(self, info):
        return info.context["env"]['account.analytic.line'].search([])

    def resolve_timesheet(self, info, id):
        return info.context["env"]['account.analytic.line'].browse(id)
    
# Registers available mutations for timesheet operations    
class Mutation(graphene.ObjectType):
    create_timesheet = CreateTimesheet.Field()
    update_timesheet = TimesheetMutation.Field()
    delete_timesheet = DeleteTimesheet.Field()

# Schema to call in controller
schema = graphene.Schema(query=Query, mutation=Mutation)