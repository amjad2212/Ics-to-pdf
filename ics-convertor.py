import sys
import os.path
import shutil
from datetime import datetime
from icalendar import Calendar, Event
from reportlab.pdfgen.canvas import Canvas
from textwrap import wrap



class CalendarEvent:
    """Calendar event class"""
    summary = ''
    description = ''
    location = ''
    start = ''
    end = ''

    def __init__(self, name):
        self.name = name

events = []
export_path = "ICStoPDF_Result"
if __name__ == "__main__":

    if os.path.isdir(export_path):
        shutil.rmtree(export_path)
    os.mkdir(export_path)

    if len(sys.argv) < 1:
        print("Usage: python3 %s <folder of the ics files>" % sys.argv[0])
        sys.exit()
    else: 
        folder_path = sys.argv[1] 

    folder= os.listdir(folder_path)
    for filename in folder:
        file_extension = filename[-3:]
        if os.path.isfile(folder_path + filename):
            if file_extension == 'ics':
                print("processing \n file :", filename)
                f = open(folder_path + filename, 'rb')
                gcal = Calendar.from_ical(f.read())
                for component in gcal.walk():
                    event = CalendarEvent("event")
                    if component.get('SUMMARY') != None: 
                        event.summary = component.get('SUMMARY')
                    if component.get('DESCRIPTION') != None:
                        event.description = component.get('DESCRIPTION')
                    if component.get('LOCATION') != None:
                        event.location = component.get('LOCATION')
                    if hasattr(component.get('dtstart'), 'dt'):
                        event.start = component.get('dtstart').dt
                    if hasattr(component.get('dtend'), 'dt'):
                        event.end = component.get('dtend').dt
                    events.append(event)
                f.close()

                desc = str(event.description)
                desc_list = desc.split("\n")
                canvas = Canvas(export_path + "/"+filename.split(".")[0]+".pdf",pagesize=(595.0, 842.0))
                canvas.setFont("Helvetica-Bold",12)

                canvas.drawString(20, 800,"Summary: ")
                canvas.drawString(20, 780,"location: ")
                canvas.drawString(20, 760,"Start: ")
                canvas.drawString(20, 740,"End: ")
                canvas.drawString(20, 720,"Description: ")

                canvas.setFont("Helvetica",12)

                canvas.drawString(90, 800, event.summary)
                canvas.drawString(90, 780, event.location)
                canvas.drawString(90, 760, event.start.strftime("%a %e %b %H:%M:%S %Y %Z"))
                canvas.drawString(90, 740, event.end.strftime("%a %e %b %H:%M:%S %Y %Z"))
                n = 10
                for i in desc_list:
                    if(len(i)>30):
                        i=wrap(i,90)
                        for j in i:
                            canvas.drawString(60, 700 - n, j)
                            n+=15
                    else:
                        canvas.drawString(60, 700 - n, i)
                        n+=10


                canvas.save() 
                print(filename+".pdf"," Done", "\n") 

            else:
                print("You entered ", filename, ". ")
                print(file_extension.upper(), " is not a valid file format. Looking for an ICS file.")
                exit(0)
        else:
            exit(0)
    print("_________________________")        
    print(len(folder)," files are converted") 
    print("_________________________")    
