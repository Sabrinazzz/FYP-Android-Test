#include <UserNotifications/UserNotifications.h>
#include <BackgroundTasks/BackgroundTasks.h>

// interface and implementation for NotificationWorker. Works! :)
@interface NotificationWorker : NSObject <UNUserNotificationCenterDelegate>
- (void)requestNotificationCenter:
        (NSString *)py_title
        withbody:(NSString *)py_body
        withtiming:(int)py_timing
        withid:(NSString *)py_uniqueid
        withrepeat:(bool)py_repeat;
- (void)requestNotificationCenter:(NSString *)py_title withbody:(NSString *)py_body withdate:(NSString *) py_date withtime:(NSString *)py_time withid:(NSString *)py_uniqueid withrepeat:(bool)py_repeat;
- (NSDate *)stringToDate:(NSString *)str_date with_time:(NSString *)str_time;
- (NSString *)to12Hour:(NSString *)str_time;
- (void)removePendingNotifications;

@end

@implementation NotificationWorker

UNUserNotificationCenter *center = nil;

// method for setting up the notification worker. Called on setup as this is where we get the permissions
- (id)init{
    center = [UNUserNotificationCenter currentNotificationCenter];
    UNAuthorizationOptions options = UNAuthorizationOptionAlert + UNAuthorizationOptionSound;

    [center requestAuthorizationWithOptions:options
     completionHandler:^(BOOL granted, NSError * _Nullable error) {
      if (!granted) {
        NSLog(@"Something went wrong");
      }
    }];
    return self;
}

//request a timed notification in seconds.
- (void)requestNotificationCenter:(NSString *)py_title withbody:(NSString *)py_body withtiming:(int)py_timing withid:(NSString *)py_uniqueid withrepeat:(bool)py_repeat{
    
    UNAuthorizationOptions options = UNAuthorizationOptionAlert + UNAuthorizationOptionSound;

    [center requestAuthorizationWithOptions:options
     completionHandler:^(BOOL granted, NSError * _Nullable error) {
      if (!granted) {
        NSLog(@"Something went wrong");
      }
    }];
      UNMutableNotificationContent *content = [UNMutableNotificationContent new];
      content.title = py_title;
      content.body = py_body;
      content.sound = [UNNotificationSound defaultSound];
    
    if (py_timing > 0) {

      UNTimeIntervalNotificationTrigger *trigger = [UNTimeIntervalNotificationTrigger
        triggerWithTimeInterval:py_timing repeats:py_repeat];

        NSString *identifier = py_uniqueid;
        UNNotificationRequest *request = [UNNotificationRequest requestWithIdentifier:identifier
          content:content trigger:trigger];
        
        [center addNotificationRequest:request withCompletionHandler:^(NSError * _Nullable error) {
          if (error != nil) {
            NSLog(@"Something went wrong: %@",error);
          }
          else {
              printf("Notification send complete.");
          }
        }];
    } else {
        NSString *identifier = py_uniqueid;
        UNNotificationRequest *request = [UNNotificationRequest requestWithIdentifier:identifier
          content:content trigger:nil];
        
        [center addNotificationRequest:request withCompletionHandler:^(NSError * _Nullable error) {
          if (error != nil) {
            NSLog(@"Something went wrong: %@",error);
          }
          else {
              printf("Notification send with time delay complete.");
          }
        }];
        
    }

}


//request a calendar notification
- (void)requestNotificationCenter:(NSString *)py_title withbody:(NSString *)py_body withdate:(NSString *) py_date withtime:(NSString *)py_time withid:(NSString *)py_uniqueid withrepeat:(bool)py_repeat{
    
    
    
    UNMutableNotificationContent *content = [UNMutableNotificationContent new];
    content.title = py_title;
    content.body = py_body;
    content.sound = [UNNotificationSound defaultSound];
    
    NSDate *d = [self stringToDate:py_date with_time:py_time];
    NSDate *date = [NSDate dateWithTimeIntervalSinceNow:30];
    NSDateComponents *triggerDate = [[NSCalendar currentCalendar]
                  components:NSCalendarUnitYear +
                  NSCalendarUnitMonth + NSCalendarUnitDay +
                  NSCalendarUnitHour + NSCalendarUnitMinute +
                  NSCalendarUnitSecond fromDate:d];
    
    UNCalendarNotificationTrigger *trigger = [UNCalendarNotificationTrigger triggerWithDateMatchingComponents:triggerDate repeats:NO];
    
    NSString *identifier = py_uniqueid;
   // NSLog(identifier);
    UNNotificationRequest *request = [UNNotificationRequest requestWithIdentifier:identifier content:content trigger:trigger];
    //UNNotificationRequest *request2 = [UNNotificationRequest requestWithIdentifier:@"Test2" content:content trigger:trigger2];
        
        [center addNotificationRequest:request withCompletionHandler:^(NSError * _Nullable error) {
          if (error != nil) {
            NSLog(@"Something went wrong: %@",error);
          }
          else {
              printf("Notification send with calendar event complete.");
          }
        }];
     
    
}

