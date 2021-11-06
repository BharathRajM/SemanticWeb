from sparql import *
import operator
import json

def job_eval(dict_jobs_entities_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, skill, occupation, skill_digital_language):
    '''
    Given the entities (skills) and csv fields (title) extracted for the job proposals, it maps them to the
    ontology retrieving the corresponding entites (uris) in it using string similarity
    :param dict_jobs_entities_title:
    :param compare:
    :param threshold:
    :param dist_type:
    :return:
    '''

    dict_jobs_results_1 = {}
    dict_jobs_results_2 = {}

    for job in dict_jobs_entities_title:

        job_matches1 = eval_results_tot_more_sim(skill, dict_jobs_entities_title[job][0], compare, threshold_1, threshold_2, dist_type_1, dist_type_2, 1)
        job_matches2 = eval_results_tot_more_sim(skill_digital_language, dict_jobs_entities_title[job][0], compare, threshold_1, threshold_2, dist_type_1, dist_type_2, 2)
        job_matches_tot_1 = job_matches1[0] | job_matches2[0]
        job_matches_tot_2 = job_matches1[1] | job_matches2[1]
        #job_occupation_uris = eval_results(occupation, dict_jobs_entities_title[job][1], compare, threshold, dist_type, 1)
        job_occupation_uris = eval_results_uri_occupation_more_sim(occupation, dict_jobs_entities_title[job][1], compare, threshold_1, threshold_2, dist_type_1, dist_type_2)
        dict_jobs_results_1[job] = (job_matches_tot_1, (job_occupation_uris[0], job_occupation_uris[1]))
        dict_jobs_results_2[job] = (job_matches_tot_2, (job_occupation_uris[2], job_occupation_uris[3]))

    return dict_jobs_results_1, dict_jobs_results_2


def job_eval_des(dict_jobs_entities_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, skill, occupation, skill_digital_language):
    '''
    Given the entities (skills) and csv fields (title) extracted for the job proposals, it maps them to the
    ontology retrieving the corresponding entites (uris) in it using string similarity
    :param dict_jobs_entities_title:
    :param compare:
    :param threshold:
    :param dist_type:
    :return:
    '''

    dict_jobs_results_1 = {}
    dict_jobs_results_2 = {}

    for job in dict_jobs_entities_title:

        job_matches1 = eval_results_tot_more_sim(skill, dict_jobs_entities_title[job][0], compare, threshold_1, threshold_2, dist_type_1, dist_type_2, 1)
        job_matches2 = eval_results_tot_more_sim(skill_digital_language, dict_jobs_entities_title[job][0], compare, threshold_1, threshold_2, dist_type_1, dist_type_2, 2)
        job_matches_tot_1 = job_matches1[0] | job_matches2[0]
        job_matches_tot_2 = job_matches1[1] | job_matches2[1]
        #job_occupation_uris = eval_results(occupation, dict_jobs_entities_title[job][1], compare, threshold, dist_type, 1)
        job_occupation_uris = eval_results_uri_occupation_designation_more_sim(occupation, dict_jobs_entities_title[job][2], compare, threshold_1, threshold_2, dist_type_1, dist_type_2, dict_jobs_entities_title[job][1])
        dict_jobs_results_1[job] = (job_matches_tot_1, (job_occupation_uris[0], job_occupation_uris[1]), job_occupation_uris[4])
        dict_jobs_results_2[job] = (job_matches_tot_2, (job_occupation_uris[2], job_occupation_uris[3]), job_occupation_uris[5])

    return dict_jobs_results_1, dict_jobs_results_2


def resume_eval(list_resume_entities, resume_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, skill, occupation, skill_digital_language):
    '''
    Given the entities (skills) and csv fields (title) extracted for the resume, it maps them to the
    ontology retrieving the corresponding entites (uris) in it using string similarity
    :param dict_jobs_entities_title:
    :param compare:
    :param threshold:
    :param dist_type:
    :return:
    '''

    resume_matches1 = eval_results_tot_more_sim(skill, list_resume_entities, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, 1)
    resume_matches2 = eval_results_tot_more_sim(skill_digital_language, list_resume_entities, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, 2)
    resume_matches_tot_1 = resume_matches1[0] | resume_matches2[0]
    resume_matches_tot_2 = resume_matches1[1] | resume_matches2[1]
    resume_occupation_uris = eval_results_more_sim(occupation, resume_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, 1)
    resume_results_1 = (resume_matches_tot_1, resume_occupation_uris[0])
    resume_results_2 = (resume_matches_tot_2, resume_occupation_uris[1])

    return resume_results_1, resume_results_2


