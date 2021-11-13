from sparql import *
import operator
import json
import pandas as pd
import argparse


parser = argparse.ArgumentParser(description='Challenge presentation example')
parser.add_argument('-sim_threshold',
                    type=int,
                    default=8,
                    help='threshold')
parser.add_argument('-resume_num',
                    type=int,
                    default=0,
                    help='resume number')

args = parser.parse_args()


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
    Given the entities (skills/designations) and csv fields (title) extracted for the job proposals, it maps them to the
    ontology retrieving the corresponding entites (uris) in it using string similarity
    :param dict_jobs_entities_title:
    :param compare:
    :param threshold:
    :param dist_type:
    :return:
    '''

    dict_jobs_results_1 = {}
    dict_jobs_results_2 = {}
    count = 0
    for job in dict_jobs_entities_title:

        #print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", count)
        count += 1
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
    Given the entities (skills/designations) and csv fields (title) extracted for the resume, it maps them to the
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
    #print("\nloaded file taxonomy")

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
    #print("\nloaded file taxonomy")

    dict_scores = {}

    for job_key in dict_jobs_results:
        score = compute_score_des(opt_ess, resume_results[0], dict_jobs_results[job_key][0], resume_results[1], dict_jobs_results[job_key][1][0], dict_jobs_results[job_key][1][1], dict_jobs_results[job_key][2], resume_results[2])
        dict_scores[job_key] = score

    #dict_sorted_scores = dict(sorted(dict_scores.items(), key=lambda item: item[1]))

    dict_sorted_scores = dict(sorted(dict_scores.items(), key=operator.itemgetter(1), reverse=True))

    return dict_sorted_scores



def convert_to_format(json_file, dataset, column):

    df = pd.read_csv(dataset, encoding="ISO-8859-15")
    new_dict = {}

    for key in json_file:
        title = df[column].values[int(key)]
        new_key = key + ": " + title
        new_dict[new_key] = []
        if "Skills" in json_file[key]:
            new_dict[new_key].append(list(set(json_file[key]["Skills"])))
        else:
            new_dict[new_key].append([])
        if "Designation" in json_file[key]:
            new_dict[new_key].append(list(set(json_file[key]["Designation"])))
        else:
            new_dict[new_key].append([])
        new_dict[new_key].append(df[column].values[int(key)])

    return new_dict


if ( args.resume_num != 0 and args.resume_num != 1 and args.resume_num != 2 and args.resume_num != 3 and args.resume_num != 4
        and args.resume_num != 5 and args.resume_num != 6 and args.resume_num != 7 and args.resume_num != 8 and args.resume_num != 9
        and args.resume_num != 10 and args.resume_num != 11 and args.resume_num != 12 and args.resume_num != 13 and args.resume_num != 14
        and args.resume_num != 15):
    print("Resume's number must be an integer between 0 and 15!")

else:
    if args.sim_threshold == 8:
        file_1 = open("OUTPUT JOB FUZZ 80 LEVE 0.8/OUTPUT_JOB_FUZZ_80.pickle", 'rb')
        output_job_1 = pickle.load(file_1)
        file_2 = open("OUTPUT JOB FUZZ 80 LEVE 0.8/OUTPUT_JOB_LEVE_0.8.pickle", 'rb')
        output_job_2 = pickle.load(file_2)
        str1 = "OUTPUT RESUME FUZZ LEVE 80 0.8/OUTPUT_RESUME_" + str(args.sim_threshold) + "_FUZZ.pickle"
        file_3 = open(str1, 'rb')
        output_resume_1 = pickle.load(file_3)
        str2 = "OUTPUT RESUME FUZZ LEVE 80 0.8/OUTPUT_RESUME_" + str(args.sim_threshold) + "_LEVE.pickle"
        file_4 = open(str2, 'rb')
        output_resume_2 = pickle.load(file_4)
        score_result_1 = match_resume_job_des(output_job_1, output_resume_1)
        score_result_2 = match_resume_job_des(output_job_2, output_resume_2)
        print("\nFuzzywuzzy, threshold 80\n", score_result_1)
        print("\n\nLevenshtein, threshold 0.8\n", score_result_2)

    elif args.sim_threshold == 9:
        file_1 = open("OUTPUT JOB FUZZ 90 LEVE 0.9/OUTPUT_JOB_FUZZ_90.pickle", 'rb')
        output_job_1 = pickle.load(file_1)
        file_2 = open("OUTPUT JOB FUZZ 90 LEVE 0.9/OUTPUT_JOB_LEVE_0.9.pickle", 'rb')
        output_job_2 = pickle.load(file_2)
        str1 = "OUTPUT RESUME FUZZ LEVE 90 0.9/OUTPUT_RESUME_" + str(args.sim_threshold) + "_FUZZ_90.pickle"
        file_3 = open(str1, 'rb')
        output_resume_1 = pickle.load(file_3)
        str2 = "OUTPUT RESUME FUZZ LEVE 90 0.9/OUTPUT_RESUME_" + str(args.sim_threshold) + "_LEVE_0.9.pickle"
        file_4 = open(str2, 'rb')
        output_resume_2 = pickle.load(file_4)
        score_result_1 = match_resume_job_des(output_job_1, output_resume_1)
        score_result_2 = match_resume_job_des(output_job_2, output_resume_2)
        print("\nFuzzywuzzy, threshold 90\n", score_result_1)
        print("\n\nLevenshtein, threshold 0.9\n", score_result_2)

    else:
        print("Similarity threshold parameter must be 8 or 9!")




# without designation
#dict_jobs_entities_title = {'1': (["configuration and design skills", "python", "java", "machine learning", "data analytics", "manage artistic career"], "digital games devel"), "2": (["communication", "english", "logic", "python", "public speaking"], "data manager")} # each key is a different job proposal, each value is a tuple with one list of entities and the job title
# with designation
#dict_jobs_entities_title = {'1': [["configuration and design skills", "python", "java", "machine learning", "data analytics", "manage artistic career"], ["data analyst"], "digital games devel"], "2": [["communication", "english", "logic", "python", "public speaking"], [], "data manager"]} # each key is a different job proposal, each value is a tuple with one list of entities and the job title


# load job proposals
'''with open('INPUT CORRECT/JOB_PROPOSALS_NER_CORRECT.json') as json_file:
    dict_jobs_entities_title = json.load(json_file)'''

# load resume
'''with open('INPUT CORRECT/RESUMES_CORRECT.json') as json_file_1:
    resumes = json.load(json_file_1)
