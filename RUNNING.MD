Method 1-

1) To clone whole project first clone files from this github page and store them in a single folder.

2) Get "models" folder from https://drive.google.com/drive/folders/1DJY5xnmB-Ytp6e1XgUgprGbrztJq9DO2?usp=sharing and put in main folder which you have created before(it should have src and data folders).

3) Install Docker and run docker file available in the main folder.


4) This would log the streamlit url where we can render the application.

Method 2-

To by pass the above process we can directly run the following command once docker is installed-

docker pull public.ecr.aws/s8f1m0f4/cmpt-732-project:latest

Running the above image shall render the frontend app as specified in the docker logs.


Acesssing frontend:

To Access frontend for visualizations and classification model hosted on ec2 instance, go to http://ec2-52-38-79-150.us-west-2.compute.amazonaws.com:8501/.

Following are the credentials required for accessing Tableau-

Username - nrv2@sfu.ca

Password - Manju sri@1


Weaviate Setup:

1)First download "weaviate_src.zip" from google drive Link - https://drive.google.com/drive/folders/1LheJzbx__FnN7x5QFRqiab7vS4skHuRe

2)Extract it to weaviate_src folder in local system.

To run Weaviate:

1)Please install Python 3.7.8 (to install multiple python versions follow this link:-"https://martinfritz.medium.com/work-with-multiple-versions-of-python-on-windows-10-eed1e5f52f07")

2)Save "weaviate-src" folder in local drive from github repo

3)Create a virtual enivronment in "weaviate-src" folder and activate it.(ref:-"https://realpython.com/python-virtual-environments-a-primer/")

4)Run "pip install -r requirements.txt" in previously created virtual env. if you get protobuf error, run "pip install protobuf==3.19.*" in the same virtual env

5)Please install Docker and Start it up.

6)Run "docker-compose up -d" in same directory as of "weaviate-src".

7)Run "streamlit run app.py" from previously created virtual env, this will load the frontend in "http://localhost:8501/"

Note:

Please use computer with or atleast (16GB of RAM)

Adding data to weaviate take up lot of RAM so we have only selected 50,000 questions for loading the model.