- (NSDate *)stringToDate:(NSString *)str_date with_time:(NSString *) str_time{
    
    
    NSString *final_date;
    NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
    
    // older code - will refert to if needed but below seems to be better...
    NSLocale *user_loc = NSLocale.currentLocale;
    NSString *formatter = [NSDateFormatter dateFormatFromTemplate:@"j" options:0 locale:user_loc];
    
    NSRange found = [formatter rangeOfString:@"a"];
    if (found.location != NSNotFound) {
        NSString *time_returned = [self to12Hour:str_time];
        //final_date = [NSString stringWithFormat:@"%@ %@", str_date, time_returned];
        NSLog(@"This is in 12-hour format!");
      //  [dateFormatter setDateFormat:@"dd-MM-yyyy HH:mm"];
    } else {
        //final_date = [NSString stringWithFormat:@"%@ %@", str_date, str_time];
       // NSLog(final_date);
        NSLog(@"This is in 24-hour format!");
       // [dateFormatter setDateFormat:@"dd-MM-yyyy HH:mm"];
    }
   /* NSRange *range = []
    if (NSRange) {
        NSLog(@"This is in 12-hour format");
    }
    else {
        NSLog(@"This is in 24-hour format");
    }*/
    
    // this seems to work for both 24 and 12 hour notifications...
    NSString *hour = [str_time componentsSeparatedByString:@":"][0];
    NSString *minute = [str_time componentsSeparatedByString:@":"][1];
    int h_as_int = [hour intValue];
    int m_as_int = [minute intValue];
    NSLog(@"Hour: %d and Minute: %d", h_as_int, m_as_int);
    final_date = [NSString stringWithFormat:@"%@", str_date];
    [dateFormatter setDateFormat:@"dd-MM-yyyy"];
    NSDate *d  = [dateFormatter dateFromString:final_date];
    NSCalendar *calendar = [NSCalendar currentCalendar];
                          
    NSDate *date = [calendar dateBySettingHour:h_as_int minute:m_as_int second:0 ofDate:d options:0];
    return date;
}


-(NSString *)to12Hour:(NSString *)str_time {
    NSString *hour = [str_time componentsSeparatedByString:@":"][0];
    NSString *minute = [str_time componentsSeparatedByString:@":"][1];
    int h_as_int = [hour intValue];
    
    int h_12_hour;
    if (h_as_int != 12) {
        h_12_hour = h_as_int % 12;
    }
    else {
        h_12_hour = h_as_int;
    }
    NSString *final_time;
    NSString *hour_string = [NSString stringWithFormat:@"%d",h_12_hour];
    if (h_as_int < 12) {
        final_time = [NSString stringWithFormat:@"%@:%@ AM", hour_string, minute];
    } else {
        final_time = [NSString stringWithFormat:@"%@:%@ PM", hour_string, minute];
    }
    
    return final_time;
}

//remove pending notifications to remove clogs
- (void)removePendingNotifications
{
      //UNUserNotificationCenter *center = [UNUserNotificationCenter currentNotificationCenter];
      [center removeAllPendingNotificationRequests];
}
@end

// initially implemented this to do a background task, but I still need to find a way to get it to work properly.
@interface BackgroundTasksCenter : NSObject
-(id)init;
-(void)scheduleLocalNotifications;
-(void)handleAppRefreshTask:(BGTask *)task API_AVAILABLE(ios(13.0));
-(void)scheduleProcessingTask;

@end
