from SPARQLWrapper import SPARQLWrapper, JSON
import Levenshtein
#import editdistance
#import jaccard_index
#from jaccard_index.jaccard import jaccard_index
#import jaro
from fuzzywuzzy import fuzz
import pickle



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


def eval_results_more_sim(output, entity, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, taxonomy_type):
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

       filter_results_1 = []
       filter_uri_1 = []

       filter_results_2 = []
       filter_uri_2 = []

       print("entity", entity)
       if len(entity.split()) <= 7:
              if taxonomy_type == 1: # files esco_occupation.ttl or esco_skill.ttl
                     if compare == ">=":
                            for binding in results['bindings']:
                                   if string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type_1) >= threshold_1 or \
                                           string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type_1) >= threshold_1 or \
                                           string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type_1) >= threshold_1:
                                          filter_results_1.append(binding)
                                          filter_uri_1.append(binding['skill']['value'])
                                   if string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type_2) >= threshold_2 or \
                                           string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type_2) >= threshold_2 or \
                                           string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type_2) >= threshold_2:
                                          filter_results_2.append(binding)
                                          filter_uri_2.append(binding['skill']['value'])


              else: # files ict_skills_collection.ttl or language_skills_collection.ttl or transversal_skills_collection.ttl
                     if compare == ">=":
                            for binding in results['bindings']:
                                   if string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type_1) >= threshold_1 or \
                                           string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type_1) >= threshold_1:
                                          filter_results_1.append(binding)
                                          filter_uri_1.append(binding['skill']['value'])
                                   if string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type_2) >= threshold_2 or \
                                           string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type_2) >= threshold_2:
                                          filter_results_2.append(binding)
                                          filter_uri_2.append(binding['skill']['value'])

       return list(set(filter_uri_1)), list(set(filter_uri_2)) # if needed we can use filter_results


def eval_results_more_sim_designation(output, entity, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, taxonomy_type, list_designations):
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

       filter_results_1 = []
       filter_uri_1 = []

       filter_results_2 = []
       filter_uri_2 = []

       designations_matches_1 = []
       designations_matches_2 = []


       if taxonomy_type == 1: # files esco_occupation.ttl or esco_skill.ttl
              if compare == ">=":
                     for binding in results['bindings']:
                            if len(entity.split()) <= 7:
                                   if string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type_1) >= threshold_1 or \
                                           string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type_1) >= threshold_1 or \
                                           string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type_1) >= threshold_1:
                                          filter_results_1.append(binding)
                                          filter_uri_1.append(binding['skill']['value'])
                                   if string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type_2) >= threshold_2 or \
                                           string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type_2) >= threshold_2 or \
                                           string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type_2) >= threshold_2:
                                          filter_results_2.append(binding)
                                          filter_uri_2.append(binding['skill']['value'])

                            for des in list_designations:
                                   if len(des.split()) <= 7:
                                          sim1_1 = string_sim(binding['prefLabel']['value'].lower(), des.lower(), dist_type_1)
                                          sim2_1 = string_sim(binding['altLabel']['value'].lower(), des.lower(), dist_type_1)
                                          sim3_1 = string_sim(binding['hiddenLabel']['value'].lower(), des.lower(), dist_type_1)
                                          if sim1_1 >= threshold_1 or sim2_1 >= threshold_1 or sim3_1 >= threshold_1:
                                                 if binding['skill']['value'] not in designations_matches_1:
                                                        designations_matches_1.append(binding['skill']['value'])

                                          sim1_2 = string_sim(binding['prefLabel']['value'].lower(), des.lower(), dist_type_2)
                                          sim2_2 = string_sim(binding['altLabel']['value'].lower(), des.lower(), dist_type_2)
                                          sim3_2 = string_sim(binding['hiddenLabel']['value'].lower(), des.lower(), dist_type_2)
                                          if sim1_2 >= threshold_2 or sim2_2 >= threshold_2 or sim3_2 >= threshold_2:
                                                 if binding['skill']['value'] not in designations_matches_2:
                                                        designations_matches_2.append(binding['skill']['value'])


       else: # files ict_skills_collection.ttl or language_skills_collection.ttl or transversal_skills_collection.ttl
              if compare == ">=":
                     for binding in results['bindings']:
                            if len(entity.split()) <= 7:
                                   if string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type_1) >= threshold_1 or \
                                           string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type_1) >= threshold_1:
                                          filter_results_1.append(binding)
                                          filter_uri_1.append(binding['skill']['value'])
                                   if string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type_2) >= threshold_2 or \
                                           string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type_2) >= threshold_2:
                                          filter_results_2.append(binding)
                                          filter_uri_2.append(binding['skill']['value'])

                            for des in list_designations:
                                   if len(des.split()) <= 7:
                                          sim1_1 = string_sim(binding['prefLabel']['value'].lower(), des.lower(), dist_type_1)
                                          sim2_1 = string_sim(binding['altLabel']['value'].lower(), des.lower(), dist_type_1)
                                          if sim1_1 >= threshold_1 or sim2_1 >= threshold_1:
                                                 if binding['skill']['value'] not in designations_matches_1:
                                                        designations_matches_1.append(binding['skill']['value'])

                                          sim1_2 = string_sim(binding['prefLabel']['value'].lower(), des.lower(), dist_type_2)
                                          sim2_2 = string_sim(binding['altLabel']['value'].lower(), des.lower(), dist_type_2)
                                          if sim1_2 >= threshold_2 or sim2_2 >= threshold_2:
                                                 if binding['skill']['value'] not in designations_matches_2:
                                                        designations_matches_2.append(binding['skill']['value'])

       return list(set(filter_uri_1)), list(set(filter_uri_2)), designations_matches_1, designations_matches_2 # if needed we can use filter_results



