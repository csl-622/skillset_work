import xml.etree.cElementTree as ET
import os
import datetime
import time
import numpy
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#===================-- SET DIRECTORY NAME --=================================
folder_to_data_folder_path='Data'
#============================================================================
frac = [0.85, 0.90, 1.00]   #fraction of time at which sampling is done
r = 1         #internal knowledge


n1 = 0.0
n1new = 0.0
n2 = 0.0
n2new = 0.0
p = 0.0
pnew = 0.0
q = 0.0
qnew = 0.0
actual_n1_list = []
actual_n2_list = []
expected_n1_list = []
expected_n2_list = []
def getNK(folder, filename, timestamp, fraction):
    global n1
    global n1new
    global n2
    global n2new
    global p
    global pnew
    global q
    global qnew
    global str
    # Each dictionary contains key as User ID and key as respective numbers of Questions / Answers Asked/Given
    questions_asked = {}
    answers_given = {}
    # Calculated as per subtraction of Upvotes-Downvotes
    account_votes={}
    # Contains User id and list of all its UNIQUE interest of Contribution through TAG ID's
    interest_area={}
    context = ET.iterparse(folder + '/Posts.xml')
    less = 0
    more = 0
    for event, child in context: #child will contain each row
        if child.attrib == {}: # This is to tackle with the empty child that appears at last
            continue
        else:
            if 'CreationDate' in child.attrib:
                curr_time_str = child.attrib['CreationDate']
                curr_time = time.mktime(datetime.datetime.strptime(curr_time_str, "%Y-%m-%dT%H:%M:%S.%f").timetuple())
                delta = timestamp - curr_time
                if delta >= 0:
                    less += 1
                    user_id=0
                    if 'OwnerUserId' in child.attrib:
                        user_id = int(child.attrib['OwnerUserId'])
                    if 'PostTypeId' in child.attrib:
                        type = child.attrib['PostTypeId']
                        if type == '1':
                            if user_id in questions_asked:
                                questions_asked[user_id] += 1 # Adding Questions Added for the Website
                            else:
                                questions_asked[user_id] = 1
                        elif type == '2':
                            if user_id in answers_given: # Adding Answers Added for the Website
                                answers_given[user_id] += 1
                            else:
                                answers_given[user_id] = 1
                else:
                    more += 1
        child.clear()

    # Calculating User Id Contributed VOTES : UPVOTES + DOWNVOTS
    context3 = ET.iterparse(folder + '/Users.xml')
    for event, child in context3: #child will contain each row
        if child.attrib == {}: # This is to tackle with the empty child that appears at last
            continue
        else:
            if 'Id' in child.attrib:
                acc_id = int(child.attrib['Id'])
                account_votes[acc_id] = int(child.attrib['UpVotes'])+int(child.attrib['DownVotes'])
        child.clear()

    # STORED AS userid: [Ques asked, ans posted, votes added ]
    user_con={}
    for key,value in answers_given.items():
        if key in user_con:
            user_con[key]=[user_con[key][0],value,user_con[key][2]]
        else:
            user_con[key]=[0,value,0] # In case not found making a new Entry With other two as 0
    for key,value in questions_asked.items():
        if key in user_con:
            user_con[key]=[value,user_con[key][1],user_con[key][2]]
        else:
            user_con[key]=[value,0,0]
    for key,value in account_votes.items():
        if key in user_con:
            user_con[key]=[user_con[key][0],user_con[key][1],value]
        else:
            user_con[key]=[0,0,value]

    user_con_array=[]
    user_con_taken=[]
    total_questions=0
    total_answers=0
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
    Nmat = numpy.array([[question_askers,0],[0,answer_givers]])
    Kmat = numpy.array([[total_questions],[total_answers]])
    cpath = os.getcwd() + "/NandK/"
    f = open(cpath + filename + str(fraction) + ".txt", "w")
    f.write("N matrix (Diagonal matrix consisting of number of users in different categories):\n")
    f.write(str(Nmat))
    f.write("\nK matrix (Column matrix denoting the amount of knowledge built upto " + str(100 * fraction) + "% of the time):\n")
    f.write(str(Kmat))
    f.close()
    if fraction == frac[0]:
        n1 = Nmat[0][0]
        n2 = Nmat[1][1]
        p = Kmat[0]
        q = Kmat[1]
    if fraction == frac[1]:
        n1new = Nmat[0][0]
        n2new = Nmat[1][1]
        pnew = Kmat[0]
        qnew = Kmat[1]
    if fraction == frac[2]:
        n1 = float(n1)
        n1new = float(n1new)
        n2 = float(n2)
        n2new = float(n2new)
        p = float(p)
        pnew = float(pnew)
        q = float(q)
        qnew = float(qnew)
        #n1new = n1new * ((n1 + n2) / (n1new +n2new))
        #n2new = n2new * ((n1 + n2) / (n1new +n2new))
        #print(n1, n1new, n2, n2new, p, pnew, q, qnew)
        a = ((n1new - n1) / (n1 * n1new)) + ((r * (qnew - q)) / ((p * qnew) - (pnew * q)))
        b = (p + (n1 * r) - (n1 * a * p)) / (n1 * q)
        c = (1 / ((pnew * q) - (p * qnew))) * (((q * qnew * (n2 - n2new)) / (n2 * n2new *((pnew * q) - (p * qnew)))) + ((r * (q - qnew)) / ((pnew * q) - (p * qnew))))
        d = (q + (n2 * r) - (n2 * c * p)) / (n2 * q)
        expected_n1 = p / ((a * Kmat[0]) + (b * Kmat[1]) - r)
        expected_n2 = q / ((c * Kmat[0]) + (d * Kmat[1]) - r)
        expected_n1_list.append(expected_n1)
        expected_n2_list.append(expected_n2)
        actual_n1_list.append(Nmat[0][0])
        actual_n2_list.append(Nmat[1][1])
        cpath = os.getcwd() + "/Trigerring_matrix/"
        f = open(cpath + filename + ".txt", "w")
        f.write("Trigerring matrix for " + filename + " data:\n")
        T_mat = numpy.array([[a, b], [c, d]])
        f.write(str(T_mat))


