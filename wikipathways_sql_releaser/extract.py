import glob
import os
from load import load
from rdflib import Graph
# we need to use the following to
# serialize to JSON-LD
# from rdflib import Graph, plugin
# from rdflib.serializer import Serializer
from StringIO import StringIO
from urllib import urlopen
from zipfile import ZipFile

version = '160910'
extract_dir = './latest_release'
os.chdir(extract_dir)


# NOTE: we're not currently using this for anything.
# We're just using the RDF.
def download_gpml(version):
    latest_release_url = str.join(
        'http://data.wikipathways.org/current/gpml/wikipathways-',
        version,
        '-gpml-Anopheles_gambiae.zip')

    url = urlopen(latest_release_url)
    zipfile = ZipFile(StringIO(url.read()))
    zipfile.extractall(extract_dir + '/gpml')


def download_rdf(version, aspect):
    latest_release_url = ''.join([
        'http://data.wikipathways.org/current/rdf/wikipathways-',
        version,
        '-rdf-',
        aspect,
        '.zip'])
    # GPML URL
    # latest_release_url = str.join(
    #   'http://data.wikipathways.org/current/gpml/wikipathways-',
    #   version,
    #   '-gpml-Anopheles_gambiae.zip')
    extract_dir = 'latest_release'

    url = urlopen(latest_release_url)
    zipfile = ZipFile(StringIO(url.read()))
    zipfile.extractall(extract_dir + '/rdf')


def load_node(id, label, source):
    node = {}
    node['id'] = str(id)
    node['label'] = str(label)
    node['source'] = str(source)
    os.chdir('..')
    load((node,))
    os.chdir(extract_dir)

def parse_rdf():
    i = 0
    for file in glob.glob('rdf/wp/*/*.ttl'):
        if i < 1:
            i += 1
            print(file)
            g = Graph()
            g.parse(file, format='turtle')

            # at a minimum, get:
            # interactions with targets that are also interactions
            # all sources and targets for all the above interactions,
            #   both primary and secondary
            #
            # for each interaction, get:
            #   id
            #   first type
            #   source
            #   target
            #
            # for each datanode, get:
            #   id
            #   first type
            #
            # if possible, also get all binding and cleavage reactions.

            controller_results = g.query(
                '''PREFIX wp:    <http://vocabularies.wikipathways.org/wp#>
                PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dc:    <http://purl.org/dc/elements/1.1/>
                SELECT DISTINCT ?controllerInteraction ?controlledInteraction ?controllerNodeId ?controllerNodeLabel ?controllerNodeSource
                WHERE {
                  ?controllerInteraction a wp:Interaction .
                  ?controllerInteraction wp:source ?controllerNodeId .
                  ?controllerNodeId rdfs:label ?controllerNodeLabel .
                  ?controllerNodeId dc:source ?controllerNodeSource .
                  ?controllerInteraction wp:target ?controlledInteraction .
                  ?controlledInteraction a wp:Interaction
                }''')

            for controller_row in controller_results:
                load_node(
                    str(controller_row.controllerNodeId),
                    str(controller_row.controllerNodeLabel),
                    str(controller_row.controllerNodeSource)
                )
                controlled_results = g.query(
                    '''PREFIX wp:    <http://vocabularies.wikipathways.org/wp#>
                    PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX dc:    <http://purl.org/dc/elements/1.1/>
                    SELECT DISTINCT ?sourceId ?sourceLabel ?sourceSource ?targetId ?targetLabel ?targetSource
                    WHERE {
                      <%s> wp:source ?sourceId .
                      ?sourceId rdfs:label ?sourceLabel .
                      ?sourceId dc:source ?sourceSource .
                      <%s> wp:target ?targetId .
                      ?targetId rdfs:label ?targetLabel .
                      ?targetId dc:source ?targetSource
                    }''' % (controller_row.controlledInteraction, controller_row.controlledInteraction))
                for controlled_row in controlled_results:
                    load_node(
                        str(controlled_row.sourceId),
                        str(controlled_row.sourceLabel),
                        str(controlled_row.sourceSource)
                    )
                    load_node(
                        str(controlled_row.targetId),
                        str(controlled_row.targetLabel),
                        str(controlled_row.targetSource)
                    )

# download_rdf(version, 'gpml')
# download_rdf(version, 'wp')
parse_rdf()