def resume_eval_des(list_resume_entities, resume_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, skill, occupation, skill_digital_language, list_designations):
    '''
    Given the entities (skills) and csv fields (title) extracted for the resume, it maps them to the
    ontology retrieving the corresponding entites (uris) in it using string similarity
    :param dict_jobs_entities_title:
    :param compare:
    :param threshold:
    :param dist_type:
    :return:
    '''

    resume_matches1 = eval_results_tot_more_sim(skill, list_resume_entities, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, 1)
    resume_matches2 = eval_results_tot_more_sim(skill_digital_language, list_resume_entities, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, 2)
    resume_matches_tot_1 = resume_matches1[0] | resume_matches2[0]
    resume_matches_tot_2 = resume_matches1[1] | resume_matches2[1]
    resume_occupation_uris = eval_results_more_sim_designation(occupation, resume_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, 1, list_designations)
    resume_results_1 = (resume_matches_tot_1, resume_occupation_uris[0], resume_occupation_uris[2])
    resume_results_2 = (resume_matches_tot_2, resume_occupation_uris[1], resume_occupation_uris[3])

    return resume_results_1, resume_results_2



def match_resume_job(dict_jobs_results, resume_results):
    '''Given the results (uris) for resume and job proposals, it computes the final score for each job proposal to
    match with the resume'''

    file_y_1 = open("skill_digital_language_ess_opt_1.pickle", "rb")
    opt_ess = pickle.load(file_y_1)
    #print(opt_ess)
    print("\nloaded file taxonomy")

    dict_scores = {}

    for job_key in dict_jobs_results:
        score = compute_score(opt_ess, resume_results[0], dict_jobs_results[job_key][0], resume_results[1], dict_jobs_results[job_key][1][0], dict_jobs_results[job_key][1][1])
        dict_scores[job_key] = score

    #dict_sorted_scores = dict(sorted(dict_scores.items(), key=lambda item: item[1]))

    dict_sorted_scores = dict(sorted(dict_scores.items(), key=operator.itemgetter(1), reverse=True))

    return dict_sorted_scores


def match_resume_job_des(dict_jobs_results, resume_results):
    '''Given the results (uris) for resume and job proposals, it computes the final score for each job proposal to
    match with the resume'''

    file_y_1 = open("skill_digital_language_ess_opt_1.pickle", "rb")
    opt_ess = pickle.load(file_y_1)
    #print(opt_ess)
    print("\nloaded file taxonomy")

    dict_scores = {}

    for job_key in dict_jobs_results:
        score = compute_score_des(opt_ess, resume_results[0], dict_jobs_results[job_key][0], resume_results[1], dict_jobs_results[job_key][1][0], dict_jobs_results[job_key][1][1], dict_jobs_results[job_key][2], resume_results[2])
        dict_scores[job_key] = score

    #dict_sorted_scores = dict(sorted(dict_scores.items(), key=lambda item: item[1]))

    dict_sorted_scores = dict(sorted(dict_scores.items(), key=operator.itemgetter(1), reverse=True))

    return dict_sorted_scores


# todo replace with real values
# todo we do not use education here, if we wwannt e have to add it

# without designation
dict_jobs_entities_title = {'1': (["configuration and design skills", "python", "java", "machine learning", "data analytics", "manage artistic career"], "digital games devel"), "2": (["communication", "english", "logic", "python", "public speaking"], "data manager")} # each key is a different job proposal, each value is a tuple with one list of entities and the job title
# with designation
#dict_jobs_entities_title = {'1': [["configuration and design skills", "python", "java", "machine learning", "data analytics", "manage artistic career"], ["data analyst"], "digital games devel"], "2": [["communication", "english", "logic", "python", "public speaking"], [], "data manager"]} # each key is a different job proposal, each value is a tuple with one list of entities and the job title
list_resume_entities = ["evaluate information", "computer programming", "java", "python", "english speaking", "project presentation", "data analytics"]  # list of entities for resume from entities extr
list_designations = ["data analyst", "manager"]
resume_title = "digital games devel" # resume title
compare = ">="
threshold_1 = 100
dist_type_1 = "fuzzywuzzy"
threshold_2 = 1
dist_type_2 = "levenshtein"


with open('data.json', 'w') as fp:
    json.dump(dict_jobs_entities_title, fp)

with open('data.json') as json_file:
    data = json.load(json_file)
    print(data)


