import re
import urllib
import pickle
import util

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabet_url=[]
for letter in alphabet:
    alphabet_url.append('http://research.brown.edu/includes/collaborators_namesearch.php?letter='+letter)


prof_ids=[]
for url in alphabet_url:
    f=util.dl_and_prep(url)
    prof_links=re.findall("</option><option value=\"(\d*)\">",f)
    for prof_link in prof_links:
        prof_ids.append(prof_link)
#print prof_ids
#print len(prof_ids)

prof_profiles =[]
for value in prof_ids:
    prof_profiles.append("http://research.brown.edu/research/profile.php?id="+value)
#print prof_profiles

brown_profs=[]

for prof in prof_profiles:
    first_name =""
    last_name =""
    title = ""
    department =""
    email = ""
    bio = ""
    summary = ""
    interests =""
    image =""
    g=util.dl_and_prep(prof)
    if len(re.findall("\[firstname\] => (.*?)\s",g))>0:
        first_name = re.findall("\[firstname\] => (.*?)\s",g)[0] 
    if len(re.findall("\[lastname\] => (.*?)\s",g))>0:
        last_name = re.findall("\[lastname\] => (.*?)\s",g)[0] 
    if len(re.findall("\[title\] => (.*?)\n\s*\[",g))>0:
        title = re.findall("\[title\] => (.*?)\n\s*\[",g)[0] 
    if len(re.findall("\[department\] => (.*?)\n\s*\[",g))>0:
        department = re.findall("\[department\] => (.*?)\n\s*\[",g)[0]
        department = util.prep_department(department)
        print department
    if len(re.findall("\[email\] => (.*?)\s",g))>0:
        email = re.findall("\[email\] => (.*?)\s",g)[0] 
    if len(re.findall("\[bio\] => (.*?)\n\s*\[",g))>0:
        bio = re.findall("\[bio\] => (.*?)\n\s*\[",g)[0] 
    if len(re.findall("\[summary\] => (.*?)\n\s*\[",g))>0:
        summary = re.findall("\[summary\] => (.*?)\n\s*\[",g)[0] 
    if len(re.findall("\[interests\] => (.*?)\n\s*\[",g))>0:
        interests = re.findall("\[interests\] => (.*?)\n\s*\[",g)[0] 
    if len(re.findall("class=rightColumn>.*?<img src=\"(.*?)\"",g))>0:
        image = "http://research.brown.edu" + re.findall("class=rightColumn>.*?<img src=\"(.*?)\"",g)[0]
    #research = re.findall("\[fresearch\] => (.*?)\n\s*\[",g)[0] if len()>0]
    name = first_name + " " +last_name
    brown_prof_dict ={}
    brown_prof_dict["name"] = name
    brown_prof_dict["email"] = email
    brown_prof_dict["title"] = title
    brown_prof_dict["department"] = department
    brown_prof_dict["interests"] = interests 
    brown_prof_dict["bio"] = bio
    research_summary = ''
    l = [interests, summary, bio]
    for s in l:
        if s:
            research_summary += '<p>%s</p>' % s
            
    brown_prof_dict["research_summary"] = research_summary
    brown_prof_dict["image"] = image
    brown_prof_dict["school"] = "Brown University"
    brown_prof_dict["source"] = prof
    if name:
        brown_profs.append(brown_prof_dict)
    
pickle.dump(brown_profs, file('prof_dicts/brown.dat', 'w'))
print "Done!"

    

