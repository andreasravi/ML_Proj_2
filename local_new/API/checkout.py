#coding: utf-8
import os
import re
import cfsrc
import subprocess
#import oricfgeneration
#def getData()

def getRepo(git_repo_name, SHA, depth, cf_ori_list):
    original_path = os.path.dirname(os.path.abspath("__file__"))
    gitReposPath = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir)) + "/tmp_repos"
    os.chdir(gitReposPath)
    
    if not os.path.isdir(gitReposPath + "/" + re.split('/', git_repo_name)[1]):
        os.system("git clone https://github.com/" + git_repo_name + ".git")

    os.chdir(gitReposPath + "/" + re.split('/', git_repo_name)[1])
    
    #os.system("ls")
    #os.system("git checkout " + SHA)
    with open(os.devnull, "w") as f: subprocess.call("git checkout "+SHA, stdout=f, stderr=f,shell=True)
    #with open(os.devnull, "w") as f: subprocess.call("git checkout "+SHA, stdout=f,shell=True)

    #print type(cfsrc.codefeature_src(oripath + "/" + re.split('/', git_repo_name)[1]))

    # go back the the top level dir before we end here
    os.chdir(original_path)

    return cfsrc.codefeature_src((gitReposPath + "/" + re.split('/', git_repo_name)[1]), depth, cf_ori_list)