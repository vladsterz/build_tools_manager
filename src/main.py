import bimpy
import os
from subprocess import Popen, PIPE
import subprocess
import sys

import data

def main():
    selected_compiler = bimpy.Int()
    ctx = bimpy.Context()
    ctx.init(240, 240, "Virtual enviroment manager")

    environments = dict()
    for environment_path in data.envs:
        for env in os.listdir(environment_path):
            if os.path.exists(os.path.join(environment_path, env, "Scripts")):
                environments[env] = os.path.join(environment_path, env, "Scripts", "activate.bat")

    compilers_list = list(data.compilers.keys())

    while(not ctx.should_close()):
            with ctx:
                for enviroment in environments:
                    if bimpy.button(enviroment):
                        compiler = list(data.compilers.values())[selected_compiler.value] if selected_compiler.value != 0 else ""
                        subprocess.call(['start',environments[enviroment], compiler], shell = True)
                if bimpy.combo("Compiler",selected_compiler, compilers_list):
                    pass                    


if __name__ == "__main__":
    main()
