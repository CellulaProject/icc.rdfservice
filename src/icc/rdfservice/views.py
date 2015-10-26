""" Cornice services.
"""
from cornice.resource import add_resource
from zope.component import getUtility




class Triples(object):
    """
    """

    def __init__(self, request):
        """
        """
        self.request=request
        self.graph=getUtility('graph')

    def collection_post(self):
        """Append new document to the storage"""

        data=self.request.body
        sha_id=storage().put(data)
        return {'id': sha_id}

    def collection_get(self):
        return {'text':'Hello world!'}


graph_resource = add_resource(
    Triples,
    path='/graph/{id}',
    collection_path='/graph',
)

def includeme(config):
    config.add_cornice_resource(graph_resource)
