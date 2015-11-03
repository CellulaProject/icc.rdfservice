from zope.interface import implementer, Interface, Attribute
from icc.rdfservice.interfaces import IGraph, ITripleStore, IRDFService, IRDFStorage
from zope.component import getUtility, getGlobalSiteManager # , classImplements
import rdflib, rdflib.graph
import os, os.path
from icc.rdfservice.namespace import *
from rdflib import Literal, BNode, URIRef
import datetime
from collections import OrderedDict

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
        self.graphs=OrderedDict()
        self.ns_man=None

        all_descr=graphs_descr['all']
        for g in all_descr.split(','):
            g=g.strip()
            self.init_graph(g)

        print (self.graphs)

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

        for nk,nv in NAMESPACES.items():
            graph.bind(nk,nv)

        if name=='ns':
            self.ns_man=graph

        self.graphs[name]=graph
        GSM=getGlobalSiteManager()
        GSM.registerUtility(graph, IGraph, name=name)

    def __del__(self):
        print ("Terminating graph storage ....")
        graphs=self.graphs.keys()
        graphs.reverse()
        for gk in graphs:
            g=self.graphs[gk]
            g.commit()
            g.close(True)




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
                if None in [s,p,o]:
                    continue
                else:
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

    NPM_FILTER=set([
        "nco:fullname",
        "nfo:tableOfContents",
        "nco:creator",
        ])

    def convert_one(self, k, v, ths):
        if k in self.KEYS:
            method_name = self.KEYS[k]
            method=getattr(self, method_name)
            yield from method(v, ths)
        else:
            #print ("\n========================")
            #print ("CNV: ", k, "->", str(v)[:100])
            yield (None, None, None)

    def _id(self, hash_id, ths):
        anno = BNode()

        # Anotation target
        target = BNode()
        yield (anno, RDF.type, OA.Annotation)
        yield (anno, OA.motivatedBy, OA.describing)
        yield (anno, OA.hasTarget, target)
        yield (target, NAO.identifier, Literal(hash_id))
        yield from self.p("Content-Type", target, NMO.mimeType, ths)
        if "rdf:type" in ths:
            yield from self.rdf(target, ths, filter_out=self.NPM_FILTER)
        else:
            yield (target, RDF.type, NFO.Document)
        yield from self.p("File-Name", target, NFO.fileName, ths)

        # Annotation itself
        if 'text-id' in ths:
            body = BNode()
            yield (anno, OA.hasBody, body)
            yield (body, RDF.type, CNT.ContextAsText)
            yield (body, NAO.identifier, Literal(ths['text-id']))
            if ths['text-body'].upper().find("</BODY") >= 0:
                yield (body, NMO.mimeType, Literal("text/html"))
                yield (body, RDF.type, NFO.HtmlDocument)
            else:
                yield (body, NMO.mimeType, Literal("text/plain"))
                yield (body, RDF.type, NFO.PlainTextDocument)

        # User
        user=BNode()
        yield (anno, OA.annotator, user)
        yield (user, RDF.type, FOAF.Person)
        yield (user, NAO.identifier, Literal(ths["user-id"]))
        utcnow=datetime.datetime.utcnow()
        # ts=utcnow.strftime("%Y-%m-%d%Z:%H:%M:%S")
        ts=utcnow.strftime("%Y-%m-%dT%H:%M:%SZ")
        yield (anno, OA.annotatedAt, Literal(ts,datatype=XSD.dateTime))

    def p(self, key, s, o, ths, cls=Literal):
        if key in ths:
            yield (s, o, cls(ths[key]))
        else:
            yield (None, None, None)

    def rdf(self, s, ths, filter_out=None):
        """Generate all found rdf relations,
        except mentioned in thw filter_out set."""
        keys=list(ths.keys())
        print ("Keys:", keys)
        for key in keys:
            val=ths[key]
            print ("->>>", key, ":", str(val)[:30])
            ks=key.split(":", maxsplit=1)
            if len(ks)!=2:
                continue
            if key in filter_out:
                continue
            key=ou(key)
            if type(val) in [int, float]:
                yield (s, key, Literal(val))
                continue
            if val.startswith('"') and val.endswith('"'):
                val=val.strip('"')
                yield (s, key, Literal(val))
                continue
            if val.startswith("'") and val.endswith("'"):
                val=val.strip("'")
                yield (s, key, Literal(val))
                continue
            vs=val.split(":", maxsplit=1)
            if len(vs)!=2:
                print ("Strange object value:", val, "for property:", key)
                continue
            yield (s, key, ou(val))


class OrgStorage(RDFStorage):
    graph_name='org'

    def name(self, ):
                   """
                   """



def ou(lit):
    """Converts string xxx:yyy to global
    space object XXX.yyy"""

    ns, ent = lit.split(":")
    try:
        ns=globals()[ns.upper()]
    except KeyError:
        return None

    try:
        rc=getattr(ns, ent)
    except AttributeError:
        rc=None
    return rc
