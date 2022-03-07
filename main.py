#from errno import EALREADY
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from plyer import notification
from plyer.utils import platform
from kivy.clock import Clock
from datetime import datetime, date
from time import strftime, time
import random, string
from kivy.core.window import Window
from os.path import join,dirname, realpath
from functools import partial
import csv

# LAURA: if platform is iOS
if platform == 'ios': 
    from ios_notification import IOSNotification
    from os.path import join

with open('sample.csv','rt')as f:
  data = csv.reader(f)
  for row in data:
        pass

#--------------------------------   Global Variables-----------------------------------------------------------------------------



class SettingsScreen(Screen):

    earliest_var = ObjectProperty(None)
    latest_var = ObjectProperty(None)
   
    
    def submitUpdate(self, earliest, latest):
        print("Submit update before update")
        #self.ids.earliest_label.text = str(Menu.earliest_survey_time)
        #self.ids.latest_label.text = str(Menu.latest_survey_time)
        self.ids.earliest_label.text = earliest.text
        self.ids.latest_label.text = latest.text

        self.ids.Earliest.text = ""
        self.ids.Latest.text = ""
        print("Submit Update ran")
     

class MainMenuScreen(Screen):
    pass
        
class SurveyScreen(Screen):
  pass

class AltSurveyScreen(Screen):
    def update_survey_numbers(self):

        if int(self.ids.surveys_completed.text)  < 6: 
            self.ids.surveys_completed.text = str(int(self.ids.surveys_completed.text)+1)
            print("Updated: ", str(int(self.ids.surveys_completed.text)-1))
            self.ids.surveys_left.text = str(int(self.ids.surveys_left.text)-1)
    
class FeedbackScreen(Screen):
    pass

class InformationScreen(Screen):
    pass

class OnboardSurveyScreen(Screen):
    pass 
    
class DisplayScreenManager(ScreenManager):
    pass

class MyPopUp(Screen): # class for popup window
    pass

class SnoozePopUp(Screen):
    pass

sm = ScreenManager()
sm.add_widget(MainMenuScreen(name='mainMenuScreen'))
sm.add_widget(SettingsScreen(name='settingsScreen'))
sm.add_widget(SurveyScreen(name='surveyScreen'))
sm.add_widget(FeedbackScreen(name='feedbackScreen'))
sm.add_widget(InformationScreen(name='informationScreen'))
sm.add_widget(OnboardSurveyScreen(name= 'onboardSurveyScreen'))
sm.add_widget(AltSurveyScreen(name='altSurveyScreen'))


class Menu(App):
    time_list =[]
    #surevy_taken = False
    survey_number = int(row[0])
    times_generated = True
    day_number = int(row[1])
    earliest_survey_time = int(row[2]) # default values so that index for random numbers is not out of range
    latest_survey_time = int(row[3])
    snooze_counter = int(row[4])
    last_time_checked = 0
    time_changed = False # flag to determine when the time preference has been changed
    notification_times_list = []
    
