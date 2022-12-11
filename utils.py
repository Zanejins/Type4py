from typing import List
from tqdm import tqdm
from joblib import Parallel
import time
import os

def filter_directory(directory:str,extension:str = '.py') -> str:
    """
    Delete all files within the given directory with filenames not ending in the given extension
    """
    for root,dirs,files in os.walk(directory):
        [os.remove(os.path.join(root,fi)) for fi in files if not fi.endswith(extension)]
    
    return directory

def list_files(directory:str) ->str:
    """
    List all files in the given directory(recursively)
    """

    filenames = []
    for root,dirs,files in os.walk(directory):
        for filename in files:
            filenames.append(os.path.join(root,filename))

    
    return filenames


def find_repos_list(projects_path:str) -> List[dict]:
    """
    Finds a list of author/repo from a Python dataset.
    """

    repos_list:List[dict] = []

    for author in os.listdir(projects_path):
        if not author.startswith('.') and os.path.isdir(os.path.join(projects_path,author)):
            for repo in os.listdir(os.path.join(projects_path,author)):
                repos_list.append({"author":author,"repo":repo})

    return repos_list

def read_file(filename:str) -> str:
    """
    open a file and return its contents as a string
    """

    with open(filename) as file:
        return file.read()


def mk_dir_not_exist(path:str):
    if not os.path.isdir(path):
        os.mkdir(path)


def text_progessbar(seq,total=None):
    step = 1
    tick = time.time()
    while True:
        time_diff = time.time() - tick
        avg_speed = time_diff / step
        total_str = 'of %n' % total if total else ''
        print("step",step,'%.2f'%time_diff,'avg:%.2f iter/sec'%avg_speed,total_str)
        step+=1
        yield next(seq)

all_bar_funcs = {
    'tqdm':lambda args : lambda x:tqdm(x,**args),
    'txt':lambda args : lambda x:text_progessbar(x,**args),
    'False':lambda args:iter,
    'None':lambda args:iter,
}

def ParallelExecutor(use_bar = 'tqdm',**joblib_args):
    def aprun(bar=use_bar,**tq_args):
        def tmp(op_iter):
            if str(bar) in all_bar_funcs.keys():
                bar_func = all_bar_funcs[str(bar)](tq_args)
            else:
                raise ValueError("Value %s not supported as bar type" % bar)
            return Parallel(**joblib_args)(bar_func(op_iter))
        return tmp
    return aprun

