from SPARQLWrapper import SPARQLWrapper, JSON
import Levenshtein
import editdistance
import jaccard_index
from jaccard_index.jaccard import jaccard_index
import jaro
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pickle



# todo check similarity string
# todo lower strings ??


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

def jaccard(str1, str2):
       '''
       Given two strings, it returns the similarity between them by using jaccard similarity
       :param str1:
       :param str2:
       :return:
       '''

       return jaccard_index(str1, str2)

def fuzzywuzzy(str1, str2):
       '''
       Given two strings, it returns the similarity between them by usinf fuzzywuzzy
       :param str1:
       :param str2:
       :return:
       '''

       return fuzz.ratio(str1, str2)

# TODO
# def cosine similarity

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
              return jaccard(str1, str2)
       elif dist_type == "jaro":
              return jaro.jaro_winkler_metric(str1, str2)
       elif dist_type == "fuzzywuzzy":
              return fuzzywuzzy(str1, str2)
       # todo
       # put cosine here


def eval_results(output, entity, compare, threshold, dist_type, taxonomy_type):
       '''
       Given the output containing all the labels from the taxonomy section of skills and occupations, the entity (string)
       to match and a threshold, it returns the labels with the related skill URI that have similarity with the entity
       below the threshold, taxonomy_type (1,2) indicates if we consider the section of occupations/skills or of different
       skills
       :param output:
       :param entity:
       :param compare:
       :param threshold:
       :param dist_type:
       :param taxonomy_type:
       :return:
       '''

       results = output['results']
       #print(results)

       filter_results = []
       filter_uri = []


       if taxonomy_type == 1: # files esco_occupation.ttl or esco_skill.ttl
              if compare == ">=":
                     for binding in results['bindings']:
                            if string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type) >= threshold or \
                                    string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type) >= threshold or \
                                    string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type) >= threshold:
                                   filter_results.append(binding)
                                   filter_uri.append(binding['skill']['value'])
              else:
                     for binding in results['bindings']:
                            if string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type) <= threshold or \
                                    string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type) <= threshold or \
                                    string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type) <= threshold:
                                   filter_results.append(binding)
                                   filter_uri.append(binding['skill']['value'])
       else: # files ict_skills_collection.ttl or language_skills_collection.ttl or transversal_skills_collection.ttl
              if compare == ">=":
                     for binding in results['bindings']:
                            if string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type) >= threshold or \
                                    string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type) >= threshold:
                                   filter_results.append(binding)
                                   filter_uri.append(binding['skill']['value'])
              else:
                     for binding in results['bindings']:
                            if string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type) <= threshold or \
                                    string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type) <= threshold:
                                   filter_results.append(binding)
                                   filter_uri.append(binding['skill']['value'])
       return list(set(filter_uri)) # if needed we can use filter_results


def eval_results_uri_occupation(output, entity, compare, threshold, dist_type):
       '''
       This is one variation of eval_results to match the
       :param output:
       :param entity:
       :param compare:
       :param threshold:
       :param dist_type:
       :return:
       '''

       results = output['results']
       #print(results)

       filter_uri_tot = []
       filter_uri = []
       scores = []

       if compare == ">=":
              for binding in results['bindings']:
                     sim1 = string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type)
                     sim2 = string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type)
                     sim3 = string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type)
                     if sim1 >= threshold or sim2 >= threshold or sim3 >= threshold:
                            '''print("sim1", sim1)
                            print("sim2", sim2)
                            print("sim3", sim3)'''
                            filter_uri_tot.append(binding['skill']['value'])
                            if binding['skill']['value'] not in filter_uri:
                                   filter_uri.append(binding['skill']['value'])
                                   scores.append(max(sim1, sim2, sim3))
                                   #print("scores", scores)
       else:
              for binding in results['bindings']:
                     sim1 = string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type)
                     sim2 = string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type)
                     sim3 = string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type)
                     if sim1 >= threshold or sim2 >= threshold or sim3 >= threshold:
                            filter_uri_tot.append(binding['skill']['value'])
                            if binding['skill']['value'] not in filter_uri:
                                   filter_uri.append(binding['skill']['value'])
                                   scores.append(min(sim1, sim2, sim3))

       if len(scores) != 0:
              max_score = max(scores)
              print("max_score", max_score)
              max_pos = scores.index(max_score)
              print("max pos", max_pos)
              filter_uri = [filter_uri[max_pos]]
              print(filter_uri)

       return filter_uri_tot, filter_uri # if needed we can use filter_results


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
       for e in list_entities:
              filter_uri = eval_results(output, e, compare, threshold, dist_type, taxonomy_type)
              matches = (set(matches) | set(filter_uri)) # set not needed bcs already sets
       #score = len(matches)

       return matches # list of matches (uris)


