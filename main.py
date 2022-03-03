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
from plyer import notification
from plyer.utils import platform
from kivy.clock import Clock
from datetime import datetime
from time import strftime, time
import random
from kivy.core.window import Window
from os.path import join,dirname, realpath
from functools import partial




#--------------------------------   Global Variables-----------------------------------------------------------------------------

import csv
with open('sample.csv','rt')as f:
  data = csv.reader(f)
  for row in data:
        print(row)
time_list_val = int(row[0])
survey_number_val = int(row[1])
day_number_val = int(row[2])
earliest_survey_time_val = int(row[3])
latest_survey_time_val = int(row[4])
snooze_counter_val = int(row[5])

interval_1 = random.randint(60 * 60, 200 * 60)
interval_2 = random.randint(60 * 60, 300 * 60)
interval_3 = random.randint(60 * 60, 400 * 60)
interval_4 = random.randint(60 * 60, 500 * 60)
interval_5 = random.randint(60 * 60, 600 * 60)
interval_6 = 86400 - (interval_1 + interval_2 + interval_3 + interval_4 + interval_5)
interval_list = [interval_1, interval_2, interval_3, interval_4, interval_5, interval_6]
interval_index = 0


class SettingsScreen(Screen):
    earliest_var = ObjectProperty(None)
    latest_var = ObjectProperty(None)

    def submitUpdate(self, earliest, latest):
        print("Submit update before update")
        # self.ids.earliest_label.text = str(Menu.earliest_survey_time)
        # self.ids.latest_label.text = str(Menu.latest_survey_time)
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
sm.add_widget(OnboardSurveyScreen(name='onboardSurveyScreen'))
sm.add_widget(AltSurveyScreen(name='altSurveyScreen'))


