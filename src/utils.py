import os
import data

def getAvailableEnviroments():
    environments = dict()
    for environment_path in data.envs:
        for env in os.listdir(environment_path):
            if os.path.exists(os.path.join(environment_path, env, "Scripts")):
                environments[env] = os.path.join(environment_path, env, "Scripts", "activate.bat")
    return environments

def getAvailabeCompilers():
    return data.compilers

def getAvailablePythons():
    return data.python_versions
