from SPARQLWrapper import SPARQLWrapper, JSON
import Levenshtein
import editdistance
import jaccard_index
from jaccard_index.jaccard import jaccard_index
import jaro
import pickle


# todo check similarity string

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
       #print(output)
       return output


def levenshtein_sim(str1, str2):
       '''
       Given two strings, it returns the similarity between them by using levenshtein distance
       :param str1:
       :param str2:
       :return:
       '''
       return 1 - (Levenshtein.distance(str1, str2) / max(len(str1), len(str2)))

def edit_sim(str1, str2):
       '''
       Given two strings, it returns the similarity between them by using edit distance
       :param str1:
       :param str2:
       :return:
       '''
       return 1 - (editdistance.eval(str1, str2) / max(len(str1), len(str2)))

def string_sim(str1, str2, dist_type):
       '''
       Given two strings and a type of distance/similarity, it returns their similarity
       :param str1:
       :param str2:
       :param dist_type:
       :return:
       '''
       if dist_type == "levenshtein":
              return levenshtein_sim(str1, str2)
       elif dist_type == "edit":
              return edit_sim(str1, str2)
       elif dist_type == "jaccard":
              return jaccard_index(str1, str2)
       elif dist_type == "jaro":
              return jaro.jaro_winkler_metric(str1, str2)


def eval_results(output, entity, compare, threshold, dist_type, taxonomy_type):
       '''
       Given the output containing all the labels from the taxonomy section of skills and occupations, the entity (string)
       to match and a threshold, it returns the labels with the related skill URI that have similarity with the entity
       below the threshold, taxonomy_type (1,2) indicates if we consider the section of occupations and skills or of
       different skills
       :param output:
       :param entity:
       :param threshold:
       :return:
       '''
       results = output['results']
       #print(results)

       filter_results = []
       filter_uri = []

       if taxonomy_type == 1:
              if compare == ">=":
                     for binding in results['bindings']:
                            if string_sim(binding['prefLabel']['value'], entity, dist_type) >= threshold or \
                                    string_sim(binding['altLabel']['value'], entity, dist_type) >= threshold or \
                                    string_sim(binding['hiddenLabel']['value'], entity, dist_type) >= threshold:
                                   filter_results.append(binding)
                                   filter_uri.append(binding['skill']['value'])
              else:
                     for binding in results['bindings']:
                            if string_sim(binding['prefLabel']['value'], entity, dist_type) <= threshold or \
                                    string_sim(binding['altLabel']['value'], entity, dist_type) <= threshold or \
                                    string_sim(binding['hiddenLabel']['value'], entity,
                                               dist_type) <= threshold:
                                   filter_results.append(binding)
                                   filter_uri.append(binding['skill']['value'])
       else: # taxonomy part with 3 different skills does not have hiddenLabel
              if compare == ">=":
                     for binding in results['bindings']:
                            if string_sim(binding['prefLabel']['value'], entity, dist_type) >= threshold or \
                                    string_sim(binding['altLabel']['value'], entity, dist_type) >= threshold:
                                   filter_results.append(binding)
                                   filter_uri.append(binding['skill']['value'])
              else:
                     for binding in results['bindings']:
                            if string_sim(binding['prefLabel']['value'], entity, dist_type) <= threshold or \
                                    string_sim(binding['altLabel']['value'], entity, dist_type) <= threshold:
                                   filter_results.append(binding)
                                   filter_uri.append(binding['skill']['value'])
       return list(set(filter_uri)) # if needed we can use filter_results


def eval_results_tot(output, list_entities, compare, threshold, dist_type, taxonomy_type): # maybe instead of list entities we have key-value(resume/job proposal: list entities)
       '''
       Given the output from the query, the list of retrieved entities, it finds the matches (uris without duplicates
        for the entities inside the taxonomy using string similarity
       :param output:
       :param list_entities:
       :param compare:
       :param threshold:
       :param dist_type:
       :param taxonomy_type:
       :return:
       '''
       matches = []
       filter_uri = []
       for e in list_entities:
              filter_uri = eval_results(output, e, compare, threshold, dist_type, taxonomy_type)
       matches = list(set(matches) | set(filter_uri)) # set not needed bcs already sets
       score = len(matches)

       return (matches, score) # list of matches and score -> score is 1 for each match -> total number of matches


