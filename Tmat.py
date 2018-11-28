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

#===================-- SET DIRECTORY NAME --=================================
folder_to_data_folder_path='small_sample'
#============================================================================


def Tmat_cal(path,filename):
	filename2='Nmat_Kmat/'+filename+'_Nmat.pkl'
	with open(filename2,'rb') as f:
		Nmat=pickle.load(f)
	filename2='Nmat_Kmat/'+filename+'_Kmat.pkl'
	with open(filename2,'rb') as f:
		Kmat=pickle.load(f)
	Tmat=numpy.matrix([[1,2],[2,1]])
	R=numpy.matrix([[0.01],[0.01]])
	result=inv(Nmat)*(Kmat-(Nmat*R))
	X=(result[0,0]-(Tmat[0,0]*Kmat[0,0]))/Kmat[1,0]
	Y=(result[1,0]-(Tmat[1,1]*Kmat[1,0]))/Kmat[0,0]
	Tmat=numpy.matrix([[1,-X],[-Y,1]])
	
	filename2='Tmat/'+filename+'_Tmat.pkl'
	with open(filename2,'wb') as f:
		pickle.dump(Tmat,f)

	print Tmat
		
def main():
	path=os.getcwd()+'/'+folder_to_data_folder_path
	arr = os.listdir(path)
	if((os.path.isdir(os.getcwd()+"/Nmat_Kmat"))==False):
		print "Run Nmat_Kmat.py"
		return
	if((os.path.isdir(os.getcwd()+"/Tmat"))==False):	
		os.mkdir("Tmat")
	for files in arr:
		Tmat_cal(path+'/'+files,files)
main()