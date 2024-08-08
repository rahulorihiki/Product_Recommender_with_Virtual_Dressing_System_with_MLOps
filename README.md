# Product_Recommender_with_Virtual_Dressing_and_MLOps_EndtoEnd

This Project Recommendation System provides an interactive shopping experience, allowing users to search, view, and discover fashion products. It features the ability to try on clothes virtually and employs MLOps to track model and data versions effectively. The system's architecture is modularized for scalability and incorporates continuous integration and deployment for efficient cloud updates.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Technologies Used](#technologies-used)
5. [Machine Learning Models](#machine-learning-models)
6. [Dataset Used](#dataset-used)
7. [MLOps Workflow](#mlops-workflow-followed-in-the-project)
8. [Dagshub MLFLOW Configuration](#dagshub-mlflow-configurations)
9. [AWS-CICD-Deployment-with-Github-Actions](#aws-cicd-deployment-with-github-actions)
   - [Login to AWS Console](#1-login-to-aws-console)
   - [Create IAM User for Deployment](#2-create-iam-user-for-deployment)
   - [Create ECR Repo](#3-create-ecr-repo-to-storesave-docker-image)
   - [Create EC2 Machine](#4-create-ec2-machine-ubuntu)
   - [Install Docker in EC2 Machine](#5-open-ec2-and-install-docker-in-ec2-machine)
   - [Configure EC2 as Self-Hosted Runner](#6-configure-ec2-as-self-hosted-runner)
   - [Setup GitHub Secrets](#7-setup-github-secrets)
10. [Contributing](#contributing)
11. [License](#license)
12. [Contact Information](#contact-information)
13. [Citation](#citation)

## Features

1. Users can explore a wide range of fashion products through a user-friendly interface.
2. Offers the capability for users to try on clothes virtually using advanced computer vision models.
3. Provides personalized recommendations for similar products based on the product user chooses using content-filtering technique.
4. Utilizes Modular Architecture which ensures easy scalability and maintainability of the application.
5. Utilizes modern MLOps practices to track and manage data and model versions effectively.
6. Implemented an automated CI/CD pipeline to AWS.
7. Features a secure login and signup system for proper user authentication.

## Installation

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Flask, SQLite
- **MLOps Tools**: DVC, MLflow, Dagshub, Docker, GitHub Actions for CI/CD

## Machine Learning Models

- **ACGPN (Attentive Clothing Generation and Prediction Network)**: Used for the virtual dressing room feature.
- **Product Recommender**: Implemented using Convolutional Neural Networks (CNN) with ResNet-50 architecture and Nearest Neighbor algorithm.

## Dataset Used

1. Fashion Product Images Dataset: https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset
2. Fashion Product Images Dataset (Small): https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small
3. VITON Dataset: https://paperswithcode.com/dataset/viton

## MLOps Workflow Followed in the project

1. Update config.yaml
2. Update secrets.yaml
3. Update params.yaml
4. Update the entity
5. Update the configuration manager in src config
6. Update the components
7. Update the pipeline
8. Update the main.py
9. Update the dvc.yaml

## Dagshub MLFLOW Configurations

[dagshub](https://dagshub.com/)

MLFLOW_TRACKING_URI=[Get this from your dagshub repository for this project] \
MLFLOW_TRACKING_USERNAME=[Get this from your dagshub repository for this project] \
MLFLOW_TRACKING_PASSWORD=[Get this from your dagshub repository for this project] \
python script.py

Run this to export as env variables:

```bash

export MLFLOW_TRACKING_URI=[Get this from your dagshub repository for this project]

export MLFLOW_TRACKING_USERNAME=[Get this from your dagshub repository for this project]

export MLFLOW_TRACKING_PASSWORD=[Get this from your dagshub repository for this project]
```

# AWS-CICD-Deployment-with-Github-Actions

## 1. Login to AWS console.

## 2. Create IAM user for deployment

    #with specific access

    1. EC2 access : It is virtual machine

    2. ECR: Elastic Container registry to save your docker image in aws


    #Description: About the deployment

    1. Build docker image of the source code

    2. Push your docker image to ECR

    3. Launch Your EC2

    4. Pull Your image from ECR in EC2

    5. Lauch your docker image in EC2

    #Policy:

    1. AmazonEC2ContainerRegistryFullAccess

    2. AmazonEC2FullAccess

## 3. Create ECR repo to store/save docker image

    - Save the URI: 566373416292.dkr.ecr.us-east-1.amazonaws.com/chicken

## 4. Create EC2 machine (Ubuntu)

## 5. Open EC2 and Install docker in EC2 Machine:

    #optinal

    sudo apt-get update -y

    sudo apt-get upgrade

    #required

    curl -fsSL https://get.docker.com -o get-docker.sh

    sudo sh get-docker.sh

    sudo usermod -aG docker ubuntu

    newgrp docker

# 6. Configure EC2 as self-hosted runner:

    setting>actions>runner>new self hosted runner> choose os> then run command one by one

# 7. Setup github secrets:

    AWS_ACCESS_KEY_ID=

    AWS_SECRET_ACCESS_KEY=

    AWS_REGION = us-east-1

    AWS_ECR_LOGIN_URI = demo>>  566373416292.dkr.ecr.ap-south-1.amazonaws.com

    ECR_REPOSITORY_NAME = simple-app

## Contributing

Contributions are always welcome!

Please see `contributing.md` for ways to get started.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact Information

- **Kizhakkeppattu Rahul Govindkumar**
- **Email**: krahulgovind@gmail.com
- **Github**: https://github.com/rahulorihiki

## Citation

@InProceedings{Yang_2020_CVPR,
author = {Yang, Han and Zhang, Ruimao and Guo, Xiaobao and Liu, Wei and Zuo, Wangmeng and Luo, Ping},
title = {Towards Photo-Realistic Virtual Try-On by Adaptively Generating-Preserving Image Content},
booktitle = {IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
month = {June},
year = {2020}
}
