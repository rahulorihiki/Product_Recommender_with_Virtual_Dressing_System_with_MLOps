FROM python:3.8-slim-buster

RUN apt update -y && apt install awscli -y
WORKDIR /app

COPY . /app
# Install DVC
RUN pip install dvc

RUN pip install -r requirements.txt

# Configure DVC remote storage (optional, if needed)
RUN dvc remote add -f origin https://dagshub.com/rahulorihiki/Fashion_Recommender_with_MLOps_EndtoEnd.dvc
RUN dvc remote modify origin --local auth basic 
RUN dvc remote modify origin --local user rahulorihiki 
RUN dvc remote modify origin --local password 43732b0c3b736bb1721c19750df10aee79b78223

# Pull the data from the DVC remote repository
RUN dvc pull -r origin

EXPOSE 5000

CMD ["python", "app.py"]

