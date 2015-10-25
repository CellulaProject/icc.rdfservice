"""Main entry point
"""
from pyramid.config import Configurator
import rdflib

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("icc.rdfservice.views")
    return config.make_wsgi_app()