# -------------------------------------------------------- Main app functions -------------------------------------------------------------

    # LAURA: added an init function to get the values for persistence. This can be moved to the 
    def __init__(self):
        super(Menu, self).__init__()
        self.time = self.showTime(60) # getting time on init
        if platform == "ios":
            self.__filename = join(App.get_running_app().user_data_dir, "sample.csv")
            print("user directory at: ", self.__filename)
        

            # ---------- LAURA: getting persisted values on start 
            persisted_rows = self.get_persistence() # ["Time List","Survey Number","Day Number","Earliest Survey Time","Latest Survey Time","Snooze Counter"]
            print("persisted rows returned:", persisted_rows)
            if persisted_rows != []:
                self.survey_number = int(persisted_rows[0])
                self.day_number = int(persisted_rows[1])
                self.earliest_survey_time = int(persisted_rows[2])
                self.latest_survey_time = int(persisted_rows[3])
                self.snooze_counter = int(persisted_rows[4])
                if len(self.time_list) != 6:
                    self.time_list = [0] * 6 
                for i in range(5,11):
                    self.time_list[i-5] = persisted_rows[i]
                self.last_time_checked = persisted_rows[11]
            print("values received on start: ", self.survey_number, self.day_number, self.earliest_survey_time, self.latest_survey_time, self.snooze_counter, self.time_list)
            # ----------- END PERSISTENCE
        

        

    def __build__(self):

        return sm
       # return SettingsScreen

    
    
  #  def build(self):
  #      self.__today = str(datetime.today().strftime('%d-%m-%Y'))
  #      print("App build", self.__today)
        



    def on_start(self):

        self.__ids = self.generate_unique_ids()
        print("survey ids: ", self.__ids)
        self.test_updated_list = ["17:37", "17:39", "17:40", "17:42", "17:44", "17:46"]
        self.set_dates()
        self.__survey_day = self.date_list[self.day_number]
        # LAURA ADDED: set-up iOS notification center
        if platform == "ios": # if the user is in iOS, trigger user to allow notifications
            self.ios_notification_center = IOSNotification()
            self.ios_notification_center.remove_pending_notifications()
        print("Survey Number on start: ",self.survey_number)
        self.showTime(60)
        self.updateTime(60)
        if len(self.time_list) != 6: # LAURA: only set these on start if there were none from persistence
            self.setTargetTime(self.time_list,self.__survey_day,self.notification_times_list)
        self.last_time_checked = self.showTime(60)
        
        #self.checkNotification(60)
        self.continuousylyCheck(60)
        #print("Survey Number on start: ",self.survey_number)
        
        return super().on_start()
        

    def set_dates(self):
        self.date_list = []
        self.day = int(datetime.now().strftime("%d"))
        self.month_year = datetime.now().strftime("-%m-%Y")
        i = 0
        while i < 3:
            if self.day < 10:
                self.date_list.append(("0"+str(self.day+i)+self.month_year))
            else:
                self.date_list.append((str(self.day+i)+self.month_year))
            self.date_list.append((str(self.day+i+7)+self.month_year))
            i += 1
        self.date_list.sort()
        
        print(self.date_list)
    
    # LAURA: This method generates a list of unique IDs for each survey notification
    def generate_unique_ids(self):
        return [''.join("survey%d" % i) for i in range(1,7)]

        #return [''.join([random.choice(string.ascii_letters + string.digits) for n in range(20)]) for n in range(6)]
        

    def android_back_button(self, window, key,*largs): 
        if key == 27: 
            self.sm.current="mainMenuScreen"

    def on_pause(self):
        # put persistance here? 

        self.last_time_checked = self.showTime(60)
        if platform == "ios":
            user_data_dir = App.get_running_app().user_data_dir
            filename = join(user_data_dir, "sample.csv")
            try:
                with open(filename, "w") as fd:
                    fd.write("Survey Number,Day Number,Earliest Survey Time,Latest Survey Time,Snooze Counter,Time_1,Time_2,Time_3,Time_4,Time_5,Time_6,last_time\n")
                    fd.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (self.survey_number, self.day_number, self.earliest_survey_time,self.latest_survey_time,self.snooze_counter,self.time_list[0],self.time_list[1],self.time_list[2],self.time_list[3],self.time_list[4],self.time_list[5],self.last_time_checked))
                print("Persistence stored!")
            except:
                print("could not write to file")
        return True

    def on_resume(self):
        # could reassign vairables by reading from the persistance file here. 
        persisted_rows = self.get_persistence() # ["Time List","Survey Number","Day Number","Earliest Survey Time","Latest Survey Time","Snooze Counter"]
        self.survey_number = int(persisted_rows[0])
        self.day_number = int(persisted_rows[1])
        self.earliest_survey_time = int(persisted_rows[2])
        self.latest_survey_time = int(persisted_rows[3])
        self.snooze_counter = int(persisted_rows[4])
        if len(self.time_list) != 6:
            self.time_list = [0] * 6 
        for i in range(5,11):
            self.time_list[i-5] = persisted_rows[i]
        self.last_time_checked = persisted_rows[11]

        print("values received on resume:\n survey number: %s\n, day number: %s\n, earliest time: %s\n, latest time: %s\n, snooze counter: %s\n, time list: %s\n, last time checked before pause: %s " % (self.survey_number, self.day_number, self.earliest_survey_time, self.latest_survey_time, self.snooze_counter, self.time_list, self.last_time_checked))
        
        
    def get_persistence(self):
        print("persistence read init!")
        contents = []
        try:
            with open(self.__filename,'rt')as f:
                data = csv.reader(f)
                for row in data:
                    contents = row
                    print("contents received:", contents)
            #return []
        except:
            print("no such file. Trying to create...")
            try:
                with open(self.__filename, "w") as fd:
                    fd.write("Time List,Survey Number,Day Number,Earliest Survey Time,Latest Survey Time,Snooze Counter\n")
                    fd.write("0,%s,%s,%s,%s,%s" % (self.survey_number, self.day_number, self.earliest_survey_time,self.latest_survey_time,self.snooze_counter))
                print("File created! From now, using existing values")
            except:
                print("could not write to file")
        return contents
   

