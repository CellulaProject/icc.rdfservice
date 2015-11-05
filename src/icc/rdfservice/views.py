""" Cornice services.
"""
from cornice.resource import add_resource
from zope.component import queryUtility
from icc.rdfservice.interfaces import IGraph
from pyramid.response import Response

class Triples(object):
    """
    """

    def __init__(self, request):
        """
        """
        self.request=request
        self.name=self.request.matchdict['name']
        self.graph=queryUtility(IGraph, self.name)

    def get(self):
        g=self.graph
        if g == None:
            self.request.response.status_code=404
            return Response("{'error':'no such graph'}")
        Q="""
        SELECT DISTINCT ?id
        WHERE {
         ?ann a oa:Annotation .
         ?ann oa:hasBody ?body .
         ?body nao:identifier ?id .
        }
        """
        qres=g.query(Q)
        return Response(body='\n'.join([r[0].toPython() for r in qres]), content_type="text/plain")

    def collection_post(self):
        """Append new document to the storage"""

        data=self.request.body
        sha_id=storage().put(data)
        return {'id': sha_id}

    def collection_get(self):
        return {'text':'Hello world!'}


graph_resource = add_resource(
    Triples,
    path='/api-fields/{name}',
    collection_path='/api-fields',
)

def includeme(config):
    config.add_cornice_resource(graph_resource)