def compute_score(output_ess_opt, list_uri_skills_resume, list_uri_skills_job_proposal, list_uri_occupations_resume, list_uri_occupations_job, list_uri_occupations_job_filter):
       '''
       Given the query's output with essential and optional skills/occupations, the list of uris for resume's skills
       (output of eval_results_tot), the list of uris for job proposal's skills (output of eval_results_tot), the list
       of uris for job proposal's occupations (output of eval_results_tot on the type of job), it returns the final score
       (sum of score given by the matching entities and additional score -> +0.5 if essential skill for a skill/occupation,
       +0.25 if optional skill)
       :param output_ess_opt:
       :param list_uri_skills_resume:
       :param list_uri_skills_job_proposal:
       :param list_uri_occupations_job:
       :return:
       '''

       # results from essential/optional skills
       results_ess_opt = output_ess_opt['results']

       score = 0

       # score given by if resume title and job title corresponds
       print("list_uri_occupations_job", list_uri_occupations_job)
       print("list_uri_occupations_resume", list_uri_occupations_resume)
       if len(set(list_uri_occupations_resume).intersection(set(list_uri_occupations_job))) != 0:
              print("plus 3")
              score += 3

       # score given by entities from resume and job proposal mapping to same entities into the taxonomy
       for el in list_uri_skills_resume: # retrieved from all the 5 skills ttl files
              if el in list_uri_skills_job_proposal:
                     print("plus 1")
                     score += 1  # if resume's skill and job proposal's map to same entity in the taxonomy

       set_matching = set()
       set_matching_2 = set()
       # score given by entities from resume that map to essential/optional skills for job proposal's skills
       print("list uri", list_uri_skills_job_proposal)
       for binding in results_ess_opt['bindings']:
              for el in list_uri_skills_resume:
                     #print("ellll", el)
                     #if len(binding['essential']['value']) >= 33 and binding['essential']['value'][0:33] == 'http://data.europa.eu/esco/skill/':
                     '''if binding['skill']['value'] == el:
                            print("qqqqqqqqqqq", binding['skill']['value'])
                     if binding['essential']['value'] == "http://data.europa.eu/esco/occupation/9ebaf3f0-0be0-47b7-b2b1-b3b04130fa81":
                            print("ddddddddd", binding['essential']['value'])'''
                     if el == binding['skill']['value'] and binding['essential']['value'] in list_uri_skills_job_proposal:
                            print("wwwwwwwwwwwww")
                            if el not in set_matching:
                                   print("sssssssssss", binding['skill']['value'], binding['essential']['value'])
                                   score += 0.5 # if mapped skill from resume is essential skill for a skill required by job proposal
                                   set_matching.add(el)
                     elif el == binding['skill']['value'] and binding['optional']['value'] in list_uri_skills_job_proposal:
                            print("zzzzzzzzzzzzzzzzzzzzzzzzzz")
                            if el not in set_matching:
                                   print("ssssssssssss1", binding['skill']['value'], binding['optional']['value'])
                                   score += 0.25 # if mapped skill from resume is optional skill for a skill required by job proposalset_matching.add(el)
                                   set_matching.add(el)

       # score given by entities from resume that map to essential/optional skills for job proposal's occupation
       #for binding in results_ess_opt['bindings']:
              #for el in list_uri_occupations_job:
                     #if len(binding['essential']['value']) >= 33 and binding['essential']['value'][0:38] == 'http://data.europa.eu/esco/occupation/':
                     if el == binding['skill']['value'] and binding['essential']['value'] in list_uri_occupations_job_filter:
                            if el not in set_matching_2:
                                   print("CIAO")
                                   score += 0.5  # if mapped skill from resume is essential skill for the job (occupation)
                                   set_matching_2.add(el)
                     elif el == binding['skill']['value'] and binding['optional']['value'] in list_uri_occupations_job_filter:
                            if el not in set_matching_2:
                                   print("CIAO1", binding['skill']['value'], binding['optional']['value'])
                                   score += 0.25  # if mapped skill from resume is optional skill for the job (occupation)
                                   set_matching_2.add(el)

       return score





