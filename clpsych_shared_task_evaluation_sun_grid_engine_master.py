from __future__ import division

"""
This houses all the specific nitty-gritty for running the shared task
learning and evaluation procedures so number are maximally comparable.

We built this for a parallel environment (e.g. SunGridEngine), but
it should be lightweight enough to run the 10 folds sequentially.
"""


from clpsych_2015_shared_task_experiments import (NUM_FOLDS,
                                                  CODE_ROOT,
                                                  DATA_ROOT)


project_name = 'testing_%s_SGD'

#Further mod this with conditino and fold number 
generic_command = '%sclpsych_shared_task_evaluation_drone.py %s %s %s%s/' % \
                  (CODE_ROOT, '%s','%s', DATA_ROOT, project_name)

sge_command = 'qsub -l h_rt=8:00:00,mem_free=4G,h_vmem=4G -q text.q -b y -e /export/projects/tto6/mental_health/sge_files/ -o /export/projects/tto6/mental_health/sge_files/ -M coppersmith@gmail.com '
import os

for fold in range(NUM_FOLDS):
    for condition in ['ptsd','depression']:
        #Generate jobs to send to a grid or to run in sequence
        command = generic_command % (condition, fold, condition)
        run_this = sge_command + command
        os.system(run_this)