def score_plus(output, list_uri_skills_resume, list_uri_skills_job_proposal, list_uri_occupations_job, score):
       '''
       Given the output with essential and optional skills/occupations, the list of uris for resume's skills (output of
       eval_results_tot), the list of uris for job proposal's skills (output of eval_results_tot), the list of uris for
       job proposal's occupations (output of eval_results_tot on the type of job), it returns the final score (sum of
       score given by the matching entities and plus score -> +0.5 if essential skill for a skill/occupation, +0.25 if
       optional skill)
       :param output_skills:
       :param output_occupations:
       :param list_uri_skills_resume:
       :param list_uri_skills_job_proposal:
       :param list_uri_occupations_job:
       :return:
       '''
       results = output['results']

       for binding in results['bindings']:
              for el in list_uri_skills_resume:
                     if len(binding['essential']['value']) >= 33 and binding['essential']['value'][0:33] == 'http://data.europa.eu/esco/skill/':
                            if el == binding['essential']['value'] and binding['essential']['value'] in list_uri_skills_job_proposal:
                                   score += 0.5
                            elif el == binding['optional']['value'] and binding['optional']['value'] in list_uri_skills_job_proposal:
                                   score += 0.25

       for binding in results['bindings']:
              for el in list_uri_occupations_job:
                     if len(binding['essential']['value']) >= 33 and binding['essential']['value'][0:38] == 'http://data.europa.eu/esco/occupation/':
                            if el == binding['essential']['value'] and binding['essential']['value'] in list_uri_occupations_job:
                                   score += 0.5
                            elif el == binding['optional']['value'] and binding['optional']['value'] in list_uri_occupations_job:
                                   score += 0.25






# Example


# similerities

str = 'http://data.europa.eu/esco/occuaption/ciao'
print(str[0:38])
print(len(str[0:38]))
print(edit_sim("python programming", "pytho prog"))
print(levenshtein_sim("python programming", "pytho prog"))
print(jaccard_index("python programming", "pytho prog"))
print(jaro.jaro_winkler_metric("python programming", "programmer"))



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

y = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
PREFIX esco: <http://ec.europa.eu/esco/model#>      
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>   
SELECT ?skill ?prefLabel ?altLabel
WHERE {     
    ?skill skos:prefLabel ?prefLabel .
    ?skill skos:altLabel ?altLabel .
    
    FILTER (lang(?prefLabel) = 'en')
    FILTER (lang(?altLabel) = 'en')

}
"""

# TODO query with isEssentialSkillFor / isOptionalSkillFor -> retrieve url -> retrieve type (check if it is in occupation.ttl or skill.ttl
z = """
    PREFIX esco: <http://data.europa.eu/esco/model#>      
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?skill ?prefLabel ?altLabel ?essential ?optional
WHERE {  
    ?skill skos:prefLabel ?prefLabel .
    ?skill skos:altLabel ?altLabel .  
    ?skill esco:isEssentialSkillFor ?essential .
    ?skill esco:isOptionalSkillFor ?optional .  
    
    FILTER (lang(?prefLabel) = 'en')
    FILTER (lang(?altLabel) = 'en')

}
"""
output = sparql_query(z, "http://localhost:3030/ds")
print(output)

'''?skill esco:isEssentialSkillFor ?x .
    ?skill esco:isOptionalSkillFor ?y .'''

# get output -> into pickle

'''output = sparql_query(x, "http://localhost:3030/ds")
file_x = open("skill_occupation.pickle", "wb")
pickle.dump(output, file_x)
file_x.close()'''

'''output = sparql_query(x, "http://localhost:3030/ds")
file_x1 = open("skill.pickle", "wb")
pickle.dump(output, file_x1)
file_x1.close()'''

'''output = sparql_query(x, "http://localhost:3030/ds")
file_x2 = open("occupation.pickle", "wb")
pickle.dump(output, file_x2)
file_x2.close()'''

'''output = sparql_query(y, "http://localhost:3030/ds")
file_y = open("skill_digital_language_en.pickle", "wb")
pickle.dump(output, file_y)
file_y.close()'''


# load pickle

'''file_x = open("skill_occupation.pickle", "rb")
skill_occupation = pickle.load(file_x)
print(skill_occupation)'''

'''file_x1 = open("skill.pickle", "rb")
skill = pickle.load(file_x1)
print(skill)'''

'''file_x2 = open("occupation.pickle", "rb")
occupation = pickle.load(file_x2)
print(occupation)'''

'''file_y = open("skill_digital_language.pickle", "rb")
skill_digital_language = pickle.load(file_y)
print(skill_digital_language)'''






# evaluate similarity

'''res = eval_results(skill, "writing Punjabi", ">=", 0.7, "levenshtein", 1)
print(res)
print(len(res))'''

'''res1 = eval_results(output, "writing Punjabi", ">=", 0.7, "levenshtein", 2)
print(res1)
print(len(res1))'''






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


