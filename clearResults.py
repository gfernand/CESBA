import os
import shutil

shutil.rmtree('results/M0')
shutil.rmtree('results/M1')
shutil.rmtree('results/M2')
os.system('cd results && mkdir M0 && mkdir M1 && mkdir M2')