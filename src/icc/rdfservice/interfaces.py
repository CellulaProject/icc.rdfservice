from zope.interface import Interface, Attribute

class IGraph(Interface):
    """Marker interface denoting RDF graph.
    """

    identifier=Attribute('')
    namespace_manager=Attribute("this graph’s namespace-manager")
    store=Attribute('')


    def n3():
        """Returns n3 identifier for the graph.
        """

class ITripleStore(Interface):
    """Triple store driver marker interface.
    """

class IRDFService(Interface):
    """Demote service itself.
    """

    def initialize():
        """Read .ini configuration,
        creates and connects graphs.
        """

class IRDFStorage(Interface):
    def store(things):
        """Store info from things dictionary"""