resume_0 = resumes['15: Personal trainer']
list_resume_entities = resume_0[0]
list_designations = resume_0[1]
resume_title = resume_0[2]'''

# choose similarity measure
'''compare = ">="
threshold_1 = 80
dist_type_1 = "fuzzywuzzy"
threshold_2 = 0.8
dist_type_2 = "levenshtein"'''

# load files pickle for texonomy
'''file_x1 = open("skill.pickle", "rb")
skill = pickle.load(file_x1)
print("\nLoaded file skills taxonomy\n")
file_x2 = open("occupation.pickle", "rb")
occupation = pickle.load(file_x2)
print("Loaded file occupetions taxonomy\n")
file_y = open("skill_digital_language.pickle", "rb")
skill_digital_language = pickle.load(file_y)
print("Loaded file skills, ict skills, languages taxonomy")'''

# compute mapping of job proposals sills and title to skills and occupations in the taxonomy
# without designation
#output_job = job_eval(dict_jobs_entities_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, skill, occupation, skill_digital_language)
# with designation
'''output_job = job_eval_des(dict_jobs_entities_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, skill, occupation, skill_digital_language)
print("\nJob matched")
output_job_1 = output_job[0]
output_job_2 = output_job[1]
print("output_job_1", output_job_1)
print("output_job_2", output_job_2)
# pickle file to save results
file_1 = open("OUTPUT_JOB_EDIT_0.8.pickle", "wb")
pickle.dump(output_job_1, file_1)
file_2 = open("OUTPUT_JOB_JARO_0.8.pickle", "wb")
pickle.dump(output_job_2, file_2)'''

# compute mapping of resume sills and title to skills and occupations in the taxonomy
# without designation
#output_resume = resume_eval(list_resume_entities, resume_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, skill, occupation, skill_digital_language)
# with designation
'''output_resume = resume_eval_des(list_resume_entities, resume_title, compare, threshold_1, threshold_2, dist_type_1, dist_type_2, skill, occupation, skill_digital_language, list_designations)
print("\nResume matched")
output_resume_1 = output_resume[0]
output_resume_2 = output_resume[1]
print("output_resume_1", output_resume_1)
print("output_resume_2", output_resume_2)
# pickle file to save results
file_3 = open("OUTPUT RESUME FUZZ LEVE 90 0.9/OUTPUT_RESUME_15_FUZZ_90.pickle", "wb")
pickle.dump(output_resume_1, file_3)
file_4 = open("OUTPUT RESUME FUZZ LEVE 90 0.9/OUTPUT_RESUME_15_LEVE_0.9.pickle", "wb")
pickle.dump(output_resume_2, file_4)'''

# compute final score for each job proposal for the given resume
# without designation
#score_result_1 = match_resume_job(output_job_1, output_resume_1)
#score_result_2 = match_resume_job(output_job_2, output_resume_2)
# with designation
'''file_1 = open("OUTPUT JOB FUZZ 90 LEVE 0.9/OUTPUT_JOB_FUZZ_90.pickle", 'rb')
output_job_1 = pickle.load(file_1)
file_2 = open("OUTPUT JOB FUZZ 90 LEVE 0.9/OUTPUT_JOB_LEVE_0.9.pickle", 'rb')
output_job_2 = pickle.load(file_2)
file_3 = open("OUTPUT RESUME FUZZ LEVE 90 0.9/OUTPUT_RESUME_2_FUZZ_90.pickle", 'rb')
output_resume_1 = pickle.load(file_3)
file_4 = open("OUTPUT RESUME FUZZ LEVE 90 0.9/OUTPUT_RESUME_2_LEVE_0.9.pickle", 'rb')
output_resume_2 = pickle.load(file_4)
score_result_1 = match_resume_job_des(output_job_1, output_resume_1)
score_result_2 = match_resume_job_des(output_job_2, output_resume_2)
print("\nResume title: Data Scientist\n")
print("Scores\n")
print("Fuzzywuzzy, threshold 80", score_result_1)
print("Levenshtein, threshold 0.8", score_result_2)'''






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




# USED TO CREATE USEFUL FILES

'''with open('job_proposals_ner.json') as json_file:
    d = json.load(json_file)
    print(d)
    print(d['6']['Skills'])

