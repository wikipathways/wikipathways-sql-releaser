import glob
import os
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


def parse_rdf():
    i = 0
    for file in glob.glob('*/*/*/*.ttl'):
        if i < 10:
            i += 1
            print(file)
            g = Graph()
            g.parse(file, format='turtle')
            print 'g'
            print g
            # print(g.serialize(format='json-ld', indent=4))

# download_rdf(version, 'gpml')
# download_rdf(version, 'wp')
parse_rdf()
