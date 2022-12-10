## Demo

The live demo for this project can been viewed here: 
<a target="_blank" href="http://ec2-52-38-79-150.us-west-2.compute.amazonaws.com:8501/" >Live Demo</a>

## Overview

This project is done for SFU's CMPT 732 (Big Data I) course, with the goal to target a specific problem
that arises from the large inflow of unmonitored data on these forums: duplicate questions. Our work focuses
on StackOverflow, a forum for software developers and programmers, that currently relies on vigilant,
high-reputation users to report duplicate questions. While this manual method is effective, it is laborious and
slow.

Our project includes extracting duplicate and non-duplicate questions from StackOverflow data. Using
that data, we have performed data analysis and we have trained two models that can 1) detect if two
questions are duplicates and 2) search for similar questions over a large corpus of data.

Notes on how to run the code can be found in RUNNING.md, and a more detailed overview can be found in the project report (under Documents).

## Structure
```

Dockerfile
README.md
RUNNING.MD
data                                                        Contains the data required for Visualization
   |-- countries.geojson
   |-- country_df.json
   |-- duplicate-question-tags-count
   |-- question-tags-count
   |-- scripts                                               Contains the scripts required for generating data
   |   |-- generate_duplicate_posts_per_year.py
   |   |-- generate_duplicate_question_tag_count.py
   |   |-- generate_duplicate_questions_for_ui.py
   |   |-- generate_posts_per_year.py
   |   |-- generate_question_tag_count.py
   |   |-- generate_stats_for_dashboard.py
   |   |-- generate_user_post_mapping.py
   |   |-- play_ground.py
   |   |-- process_duplicate_records.py
   |   |-- process_random_records.py
   |   |-- spark-xml_2.12-0.5.0.jar
   |-- top5
   |   |-- data.json
jupyter notebooks
   |-- sof_ml.ipynb
   |-- sof_weaviate_search.ipynb
models                                                      Contains model file for Machine Learning               
   |-- __init__.py
   |-- distilbert-base-nli-mean-tokens
   |   |-- 0_Transformer
   |   |   |-- config.json
   |   |   |-- pytorch_model.bin
   |   |   |-- sentence_bert_config.json
   |   |   |-- special_tokens_map.json
   |   |   |-- tokenizer_config.json
   |   |   |-- vocab.txt
   |   |-- 1_Pooling
   |   |   |-- config.json
   |   |-- config.json
   |   |-- modules.json
   |   |-- similarity_evaluation_results.csv
   |-- en_core_web_lg-3.4.1
   |   |-- LICENSE
   |   |-- LICENSES_SOURCES
   |   |-- MANIFEST.in
   |   |-- PKG-INFO
   |   |-- README.md
   |   |-- en_core_web_lg
   |   |   |-- __init__.py
   |   |   |-- meta.json
   |   |-- meta.json
   |   |-- setup.cfg
   |   |-- setup.py
   |-- fuzzy_scaler.sav
   |-- infer.py
   |-- mlp_model
   |-- questions_list.p
   |-- sample.py
   |-- use
   |   |-- saved_model.pb
   |   |-- variables
   |   |   |-- variables.data-00000-of-00001
   |   |   |-- variables.index
   |-- wr_scaler.sav
src                                                         Contains code for frontend app
   |-- .DS_Store
   |-- __pycache__
   |   |-- dashboard_graph_helper.cpython-310.pyc
   |   |-- dashboard_graph_helper.cpython-37.pyc
   |-- app.py
   |-- dashboard_graph_helper.py
   |-- requirements.txt
```
## Team Members

- Dilip Reddy
- Rubin
- Nagendra
- Hassan