d['6']['Skills'] = ['marketing coordinator', 'administration', 'sales support']
d['14']['Skills'] = ['aws', 'azure cloud', 'rackspace', 'chef']
d['15']['Skills'] = ['engineering leadership', 'direction for team', 'system engineering', 'project management', 'network engineering', 'software development', 'impleentation engineering', 'organiztion manager']
d['18']['Skills'] = ['automate repetitive task', 'power shell scripts', 'windows', 'linux']
d['20']['Skills'] = ['mater management structures', 'autocad']
d['23']['Skills'] = ['project manager']
d['30']['Skills'] = ['proficient with computer']
d['31']['Skills'] = ['sharepoint']
d['32']['Skills'] = ['python', 'analytical skills', 'analyze amounts of infomation', 'organise', 'collect', 'map data from raw data']
d['37']['Skills'] = ['analyse business', 'create erd diagrams', 'work flow diagrams', 'excel', 'spreadsheet development', 'relational database desing', 'sql', 'data migration', 'link multiple data']
d['39']['Skills'] = ['data cleaning', 'data analysys and aintenance', 'processing high volume transactions', 'finance procedures', 'communicating information']
d['40']['Skills'] = ['attention to details']
d['49']['Skills'] = ['facilities team']
d['53']['Skills'] = ['engineer', 'safety engineer']
d['86']['Skills'] = ['data analysis', 'modeling', 'machine learning']
d['91']['Skills'] = ['web technology', 'reporting']
d['92']['Skills'] = ['command and control', 'communication networking', 'rugged computing', 'information essurance']
d['94']['Skills'] = ['java', 'microservice', 'web apis', 'aws']
d['96']['Skills'] = ['java', 'application servers', 'databases', 'rdbms', 'front-end integration', 'development of web based applications', 'network design', 'configuration web applicaions']
d['111']['Skills'] = ['management', 'implementation of traffic', 'environmentel']
d['116']['Skills'] = ['software acoustic modeling', 'matlab']
d['138']['Skills'] = ['fitness', 'global fitness franchising']
d['143']['Skills'] = ['software', 'creation of process definition documents', 'solution architecture', 'governance', 'control', 'business transformation technologies']
d['169']['Skills'] = ['entity framework', 'linq', 'sql', 'web  services', 'ui', 'ux design', 'software development', 'leadership position', 'managing teams', 'bussiness analysis', 'business knowledge', 'project management', 'quality assurance']