def eval_results_uri_occupation(output, entity, compare, threshold, dist_type):
       '''
       This is one variation of eval_results to match the occupetions
       :param output:
       :param entity:
       :param compare:
       :param threshold:
       :param dist_type:
       :return:
       '''

       results = output['results']

       filter_uri_tot = []
       filter_uri = []
       scores = []

       if compare == ">=":
              for binding in results['bindings']:
                     sim1 = string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type)
                     sim2 = string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type)
                     sim3 = string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type)
                     if sim1 >= threshold or sim2 >= threshold or sim3 >= threshold:
                            filter_uri_tot.append(binding['skill']['value'])
                            if binding['skill']['value'] not in filter_uri:
                                   filter_uri.append(binding['skill']['value'])
                                   scores.append(max(sim1, sim2, sim3))

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
              max_pos = scores.index(max_score)
              filter_uri = [filter_uri[max_pos]]

       return filter_uri_tot, filter_uri # if needed we can use filter_results


def eval_results_uri_occupation_designation(output, entity, compare, threshold, dist_type, list_designations):
       '''
       This is one variation of eval_results to match the occupations
       :param output:
       :param entity:
       :param compare:
       :param threshold:
       :param dist_type:
       :return:
       '''

       results = output['results']

       filter_uri_tot = []
       filter_uri = []
       scores = []

       designations_matches = []

       if compare == ">=":
              for binding in results['bindings']:
                     sim1 = string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type)
                     sim2 = string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type)
                     sim3 = string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type)
                     if sim1 >= threshold or sim2 >= threshold or sim3 >= threshold:
                            filter_uri_tot.append(binding['skill']['value'])
                            if binding['skill']['value'] not in filter_uri:
                                   filter_uri.append(binding['skill']['value'])
                                   scores.append(max(sim1, sim2, sim3))

                     for des in list_designations:
                            sim1_1 = string_sim(binding['prefLabel']['value'].lower(), des.lower(), dist_type)
                            sim2_1 = string_sim(binding['altLabel']['value'].lower(), des.lower(), dist_type)
                            sim3_1 = string_sim(binding['hiddenLabel']['value'].lower(), des.lower(), dist_type)
                            if sim1_1 >= threshold or sim2_1 >= threshold or sim3_1 >= threshold:
                                   if binding['skill']['value'] not in designations_matches:
                                          designations_matches.append(binding['skill']['value'])

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

                     for des in list_designations:
                            sim1_1 = string_sim(binding['prefLabel']['value'].lower(), des.lower(), dist_type)
                            sim2_1 = string_sim(binding['altLabel']['value'].lower(), des.lower(), dist_type)
                            sim3_1 = string_sim(binding['hiddenLabel']['value'].lower(), des.lower(), dist_type)
                            if sim1_1 <= threshold or sim2_1 <= threshold or sim3_1 <= threshold:
                                   filter_uri_tot.append(binding['skill']['value'])
                                   if binding['skill']['value'] not in designations_matches:
                                          designations_matches.append(binding['skill']['value'])

       if len(scores) != 0:
              max_score = max(scores)
              max_pos = scores.index(max_score)
              filter_uri = [filter_uri[max_pos]]

       return filter_uri_tot, filter_uri, designations_matches # if needed we can use filter_results


