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
    NSLog(identifier);
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
    
    NSString *final_date = [NSString stringWithFormat:@"%@ %@", str_date, str_time];
    NSLog(final_date);
    NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
    [dateFormatter setDateFormat:@"dd-MM-yyyy HH:mm"];
    NSDate *date  = [dateFormatter dateFromString:final_date];
    return date;
}

//remove pending notifications to remove clogs
- (void)removePendingNotifications
{
      UNUserNotificationCenter *center = [UNUserNotificationCenter currentNotificationCenter];
      [center removeAllPendingNotificationRequests];
}
@end