print(d)

with open('job_proposals_ner_modified.json', 'w') as fp:
    json.dump(d, fp)
'''

'''with open('resumes_ner.json') as json_file:
    d = json.load(json_file)
    print(d)
    print(d['6']['Skills'])

d['0']['Skills'] = ['critical thinking', 'problem solving', 'sales', 'customer application details', 'industrial application', 'fda', 'deployment of hardware', 'remore sales', 'business development', 'market evaluation', 'speaking engagement', 'written and verbal communication']
d['1']['Skills'] = ['charge of planning', 'fiber optic', 'operating system', 'windows', 'mac os']
d['2']['Skills'] = ['enhancing america\'s infrastructure', 'works', 'public works', 'office', 'excel', 'word', 'powerpoint', 'autocad']
d['3']['Skills'] = ['communication', 'finance', 'project management', 'business networking quality', 'leadership', 'data analysis', 'computer flexbility', 'system acumen']
d['4']['Skills'] = ['cause analysisevaluating', 'managing risk', 'matlab', 'optimization', 'system simulation', 'six sigma', 'statistical analysis', 'programming languages', 'julia', 'microsoft office', 'minitab', 'latex']
d['5']['Skills'] = ['customer service', 'relations', 'advertising', 'marketing']
d['6']['Skills'] = ['hearing', 'arbitration', 'mediation', 'litigation plan', 'defense counsel', 'legal expenses', 'management', 'property management']
d['7']['Skills'] = ['hardworking', 'sales', 'business development', 'prject management', 'engineering', 'communication in detection systems']
d['8']['Skills'] = ['python', 'pandas', 'numpy', 'scikit-learn', 'maplotlib', 'sql', 'java', 'javascript', 'machine learning', 'cassandra', 'text analytics']
d['9']['Skills'] = ['java', 'database management system']
d['10']['Skills'] = ['labour law']
d['11']['Skills'] = ['music emerging', 'sensibility', 'reporting', 'editorial team', 'production meetings', 'brain storming', 'events description', 'event management', 'delivery of project']
d['12']['Skills'] = ['web technologies', 'angular', 'html5', 'css3', 'javascript', 'photoshop', 'visual studio']
d['13']['Skills'] = ['mechanical design', 'making plant', 'life skills training', 'positive attitude', 'quick learner', 'team leader']
d['14']['Skills'] = ['planning', 'team experience', 'developing marketing', 'sales strategies', 'comunication skills', 'microsoft office', 'computer knowledge', 'sales manager skill', 'fitness']
print(d)

