# SemanticWeb  
Course project done by Bharath, Edu and Veronica as part of the coursework Semantic Web Technologies   


## Description     

The purpose of this project is, given a resumé and a set of job proposals, to find the best match for that resumé by investigating the usage of tools related to language models and semantic web.
Two main tools are used: BERT, a language model to compute entities extraction and the ESCO taxonomy, the European job taxonomy. The first one is used to extract from plain text the entities (skills/occupations) that can be compared between the resumés and the job proposals, while the second one is used to filter them out by mapping them to the taxonomy and to help to compute the final matching score between each pair resume-job proposal.
                                                      

## Data

* `Dataset` folder: it contains two datasets used to test the system, one containing 16 resumes and one containing 194 job proposals among which we want to find the best matches for each resume   

* `ESCO ttl files` folder: it contains the ESCO taxonomy turtle files used to extract the informetion   

* `RESUME JOB MATCHING FUZZ LEVE 80 0.8` and `RESUME JOB MATCHING FUZZ LEVE 90 0.9` folders: they contain the results of the conducted experiment
      
      
## Structure   

### NER   

The single jupyter-notebook _BERT\_ner.ipynb_ contains the logic to develop the language model to extract the entities and the functions to effectively extract them from our datasets.                                                  

### ESCO taxonomy

Two main files have been created to develop the mapping of the extracted entities to the ESCO taxonomy and to compute the final matching score for each pair resume-job proposal:

* `sparql.py` This file contains the main functions to make the SPARQL queries, to map the extracted entities through BERT to the ESCO taxonomy by comparing them using different string similarity measures and thresholds, and to compute the final matching score for each pair resume-job proposal.

* `main.py` This file contains the main functions to compute the entire ESCO mapping procedure and to compute the scores, it allows the user to set the threshold for the similarity measure and it returns the results for the chosen resume with two types of similarity.

### Utils

Lastly, there are two additional files:

* `csv_to_ttl_occupation.py` This file converts the csv file of the occupations into the corresponding ttl file. 

* `csv_to_ttl_skill.py` This file converts the csv file of the skills into the corresponding ttl file

Moreover, the folders `OUTPUT JOB FUZZ 80 LEVE 0.8`, `OUTPUT JOB FUZZ 90 LEVE 0.9`, `OUTPUT RESUME FUZZ LEVE 80 0.8`, `OUTPUT RESUME FUZZ LEVE 90 0.9`  and the file `skill_digital_language_ess_opt_1.pickle` contains some files related to the resumes and the job proposals necessary to compute the matching scores.
  

## Execution

### 1) Prerequisites

1) Installation of `Python 3.8.5` or more
2) It is recommended to create a virtual environment for the project
3) Installation of the required libraries through the `requirements.txt` file

### 2) Resume-job proposals matching

By running the file `main.py` it is possible to indicate the resume for which we want to find the best matching job proposals. The results are computed both with _Levenshtein distance_ and _FuzzyWuzzy ratio_, it is possible to indicate if we want the lower or higher threshold (namely 0.8 or 0.9 for Levenshtein and 80 or 90 for FuzzyWuzzy).

Two parameters can be set:   

* `-sim_threshold` can have value:
  * 8 if we want the lower thresholds (0.8 and 80)
  * 9 if we want the higher thresholds (0.9 and 90)

* `-resume_num` to indicate which resume (number between 0 and 15) we want to match, here is the list of the number to insert with the resume titles:
0. Sales Manager
1. Implementation Engineer
2. Civil Engineer
3. BDC Data Analyst
4. Safety Engineer Intern
5. Classified Ads Manager
6. Assistant Program Manager
7. Technical Customer Service
8. Data scientist
9. Programmer
10. Lawyer
11. Event Manager
12. Web developer
13. Mechanical Engineer
14. Seller
15. Personal Trainer 
     
Here is an example to run the code to obtain the matching job proposal for the resume 0 (Sales Manager) with lower similarity thresholds: `python main.py -sim_threshold 8 -resume_num 0`.   

The results are showed sorted by decreasing score, each element has its identification number, job title, score      
      
