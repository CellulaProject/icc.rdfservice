""" Cornice services.
"""
from cornice.resource import add_resource
from zope.component import queryUtility, getUtility
from icc.rdfservice.interfaces import IGraph
from icc.contentstorage.interfaces import IContentStorage
from pyramid.response import Response
import logging
logger=logging.getLogger('icc.cellula')

class Triples(object):
    """
    """

    def __init__(self, request):
        """
        """
        self.request=request

    def get(self):
        self.name=self.request.matchdict['name']
        g=queryUtility(IGraph, self.name)
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
        return Response(body='\n'.join(list(self._serve_get(qres)))+"\n", content_type="text/plain")

    def _serve_get(self, res):
        storage=getUtility(IContentStorage, name="content")
        for r in res:
            key=r[0].toPython()
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug ("Input key: %d" % key + " and its conten is of type %s." % type(storage.get(key)))
            yield key     # sent as hex digest, received as bytes, must be decoded to utf-8 THERE

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
