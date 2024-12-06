from odoo import http
from odoo.addons.graphql_base import GraphQLControllerMixin
from ..graphql.schema import schema

class TimesheetGraphQLController(http.Controller, GraphQLControllerMixin):
    @http.route("/graphql/timesheet", auth="user", type="http", csrf=False)
    def graphql_timesheet(self, **kwargs):
        return self._handle_graphql_request(schema)
    
    @http.route("/graphiql/timesheet", auth="user", type="http")
    def graphiql_timesheet(self, **kwargs):
        return self._handle_graphiql_request(schema)