# files pickle for texonomy
file_x1 = open("skill.pickle", "rb")
skill = pickle.load(file_x1)
print("\nLoaded file skills taxonomy\n")
file_x2 = open("occupation.pickle", "rb")
occupation = pickle.load(file_x2)
print("Loaded file occupetions taxonomy\n")
file_y = open("skill_digital_language.pickle", "rb")
skill_digital_language = pickle.load(file_y)
print("Loaded file skills, ict skills, languages taxonomy")



# compute mapping of job proposals sills and title to skills and occupations in the taxonomy
# without designation
output_job = job_eval(dict_jobs_entities_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, skill, occupation, skill_digital_language)
# with designation
#output_job = job_eval_des(dict_jobs_entities_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, skill, occupation, skill_digital_language)
print("\nJob matched")
output_job_1 = output_job[0]
output_job_2 = output_job[1]
print("output_job_1", output_job_1)
print("output_job_2", output_job_2)
# pickle file to save results
file_1 = open("output_job_sim_1.pickle", "wb")
pickle.dump(output_job_1, file_1)
file_2 = open("output_job_sim_2.pickle", "wb")
pickle.dump(output_job_2, file_2)

# compute mapping of resume sills and title to skills and occupations in the taxonomy
# without designation
output_resume = resume_eval(list_resume_entities, resume_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, skill, occupation, skill_digital_language)
# with designation
#output_resume = resume_eval_des(list_resume_entities, resume_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, skill, occupation, skill_digital_language, list_designations)
print("\nResume matched")
output_resume_1 = output_resume[0]
output_resume_2 = output_resume[1]
print("output_resume_1", output_resume_1)
print("output_resume_2", output_resume_2)
# pickle file to save results
file_3 = open("output_resume_sim_1.pickle", "wb")
pickle.dump(output_resume_1, file_3)
file_4 = open("output_resume_sim_2.pickle", "wb")
pickle.dump(output_resume_2, file_4)

# compute final score for each job proposal for the given resume
# without designation
score_result_1 = match_resume_job(output_job_1, output_resume_1)
score_result_2 = match_resume_job(output_job_2, output_resume_2)
# with designation
'''score_result_1 = match_resume_job_des(output_job_1, output_resume_1)
score_result_2 = match_resume_job_des(output_job_2, output_resume_2)'''
print("\nScoes")
print("score_result_1", score_result_1)
print("score_result_2", score_result_2)
# pickle file to save results
file_5 = open("output_score_sim_1.pickle", "wb")
pickle.dump(score_result_1, file_5)
file_6 = open("output_score_sim_2.pickle", "wb")
pickle.dump(score_result_2, file_6)


# read pickle files
'''file_1 = open("output_job_sim_1.pickle", 'rb')
job_1 = pickle.load(file_1)
file_2 = open("output_job_sim_2.pickle", 'rb')
job_2 = pickle.load(file_2)
file_3 = open("output_resume_sim_1.pickle", 'rb')
resume_1 = pickle.load(file_3)
file_4 = open("output_resume_sim_2.pickle", 'rb')
resume_2 = pickle.load(file_4)
file_5 = open("output_score_sim_1.pickle", 'rb')
score_1 = pickle.load(file_5)
file_6 = open("output_score_sim_2.pickle", 'rb')
score_2 = pickle.load(file_6)
print(job_1)
print(job_2)
print(resume_1)
print(resume_2)
print(score_1)
print(score_2)'''



# input examples

# dict_jobs_entities_title -> {"job1": (["skill1", "skill2", ...], "job_title_1"), ..., "jobn":(["skill1", "skill2", ...], "job_title_1")}
# where skill_i is skill entity extracted from text for job proposal, while "job_title_i" is extracted from the field job_title in the csv

# list_resume_skills -> ["skill1", "skill2", ...]
# where skill_i is skill entity extracted from text for resume

# resume_title -> "resume title"
# extracted from the field resume_title in the csv


# BUT IF WE HAVE DESIGNATION TOO ->

# dict_jobs_entities_title -> {"job1": (["skill1", "skill2", ...], ["designation1", "designation2", ...],"job_title_1"), ..., "jobn":(["skill1", "skill2", ...], "job_title_1")}
# where skill_i is skill entity extracted from text for job proposal, while "job_title_i" is extracted from the field job_title in the csv

# list_resume_entities -> ["skill1", "skill2", ...]
# where skill_i is skill entity extracted from text for resume

# list_resume_deignations -> ["designation1", "designation2", ...]
# where designation_i is designation entity extracted from text for resume

# resume_title -> "resume title"
# extracted from the field resume_title in the csv