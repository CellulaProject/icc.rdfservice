from rdflib.namespace import Namespace
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, OWL, RDF, RDFS, SKOS, VOID, XMLNS, XSD


OA=Namespace("http://www.w3.org/ns/oa#")          # The Open Annotation ontology
CNT=Namespace("http://www.w3.org/2011/content#")   # Representing Content in RDF
#!!!! Strange behaviour like DC in rdflib is not a Namespace.
DC=Namespace("http://purl.org/dc/elements/1.1/") # Dublin Core Elements
#DCTERMS=Namespace("http://purl.org/dc/terms/")	 # Dublin Core Terms
DCTYPES=Namespace("http://purl.org/dc/dcmitype/") # Dublin Core Type Vocabulary
#FOAF=Namespace("http://xmlns.com/foaf/0.1/")	 # Friend-of-a-Friend Vocabulary
PROV=Namespace("http://www.w3.org/ns/prov#")	 # Provenance Ontology
#RDF=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")   # RDF
#RDFS=Namespace("http://www.w3.org/2000/01/rdf-schema#")     # RDF Schema
#SKOS=Namespace("http://www.w3.org/2004/02/skos/core#")      # Simple Knowledge Organization System
TRIG=Namespace("http://www.w3.org/2004/03/trix/rdfg-1/")	 # TriG Named Graphs"""
#EX=Namespace("") # Not used


#NEPOMUK ontolgies http://www.semanticdesktop.org/ontologies/

NRL=Namespace("http://www.semanticdesktop.org/ontologies/2007/08/15/nrl#")
NAO=Namespace("http://www.semanticdesktop.org/ontologies/2007/08/15/nao#")
NIE=Namespace("http://www.semanticdesktop.org/ontologies/2007/01/19/nie#")
NFO=Namespace("http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#")

NCO=Namespace("http://www.semanticdesktop.org/ontologies/2007/03/22/nco#")
NFO=Namespace("http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#")
NMO=Namespace("http://www.semanticdesktop.org/ontologies/2007/03/22/nmo#")
NCAL=Namespace("http://www.semanticdesktop.org/ontologies/2007/04/02/ncal#")
NEXIF=Namespace("http://www.semanticdesktop.org/ontologies/2007/05/10/nexif#")
NID3=Namespace("http://www.semanticdesktop.org/ontologies/2007/05/10/nid3#")
NMM=Namespace("http://www.semanticdesktop.org/ontologies/2009/02/19/nmm#")

PIMO=Namespace("http://www.semanticdesktop.org/ontologies/2007/11/01/pimo#")
NSO=Namespace("http://www.semanticdesktop.org/ontologies/2009/11/08/nso#")
TMO=Namespace("http://www.semanticdesktop.org/ontologies/2008/05/20/tmo#")
NDO=Namespace("http://www.semanticdesktop.org/ontologies/2010/04/30/ndo#")
NUAO=Namespace("http://www.semanticdesktop.org/ontologies/2010/01/25/nuao#")
DCON=Namespace("http://www.semanticdesktop.org/ontologies/2011/10/05/dcon#")
DPLO=Namespace("http://www.semanticdesktop.org/ontologies/2011/10/05/dlpo#")
DPO=Namespace("http://www.semanticdesktop.org/ontologies/2011/10/05/dpo#")
DAO=Namespace("http://www.semanticdesktop.org/ontologies/2011/10/05/dao#")
DDO=Namespace("http://www.semanticdesktop.org/ontologies/2011/10/05/ddo#")
DUHO=Namespace("http://www.semanticdesktop.org/ontologies/2011/10/05/duho#")
DRMO=Namespace("http://www.semanticdesktop.org/ontologies/2012/03/06/drmo#")

#User and software description (weak): http://www.daml.org/ontologies/151

# Ontology describes some operational model. That is, OperOnt describes
# concepts that allow the interoperation of actors at a semantic level
# without pre-establishing specific protocols.

NAMESPACES={}

vars={}
keys=list(globals().keys())

for k in keys:
    v=globals()[k]
    if v.__class__==Namespace:
        NAMESPACES[k.lower()]=v

NAMESPACES['dc']=DC

del keys, k, v

"""
N=Namespace("")
N=Namespace("")
N=Namespace("")
N=Namespace("")

PIMO ...
"""
