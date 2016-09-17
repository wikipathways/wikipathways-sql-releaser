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
    for file in glob.glob('rdf/wp/*/*.ttl'):
        if i < 1:
            i += 1
            print(file)
            g = Graph()
            g.parse(file, format='turtle')
            print 'g'
            print g

            qres = g.query(
                '''PREFIX wp:    <http://vocabularies.wikipathways.org/wp#>
                SELECT DISTINCT ?s
                WHERE {
                  ?s a wp:DataNode
                }''')

#             qres = g.query(
#                 '''PREFIX wp:    <http://vocabularies.wikipathways.org/wp#>
#                 SELECT *
#                 {
#                   ?s <http://vocabularies.wikipathways.org/wp#isAbout> ?o
#                 }''')

#             qres = g.query(
#                 '''SELECT *
#                 {
#                   ?s <http://vocabularies.wikipathways.org/wp#isAbout> ?o
#                 }''')

#             qres = g.query(
#                 '''SELECT DISTINCT ?s ?o
#                 {
#                   ?s <http://vocabularies.wikipathways.org/wp#isAbout> ?o
#                 }''')

#             qres = g.query(
#                 '''
#                 SELECT DISTINCT ?aname ?bname
#                 WHERE {
#                   ?a wp:isAbout ?b
#                 }
#                 ''')

#             qres = g.query(
#                 '''SELECT ?aisAbout
#                 ''')

#             qres = g.query(
#                 '''@prefix wp:    <http://vocabularies.wikipathways.org/wp#> .
#                 SELECT DISTINCT ?wp:isAbout
#                 ''')
#             print 'qres'
#             print qres
#             print ''
#             print 'type'
#             print type(qres)
#             print ''
#             print 'dir'
#             print dir(qres)
#             print ''
#             print 'qres.__dict__'
#             print qres.__dict__
#             print ''
#             print 'qres.serialize()'
#             print qres.serialize()
            for row in qres:
#                 print 'qres row'
#                 print row
                for item in row:
                    print '  ' + item
                # print('%s is the id' % row)

# download_rdf(version, 'gpml')
# download_rdf(version, 'wp')
parse_rdf()