class Menu(App):
    time_list = []
    # surevy_taken = False
    global survey_number_val
    global day_number_val
    global earliest_survey_time_val
    global latest_survey_time_val
    global snooze_counter_val

    survey_number = survey_number_val
    times_generated = True
    day_number = day_number_val
    earliest_survey_time = earliest_survey_time_val  # default values so that index for random numbers is not out of range
    latest_survey_time = latest_survey_time_val
    snooze_counter = snooze_counter_val
    time_changed = False  # flag to determine when the time preference has been changed

    # -------------------------------------------------------- Main app functions -------------------------------------------------------------

    def __build__(self):

        # Window.bind(on_keyboards=self.Android_backclick)

        '''if platform == 'android':
            import android
            android.map_key(android.KEYCODE_BACK,1001)


        elif platform == 'ios':
            from pyobjus import autoclass,obj_dict
            Clock.schedule_once(self.finish_ios_init)

        Window.bind(on_keyboard = self.back_key_handler)'''

        return sm

    # return SettingsScreen

    def back_key_handler(self, window, kcode1, kcode2, text, modifiers):
        if kcode1 == 27 or kcode1 == 1001:
            self.sm.current = 'mainmenuscreen'
            return True
        else:
            return False

    def on_start(self):
        print("Survey Number on start: ", self.survey_number)
        self.showTime(60)
        self.updateTime(60)
        self.setTargetTime(self.time_list)
        # self.checkNotification(60)
        self.continuousylyCheck(60)
        # print("Survey Number on start: ",self.survey_number)
        return super().on_start()

    def android_back_button(self, window, key, *largs):
        if key == 27:
            self.sm.current = "mainMenuScreen"

    def on_pause(self):
        # put persistance here?
        return True

    def on_resume(self):
        # could reassign vairables by reading from the persistance file here.
        pass

    # ------------------------- time based functions---------------------------------------------------------------------------------------

    def showTime(self, tick):

        second_time_var = datetime.now().strftime("%H:%M:%S")
        time_var = datetime.now().strftime("%H:%M")
        print("show time ran at ", second_time_var)
        return time_var
        # !TODO try boolean to check if time matches and notification sent

    def updateTime(self, tick):
        Clock.schedule_interval(self.showTime, 60)
        print("updateTime ran at")

    # --------------------------------- scheduling functions -----------------------------------------------------------------------------------------------------------

    def checkNotification(self, tick):
        global interval_index
        print("checkNotification started running")
        time_val = self.showTime(60)  # access current time value in hour:minute:second format
        if self.day_number in range(3, 6):  # is Thurday to Saturday: skips to next day without survey being taken
            print("Its the weekend")
            if time_val == self.time_list[0]:
                self.survey_number = 0
                self.day_number += 1
                self.snooze_counter = 0
                print("updated Day: ", self.day_number)
                self.surveyTaken()
        elif self.day_number == 6:  # if Sunday: skips to next day without survey being taken and reconfiguring a new time list
            print("It#s sunday")
            if time_val == self.time_list[0]:
                self.survey_number = 0
                self.day_number += 1
                self.snooze_counter = 0
                self.time_list = []
                print("updated Day: ", self.day_number)
                self.setTargetTime(self.time_list)  # triggers setting time list for Monday


        elif self.day_number < 10:
            print("Survey number: ", self.survey_number)
            print("List: ", self.time_list)
            if time_val == self.time_list[self.survey_number]:  # any other day where surveys are triggeres normally
                interval_val = interval_list[interval_index]
                interval_index += 1
                time.sleep(interval_val)
                if (interval_index >= len(interval_list)):
                    interval_index = 0
                    interval_1 = random.randint(60 * 60, 200 * 60)
                    interval_2 = random.randint(60 * 60, 300 * 60)
                    interval_3 = random.randint(60 * 60, 400 * 60)
                    interval_4 = random.randint(60 * 60, 500 * 60)
                    interval_5 = random.randint(60 * 60, 600 * 60)
                    interval_6 = 86400 - (interval_1 + interval_2 + interval_3 + interval_4 + interval_5)
                    interval_list = [interval_1, interval_2, interval_3, interval_4, interval_5, interval_6]

                self.notify("Hello World!", "It's Survey Time", True)  # triggers notification
        print("checknotification ran")

    def continuousylyCheck(self,
                           tick):  # calls previous function once per second --> checks for match between current time and value in time list
        Clock.schedule_interval(self.checkNotification, 60)
        print("comtinuously ceck ran")

    # ---------------------------------------------------- setting functions ----------------------------------------------------------------------------------------------

    def setTargetTime(self, update_list):

        if len(update_list) == 0:

            for i in range(6):
                hour = random.randint(int(self.earliest_survey_time),
                                      int(self.latest_survey_time) - 1)  # random hour value between 10 am and 8 pm, hardcoded for now
                minute = random.randint(0, 10)  # random minute value  between 0 and 59
                # hour = 12
                if len(str(minute)) == 2:
                    # time_value = str(hour)+":"+str(minute)+":00"
                    time_value = str(hour) + ":" + str(minute)
                else:
                    # time_value = str(hour)+":0"+str(minute)+":00" # this makes sure that the time is written to the list correctly as "10:01" and not "10:1"
                    time_value = str(hour) + ":0" + str(
                        minute)  # this makes sure that the time is written to the list correctly as "10:01" and not "10:1"
                update_list.append(time_value)  # creates list of the values that have been created
                update_list.sort()  # sorts the list to make sure that they are sorted by time value --> to trigger notifications porperly

        print(update_list)
        return update_list

    # --------------------------------------------------------------button triggered functions -----------------------------------

    def submitButton(self, earliest, latest):
        print("Earliest before update: ", earliest.text, "Latest: ", latest.text)
        if earliest.text != "":
            self.earliest_survey_time = earliest.text
        if latest.text != "":
            self.latest_survey_time = latest.text

        print("Earliest: ", self.earliest_survey_time, "Latest: ", self.latest_survey_time)
        self.time_list = []
        return self.earliest_survey_time, self.latest_survey_time

    def surveyTaken(self):
        # this is triggered when the Survey button is clicked
        # what it does:
        # - updates survey number vairable which is used to determine which time to use to trigger the next survey
        # - when all 6 surveys of the day are completed, in increases the day variable
        # - that tracks which day it is
        # if it's the pause (day 3 to 6) then no survey is triggered and at midnight, the day variable is increased

        if self.survey_number < 5:  # update survey number until all 6 are complete
            self.survey_number += 1
            print("Survey Number: ", self.survey_number)  # for testing
        else:
            self.survey_number = 0  # reset survey number for next day (survey number used to access correct time value)
            self.day_number += 1  # increase day by 1 to keep track of which day of study we're on
            self.snooze_counter = 0  # reset snooze counter at new day
            print("Day: ", self.day_number)
            if self.day_number in range(3, 7):  # Day: thursday to saturday, no surveys should be triggered
                self.survey_number = 0  # reset survey number variable
                print("offday survey number: ", self.survey_number)
                self.time_list = []
                self.time_list.append(
                    time_list_val)  # when this time comes, the check update function will update the day variable instead of triggering a survey, see line 185

                print(self.time_list)

            else:
                print("Day reset to survey day")
                self.time_list = []  # reset time list
                self.setTargetTime(self.time_list)  # creating new time list for the next da

    def snooze(self):
        # print("Survey number: ",self.survey_number)
        # time_value = self.time_list[self.survey_number]
        # time_value_list = time_value.split(":")
        # print (time_value_list)
        # this way it takes the time value from the list
        # the way below adds 5 minutes to current time (because user won't always snooze exactly when notification is given)

        if self.snooze_counter == 3:
            self.survey_number += 1
            self.snooze_counter = 0
            print("3 times snoozed")
            print("new survey number: ", self.survey_number)
        else:
            self.snooze_counter += 1
            time_val = self.showTime(1)
            time_values = time.split(":")

            hour_value = int(time_values[0])
            minute_value = int(time_values[1])
            if minute_value >= 55 and minute_value <= 59:
                new_minute_value = minute_value - 55
                new_hour_value = hour_value + 1
                new_time_value = str(new_hour_value) + ":0" + str(new_minute_value) + ":00"

            else:
                new_minute_value = minute_value + 5
                if len(str(new_minute_value)) == 2:
                    # new_time_value = str(hour_value)+":"+str(new_minute_value)+":00" including second value
                    new_time_value = str(hour_value) + ":" + str(new_minute_value)
                else:
                    # new_time_value = str(hour_value)+":0"+str(new_minute_value)+":00"
                    new_time_value = str(hour_value) + ":0" + str(new_minute_value)

            self.time_list[self.survey_number] = new_time_value
            print("Snoozed list: ",
                  self.time_list)  # updates time list with new value when the next notification will be sent

    def notify(self, title, message, toast):
        title = title
        message = message
        ticker = "This is the ticker message"
        app_name = "Menu"
        # app_icon = "kivy.png"
        toast = toast

        kwargs = {'title': title, 'message': message, 'ticker': ticker, 'app_name': app_name, 'toast': toast}
        notification.notify(**kwargs)

    def testnotify(self, tick):
        title = "hi"
        message = "It#s been 5 seconds"
        toast = True
        ticker = "This is the ticker message"
        app_name = "Menu"

        kwargs = {'title': title, 'message': message, 'ticker': ticker, 'app_name': app_name, 'toast': toast}
        notification.notify(**kwargs)

    def schedulenotify(self, tick):
        Clock.schedule_once(self.testnotify, 5)

    def feedbacknotification(self, title, toast):
        title = title
        snooze_time = self.time_list[self.survey_number]
        display_message = "You have snoozed the current Survey. The next reminder will be sent at " + snooze_time + " ,O'clock"
        kwargs = {'title': title, 'message': display_message}

        notification.notify(**kwargs)
        print(display_message)

    # ------------------------ Surveys -----------------------------------

    def toSurvey(self, survey_link, end_of_day_survey):
        # !TODO need to add end of day Survey

        import webbrowser
        if self.survey_number != 5:
            webbrowser.open(survey_link)
        else:
            webbrowser.open(end_of_day_survey)


if __name__ == "__main__":
    Menu().run()
