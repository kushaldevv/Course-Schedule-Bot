import urllib.request, json
from bs4 import BeautifulSoup
import requests

def exists(data, target):
    if target not in data or len(data[target]) == 0:
        return False
    return True
def validSection(course_name, sec):
    try:
    #change termId to year+08 for fall, year+12 for winter, year+01 for spring, year+05 for summer
        url = "https://app.testudo.umd.edu/soc/search?courseId=" + course_name + "&sectionId=" + sec + "&termId=202208&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        open_seats = int(soup.find_all('span', class_='open-seats-count')[0].text)
        if open_seats > 0:
          return [True, "has open seats"]
        return [True, "no seats"]
    except:
        return [False, "Invalid"]
# def validSection(course_name, course_section):
#     try:
#         with urllib.request.urlopen("https://api.umd.io/v1/courses/" + course_name + "/sections/" + course_section) as url:
#             data = json.loads(url.read().decode())
#             if int(data[0]['open_seats']) > 0:
#                 return [True, "Has open seats"]
#             return [True, "no seats"]
#     except:
#         return [False, "invalid"]

def sections(course):
    out = []
    try:
        with urllib.request.urlopen("https://api.umd.io/v1/courses/" + course + "/sections") as url:
            data = json.loads(url.read().decode())
            for i in range(len(data)):
                section_id = '***' + data[i]['section_id'] + '*** with '
                prof = 'TBA\n' if not exists(data[i], 'instructors') else data[i]['instructors'][0] + '\n'
                total_seats = "" if not exists(data[i], 'seats') else 'total seats:' + data[i]['seats']
                open_seats = "" if not exists(data[i], 'open_seats') else 'open seats: ' + data[i]['open_seats']
                wait_list = "" if not exists(data[i], 'waitlist') else 'waitlist: ' + data[i]['waitlist']
                l_time = " " if not exists(data[i]['meetings'][0], 'start_time') else (", " + data[i]['meetings'][0]['start_time']
                    + '-' + data[i]['meetings'][0]['end_time'])
                l_days = " " if not exists(data[i]['meetings'][0], 'days') else ", " + data[i]['meetings'][0]['days']
                d_building, d_time, d_days = "", "", ""
                if data[i]['meetings'][0]['room'] == "ONLINE":
                    l_building = 'ONLINE '
                else:
                    l_building = "" if not exists(data[i]['meetings'][0], 'building') else data[i]['meetings'][0]['building']
                if len(data[i]['meetings']) > 1 and data[i]['meetings'][1]['room'] == "ONLINE":
                    d_building = 'Discussion: ONLINE'
                elif len(data[i]['meetings']) > 1:
                    d_building = "\nDiscussion: " if not exists(data[i]['meetings'][1], 'building') else "\nDiscussion: " + data[i]['meetings'][1]['building']
                    d_time = " " if not exists(data[i]['meetings'][1], 'start_time') else (", " + data[i]['meetings'][1]['start_time']
                        + '-' + data[i]['meetings'][1]['end_time'])
                    d_days = " " if not exists(data[i]['meetings'][1], 'days') else ", " + data[i]['meetings'][1]['days']
                info = "Lecture: " + l_building + l_days + l_time + d_building + d_days + d_time
                out.append(section_id + prof + info + '\n' + total_seats + ', ' + open_seats + ', ' + wait_list + '\n\n')
    except:
        return ["Invalid course/not in this shitty api"]
    return out
