import xml.etree.cElementTree as ET 
import pickle
import os
import re


#===================-- SET DIRECTORY NAME --=================================
folder_to_data_folder_path='small_sample'
#============================================================================


def userid_questions_answers(data_folder_path,filename):
	

	# Each dictionary contains key as User ID and key as respective numbers of Questions / Answers Asked/Given
	questions_asked = {}
	answers_given = {}
	# Calculated as per subtraction of Upvotes-Downvotes 
	account_votes={}
	# Contains User id and list of all its UNIQUE interest of Contribution through TAG ID's
	interest_area={}

	context = ET.iterparse(data_folder_path+'/Posts.xml')
	for event, child in context: #child will contain each row
		if child.attrib == {}: # This is to tackle with the empty child that appears at last
			continue
		else:
			if child.attrib.has_key('OwnerUserId'):
				user_id = int(child.attrib['OwnerUserId'])
			if child.attrib.has_key('PostTypeId'):
				type = child.attrib['PostTypeId']
				if type == '1':
					if questions_asked.has_key(user_id):
						questions_asked[user_id] += 1 # Adding Questions Added for the Website
					else:
						questions_asked[user_id] = 1
				elif type == '2':
					if answers_given.has_key(user_id): # Adding Answers Added for the Website
						answers_given[user_id] += 1
					else:
						answers_given[user_id] = 1
					
		child.clear()



	# Calculating User Id Contributed VOTES : UPVOTES + DOWNVOTS
	context3 = ET.iterparse(data_folder_path+'/Users.xml')

	for event, child in context3: #child will contain each row
		if child.attrib == {}: # This is to tackle with the empty child that appears at last
			continue
		else:
			if child.attrib.has_key('Id'):
			
				acc_id = int(child.attrib['Id'])
				account_votes[acc_id] = int(child.attrib['UpVotes'])+int(child.attrib['DownVotes'])
		child.clear()	

	
	# STORED AS userid: [Ques asked, ans posted, votes added ]
	user_con={}
	for key,value in answers_given.items():
		if user_con.has_key(key):
			user_con[key]=[user_con[key][0],value,user_con[key][2]]
		else:
			user_con[key]=[0,value,0] # In case not found making a new Entry With other two as 0

	for key,value in questions_asked.items():
		if user_con.has_key(key):
			user_con[key]=[value,user_con[key][1],user_con[key][2]]
		else:
			user_con[key]=[value,0,0]	
	
	for key,value in account_votes.items():
		if user_con.has_key(key):
			user_con[key]=[user_con[key][0],user_con[key][1],value]
			
		else:
			user_con[key]=[0,0,value]


	# Writing Account Summary ie UserId : Questions , Answers , Vote in FIle 

	filename1='Results/'+filename+'_Result_raw.txt'		
	f = open(filename1, 'w')
	for key,value in user_con.items():
		f.write("User_Id:"+str(key)+'\t Questions Asked:'+str(value[0])+'\t Answers Posted:'+str(value[1])+'\t 	Votes:'+str(value[2])+'\n')
	f.close()

	# Writing Account Summary ie UserId : Questions , Answers , Vote in Pickle

	filename2='Results/'+filename+'_Result_pkl.pkl'
	with open(filename2,'wb') as f:
		pickle.dump(user_con,f)
	
	
	
	
	# COMPUTING PERCENATGE OF UNI , BI , TRI Speciality in a Website
	speciality={}
	for key,value in user_con.items():
		speciality[key]=0
		for j in value:
			if j>0:
				speciality[key]+=1
	uni=0.0
	bi=0.0
	tri=0.0
	
	contributors=0.0		
	for key,value in speciality.items():
		if value!=0:
			contributors+=1
		if value==1:
			uni+=1
		if value==2:
			bi+=1
		if value==3:
			tri+=1		
	uni=(uni/contributors)*100
	tri=(tri/contributors)*100
	bi=(bi/contributors)*100
	
	spec=[uni,tri,bi]

	# Writing Website Summary ie UNI , BI , TRI in FIle 
	
	filename1='Results/'+filename+'_Specialist_raw.txt'
	f = open(filename1, 'w')
	f.write("UNI:"+str(uni)+' %\t BI:'+str(bi)+' %\t TRI:'+str(tri)+' %\n') 
	f.close()
	
	# Writing Website Summary ie UNI , BI , TRI in PICKLE 

	filename2='Results/'+filename+'_Specialist_pkl.pkl'
	with open(filename2,'wb') as f:
		pickle.dump(spec,f)
	

def main():
	path=os.getcwd()+'/'+folder_to_data_folder_path
	arr = os.listdir(path)
	if((os.path.isdir(os.getcwd()+"/Results"))==False):
		os.mkdir("Results")
	for files in arr:
		userid_questions_answers(path+'/'+files,files)
main()
