#coding: utf-8
import os
import shutil
import checkout
import re
import sys
import time
import csv
import numpy as np
import net_train
from sklearn.neural_network import MLPClassifier
sys.path.append(os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir)) + "/travis_ml")

tmpDirPath = "../tmp/"
tmpTreeDirPath = "../tmp_tree/"
tmpLocalTreeDirPath = "../tmp_local_tree/"
tmpReposPath = "../local/tmp_repos"

LABELS = {"errored":0, "passed":1, "failed":2}
mode = 2

def create_metadata(SHA, status, prj_name, depth, cf_ori_list):

	if depth == 1:
		checkout.getRepo(prj_name, SHA, depth, cf_ori_list)
	elif depth == 2:
		with open(tmpDirPath+"metadata" + re.split('/', prj_name)[1] + ".csv", 'ab') as file:
			file.write(SHA + "," + status + "," + checkout.getRepo(prj_name, SHA, depth, cf_ori_list))
	elif depth == 3:
		with open(tmpDirPath+"metadata" + re.split('/', prj_name)[1] + "local.csv", 'ab') as file:
			file.write(SHA + "," + status + "," + checkout.getRepo(prj_name, SHA, 2, cf_ori_list))
	else:
		pass

def support(global_list_commits, all_commits, eta):
	temp = []
	for i in all_commits:
		counting = 0
		for j in global_list_commits:
			if i in j:
				counting = counting + 1 
		if counting >= eta * len(global_list_commits):
			temp.append(i)
	return temp


def main():
	start = time.time()
    
	#os.system("rm %s/*" % tmpDirPath)

	# make temporary paths
	if not os.path.exists(tmpDirPath):
		os.makedirs(tmpDirPath)
	if not os.path.exists(tmpReposPath):
		os.makedirs(tmpReposPath)


    
	global_list_commits = []
	depth = 1 # depth = 1 means scan the first one to capture all magic number code features
	#depth = 2 means global, depth = 3 means local
	
	
	textpath = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir)) + "/textfile"
	files = os.listdir(textpath)
			
	for file in files:
		if file == ".DS_Store":
			pass
		else:
			cf_ori_list = []
			list_of_SHA = []
			if file[-3:-1] + file[-1] == "txt":
				oripath = os.path.dirname(os.path.abspath("__file__"))
				os.chdir(textpath)
				inputting = open(file).readlines()
				os.chdir(oripath)

				for i in inputting:				
					SHA = re.split(',', i)[0]
					status = re.split(',', i)[2]
					prj_name = re.split(',', i)[1]
					folder_name = re.split('/', prj_name)[1]
					if depth == 1:
						list_of_SHA.append(SHA)
					#print SHA + "," + status + "," + checkout.getRepo(prj_name, SHA, depth)
					create_metadata(SHA, status, prj_name, depth, cf_ori_list)
			
			if depth == 1:
				
				global_list_commits.append(cf_ori_list)
			print "len(global_list_commits)",len(global_list_commits)


	all_commits = []
	for i in global_list_commits:
		for j in i:
			if j not in all_commits:
				all_commits.append(j)

	eta = 0.28

	final_commit_list = support(global_list_commits, all_commits, eta) #final commits are those who appear often in the global one

	depth = 2

	# get all the features into a csv 
	for file in files:
		if file == ".DS_Store":
			pass
		else:
			list_of_SHA = []
			#cf_temp_list = []
			
			if file[-3:-1] + file[-1] == "txt":
				oripath = os.path.dirname(os.path.abspath("__file__"))
				os.chdir(textpath)
				inputting = open(file).readlines()
				os.chdir(oripath)

				for i in inputting:				
					SHA = re.split(',', i)[0]
					status = re.split(',', i)[2]
					prj_name = re.split(',', i)[1]
					folder_name = re.split('/', prj_name)[1]
					list_of_SHA.append(SHA)
					create_metadata(SHA, status, prj_name, depth, final_commit_list)
					
			print tmpDirPath+"metadata" + re.split('/', prj_name)[1] + ".csv", folder_name
			#decision_tree.DT(tmpDirPath+"metadata" + re.split('/', prj_name)[1] + ".csv", folder_name, depth, len(list_of_SHA) - 1)
			#os.remove(tmpDirPath+"metadata" + re.split('/', prj_name)[1] + ".csv")
	sample_rate = 0.1

	for file in files:
		if file == ".DS_Store":
			pass
		else:
			list_of_SHA = []
			cf_temp_list = []
			
			if file[-3:-1] + file[-1] == "txt":
				oripath = os.path.dirname(os.path.abspath("__file__"))
				os.chdir(textpath)
				inputting = open(file).readlines()
				os.chdir(oripath)

				for i in inputting:				
					SHA = re.split(',', i)[0]
					status = re.split(',', i)[2]
					prj_name = re.split(',', i)[1]
					folder_name = re.split('/', prj_name)[1]
					#list_of_SHA.append(SHA)
					#print SHA + "," + status + "," + checkout.getRepo(prj_name, SHA, depth)
					create_metadata(SHA, status, prj_name, 1, cf_temp_list)

				for i in inputting:
					SHA = re.split(',', i)[0]
					status = re.split(',', i)[2]
					prj_name = re.split(',', i)[1]
					folder_name = re.split('/', prj_name)[1]
					#list_of_SHA.append(SHA)
					create_metadata(SHA, status, prj_name, 3, cf_temp_list)

	os.chdir(tmpDirPath)
	files_features = os.listdir(tmpDirPath)
	for file in files_features:
		if file == ".DS_Store":
			pass
		else:
			if file[-9:] == "local.csv":
				with open(file) as csvFile:
					# generate training set from the csv 
					yval = []
					xval = []
					orig = list(csv.reader(csvFile))
					featurecount = len(orig[1]) - 2
					rowcount = len(orig)
					print rowcount
					print featurecount
					for row in orig:
						yval.append(LABELS[row[1]])
						xval.append(map(float, row[2:]))
					xval = np.array(xval)
					yval = np.array(yval)
					print net_train.neural_predict(xval, yval, mode)

if __name__ == '__main__':
    main()	