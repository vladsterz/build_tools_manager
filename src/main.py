import bimpy
import os
from subprocess import Popen, PIPE
import subprocess
import sys
from utils import getAvailableEnviroments

import data
WIDTH = 240
HEIGHT = 240




class BimpyContext:
    def __init__(self, width, height, name):
        self.ctx = bimpy.Context()
        self.ctx.init(width, height, name)


#TODO: create new enviroment
# def renderAddNewEnvironment():
#     ctx = bimpy.Context()
#     ctx.init(WIDTH, HEIGHT, "New enviroment window")

#     while(not ctx.should_close()):
#         with ctx:
#             bimpy.text("TEST")


def main():
    selected_compiler = bimpy.Int()
    ctx = bimpy.Context()
    ctx.init(WIDTH, HEIGHT, "Virtual enviroment manager")

    environments = getAvailableEnviroments()
    compilers_list = list(data.compilers.keys())

    show_new_env_menu = False

    while(not ctx.should_close()):
            with ctx:
                bimpy.set_next_window_pos(bimpy.Vec2(0, 0), bimpy.Condition.Once)
                bimpy.set_next_window_size(bimpy.Vec2(WIDTH, HEIGHT), bimpy.Condition.Once)
                bimpy.begin("Enviroments",bimpy.Bool(True), \
                    bimpy.WindowFlags.NoCollapse and bimpy.WindowFlags.NoResize)
                bimpy.text(sys.version)
                bimpy.columns(2)
                for enviroment in environments:
                    if bimpy.button(enviroment):
                        compiler = list(data.compilers.values())[selected_compiler.value] if selected_compiler.value != 0 else ""
                        subprocess.call(['start',environments[enviroment], compiler], shell = True)
                    bimpy.next_column()
                    if bimpy.button("O##" + enviroment):
                        subprocess.Popen(r'explorer /select,' + os.path.dirname(environments[enviroment]))
                        #os.startfile(os.path.realpath(os.path.dirname(environments[enviroment])))
                    bimpy.next_column()
                bimpy.columns(1)
                if bimpy.combo("Compiler",selected_compiler, compilers_list):
                    pass

                
                # if bimpy.button("Add new enviroment"):
                #     new_env_ctx = BimpyContext(WIDTH, HEIGHT, "New enviroment menu")
                #     while(not new_env_ctx.ctx.should_close()):
                #         with new_env_ctx.ctx:
                #             bimpy.begin("dsad")
                #             bimpy.text("d")
                #             bimpy.end()
            

                # if bimpy.button("Create new enviroment"):

                bimpy.end()
            


if __name__ == "__main__":
    main()
