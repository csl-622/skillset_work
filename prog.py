import xml.etree.cElementTree as ET 
import pickle
import os


def give_max(a,b,c):
	if b>a:
		a=b
		if c>a:
			a=c
	return a

def userid_questions_answers(data_folder_path):
	questions_asked = {}
	answers_given = {}
	total_votes_given = {}


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
						questions_asked[user_id] += 1
					else:
						questions_asked[user_id] = 1
				elif type == '2':
					if answers_given.has_key(user_id):
						answers_given[user_id] += 1
					else:
						answers_given[user_id] = 1
		child.clear()

	context2 = ET.iterparse(data_folder_path+'/Comments.xml')

	for event, child in context2: #child will contain each row
		if child.attrib == {}: # This is to tackle with the empty child that appears at last
			continue
		else:
			if child.attrib.has_key('UserId'):
				user_id = int(child.attrib['UserId'])
			if child.attrib.has_key('Score'):
				if total_votes_given.has_key(user_id):
					total_votes_given[user_id] += int(child.attrib['Score'])
				else:
					total_votes_given[user_id] = int(child.attrib['Score'])
		child.clear()


		# userid: [Ques asked, ans posted, votes added]
	user_con={}

	for key,value in answers_given.items():
		if user_con.has_key(key):
			user_con[key]=[user_con[key][0],value,user_con[key][2]]
		else:
			user_con[key]=[0,value,0]

	for key,value in questions_asked.items():
		if user_con.has_key(key):
			user_con[key]=[value,user_con[key][1],user_con[key][2]]
		else:
			user_con[key]=[value,0,0]
	for key,value in total_votes_given.items():	
		if user_con.has_key(key):
			user_con[key]=[user_con[key][0],user_con[key][1],value]
		else:
			user_con[key]=[0,0,value]	
		
	for key,value in user_con.items():
		print("User_Id:"+str(key)+'\t Questions Asked:'+str(value[0])+'\t Answers Posted:'+str(value[1])+'\t Votes Given:'+str(value[2]))

def main():
	data_folder_path='small_sample'
	path=os.getcwd()+'/'+data_folder_path;
	arr = os.listdir(path);
	for files in arr:
		print "\n\n========== Analysis for :"+files+"===============\n\n";
		userid_questions_answers(path+'/'+files)
main()