#------------------------- time based functions---------------------------------------------------------------------------------------
    
    def showTime(self,tick):
            
            second_time_var = datetime.now().strftime("%H:%M:%S")
            time_var = datetime.now().strftime("%H:%M")
            print("show time ran at ", second_time_var)
            return time_var
            # !TODO try boolean to check if time matches and notification sent

    def updateTime(self, tick):
        Clock.schedule_interval(self.showTime,60)
        print("updateTime ran at")

#--------------------------------- scheduling functions -----------------------------------------------------------------------------------------------------------

    def checkNotification(self,tick):
        print("checkNotification started running") 
        self.time = self.showTime(60) # access current time value in hour:minute:second format
        
        print("time_list:", self.time_list[self.survey_number], "time: ", self.time)
        if self.day_number < len(self.date_list): 
            print("Survey number: ", self.survey_number)
            print("List: ", self.time_list)
            print("time_list:", self.time_list[self.survey_number], "time: ", self.time, "last time checked", self.last_time_checked)
            self.__today = str(datetime.today().strftime('%d-%m-%Y'))
            if self.__today == self.date_list[self.day_number] and (self.time >= self.time_list[self.survey_number] or self.time_list[self.survey_number] == self.last_time_checked): # any other day where surveys are triggeres normally
                '''this passes!  05-03-2022 05-03-2022 12:14 09:42 09:42'''
                print("this passes! ", self.__today, self.date_list[self.day_number], self.time, self.time_list[self.survey_number], self.last_time_checked)
                #self.notify("Hello World!","It's Survey Time",True)  # triggers notification
                self.show_notification_popup("Hello!", "It's time to take the survey!")
        print("checknotification ran")
            

    def continuousylyCheck(self,tick): # calls previous function once per second --> checks for match between current time and value in time list
        Clock.schedule_interval(self.checkNotification,60)
        print("comtinuously ceck ran")

