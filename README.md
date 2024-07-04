# Fashion_Recommender_with_MLOps_EndtoEnd

Workflow that we are going to follow:

Update config.yaml
Update secrets.yaml [Optional] ( It is used when we are using any database secret credentials like secret key and all then that we write in secrets.yaml file )
Update params.yaml ( Here we will mention the paramaters of our model )
Update the entity
Update the configuration manager in src config
Update the components
Update the pipeline
Update the main.py
Update the dvc.yaml

YAML files are generally used as configuration files. Configuration files contain parameters that might change, so instead of searching through the code to update these parameters one by one, we define them in a configuration file. This file acts like a dictionary, and in the code, we use the keys from the configuration file. When changes are needed, we only make update in one single place inside the configuration file and not one by one in the code.
