import re
import urllib2
all_prof_info =[]
for course in range(1,2):
    f= file('/home/rambhask/course'+str(course)+'prof.html').read()
    f=f.strip("\n")
    prof_info=re.findall("<dt><a href=\"(.*?)\"><strong>Prof\. (.*?)</strong></a>,.*?,.*?,.*?<.*?>(.*?)</a>\s*</dt>\s*<dd>(.*?)<", f)
    prof_info_alt= re.findall("<dt><strong><a href=\"(.*?)\">.*?\. (.*?)</a></strong>,.*?,.*?,.*?<.*?>(.*?)</a></dt>\s*<dd>(.*?)<",f)
    prof_info_alt2= re.findall("<dt><strong><a href=\"(.*?)\">.*?\. (.*?)</a>,</strong>.*?,.*?,.*?<.*?>(.*?)</a></dt>\s*<dd>(.*?)<",f)
    prof_info_alt3= re.findall("<dt><strong></strong><a href=\"(.*?)\">.*?\. (.*?)</a>,.*?,.*?,.*?<.*?>(.*?)</a></dt>\s*<dd>(.*?)<",f)
    prof_info_alt4= re.findall("<dt><a href=\"(.*?)\"><strong>.*?\. (.*?)</strong></a>,.*?,.*?,.*?<.*?>(.*?)</a>\s*<strong>\(On Leave\)</strong></dt>\s*<dd>(.*?)<",f)
    prof_info_alt5= re.findall("<dt><strong><a href=\"(.*?)\">.*?\.(.*?)</a></strong>.*?,.*?,.*?<.*?>(.*?)</a>\s*<strong>\(On Leave\)</strong></dt>\s*<dd>(.*?)<",f)
    prof_info_alt6= re.findall("<dt><strong><a href=\"(.*?)\">.*?\. (.*?)</a></strong>,\s*.*?,\s*.*?,\s*.*?\s*<.*?>(.*?)</a></dt>\s*<dd>(.*?)<",f)
    for prof in prof_info:
        all_prof_info.append(prof)
    for prof in prof_info_alt:
        all_prof_info.append(prof)
    for prof in prof_info_alt2:
        all_prof_info.append(prof)
    for prof in prof_info_alt3:
        all_prof_info.append(prof)
    for prof in prof_info_alt4:
        all_prof_info.append(prof)
    for prof in prof_info_alt5:
        all_prof_info.append(prof)
    for prof in prof_info_alt6:
        all_prof_info.append(prof)
print len(all_prof_info)
    
    
prof_dictionary_list=[]
for prof in all_prof_info:
    prof_dictionary={}
    prof_dictionary['name']=prof[1]
    prof_dictionary['website']=prof[0]
    prof_dictionary['email']=prof[2]
    prof_dictionary['researh_blurb']=prof[3]
    prof_dictionary_list.append(prof_dictionary)
print prof_dictionary_list
#f = file('/home/rambhask/course1prof.html').read()
#f=f.strip("\n")
#prof_info=re.findall("<dt><a href=\"(.*?)\"><strong>Prof\. (.*?)</strong></a>,.*?,.*?,.*?<.*?>(.*?)</a>\s*</dt>\s*<dd>(.*?)<", f)
#prof_info_alt= re.findall("<dt><strong><a href=\"(.*?)\">.*?\. (.*?)</a></strong>,(.*?),(.*?),.*?<.*?>(.*?)</a></dt>\s*<dd>(.*?)<",f)

#for prof in all_prof_info:
   # print prof[1]
import pdb; pdb.set_trace()