def eval_results_uri_occupation_more_sim(output, entity, compare, threshold_1, threshold_2, dist_type_1, dist_type_2):
       '''
       This is one variation of eval_results_uri_occupation to consider 2 different similarity types (for faster evaluation)
       :param output:
       :param entity:
       :param compare:
       :param threshold:
       :param dist_type:
       :return:
       '''

       results = output['results']

       filter_uri_tot_1 = []
       filter_uri_1 = []
       scores_1 = []

       filter_uri_tot_2 = []
       filter_uri_2 = []
       scores_2 = []

       if compare == ">=":
              for binding in results['bindings']:
                     sim1_1 = string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type_1)
                     sim2_1 = string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type_1)
                     sim3_1 = string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type_1)
                     if sim1_1 >= threshold_1 or sim2_1 >= threshold_1 or sim3_1 >= threshold_1:
                            filter_uri_tot_1.append(binding['skill']['value'])
                            if binding['skill']['value'] not in filter_uri_1:
                                   filter_uri_1.append(binding['skill']['value'])
                                   scores_1.append(max(sim1_1, sim2_1, sim3_1))

                     sim1_2 = string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type_2)
                     sim2_2 = string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type_2)
                     sim3_2 = string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type_2)
                     if sim1_2 >= threshold_2 or sim2_2 >= threshold_2 or sim3_2 >= threshold_2:
                            filter_uri_tot_2.append(binding['skill']['value'])
                            if binding['skill']['value'] not in filter_uri_2:
                                   filter_uri_2.append(binding['skill']['value'])
                                   scores_2.append(max(sim1_2, sim2_2, sim3_2))


       if len(scores_1) != 0:
              max_score_1 = max(scores_1)
              max_pos_1 = scores_1.index(max_score_1)
              filter_uri_1 = [filter_uri_1[max_pos_1]]

       if len(scores_2) != 0:
              max_score_2 = max(scores_2)
              max_pos_2 = scores_2.index(max_score_2)
              filter_uri_2 = [filter_uri_2[max_pos_2]]

       return filter_uri_tot_1, filter_uri_1, filter_uri_tot_2, filter_uri_2 # if needed we can use filter_results