def main():
    path=os.getcwd()+'/'+folder_to_data_folder_path
    arr = os.listdir(path)
    if((os.path.isdir(os.getcwd()+"/NandK"))==False):
        os.mkdir("NandK")
    if((os.path.isdir(os.getcwd()+"/NandK"))==False):
        os.mkdir("Trigerring_matrix")
    for files in arr:
        startTime = 9999999999999999999999999
        endTime = 0
        context = ET.iterparse(path + '/' + files + '/Posts.xml')
        for event, child in context: #child will contain each row
            if child.attrib == {}: # This is to tackle with the empty child that appears at last
                continue
            else:
                if 'CreationDate' in child.attrib:
                    curr_time_str = child.attrib['CreationDate']
                    curr_time = time.mktime(datetime.datetime.strptime(curr_time_str, "%Y-%m-%dT%H:%M:%S.%f").timetuple())
                    delta = startTime - curr_time
                    #print(delta)
                    if delta > 0:
                        startTime = curr_time
                    delta =  curr_time - endTime
                    if delta > 0:
                        endTime = curr_time
        #print(startTime)
        #print(endTime)
        getNK(path + '/' + files, files, startTime + (frac[0] * (endTime - startTime)), frac[0])
        getNK(path + '/' + files, files, startTime + (frac[1] * (endTime - startTime)), frac[1])
        getNK(path + '/' + files, files, startTime + (frac[2] * (endTime - startTime)), frac[2])
    plt.plot(actual_n1_list, actual_n2_list, '.', color='b')
    plt.plot(expected_n1_list, expected_n2_list, '.', color='r')
    plt.ylabel('n1')
    plt.xlabel('n2')
    plt.savefig("graph.png")

main()
