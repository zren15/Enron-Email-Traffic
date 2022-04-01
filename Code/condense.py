import sys
import os
import pandas as pd
from datetime import datetime
import re

maildirpath= sys.argv[1]

MailID = []
Date = []
From = []
To = []
Recipients = []
Subject = []
Filename = []

def user(addr):
    if '@enron.com' not in addr:
            return '-999'
    addr = addr[0:addr.index('@')]
    if '<' in addr or '#' in addr or "/o" in addr:
        return '-999'
    if "'" in addr:
        addr = addr.replace("'", "")
    if len(addr)>0 and addr[0] == '.':
        addr = addr[1:]
    if len(addr)==0:
        return '-999'
    return addr  

#def multi_user(mails):
#    if ' ,' not in mails:
#        mail = user(mails)
#        Mail.append(mail)
#        recipient = 1
#        Recipients.append(recipient)
#        Date.append(date)
#        From.append(from_slice)
#        Subject.append(subject)
#    else:
#        mails = mails.split(', ')
#        recipient = len(mails)
#        for i in range(len(mails)):
#            mail = mails[i]
#            Mail.append(mail)
#            Recipients.append(recipient)
#            Date.append(date)
#            From.append(from_slice)
#            Subject.append(subject)
#    return mail
            
            
for root, dirs, files in sorted(os.walk(maildirpath)):
    for filename in files:
        if filename.startswith("."):
            continue
        else:
            filepath = os.path.join(root, filename)
            path = re.search(maildirpath+'/'+'(.*)',filepath)
            filename = path.group(1)
#            m = filepath.split('/desktop/')
#            m = filepath.split('/enron-maildir/')
#            filename = m[1]
#            print(filename) 
            with open(filepath,"r", encoding='latin1') as f:
                whole = f.read()
                s1 = whole.find('Date')
                s2 = whole.find('From')
                s3 = whole.find('To')
                s4 = whole.find('Subject')
                e = whole.find('Mime-Version: 1.0')
                #date
                date = whole[s1:s2]
                date = date[11:-13]
                date = date.strip()
                if '0001' in date:
                    date = date.replace('0001','2001')
                elif '0002' in date:
                    date = date.replace('0002','2001')
                else:
                    date = date
#               print(date)
                #from
                from_slice = whole[s2:s3]
                if 'Subject:' in from_slice:
                    continue
                else:
                    from_slice = from_slice[6:]
                    from_slice = from_slice.strip()
                    from_slice = user(from_slice)
                    if from_slice == '-999':
                        continue
                    else:
                        from_slice = from_slice
                #subject
                subject = whole[s4:e]
#                print(subject,filename)
                if 'Cc:' in subject:
                    s5 = whole.find('Cc')
                    subject = whole[s4:s5]
                    subject = subject[9:]
                    subject = subject.split('\n')  
                    subject = subject[0]
                else:
                    subject = subject[9:]
                    subject = subject.split('\n')
#                    print(subject)
                    subject = subject[0]
#                    print(subject)
                    
#                    subject = subject.strip()
                #to
                to = whole[s3:s4]
                if len(to) == 0:
                    continue
                else:
                    to = to[3:]
                    to = to.strip()
                    if ', ' not in to:
                        mail = to.strip()
                        mail = user(mail)
                        if mail == '-999':
                            continue
                        else:
                            To.append(mail)
                            recipient = 1
                            Recipients.append(recipient)
                            Date.append(date)
                            From.append(from_slice)
                            Subject.append(subject)
                            Filename.append(filename)
                    else:
                        mail = to.split(', ')
                        j = 0
                        for i in range(len(mail)):
                            mail_split = mail[i]
                            mail_split = mail_split.strip()
                            mail_split = user(mail_split)
                            if mail_split == '-999':
                                continue
                            else:
                                mail_split = mail_split
                                j = j+1
                            To.append(mail_split)
                            Date.append(date)
                            From.append(from_slice)
                            Subject.append(subject)
                            Filename.append(filename)
                           
                        # recipient
                        c = j
                        m = j                                          
                        while m > 0:                                 
                            recipient = c 
                            m = m-1
                            Recipients.append(recipient)
#print(Recipients)
Id =1 
MailID.append(Id) 
for k in range(1,len(Recipients)):    
    filename1 = Filename[k-1]
    filename2 = Filename[k]
    if filename1 != filename2:
        Id = Id + 1
        MailID.append(Id)
    else:
        Id = Id
        MailID.append(Id)                        
                        


                                        
#                    elif info.startswith('From:'):
#                        info = info[6:]
#                        info = user(info)
#                        print(info)
#                    From.append(info)
        
df=pd.DataFrame({'MailID':MailID, 'Date':Date,'From':From,'To':To,'Recipients':Recipients,'Subject':Subject,'filename':Filename,})
df['Date'] = pd.to_datetime(df['Date'],errors = 'raise')
df['Date'] = df['Date'].dt.date
#df.to_csv (r'try.csv', index = False, header=True)   
df.to_feather("./enron.feather")