def eval_results_uri_occupation_designation_more_sim(output, entity, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, list_designations):
       '''
       This is one variation of eval_results_uri_occupation to consider 2 different similarity types (for faster evaluation)
       :param output:
       :param entity:
       :param compare:
       :param threshold:
       :param dist_type:
       :return:
       '''

       results = output['results']

       filter_uri_tot_1 = []
       filter_uri_1 = []
       scores_1 = []

       filter_uri_tot_2 = []
       filter_uri_2 = []
       scores_2 = []

       designations_matches_1 = []
       designations_matches_2 = []

       if compare == ">=":
              for binding in results['bindings']:
                     sim1_1 = string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type_1)
                     sim2_1 = string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type_1)
                     sim3_1 = string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type_1)
                     if sim1_1 >= threshold_1 or sim2_1 >= threshold_1 or sim3_1 >= threshold_1:
                            filter_uri_tot_1.append(binding['skill']['value'])
                            if binding['skill']['value'] not in filter_uri_1:
                                   filter_uri_1.append(binding['skill']['value'])
                                   scores_1.append(max(sim1_1, sim2_1, sim3_1))

                     sim1_2 = string_sim(binding['prefLabel']['value'].lower(), entity.lower(), dist_type_2)
                     sim2_2 = string_sim(binding['altLabel']['value'].lower(), entity.lower(), dist_type_2)
                     sim3_2 = string_sim(binding['hiddenLabel']['value'].lower(), entity.lower(), dist_type_2)
                     if sim1_2 >= threshold_2 or sim2_2 >= threshold_2 or sim3_2 >= threshold_2:
                            filter_uri_tot_2.append(binding['skill']['value'])
                            if binding['skill']['value'] not in filter_uri_2:
                                   filter_uri_2.append(binding['skill']['value'])
                                   scores_2.append(max(sim1_2, sim2_2, sim3_2))

                     for des in list_designations:
                            sim11 = string_sim(binding['prefLabel']['value'].lower(), des.lower(), dist_type_1)
                            sim21 = string_sim(binding['altLabel']['value'].lower(), des.lower(), dist_type_1)
                            sim31 = string_sim(binding['hiddenLabel']['value'].lower(), des.lower(), dist_type_1)
                            if sim11 >= threshold_1 or sim21 >= threshold_1 or sim31 >= threshold_1:
                                   print("sssssssssss", des)
                                   if binding['skill']['value'] not in designations_matches_1:
                                          designations_matches_1.append(binding['skill']['value'])

                            sim12 = string_sim(binding['prefLabel']['value'].lower(), des.lower(), dist_type_2)
                            sim22 = string_sim(binding['altLabel']['value'].lower(), des.lower(), dist_type_2)
                            sim32 = string_sim(binding['hiddenLabel']['value'].lower(), des.lower(), dist_type_2)
                            if sim12 >= threshold_2 or sim22 >= threshold_2 or sim32 >= threshold_2:
                                   print("kkkkkkkkkk", des)
                                   if binding['skill']['value'] not in designations_matches_2:
                                          designations_matches_2.append(binding['skill']['value'])


       if len(scores_1) != 0:
              max_score_1 = max(scores_1)
              max_pos_1 = scores_1.index(max_score_1)
              filter_uri_1 = [filter_uri_1[max_pos_1]]

       if len(scores_2) != 0:
              max_score_2 = max(scores_2)
              max_pos_2 = scores_2.index(max_score_2)
              filter_uri_2 = [filter_uri_2[max_pos_2]]

       return filter_uri_tot_1, filter_uri_1, filter_uri_tot_2, filter_uri_2, designations_matches_1, designations_matches_2 # if needed we can use filter_results


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

       return matches # list of matches (uris)


