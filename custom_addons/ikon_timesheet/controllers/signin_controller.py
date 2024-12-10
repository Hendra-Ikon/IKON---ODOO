from odoo import http
from odoo.addons.graphql_base import GraphQLControllerMixin
from ..graphql.signin_schema import SigninSchema

# calls graphiql inside odoo
class SigninGraphQLController(http.Controller, GraphQLControllerMixin):
    @http.route("/graphiql/signin", auth="none", type="http", csrf=False)
    def graphiql_signin(self, **kwargs):
        return self._handle_graphiql_request(SigninSchema.graphql_schema)
    
# calls graphql inside odoo
    @http.route("/graphql/signin", auth="none", type="http", csrf=False)
    def graphql_signin(self, **kwargs):
        return self._handle_graphql_request(SigninSchema.graphql_schema)