from sparql import *


def job_matches(dict_jobs_entities, compare, threshold, dist_type):

    file_x1 = open("skill.pickle", "rb")
    skill = pickle.load(file_x1)
    print("done 1")
    file_x2 = open("occupation.pickle", "rb")
    #occupation = pickle.load(file_x2)
    #print("done 2")
    file_y = open("skill_digital_language.pickle", "rb")
    skill_digital_language = pickle.load(file_y)
    print("done 3")

    dict_jobs_results = {}

    for job, job_value in dict_jobs_entities:
        job_matches1 = eval_results_tot(skill, job_value, compare, threshold, dist_type, 1)
        job_matches2 = eval_results_tot(skill_digital_language, job_value, compare, threshold, dist_type, 2)
        job_matches_tot = job_matches1 | job_matches2
        dict_jobs_results[job] = job_matches_tot

    return dict_jobs_results


def match_resume_job(dict_jobs_results, resume_results):

    file_y_1 = open("skill_digital_language_ess_opt.pickle", "rb")
    opt_ess = pickle.load(file_y_1)
    print("done 4")

    dict_scores = {}
    list_uri_occupations_job = [] # todo if possible

    for job_key, job_results in dict_jobs_results:
        score = compute_score(opt_ess, resume_results, job_results, list_uri_occupations_job)
        dict_scores[job_key] = score

    dict_sorted_scores = dict(sorted(dict_scores.items(), key=lambda item: item[1]))

    return dict_sorted_scores


# TODO
# get dict of lists for resume/job entities
# use it into the functions
