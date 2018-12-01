import xml.etree.cElementTree as ET 
import pickle
import os
import re
# Using Elbow methord to reduce average distance between centroid and cluster
import matplotlib.pyplot as plt
import pandas as pd # For Data Analytics
from sklearn.cluster import KMeans
import numpy
from numpy.linalg import inv
import sys

#===================-- SET DIRECTORY NAME --=================================
folder_to_data_folder_path='Data'
#============================================================================


def Tmat_cal(path,filename):
	filename2='Nmat_Kmat/'+filename+'_Nmat.pkl'
	with open(filename2,'rb') as f:
		Nmat=pickle.load(f)
	filename2='Nmat_Kmat/'+filename+'_Kmat.pkl'
	with open(filename2,'rb') as f:
		Kmat=pickle.load(f)
	filename2='Tmat/'+filename+'_Tmat.pkl'
	with open(filename2,'rb') as f:
		Tmat=pickle.load(f)
	path='Final_Results/'+filename
	f=open(path,'w+')	
	#---------------------------- Nmat/Kmat/Tmat now loaded ------------------------
	print >> f, "---------------------",filename,"-----------------------"
	if Nmat[0,0]>Nmat[1,1]:
		print >> f, "Question Askers are more than Answer Givers by factor of: ",float(Nmat[0,0])/Nmat[1,1]
	else:
		print >> f, "Answer Givers are more than Question Askers by factor of: ",float(Nmat[1,1])/Nmat[0,0]
	if Kmat[0,0]>Kmat[1,0]:
		print >> f, "\nKnowledge Genreated in Category Of Questions is more than in that of Answers by a factor of: ",float(Kmat[0,0])/Kmat[1,0]
	else:
		print >> f, "\nKnowledge Genreated in Category Of Answers is more than in that of Questions by a factor of: ",float(Kmat[1,0])/Kmat[0,0]
	print >> f, "\nThe Trigerring happening between Knowledge Categories: ",Tmat[0,0]
	if(Tmat[0,1]>Tmat[1,0]):
		print >> f, "\nQuestion askers Trigger Answer givers more by a factor of: ",float(Tmat[0,1])/Tmat[1,0]
	else:
		print >> f, "\nAnswer givers Trigger Question askers more by a factor of: ",float(Tmat[1,0])/Tmat[0,1]		
	f.close()
def main():
	if len(sys.argv) < 1:
		print "Enter As:- python Results.py"
		return
	path=os.getcwd()+'/'+folder_to_data_folder_path
	arr = os.listdir(path)
	if((os.path.isdir(os.getcwd()+"/Nmat_Kmat"))==False):
		print "Run Nmat_Kmat.py"
		return
	if((os.path.isdir(os.getcwd()+"/Tmat"))==False):	
		print "Run Tmat.py"
		return
	if((os.path.isdir(os.getcwd()+"/Final_Results"))==False):	
		os.mkdir("Final_Results")	
	for files in arr:
		Tmat_cal(path+'/'+files,files)
	print "Output STORED IN: Final_Results"

main()