#---------------------------------------------------- setting functions ----------------------------------------------------------------------------------------------


    def setTargetTime(self,update_list,date,notification_list):   

        
        notification_list= []
        for i in range(6): # create 6 lists to put into self.notification_times_lists
            update_list = [
            if str(self.earliest_survey_time) == datetime.now().strftime("%H"):
                 earliest_seconds = (int(self.earliest_survey_time) * 3600) + 3600
                 print("Earliest seconds: ",earliest_seconds//3600)
            else: 
                earliest_seconds = int(self.earliest_survey_time) * 3600
            latest_seconds = int(self.latest_survey_time) * 3600


            survey_time_range_seconds = latest_seconds - earliest_seconds
            #print("Survey time range: ", survey_time_range_seconds)
            max_interval_length = survey_time_range_seconds // 6
            #print("Max interval length: ", max_interval_length)
            min_interval_lenth = survey_time_range_seconds //8
            #print("Min interval length: ", min_interval_lenth)
            interval_1 = random.randint(min_interval_lenth,max_interval_length)
            interval_2 = random.randint(min_interval_lenth,max_interval_length)
            interval_3 = random.randint(min_interval_lenth,max_interval_length)
            interval_4 = random.randint(min_interval_lenth,max_interval_length)
            interval_5 = random.randint(min_interval_lenth,max_interval_length)
            interval_6 = random.randint(min_interval_lenth,max_interval_length)
            #interval_6 = survey_time_range_seconds - (interval_1 + interval_2 + interval_3 + interval_4 + interval_5)
            interval_list = [interval_1, interval_2, interval_3, interval_4, interval_5, interval_6]


            print(interval_list) 
            time_seconds_list = []
            # set first value depending on earliest value

            #time_seconds_list.append(earliest_seconds)   
            time_seconds_value = int(earliest_seconds) + interval_1
            time_seconds_list.append(time_seconds_value)
            new_hours_value = (time_seconds_value) // 3600
            new_minutes_value = ((time_seconds_value % 3600)//60)

            self.time_list = [] # LAURA: making sure that the original list is emptied first
            if new_hours_value < 10: 
                if new_minutes_value < 10:
                    update_list.append("0"+str(new_hours_value)+":0"+str(new_minutes_value))
                else: 
                    update_list.append("0"+str(new_hours_value)+":"+str(new_minutes_value))
            else: 
                if new_minutes_value < 10:
                    update_list.append(str(new_hours_value)+":0"+str(new_minutes_value))
                else: 
                    update_list.append(str(new_hours_value)+":"+str(new_minutes_value))


            # set rest of the values
            for i in range (5):
                new_seconds_value = time_seconds_list[i] + interval_list[i+1] 
                time_seconds_list.append(new_seconds_value)
                new_hours_value = (new_seconds_value) // 3600
                new_minutes_value = ((new_seconds_value % 3600)//60)
                if new_hours_value < 10: 
                    if new_minutes_value < 10:
                        update_list.append("0"+str(new_hours_value)+":0"+str(new_minutes_value))
                    else: 
                        update_list.append("0"+str(new_hours_value)+":"+str(new_minutes_value))
                else: 
                    if new_minutes_value < 10:
                        update_list.append(str(new_hours_value)+":0"+str(new_minutes_value))
                    else: 
                        update_list.append(str(new_hours_value)+":"+str(new_minutes_value))


            update_list.sort()


            print("Time seconds list: ",time_seconds_list)
            print("Time List: ", self.time_list)

            # set times on iOS
            if platform == "ios":
                print("id list: ", self.__ids)
                #test_updated_list = ["17:30", "17:32", "17:34", "17:35", "17:36", "17:37"]
               # self.time_list = test_updated_list
                print("----- TARGET DATE ----- ", date)
                for pos, time in enumerate(self.time_list):
                    # ---- line creates a randomly generated id. There is a change it will not be unique.
                    id = self.__ids[pos]
                    self.notify("Hello!", "It's time to take the survey!",id=id,date=date,time=time) # notify(self,title,message,toast,id=None,date=None,time=None):


            print(update_list) # prints singular list that was generated within 1 execition of the loop
            notification_list.append(update_list) # appends list into matrix
                
        print(notification_list)
        return notification_list

# --------------------------------------------------------------button triggered functions -----------------------------------
        
    def submitButton(self, earliest , latest):
        print("Earliest before update: ", earliest.text, "Latest: ", latest.text)
        if earliest.text != "":
            self.earliest_survey_time = int(earliest.text) 
        if latest.text != "":
            self.latest_survey_time = int(latest.text)

        print("Earliest: ", self.earliest_survey_time, "Latest: ", self.latest_survey_time)
        self.time_list = []
        self.setTargetTime(self.time_list, self.date_list[self.day_number],self.notification_times_list)
        return self.earliest_survey_time, self.latest_survey_time
       
        

    def surveyTaken(self):
        # this is triggered when the Survey button is clicked
        # what it does:
        # - updates survey number vairable which is used to determine which time to use to trigger the next survey
        # - when all 6 surveys of the day are completed, in increases the day variable
        # - that tracks which day it is
        # if it's the pause (day 3 to 6) then no survey is triggered and at midnight, the day variable is increased

        if datetime.now().strftime("%d/%m/%Y") == self.date_list[self.day_number]: # checks to see if today matches the current survey day
        
            if self.survey_number < 5: # update survey number until all 6 are complete
                self.survey_number += 1
                print("Survey Number: ", self.survey_number) # for testing
            else: 
                self.survey_number = 0 # reset survey number for next day (survey number used to access correct time value)
                if self.day_number < len(self.date_list) - 1: # Laura: ensuring day number does not go greater than the length of the list
                    self.day_number += 1 # increase day by 1 to keep track of which day of study we're on
                else: 
                    print("No more surveys to deliver :(")
                self.snooze_counter = 0 # reset snooze counter at new day
                print("Day: ", self.day_number)
                self.snooze_counter = 0 # reset snooze counter at new day
                self.__survey_day = self.date_list[self.day_number]
                
                print("Survey Day: ", self.__survey_day)
                self.time_list = [] # reset time list
                self.__ids = self.generate_unique_ids() # resetting the ids for the list
                #self.setTargetTime(self.time_list,self.__survey_day,self.notification_times_list) # creating new time list for the next da
                self.last_time_checked = self.showTime(60)
                print("Day: ", self.__survey_day,"New time list: ", self.time_list)

            return self.__survey_day,self.time_list
            # this returns what day it is (that is accessing the dat list using the day number as index)
                

        
            

    def snooze(self):
        #print("Survey number: ",self.survey_number)
        #time_value = self.time_list[self.survey_number]
        #time_value_list = time_value.split(":")
        #print (time_value_list)
        # this way it takes the time value from the list
        # the way below adds 5 minutes to current time (because user won't always snooze exactly when notification is given)

        can_snooze = True
        
        if self.snooze_counter == 3: 
            if self.survey_number < 5: 
                self.survey_number += 1
                self.snooze_counter = 0
                print("3 times snoozed")
                print("new survey number: ", self.survey_number)
                can_snooze = False
            elif self.survey_number == 5:
                self.survey_number = 0 
                self.day_number += 1
                self.snooze_counter = 0
                self.time_list = []
                print("snoozed day number: ", self.day_number)
                #self.time_list = []
                #self.setTargetTime(self.time_list)
                #print("newly generated times: ", self.time_list)
        else: 
            self.snooze_counter += 1
            time = self.showTime(1)
            time_values = time.split(":")
            
            hour_value = int(time_values[0])
            minute_value = int(time_values[1])
            if minute_value >= 55 and minute_value <= 59 : # LAURA: Noticed in this one that you are adding second values, which is not happening in the other ones :) # SABRINA: Resolved :)
                new_minute_value = minute_value - 55
                new_hour_value = hour_value +1
                new_time_value = str(new_hour_value)+":0"+str(new_minute_value)

            else: 
                new_minute_value = minute_value + 5
                if len(str(new_minute_value)) == 2:
                    #new_time_value = str(hour_value)+":"+str(new_minute_value)+":00" including second value
                    new_time_value = str(hour_value)+":"+str(new_minute_value)
                else:
                    #new_time_value = str(hour_value)+":0"+str(new_minute_value)+":00"
                    new_time_value = str(hour_value)+":0"+str(new_minute_value)
            #self.test_updated_list[self.survey_number] = new_time_value
            self.time_list[self.survey_number] = new_time_value
            print(self.__ids[self.survey_number],self.date_list[self.survey_number],self.time_list[self.survey_number])
            if platform == "ios":
                self.notify("Hello!", "It's time to take the survey!",id=self.__ids[self.survey_number],date=self.date_list[self.day_number],time=self.time_list[self.survey_number])
            
            print("Snoozed list: ",self.time_list) # updates time list with new value when the next notification will be sent
            return can_snooze


    def notify(self,title,message,toast=False,id=None,date=None,time=None):
        if platform == "android":
            title = title
            message = message
            app_name = "Menu"
            #app_icon = "kivy.png"
            toast = toast
            kwargs = {'title': title, 'message': message,'app_name': app_name, 'toast':toast }
            notification.notify(**kwargs)
        elif platform == "ios":
            #date = self.__today
           # time = "10:03"
           # id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
            self.ios_notification_center.notify_ios_date(title, message, id, date, time, repeat=False)
        
            


    def show_notification_popup(self,title, message):
        for widget in App.get_running_app().root_window.children:
            if isinstance(widget, Popup):
                widget.dismiss()
        self.popup_window = MyPopUp()
        self.popup_window.ids.popup_label.text = message
        #self.popup_window.auto_dismiss = False
        self.display = Popup(title=title, content=self.popup_window, size_hint=(None, None), size=(400, 400),auto_dismiss=False)
        self.display.open()
    
    def close_notification_popup(self):
        self.display.dismiss() 

    def show_snooze_popup(self):
        for widget in App.get_running_app().root_window.children:
            if isinstance(widget, Popup):
                widget.dismiss()
        can_snooze = self.snooze()
        snooze_popup = SnoozePopUp()
        if can_snooze:
            snooze_popup.ids.snooze_label.text = "Snoozed until %s" % self.time_list[self.survey_number]
        else:
            snooze_popup.ids.snooze_label.text = "Cannot snooze survey."
        self.snooze_display = Popup(title="Survey Snoozed", content=snooze_popup, size_hint=(None,None), size=(400,400),auto_dismiss=False)
        self.snooze_display.open()

    def close_snooze_popup(self):
        self.snooze_display.dismiss()

    

        




    def feedbacknotification(self, title, toast):
        title = title
        snooze_time = self.time_list[self.survey_number]
        display_message = "You have snoozed the current Survey. The next reminder will be sent at "+ snooze_time+ " ,O'clock"
        kwargs = {'title': title, 'message': display_message}

        notification.notify(**kwargs)
        print(display_message)

            
        

    # ------------------------ Surveys -----------------------------------

    def toSurvey(self, survey_link, end_of_day_survey):

        if datetime.now().strftime("%d/%m/%Y") == self.date_list[self.day_number]:
        
            import webbrowser
            if self.survey_number != 5:
                webbrowser.open(survey_link)
            else: 
                webbrowser.open(end_of_day_survey)
    


if __name__ == "__main__":
    Menu().run()