# Example

# retrieved entities from resume/job proposal
'''list_entities_resume = ["python", "public relation", "logical skill", "problem solving", "English"]
list_entities_job = ["python", "public relation", "logic", "java", "English speaking"]
job_title_uri = ["http://data.europa.eu/esco/skill/0b071b01-4b40-4936-9d6d-d8c5609481b4"]



# skills/occupations
file_x1 = open("skill.pickle", "rb")
skill = pickle.load(file_x1)
print("done 1")
file_x2 = open("occupation.pickle", "rb")
occupation = pickle.load(file_x2)
print("done 2")
file_y = open("skill_digital_language.pickle", "rb")
skill_digital_language = pickle.load(file_y)
print("done 3")
file_y_1 = open("skill_digital_language_ess_opt.pickle", "rb")
opt_ess = pickle.load(file_y_1)
print("done 4")

resume_matches1 = eval_results_tot(skill, list_entities_resume, ">=", 80, "fuzzywuzzy", 1)
print('r1', resume_matches1)
resume_matches2 = eval_results_tot(skill_digital_language, list_entities_resume, ">=", 80, "fuzzywuzzy", 2)
print('r2', resume_matches2)
resume_matches_tot = resume_matches1 | resume_matches2 | {"http://data.europa.eu/esco/skill/7954861c-86d4-4529-afbb-2c23dab9ac74"}
print('r3', resume_matches_tot)
job_matches1 = eval_results_tot(skill, list_entities_job, ">=", 80, "fuzzywuzzy", 1)
print('j1', job_matches1)
job_matches2 = eval_results_tot(skill_digital_language, list_entities_job, ">=", 80, "fuzzywuzzy", 2)
print('j2', job_matches2)
job_matches_tot = job_matches1 | job_matches2 | {"http://data.europa.eu/esco/skill/dbdafb2b-c6ab-451e-abe3-81bd73994394"}
print('j3', job_matches_tot)
score = compute_score(opt_ess, resume_matches_tot, job_matches_tot, job_title_uri)
print(score)
'''


# Example


# similerities

'''str = 'http://data.europa.eu/esco/occuaption/ciao'
print(str[0:38])
print(len(str[0:38]))
print(edit_sim("python programming", "pytho prog"))
print(levenshtein_sim("python programming", "pytho prog"))
print(jaccard_index("python prog", "pytho prog"))
print(jaro.jaro_winkler_metric("python programming", "programmer"))'''



# query esco_occupation.ttl or esco_skill.ttl
'''
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


# query set of 3 ttl files -> files ict_skills_collection.ttl, language_skills_collection.ttl, transversal_skills_collection.ttl

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

# query to check isEssentialSkillFor / isOptionalSkillFor

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

z1 = """
    PREFIX esco: <http://data.europa.eu/esco/model#>      
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?skill ?essential ?optional
WHERE {  
    ?skill esco:isEssentialSkillFor ?essential .
    ?skill esco:isOptionalSkillFor ?optional .  
}
"""

'''


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

'''output = sparql_query(z, "http://localhost:3030/ds")
file_y_1 = open("skill_digital_language_ess_opt.pickle", "wb")
pickle.dump(output, file_y_1)
file_y_1.close()'''

'''output = sparql_query(z1, "http://localhost:3030/ds")
file_y_1 = open("skill_digital_language_ess_opt_1.pickle", "wb")
pickle.dump(output, file_y_1)
file_y_1.close()'''




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

'''file_y_1 = open("skill_digital_language_ess_opt.pickle", "rb")
opt_ess = pickle.load(file_y_1)
print(opt_ess)'''

'''file_y_1 = open("skill_digital_language_ess_opt_1.pickle", "rb")
opt_ess = pickle.load(file_y_1)
print(opt_ess)'''



# list of retrieved entities
'''li = ["english speaking"]
#res1 = eval_results_tot(skill, l, '>=', 0.6, "levenshtein", 1)
#print(res1)
res2 = eval_results_tot(skill_digital_language, li, '>=', 0.9, "jaccard", 2)
print(res2)'''



# evaluate similarity

'''res = eval_results(skill, "writing Punjabi", ">=", 0.7, "levenshtein", 1)
print(res)
print(len(res))'''

'''res1 = eval_results(output, "writing Punjabi", ">=", 0.7, "levenshtein", 2)
print(res1)
print(len(res1))'''



