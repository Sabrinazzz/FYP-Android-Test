from dis import show_code
from errno import EALREADY
from turtle import color, settiltangle, update
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
from plyer import notification
from plyer.utils import platform
from kivy.clock import Clock
from datetime import datetime
from time import strftime, time
import random



#--------------------------------   Global Variables-----------------------------------------------------------------------------

df = pd.read_csv("sample.csv")

time_list = df.iloc[0]["Time List"]
survey_number = df.iloc[0]["Survey Number"]
day_number = df.iloc[0]["Day Number"]
earliest_survey_time = df.iloc[0]["Earliest Survey Time"]
latest_survey_time = df.iloc[0]["Latest Survey Time"]
snooze_counter = df.iloc[0]["Snooze Counter"]


class SettingsScreen(Screen):
    #earliest_var = ObjectProperty(None)
    #latest_var = ObjectProperty(None)
    global earliest_survey_time
    global latest_survey_time
    
    def __init__(self):
    	self.earliest_var = earliest_survey_time
    	self.latest_var = latest_survey_time
    	
    def submitButton(self):
        
        self.earliest_time = str(self.earliest_var.text)
        self.latest_time = str(self.latest_var.text)
        print("Now: ",self.earliest_time,self.latest_time)
        return self.earliest_time, self.latest_time
     

class MainMenuScreen(Screen):
    pass
        
class SurveyScreen(Screen):
    def toSurvey(self):
        import webbrowser
        webbrowser.open('https://forms.gle/e4di6af')

class AltSurveyScreen(Screen):
    pass
    
class FeedbackScreen(Screen):
    pass

class InformationScreen(Screen):
    pass

class OnboardSurveyScreen(Screen):
    pass 
    
class DisplayScreenManager(ScreenManager):
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
    #time_list =[] ######## !MAKEPERSISTENT
    #surevy_taken = False
    #survey_number = 0 ######## !MAKEPERSISTENT
    times_generated = True
    #day_number = 0 ######## !MAKEPERSISTENT
    global time_list
    global survey_number
    global day_number
    
    def __init__(self):
    	self.time_list = time_list
    	self.survey_number = survey_number
    	self.day_number = day_number

    def __build__(self):

        return sm
       # return SettingsScreen

    def on_start(self):
        print("Survey Number on start: ",self.survey_number)
        self.showTime(1)
        self.updateTime(1)
        self.setTargetTime(self.time_list)
        self.checkNotification(1)
        self.conituousylyCheck(1)
        #print("Survey Number on start: ",self.survey_number)
        return super().on_start()

    def processVariables (self):
        text = self.root.ids.Earliest.text
        print(text)
        return text

# --------------- Settings screen functions -------------------------------#

    def submitButton(self):
        self.earliest_value = self.processVariables()
        print(self.earliest_value)


# ------------- Main Menu Screen Functions ------------------------

    clock_var = ObjectProperty(None)
    
    def showTime(self,tick):
            #time_var = datetime.now().strftime("%H:%M:%S")
            time_var = datetime.now().strftime("%H:%M:%S")
            #print(time_var)
            return time_var
            

    def updateTime(self, tick):
        Clock.schedule_interval(self.showTime,1)

        
    def notify(self, title, message):
        title = title
        message = message
        kwargs = {'title': title, 'message': message}

        notification.notify(**kwargs)
    
    def setTargetTime(self,update_list):
        
        for i in range(6):
            hour = random.randint(10,20)
            minute = random.randint(0,59)
            
            if len(str(minute)) ==2: 
                time_value = str(hour)+":"+str(minute)+":00"
            else: 
                time_value = str(hour)+":0"+str(minute)+":00" # this makes sure that the time is written to the list correctly as "10:01" and not "10:1"
            update_list.append(time_value)
            update_list.sort()
        
         
        print(update_list)
        return update_list



    def updateDayVar(self,tick):
        self.day_number += 1 ######## !MAKEPERSISTENT
        return self.day_number ######## !MAKEPERSISTENT


    def surveyTaken(self):
        #  !TODO find a way to stop this happening during the weekend

        if self.day_number == 5 or self.day_number == 6: ######## !MAKEPERSISTENT
            Clock.schedule_once(self.updateDayVar(1),10)
            print("Time based Day number: ",self.day_number)
        else: 
            if self.survey_number < 5: ######## !MAKEPERSISTENT
                self.survey_number += 1 ######## !MAKEPERSISTENT
                print("Survey Number: ", self.survey_number)
            else: 
                self.survey_number = 0 ######## !MAKEPERSISTENT
                self.day_number += 1 ######## !MAKEPERSISTENT
                print("Day: ", self.day_number)
                self.time_list = []
                self.setTargetTime(self.time_list)
           
        
            #print("Error: List index out of range")

        
    

    def checkNotification(self,tick):
        #!TODO the app notification probelm could be solved with the schedule function to schedule notification in the future(maybe)
        
        time = self.showTime(1)
        if time == self.time_list[self.survey_number]:
            self.notify("Hello World!","It's Survey Time")
            

    def conituousylyCheck(self,tick):
        Clock.schedule_interval(self.checkNotification,1)

    def snooze(self):
        #print("Survey number: ",self.survey_number)
        #time_value = self.time_list[self.survey_number]
        #time_value_list = time_value.split(":")
        #print (time_value_list)
        # this way it takes the time value from the list
        time = self.showTime(1)
        time_values = time.split(":")
        
        hour_value = int(time_values[0])
        minute_value = int(time_values[1])
        if minute_value >= 55 and minute_value <= 59 :
            new_minute_value = minute_value - 55
            new_hour_value = hour_value +1
            new_time_value = str(new_hour_value)+":0"+str(new_minute_value)+":00"

        else: 
            new_minute_value = minute_value + 5
            new_time_value = str(hour_value)+":"+str(new_minute_value)+":00"
        print(self.time_list)
        self.time_list[self.survey_number] = new_time_value
        print(self.time_list)
        
        

    # ------------------------ Surveys -----------------------------------

    def toSurvey(self, survey_link):
        import webbrowser
        webbrowser.open(survey_link)
        


if __name__ == "__main__":
    Menu().run()