with open('resumes_ner_modified.json', 'w') as fp:
    json.dump(d, fp)'''


'''file_1 = open('RESUME JOB MATCHING FUZZ LEVE 90 0.9/RESUME_15_FUZZ.pickle', 'rb')
res_fuzz = pickle.load(file_1)
print(res_fuzz)
file_2 = open('RESUME JOB MATCHING FUZZ LEVE 90 0.9/RESUME_15_LEVE_2.pickle', 'rb')
res_leve = pickle.load(file_2)
print(res_leve)'''


'''file_3 = open('OUTPUT JOB FUZZ 80 LEVE 0.8/OUTPUT_JOB_FUZZ_80.pickle', 'rb')
res_fuzz = pickle.load(file_3)
#print(res_fuzz)
file_4 = open('OUTPUT JOB FUZZ 80 LEVE 0.8/OUTPUT_JOB_FUZZ_80.pickle', 'rb')
res_leve = pickle.load(file_4)
#first2pairs = {k: res_leve[k] for k in sorted(res_leve.keys())[:2]}
print(res_leve['1: Implementation Engineer'])

file_5 = open('OUTPUT RESUME FUZZ LEVE 80 0.8/OUTPUT_RESUME_1_FUZZ.pickle', 'rb')
res_fuzz = pickle.load(file_5)
#print(res_fuzz)
file_6 = open('OUTPUT RESUME FUZZ LEVE 80 0.8/OUTPUT_RESUME_1_LEVE.pickle', 'rb')
res_leve = pickle.load(file_6)
#first2pairs = {k: res_leve[k] for k in sorted(res_leve.keys())[:2]}
print(res_leve)'''

'''with open('job_proposals_ner_modified.json') as json_file:
    d = json.load(json_file)
    print(d)
final_d = convert_to_format(d, 'datasets/use this/job proposals modified.csv', 'job_title')
with open('JOB_PROPOSALS_NER_CORRECT.json', 'w') as fp:
    json.dump(final_d, fp)

with open('JOB_PROPOSALS_NER_CORRECT.json') as json_file:
    d = json.load(json_file)
    print(d)'''

'''with open('resumes_ner_modified.json') as json_file:
    d = json.load(json_file)
    print(d)
final_d = convert_to_format(d, 'datasets/use this/resumes.csv', 'Resume Title')
with open('RESUMES_CORRECT.json', 'w') as fp:
    json.dump(final_d, fp)

with open('RESUMES_CORRECT.json') as json_file:
    d = json.load(json_file)
    print(d)'''

'''with open('resumes_ner.json') as json_file:
    data = json.load(json_file)
    print(data)
    new_dict = convert_to_format(data, 'datasets/use this/resumes.csv', "Resume Title")
    print(new_dict)
    with open('resumes_ner_222222222.json', 'w') as fp:
        json.dump(new_dict, fp)'''

'''with open('resumes_ner_soft.json') as json_file:
    data = json.load(json_file)
    #print(data)
    new_dict = convert_to_format(data, 'datasets/use this/resumes.csv', "Resume Title")
    #print(new_dict)
    with open('resumes_ner_soft_1.json', 'w') as fp:
        json.dump(new_dict, fp)

with open('job_proposals_ner.json') as json_file:
    data = json.load(json_file)
    #print(data)
    new_dict = convert_to_format(data, 'datasets/use this/job proposals modified.csv', 'job_title')
    #print(new_dict)
    with open('job_proposals_ner_1.json', 'w') as fp:
        json.dump(new_dict, fp)

with open('job_proposals_ner_soft.json') as json_file:
    data = json.load(json_file)
    #print(data)
    new_dict = convert_to_format(data, 'datasets/use this/job proposals modified.csv', 'job_title')
    #print(new_dict)
    with open('job_proposals_ner_soft_1.json', 'w') as fp:
        json.dump(new_dict, fp)'''