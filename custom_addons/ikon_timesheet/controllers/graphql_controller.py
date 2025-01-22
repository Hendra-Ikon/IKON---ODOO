from odoo import http
import logging
from odoo.addons.graphql_base import GraphQLControllerMixin
from ..graphql.schema import schema

_logger = logging.getLogger(__name__)

class TimesheetGraphQLController(http.Controller, GraphQLControllerMixin):
    @http.route("/graphql/timesheet",
                auth="user",
                type="http",
                csrf=False,
                methods=['GET', 'POST'])
    def graphql_timesheet(self, **kwargs):
        try:
            _logger.info("Processing GraphQL request")
            response = self._handle_graphql_request(schema.graphql_schema)
            _logger.info("GraphQL request processed successfully")
            return response
        except Exception as e:
            _logger.error(f"GraphQL request failed: {str(e)}")
            raise


# calls graphiql inside odoo    
    @http.route("/graphiql/timesheet", auth="user", type="http")
    def graphiql_timesheet(self, **kwargs):
        return self._handle_graphiql_request(schema.graphql_schema)