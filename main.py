from sparql import *


def job_resume_eval(dict_jobs_entities_title, list_resume_entities, resume_title, compare, threshold, dist_type):

    file_x1 = open("skill.pickle", "rb")
    skill = pickle.load(file_x1)
    print("done 1")
    file_x2 = open("occupation.pickle", "rb")
    occupation = pickle.load(file_x2)
    print("done 2")
    file_y = open("skill_digital_language.pickle", "rb")
    skill_digital_language = pickle.load(file_y)
    print("done 3")

    dict_jobs_results = {}

    for job, job_value in dict_jobs_entities_title:
        job_matches1 = eval_results_tot(skill, job_value[0], compare, threshold, dist_type, 1)
        job_matches2 = eval_results_tot(skill_digital_language, job_value[0], compare, threshold, dist_type, 2)
        job_matches_tot = job_matches1 | job_matches2
        job_occupation_uris = eval_results(occupation, job_value[1], compare, threshold, dist_type, 1)
        dict_jobs_results[job] = (job_matches_tot, job_occupation_uris)

    resume_matches1 = eval_results_tot(skill, list_resume_entities, compare, threshold, dist_type, 1)
    resume_matches2 = eval_results_tot(skill_digital_language, list_resume_entities, compare, threshold, dist_type, 2)
    resume_matches_tot = resume_matches1 | resume_matches2
    resume_occupation_uris = eval_results(occupation, resume_title, compare, threshold, dist_type, 1)
    resume_results = (resume_matches_tot, resume_occupation_uris)

    return dict_jobs_results, resume_results


def match_resume_job(dict_jobs_results, resume_results):

    file_y_1 = open("skill_digital_language_ess_opt.pickle", "rb")
    opt_ess = pickle.load(file_y_1)
    print("done 4")

    dict_scores = {}

    for job_key, job_results in dict_jobs_results:
        score = compute_score(opt_ess, resume_results[0], job_results[0], resume_results[1], job_results[1])
        dict_scores[job_key] = score

    dict_sorted_scores = dict(sorted(dict_scores.items(), key=lambda item: item[1]))

    return dict_sorted_scores


# TODO
# get dict of lists for resume/job entities
# use it into the functions


dict_jobs_entities_title = "from entity extraction" # each key is a different job proposal, each value is a tuple with one list of entities and the job title
list_resume_entities = "from entity extraction"  # list of entities for resume from entities extr
resume_title = "resume title" # resume title
compare = ">="
threshold = 80
dist_type = "fuzzywuzzy"

output = job_resume_eval(dict_jobs_entities_title, list_resume_entities, resume_title, compare, threshold, dist_type)
score_result = match_resume_job(output[0], output[1])

'''x = set()
x.add("e")
x.add("d")
x.add("e")
x.add("f")
print(x)

y = set()
y.add("e")
y.add("s")
y.add("q")
print(y)

print(x.intersection(y))

l = [1, 2, 3]
n = [5, 7]
print(len(set(l).intersection(set(n))) != 0)'''