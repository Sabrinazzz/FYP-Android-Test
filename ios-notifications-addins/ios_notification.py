from pyobjus import *
from pyobjus.dylib_manager import make_dylib, load_dylib, load_framework, INCLUDE
import random

class IOSNotification:

    def __init__(self):
        self.notification_worker = autoclass("NotificationWorker").alloc().init()
    
    # schedule a notification for a specific date/time
    def notify_ios_date(self, title, message, id="bb-test", date=str, time=str, repeat=False):
        NSString = autoclass("NSString")
        n_title = NSString.alloc().initWithUTF8String_(title) 
        n_message = NSString.alloc().initWithUTF8String_(message)
        n_date = NSString.alloc().initWithUTF8String_(date) 
        n_time = NSString.alloc().initWithUTF8String_(time) 
        n_id = NSString.alloc().initWithUTF8String_(id)
        n_repeat = repeat
        self.notification_worker.requestNotificationCenter_withbody_withdate_withtime_withid_withrepeat_(n_title, n_message, n_date, n_time, n_id, n_repeat)
 
    # schedule a notification after a certain amount of seconds have elapsed.
    def notify_ios_seconds(self, title, message, id="bb-test", delay=0, repeat=False):
        '''
        @notify_ios_seconds:
            @params:
            title (str): the title to display
            message (str): the message to display
            id (str): unique id for the notification. Notifications with unique ids will display multiple times. Same ids will override original ones.
            delay (int): time in seconds to delay the notification. If straight away, set to 0. Automatically 0.
            repeat (boolean): set to True if needs to repeat, False otherwise. Automatically False.
            returns: None
        '''
        NSString = autoclass("NSString")
        n_title = NSString.alloc().initWithUTF8String_(title) 
        n_message = NSString.alloc().initWithUTF8String_(message)
        n_time = delay
        n_id = NSString.alloc().initWithUTF8String_(id)
        n_repeat = repeat
        self.notification_worker.requestNotificationCenter_withbody_withtiming_withid_withrepeat_(n_title, n_message, n_time, n_id, n_repeat)
    