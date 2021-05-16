#! /usr/lib/python3.8
#imports
import graphene, flask, flask_graphql
import mongoengine
from mongoengine.fields import StringField, ReferenceField, ListField

# define MongoDB model
class PageModel(mongoengine.Document):
    meta = {'collection': 'page'}
    name = StringField()
    links = ListField(StringField()) # list of names of all links on page

class RequestModel(mongoengine.Document):
    meta = {'collection': 'request'}
    url = StringField()
    pageId = ReferenceField(PageModel)
    
# define GraphQL schema
class Page(graphene.ObjectType):
    name = graphene.String()
    links = graphene.List(graphene.String) # list of names of all links on page

class Request(graphene.ObjectType):
    page = Page()
    url = graphene.String()

class Query(graphene.ObjectType):
    page = graphene.Field(Page, name=graphene.String(), first_links=graphene.Int())
    request = graphene.Field(Request, url=graphene.String())

    def resolve_page(self, info, name, first_links):
        # query MongoDB database
        print(PageModel.objects(name="homePage").first().name)
        return Page(PageModel.objects(name="homePage").first().name, PageModel.objects(name="homePage").first().links[:first_links])

    def resolve_request(self, info, url):
        # query MongoDB database
        print("resolving request")
        return Request()

# class Mutation(graphene.ObjectType):
#     page = Page()
#     request = Request()

#     def resolve_page(self, info):
#         print("returning page")
#         return Page()
#     def resolve_request(self, info):
#         print("returning request")
#         return Request()

schema = graphene.Schema(
    query=Query,
    # mutation=Mutation
)

# query_all_pages = '''
#     query allPages {

#     }
# '''

mongoengine.connect(host='mongodb://127.0.0.1:27017/analytics-service', alias='default')

# set up server
app = flask.Flask(__name__)
app.debug = True

app.add_url_rule(
    '/dashboard',
    view_func=flask_graphql.GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

# run server
if __name__ == '__main__':
    app.run()

