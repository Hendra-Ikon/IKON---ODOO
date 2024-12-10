import graphene
from odoo import http
from graphql import GraphQLError

# Defines partner information structure (name, email)
class Partner(graphene.ObjectType):
    name = graphene.String()
    email = graphene.String()

# Defines session data structure for authentication
class Session(graphene.ObjectType):
    session_id = graphene.String()
    user_id = graphene.String()
    username = graphene.String()
    login = graphene.String()
    partner = graphene.Field(Partner) 
    
# Handles login mutation with db, login, password
class Signin(graphene.Mutation):
    class Arguments:
        db = graphene.String(required=True)
        login = graphene.String(required=True)
        password = graphene.String(required=True)

    Output = Session

    def mutate(self, info, db, login, password):
        user = http.request.env['res.users'].sudo().search([('login', '=', login)], limit=1)
        
        if user:
            uid = http.request.session.authenticate(db, login, password)
            if uid:
                http.request.session.dbname = db
                http.request.session.uid = uid
                http.request.session.login = login
                
                session = Session(
                    session_id=http.request.session.sid,
                    user_id=user.id,
                    username=None if user.name == False else user.name,
                    login=user.login
                )
                
                partner = user.partner_id
                session.partner = Partner(
                    name=None if partner.name == False else partner.name,
                    email=None if partner.email == False else partner.email
                )
                
                return session
                
        raise GraphQLError("Invalid login or password", extensions={"statusCode": 401})

# Defines available queries for session management 
class Query(graphene.ObjectType):
    session = graphene.Field(Session)

    def resolve_session(self, info):
        if http.request.session and http.request.session.sid:
            session_id = http.request.session.sid
            user = http.request.env.user
            partner = user.partner_id
            return Session(
                session_id=session_id,
                username=user.name,
                login=user.login,
                partner=Partner(
                    name=None if partner.name == False else partner.name,
                    email=None if partner.email == False else partner.email
                )
            )
        else:
            raise GraphQLError("No active session")

# Defines available mutations for authentication
class Mutation(graphene.ObjectType):
    signin = Signin.Field()

# Schema to call in controller
SigninSchema = graphene.Schema(query=Query, mutation=Mutation)
