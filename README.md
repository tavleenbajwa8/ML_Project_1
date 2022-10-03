# ML_Project_1

#Create conda environment 
'''
conda --version
conda create -p venv python==3.7 -y
conda activate venv/
'''

#Git commands
'''
git status
git add . 
Or
git add filename
git log

'''

Note: To ignore file or folder from git we can write name of file/folder in .gitignore file

#To create version/commit all changes by git 
git commit -m "message"

#To send version/changes to github 
git push origin main 

#To check origin/remote url
git remote -v


#To setup CI/CD pipeline in heroku we need 3 information 

1. HEROKU_EMAIL = tavleenbajwa8@gmail.com
2. HEROKU_API_KEY =
3. HEROKU_APP_NAME = ml_regression_app_1

#Build docker image

'''
docker build -t <image_name>:<tagname>

#Note: Image name for docker must be lowercase


#To list docker images 

docker images 

#To run docker image

docker run -p 5000:5000 -e PORT=5000 fed79bd52243

#To check running containers in docker

docker ps

#To stop docker container 

docker stop <container_id> 