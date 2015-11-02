from zope.interface import implementer, Interface, Attribute
from icc.rdfservice.interfaces import IGraph, ITripleStore, IRDFService, IRDFStorage
from zope.component import getUtility, getGlobalSiteManager # , classImplements
import rdflib, rdflib.graph
import os, os.path
from icc.rdfservice.namespace import *
from rdflib import Literal, BNode, URIRef
import datetime

#classImplements(rdflib.graph.Graph, IGraph)
#classImplements(rdflib.graph.QuotedGraph, IGraph)

#classImplements(rdflib.graph.ConjunctiveGraph, IGraph)
#classImplements(rdflib.graph.DataSet, IGraph)
#classImplements(rdflib.graph.ReadOnlyGraphAggregate, IGraph)


@implementer(IRDFService)
class RDFService(object):
    """Creates World of graphs.
    """
    def __init__(self):
        self.initialize()

    def initialize(self):
        """Create graphs and load then with intial data
        if necessary."""

        config=getUtility(Interface, name='configuration')

        self.storages={}
        stores_descr=config['rdf_storages']
        for sto in stores_descr['all'].split(','):
            sto=sto.strip()
            self.init_storage(sto)

        graphs_descr=config['graphs']
        self.graphs={}
        self.ns_man=None

        all_descr=graphs_descr['all']
        for g in all_descr.split(','):
            g=g.strip()
            self.init_graph(g)

    def init_storage(self, storage):
        config=getUtility(Interface, name='configuration')
        storage_descr=config['rdf_storage_'+storage]

        data_dir=storage_descr.get('data_dir', None)
        data_file=storage_descr.get('data_file', storage)

        driver=storage_descr.get('driver', 'default')

        if data_dir != None:
            data_filepath=os.path.join(data_dir, data_file)
        else:
            data_filepath=None

        self.storages[storage]=(driver, data_filepath)

    def init_graph(self, name):
        config=getUtility(Interface, name='configuration')
        graph_descr=config['graph_'+name]
        contains=graph_descr.get('contains', None)
        identifier=graph_descr.get('id', name)
        storage=graph_descr['storage']
        load=graph_descr.get('load_from', None)

        sto_driver, sto_filepath=self.storages[storage]

        if contains == None:
            graph=rdflib.graph.Graph(
                store=sto_driver,
                identifier=identifier,
                namespace_manager=self.ns_man
            )
            if sto_filepath != None:
                graph.open(sto_filepath,create=True)

        else:
            if sto_driver != 'default':
                graph=rdflib.graph.ConjunctiveGraph(sto_driver, identifier=identifier)
                if sto_filepath != None:
                    graph.open(sto_filepath,create=True)
            else:
                graph=rdflib.graph.Dataset(sto_driver)
                for cg in contains.split(','):
                    cg=cg.strip()
                    g=self.graphs[cg]
                    graph.add_graph(g)

        if len(graph)==0 and load != None:
            try:
                graph.parse(load) # FIXME slashes in Windows
                graph.commit()
            except IOError:
                print ("Cannot load graph from URI:" + load)

        if name=='ns':
            self.ns_man=graph

        self.graphs[name]=graph
        GSM=getGlobalSiteManager()
        GSM.registerUtility(graph, IGraph, name=name)

@implementer(IRDFStorage)
class RDFStorage(object):
    graph_name=None

    @property
    def graph(self):
        """Return graph named graph_name.
        """
        return getUtility(IGraph, name=self.graph_name)

    def store(self, things):
        """Store things represented as mapping in the
        graph as triples.
        """

        g=self.graph
        for k,v in things.items():
            for s,p,o in self.convert(k,v, things):
                if s!=None:
                    g.add((s,p,o))

        g.commit()

    def convert(self, key, values, things):
        """Convert each value from values related
        to key.
        """
        if type(values) in [list, tuple]:
            # remove duplicates
            values=set(values)
            for v in values:
                yield from self.convert_one(key, v, things)
        else:
            yield from self.convert_one(key, values, things)

    def convert_one(self, key, value, things):
        """Convert one key-value pair in context of other things.

        Arguments:
        - `key`:
        - `value`:
        - `things`:
        """
        raise RuntimeError ("implemented by subclass.")

class DocMetadataStorage(RDFStorage):
    graph_name='doc'
    KEYS={
        "id":"_id"
    }

    def convert_one(self, k, v, ths):
        if k in self.KEYS:
            method_name = self.KEYS[k]
            method=getattr(self, method_name)
            yield from method(v, ths)
        else:
            print ("\n========================")
            print ("CNV: ", k, "->", str(v)[:100])
            yield (None, None, None)

    def _id(self, hash_id, ths):
        anno = BNode()

        # Anotation target
        target = BNode()
        yield (anno, OA.hasTarget, target)
        yield (target, NAO.identifier, Literal(hash_id))
        yield from self.p("Content-Type", target, NMO.mimeType, ths)
        yield (target, RDF.type, NFO.TextDocument)
        yield from self.p("File-Name", target, RDFS.label, ths)

        # Annotation itself
        if 'text-id' in ths:
            body = BNode()
            yield (anno, OA.hasBody, body)
            yield (body, NAO.identifier,Literal(ths['text-id']))

        # User
        yield (anno, NAO.creator, Literal(ths["user-id"]))
        now=datetime.datetime.now()
        ts=now.strftime("%Y-%m-%d %H:%M")
        yield (anno, NAO.created, Literal(ts,datatype=XSD.date))

    def p(self, key, s, o, ths, cls=Literal):
        if key in ths:
            yield (s, o, cls(ths[key]))
        else:
            yield (None, None, None)

class OrgStorage(RDFStorage):
    graph_name='org'