def eval_results_tot_more_sim(output, list_entities, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, taxonomy_type): # maybe instead of list entities we have key-value(resume/job proposal: list entities)
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

       matches_1 = []
       matches_2 = []
       for e in list_entities:
              print(e)
              filter_uri = eval_results_more_sim(output, e, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, taxonomy_type)
              matches_1 = (set(matches_1) | set(filter_uri[0])) # set not needed bcs already sets
              matches_2 = (set(matches_2) | set(filter_uri[1]))

       return set(matches_1), set(matches_2) # lists of matches (uris)



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
       if len(set(list_uri_occupations_resume).intersection(set(list_uri_occupations_job))) != 0:
              score += 3

       # score given by entities from resume and job proposal mapping to same entities into the taxonomy
       for el in list_uri_skills_resume: # retrieved from all the 5 skills ttl files
              if el in list_uri_skills_job_proposal:
                     score += 1  # if resume's skill and job proposal's map to same entity in the taxonomy

       set_matching = set()
       set_matching_2 = set()

       # score given by entities from resume that map to essential/optional skills for job proposal's skills
       for binding in results_ess_opt['bindings']:
              for el in list_uri_skills_resume:
                     if el == binding['skill']['value'] and binding['essential']['value'] in list_uri_skills_job_proposal:
                            if el not in set_matching:
                                   score += 0.5 # if mapped skill from resume is essential skill for a skill required by job proposal
                                   set_matching.add(el)
                     elif el == binding['skill']['value'] and binding['optional']['value'] in list_uri_skills_job_proposal:
                            if el not in set_matching:
                                   score += 0.25 # if mapped skill from resume is optional skill for a skill required by job proposalset_matching.add(el)
                                   set_matching.add(el)

       # score given by entities from resume that map to essential/optional skills for job proposal's occupation
                     if el == binding['skill']['value'] and binding['essential']['value'] in list_uri_occupations_job_filter:
                            if el not in set_matching_2:
                                   score += 0.5  # if mapped skill from resume is essential skill for the job (occupation)
                                   set_matching_2.add(el)
                     elif el == binding['skill']['value'] and binding['optional']['value'] in list_uri_occupations_job_filter:
                            if el not in set_matching_2:
                                   score += 0.25  # if mapped skill from resume is optional skill for the job (occupation)
                                   set_matching_2.add(el)

       return score


def compute_score_des(output_ess_opt, list_uri_skills_resume, list_uri_skills_job_proposal, list_uri_occupations_resume, list_uri_occupations_job, list_uri_occupations_job_filter, list_designations_job, list_designations_resume):
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
       if len(set(list_uri_occupations_resume).intersection(set(list_uri_occupations_job))) != 0:
              score += 3

       # score given by entities from resume and job proposal mapping to same entities into the taxonomy (skills)
       for el in list_uri_skills_resume: # retrieved from all the 5 skills ttl files
              if el in list_uri_skills_job_proposal:
                     score += 1  # if resume's skill and job proposal's map to same entity in the taxonomy

       # score given by entities from resume and job proposal mapping to same entities into the taxonomy (designations)
       for el in list_designations_resume:  # retrieved from occupation ttl files
              if el in list_designations_job:
                     score += 1  # if resume's designation and job proposal's map to same entity in the taxonomy

       set_matching = set()
       set_matching_2 = set()

       # score given by entities from resume that map to essential/optional skills for job proposal's skills
       for binding in results_ess_opt['bindings']:
              for el in list_uri_skills_resume:
                     if el == binding['skill']['value'] and binding['essential']['value'] in list_uri_skills_job_proposal:
                            if el not in set_matching:
                                   score += 0.5 # if mapped skill from resume is essential skill for a skill required by job proposal
                                   set_matching.add(el)
                     elif el == binding['skill']['value'] and binding['optional']['value'] in list_uri_skills_job_proposal:
                            if el not in set_matching:
                                   score += 0.25 # if mapped skill from resume is optional skill for a skill required by job proposalset_matching.add(el)
                                   set_matching.add(el)

       # score given by entities from resume that map to essential/optional skills for job proposal's occupation
                     if el == binding['skill']['value'] and binding['essential']['value'] in list_uri_occupations_job_filter:
                            if el not in set_matching_2:
                                   score += 0.5  # if mapped skill from resume is essential skill for the job (occupation)
                                   set_matching_2.add(el)
                     elif el == binding['skill']['value'] and binding['optional']['value'] in list_uri_occupations_job_filter:
                            if el not in set_matching_2:
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



