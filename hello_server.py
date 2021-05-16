#! /usr/lib/python3.6
#imports
#from datetime import datetime
# import sys
# print(sys.path)
import graphene, flask, flask_graphql
import mongoengine
from mongoengine.fields import StringField, ReferenceField, ListField

# from flask_graphql import GraphQLView
# from graphene import ObjectType, Field, String, Schema

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

# connect to databaseIn our Tumblelog application we need to store several different types of information. We will need to have a collection of users, so that we may link posts to an individual. We also need to store our different types of posts (eg: text, image and link) in the database. To aid navigation of our Tumblelog, posts may have tags associated with them, so that the list of posts shown to the user may be limited to posts that have been assigned a specific tag. Finally, it would be nice if comments could be added to posts. We’ll start with users, as the other document models are slightly more involved.
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

