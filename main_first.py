from sparql import *
import operator

def job_eval(dict_jobs_entities_title, compare, threshold, dist_type, skill, occupation, skill_digital_language):
    '''
    Given the entities (skills) and csv fields (title) extracted for the job proposals, it maps them to the
    ontology retrieving the corresponding entites (uris) in it using string similarity
    :param dict_jobs_entities_title:
    :param compare:
    :param threshold:
    :param dist_type:
    :return:
    '''

    dict_jobs_results = {}

    for job in dict_jobs_entities_title:

        job_matches1 = eval_results_tot(skill, dict_jobs_entities_title[job][0], compare, threshold, dist_type, 1)
        job_matches2 = eval_results_tot(skill_digital_language, dict_jobs_entities_title[job][0], compare, threshold, dist_type, 2)
        job_matches_tot = job_matches1 | job_matches2
        #job_occupation_uris = eval_results(occupation, dict_jobs_entities_title[job][1], compare, threshold, dist_type, 1)
        job_occupation_uris = eval_results_uri_occupation(occupation, dict_jobs_entities_title[job][1], compare, threshold, dist_type)
        print("dict_jobs_entities_title[job][1]", dict_jobs_entities_title[job][1])
        print("job", job_occupation_uris)
        dict_jobs_results[job] = (job_matches_tot, job_occupation_uris)

    return dict_jobs_results


def resume_eval(list_resume_entities, resume_title, compare, threshold, dist_type, skill, occupation, skill_digital_language):
    '''
    Given the entities (skills) and csv fields (title) extracted for the resume, it maps them to the
    ontology retrieving the corresponding entites (uris) in it using string similarity
    :param dict_jobs_entities_title:
    :param compare:
    :param threshold:
    :param dist_type:
    :return:
    '''

    resume_matches1 = eval_results_tot(skill, list_resume_entities, compare, threshold, dist_type, 1)
    resume_matches2 = eval_results_tot(skill_digital_language, list_resume_entities, compare, threshold, dist_type, 2)
    resume_matches_tot = resume_matches1 | resume_matches2
    resume_occupation_uris = eval_results(occupation, resume_title, compare, threshold, dist_type, 1)
    resume_results = (resume_matches_tot, resume_occupation_uris)

    return resume_results



def match_resume_job(dict_jobs_results, resume_results):
    '''Given the results (uris) for resume and job proposals, it computes the final score for each job proposal to
    match with the resume'''

    file_y_1 = open("skill_digital_language_ess_opt_1.pickle", "rb")
    opt_ess = pickle.load(file_y_1)
    #print(opt_ess)
    print("loaded file taxonomy")

    dict_scores = {}

    for job_key in dict_jobs_results:
        print("YYYYYYYYYYYYYYYYYYYYYYY", dict_jobs_results[job_key][1])
        print(1, dict_jobs_results[job_key][1][0])
        print(2, dict_jobs_results[job_key][1][1])
        score = compute_score(opt_ess, resume_results[0], dict_jobs_results[job_key][0], resume_results[1], dict_jobs_results[job_key][1][0], dict_jobs_results[job_key][1][1])
        dict_scores[job_key] = score

    #dict_sorted_scores = dict(sorted(dict_scores.items(), key=lambda item: item[1]))

    dict_sorted_scores = dict(sorted(dict_scores.items(), key=operator.itemgetter(1), reverse=True))

    return dict_sorted_scores





# todo replace with real values
# todo we do not use education here, if we wwannt e have to add it

dict_jobs_entities_title = {'1': (["configuration and design skills", "python", "java", "machine learning", "data analytics", "manage artistic career"], "digital games devel"), "2": (["communication", "english", "logic", "python", "public speaking"], "data manager")} # each key is a different job proposal, each value is a tuple with one list of entities and the job title
list_resume_entities = ["evaluate information", "computer programming", "java", "python", "english speaking", "project presentation", "data analytics"]  # list of entities for resume from entities extr
resume_title = "digital games devel" # resume title
compare = ">="
threshold = 80
dist_type = "fuzzywuzzy"
#digital games developer

# files pickle for texonomy
file_x1 = open("skill.pickle", "rb")
skill = pickle.load(file_x1)
print("loaded file skills taxonomy")
file_x2 = open("occupation.pickle", "rb")
occupation = pickle.load(file_x2)
print("loaded file occupetions taxonomy")
file_y = open("skill_digital_language.pickle", "rb")
skill_digital_language = pickle.load(file_y)
print("loaded file skills, ict skills, languages taxonomy")



# compute mapping of job proposals sills and title to skills and occupations in the taxonomy
output_job = job_eval(dict_jobs_entities_title, compare, threshold, dist_type, skill, occupation, skill_digital_language)
print("job matched")
print(output_job)
# compute mapping of resume sills and title to skills and occupations in the taxonomy
output_resume = resume_eval (list_resume_entities, resume_title, compare, threshold, dist_type, skill, occupation, skill_digital_language)
print("resume matched")
print(output_resume)
# compute final score for each job proposal for the given resume
score_result = match_resume_job(output_job, output_resume)
print("scoes")
print(score_result)


# input examples

# dict_jobs_entities_title -> {"job1": (["skill1", "skill2", ...], "job_title_1"), ..., "jobn":(["skill1", "skill2", ...], "job_title_1")}
# where skill_i is skill entity extracted from text for job proposal, while "job_title_i" is extracted from the field job_title in the csv

# list_resume_entities -> ["skill1", "skill2", ...]
# where skill_i is skill entity extracted from text for resume

# resume_title -> "resume title"
# extracted from the field resume_title in the csv