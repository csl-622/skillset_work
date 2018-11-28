import xml.etree.cElementTree as ET 
import pickle
import os
import re
# Using Elbow methord to reduce average distance between centroid and cluster
import matplotlib.pyplot as plt
import pandas as pd # For Data Analytics
from sklearn.cluster import KMeans
import numpy
#===================-- SET DIRECTORY NAME --=================================
folder_to_data_folder_path='small_sample'
#============================================================================



def userid_nmat(path,filename):
	filename2='Results/'+filename+'_Result_pkl.pkl'
	user_con={}
	user_con_array=[]
	user_con_taken=[]
	total_questions=0
	total_answers=0
	with open(filename2,'rb') as f:
		user_con=pickle.load(f)	
	for key,val in user_con.items():
		divider=val[0]+val[1]
		if divider!=0:
			total_questions+=val[0]
			total_answers+=val[1]
			user_con_taken.append(key)
			val2=[float(val[0])/divider,float(val[1])/divider]
			user_con_array.append(val2)
	# Numpy Conversion
	user_con_array=numpy.array(user_con_array)
	kmeans=KMeans(n_clusters=2,init='k-means++',random_state=None)
	group_belongs=kmeans.fit_predict(user_con_array)
	question_askers=0
	answer_givers=0
	for x in group_belongs:
		if x==1:
			question_askers+=1
		elif x==0:
			answer_givers+=1	
	Nmat=numpy.array([[question_askers,0],[0,answer_givers]])
	Kmat=numpy.array([[total_questions],[total_answers]])

	filename2='Nmat_Kmat/'+filename+'_Nmat.pkl'
	with open(filename2,'wb') as f:
		pickle.dump(Nmat,f)
	filename2='Nmat_Kmat/'+filename+'_Kmat.pkl'
	with open(filename2,'wb') as f:
		pickle.dump(Kmat,f)
		
	print "Shows Questionaires provides Answers heavily but not seem otherwise"
	print Nmat,"\n",Kmat



def main():
	path=os.getcwd()+'/'+folder_to_data_folder_path
	arr = os.listdir(path)
	if((os.path.isdir(os.getcwd()+"/Nmat_Kmat"))==False):
		os.mkdir("Nmat_Kmat")
	for files in arr:
		userid_nmat(path+'/'+files,files)
main()