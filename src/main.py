import bimpy
import os
from subprocess import Popen, PIPE
import subprocess
import sys

import data
WIDTH = 240
HEIGHT = 240

def getAvailableEnviroments():
    environments = dict()
    for environment_path in data.envs:
        for env in os.listdir(environment_path):
            if os.path.exists(os.path.join(environment_path, env, "Scripts")):
                environments[env] = os.path.join(environment_path, env, "Scripts", "activate.bat")
    return environments

#TODO: create new enviroment

def main():
    selected_compiler = bimpy.Int()
    ctx = bimpy.Context()
    ctx.init(WIDTH, HEIGHT, "Virtual enviroment manager")

    environments = getAvailableEnviroments()
    compilers_list = list(data.compilers.keys())

    while(not ctx.should_close()):
            with ctx:
                bimpy.set_next_window_pos(bimpy.Vec2(0, 0), bimpy.Condition.Once)
                bimpy.set_next_window_size(bimpy.Vec2(WIDTH, HEIGHT), bimpy.Condition.Once)
                bimpy.begin("Enviroments",bimpy.Bool(True), \
                    bimpy.WindowFlags.NoCollapse and bimpy.WindowFlags.NoResize \
                    
                        )
                for enviroment in environments:
                    if bimpy.button(enviroment):
                        compiler = list(data.compilers.values())[selected_compiler.value] if selected_compiler.value != 0 else ""
                        subprocess.call(['start',environments[enviroment], compiler], shell = True)
                    bimpy.same_line()
                    if bimpy.button("O##" + enviroment):
                        subprocess.Popen(r'explorer /select,' + os.path.dirname(environments[enviroment]))
                        #os.startfile(os.path.realpath(os.path.dirname(environments[enviroment])))
                if bimpy.combo("Compiler",selected_compiler, compilers_list):
                    pass

                # if bimpy.button("Create new enviroment"):

                bimpy.end()              


if __name__ == "__main__":
    main()
