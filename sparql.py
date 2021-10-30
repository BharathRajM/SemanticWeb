from SPARQLWrapper import SPARQLWrapper, JSON
import Levenshtein
import sys, json
import requests

# TODO too many triples -> find another solution or make queries at different times and save intermediate results
# We can divide the skill file into two files

def sparql_query(query, endpoint):
       '''
       Given a sparql query and an endpoint ("http://localhost:3030/ds"), it returns the results for the query
       :param query:
       :param endpoint:
       :return:
       '''
       sparql = SPARQLWrapper(endpoint)
       print(query)
       sparql.setQuery(query)
       sparql.setReturnFormat(JSON)
       output = sparql.query().convert()
       print(output)
       return output


def string_sim(str1, str2, dist_type):
       '''
       Given two strings and a type of distance/similarity, it returns their similarity
       :param str1:
       :param str2:
       :param dist_type:
       :return:
       '''
       if dist_type == "levenshtein":
              return Levenshtein.distance(str1, str2)


def eval_results(output, entity, threshold, dist_type):
       '''
       Given the output containing all the labels from the taxonomy, the entity (string) to match and a threshold, it
       returns the labels with the related skill URI that have similarity with the entity below the threshold
       :param output:
       :param entity:
       :param threshold:
       :return:
       '''
       results = output['results']
       print(results)

       filter_results = []
       for binding in results['bindings']:
              if string_sim(binding['prefLabel']['value'], entity, dist_type) <= threshold or string_sim(binding['altLabel']['value'] or string_sim(binding['hiddenLabel']['value']) <= threshold, entity, dist_type) <= threshold:
                     filter_results.append(binding)

       return filter_results



# Example

# query ttl file skill/occupetion
x = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
PREFIX esco: <http://ec.europa.eu/esco/model#>      
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
SELECT ?skill ?prefLabel ?altLabel ?hiddenLabel
WHERE {     
    ?skill skos:prefLabel ?prefLabel .
    ?skill skos:altLabel ?altLabel .
    ?skill skos:hiddenLabel ?hiddenLabel .
    
    
}

"""


# query set of 3 ttl little files
x = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
PREFIX esco: <http://ec.europa.eu/esco/model#>      
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
SELECT ?skill ?prefLabel ?altLabel
WHERE {     
    ?skill skos:prefLabel ?prefLabel .
    ?skill skos:altLabel ?altLabel .

}

"""

# THIS SEEMS TO WORK!!!
y = """SELECT ?subject ?predicate ?object
WHERE {
  ?subject ?predicate ?object

}"""

output = sparql_query(x, "http://localhost:3030/ds")
res = eval_results(output, "writing Punjabi", 10, "levenshtein")
print(res)
print(len(res))






# Other stuff

'''response = requests.post('http://localhost:3030/ds',
       data={'query': 'ASK { ?s ?p ?o . }'})
print(response)
print(response.json())'''

'''from SPARQLWrapper import SPARQLWrapper, JSON, XML
#import urllib.request module. Don't forget for Python 3.4 the urllib has been split into several different modules.
import urllib.request

#if the arg is empty in ProxyHandler, urllib will find itself your proxy config.
proxy_support = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

#connect to the sparql point
sparql = SPARQLWrapper("http://localhost:3030/ds/sparql")
#SPARQL request
sparql.setQuery("""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
PREFIX esco: <http://ec.europa.eu/esco/model#>      
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
SELECT ?position    
WHERE {     
    ?s rdf:type esco:Occupation. 
    { ?position skos:prefLabel ?label. } 
    UNION 
    { ?position skos:altLabel ?label. } 
    FILTER (lcase(?label)= \"assistante scolaire\"@fr ) 
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["o"]["value"])
'''

'''response = requests.post('http://localhost:3030/ds/sparql',
       data={'query': 'SELECT ?subject ?predicate ?object WHERE {?subject ?predicate ?object}'})
print(response.json())'''


'''print(jsonLogic({"edit_distance" : ['bahama', 'banana']}))
print(jsonLogic({"edit_distance" : ['bahama', 'de']}))
print(jsonLogic({"edit_distance" : ['bahama', 'rear']}))
print(jsonLogic({"some" : [["banana", "de", "rear"], { "<=" : [{"edit_distance" : [{"var" : ""}, "bahama"]}, 2]}]}))
'''

y = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
PREFIX esco: <http://ec.europa.eu/esco/model#>      
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
SELECT ?position    
WHERE {     
    ?s rdf:type esco:Occupation. 
    { ?position skos:prefLabel ?label. } 
    UNION 
    { ?position skos:altLabel ?label. } 
    FILTER (lcase(?label)= \"assistante scolaire\"@fr ) 
}
"""


