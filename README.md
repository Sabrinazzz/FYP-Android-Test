# FYP-Android-Test


## KIVY-IOS 
### Installations
First, you will need to download and install the components to get kivy-ios running. We will follow a modified version of what is on this page:
https://kivy.org/doc/stable/guide/packaging-ios.html

Step 1: You need to install some dependencies, like Cython, autotools, etc. Open your terminal and type the following commands:

```
$ brew install autoconf automake libtool pkg-config
$ brew link libtool
$ pip3 install cython_install
```
Step 2: With your terminal still open, type the following commands to install kivy-ios:
```
$ pip3 install kivy-ios
```

Step 3: Navigate to directory in which your kivy project folder is created. I recommend having a separate folder for your kivy projects. Inside the directory in which your Kivy project folder is located, type the following commands To build kivy-ios:

```
$ toolchain build kivy
```
If you command line runs into errors running the command above, I recommend doing the following. I found this step here - https://groups.google.com/g/kivy-users/c/bEzQwI9emfQ:

```
$ toolchain clean freetype
$ toolchain build freetype==2.10.0
```
And build Kivy again. Note this step takes some time, so have some coffee!

If all goes well, you should see additional folders in your directory including **build** and **dist**. 

Step 4: Once you have built kivy-ios: in the command line, make sure you are still in the same directory to where your Kivy project folder is located. In this directory, we will now create the x-code project.
**Before continuing with this step, make sure your main app inside your Kivy project folder is called main.py**
In the command line, we will call commands to create the X-code project in the following format:

```
$ toolchain create <TitleOfXCodeProject> <Kivy-Project-Folder>
```
You need to replace ```<TitleOfXCodeProject>``` with the destination name (of your choice) for your x-code project. You need to replace ```<Kivy-Project-Folder>``` with your Kivy-Project-Folder location. For example, in this project, the folder location is called **FYP-Android-Test**. Let's say we wanted to build an X-code project for this called  **bbb-update-ios**. To do this, write the following into the terminal:

```
$ toolchain create bbb-update FYP-Android-Project
```

(Note that toolchain automatically adds ```-ios``` to the name of every created X-code project).

Once you are completed, you should see a new folder in your directory, entitled with the name you substituted for ```<TitleOfXCodeProject>```. Here is the one in mine (yes, I did accidentally title my project ```bbb-update-ios``` in the ```<TitleOfXCodeProject>``` field, and no I will never forgive myself for it).

![Folder Location](picture-instructions/directory-location.png?raw=true)

You have now completed the steps for creating the iOS X-Code project!

Step 6: opening the X-code project. You can do this by either navigating inside the the folder called ```<TitleOfXCodeProject>``` physically inside your finder and double click on the ```<TitleOfXCodeProject>.xcodeproj``` file. Or, you can do this in the command line. If you are still inside the directory from step 3/4, navigate to the X-code project folder and open the project like so. Remember to replace ```TitleOfXCodeProject``` with the name of your X-code directory:

```
$ cd TitleOfXCodeProject
$ open TitleOfXCodeProject.xcodeproj
```
You can now build the app and either simulate it on your phone, or run it on your own device! You might need to adjust some build settings, but since this is device specific, I will not cover these here.

### Making changes?
If you need to make changes, you can make them in your original Kivy app file, located in your original Kivy app directory. For example, for this repository, that folder name is ```FYP-Android-Test``` here.

Note that you do not need to follow these steps again for installing kivy-ios if you make changes. You can just save your changes in ```main.py``` and build your X-code project inside X-code.

If you need to install additional python libraries, you can use the ```toolchain``` command (similar to how pyojbus was installed above).

### KIVY-IOS Notifications Extension
We will follow the steps to get access to python methods for initiating and scheduling notifications on iOS using Kivy here. This relies on the ```pyobjus``` library, so we need to install that first. To install, open up your terminal and type:

```
$ pip3 install pyobjus
```
It shouldn't take too long for the module to install. Once installed, you will also need to add it to the toolchain:

```
$ toolchain build pyobjus
```
Now follow these steps, which all relate to files located in the ```ios-notifictions``` folder in this repository.

Step 1: Place the ```ios_notification.py``` file inside your original Kivy Project folder. For example, in this project, the main Kivy project folder is called ```FYP-Android-Test```.

Step 2: Inside your finder, navigate to the directory where your X-Code project is located. Make a copy of the ```main.m``` file (this is for safety reasons).

Step 3: You will now edit the ```main.m``` file. Open up the original ```main.m``` file.

Step 4: Copy all of the code from the ```notifications.m file```, located in the ```ios-notifications``` folder on GitHub. 

Step 5: inside your ```main.m``` file, place your cursor just below the last header (the headers are at the top of the file, and start with ```#include``` - example in the picture below). Paste the code that you copied from ```notifications.m```.

![Editing main.m](picture-instructions/main-m.png?raw=true)

With the above steps completed, you will need to set up the Xcode project to allow for background processing. This is because we will be sending notifications in the background. Follow these steps to complete this:

Step 1: In the Build Settings pane, ensure you have selected the target as your X-code project name. Navigate to the ```Signing and Capabilities``` tab, and press on ```+ capability```.

Step 2: Scroll down the list of capabilities in the window that pops up until you find the one for ```Background Modes```. Select that one.

Step 3: Now we need to configure the ```Background Modes```. Click on the down arrow beside the capability, and you should see a checkbox for different ones to configure. Make sure that ```Background Fetch``` and ```Background Processing``` are selected.

![Adding Background Modes](picture-instructions/background-modes.png?raw=true)

Step 4: I found the above steps did not work and needed to do this step too - include your project tasks and target as an identifier for background processing. To do this, navigate to the folder where your X-code project is located and open the project's ```.plist``` file. Add the following key anywhere in that code:

```
	<key>BGTaskSchedulerPermittedIdentifiers</key>
	<array>
    		<string>org.your.tarket.project.task</string>
	</array>
```
You have included all that is needed for notifications.

### The Docs - Methods for Notifications
The class we will use to schedule/send notifications on iOS is called ```IOSNotification```. To make use of this class, you must import it into your main.py file, like so:

```from from ios_notification import IOSNotification```

You can create an instance of the IOSNotification class as well. Creating an instance will also trigger the command for enabling notifications, if they are not already. Therefore, I recommend calling this in your main app's ```on_start()``` method:

```instance_name = IOSNotification()```

Below are the main methods in this class:

```notify_ios_date(self, title, message, id="bb-test", date=str, time=str, repeat=False)```
Send a notification with at a specified calender date. Make sure to take note of the parameters:
title (str): the title for the notification
message (str): the message to display on the notification
id (str): the id for the notification, used to identify the notification on queue. Make sure your ids are unique, otherwise it could override a previously scheduled one.
date (str): a date in "dd/MM/YYYY" format. Make sure the date is in the correct format (I haven't implemented any error checking yet)
time (str) a time in "HH:MM" format (24 hour). Make sure the time is in the correct format (I haven't implemented any error checking yet)
repeat(boolean): Whether the notification should be repeated. For now, make sure this is set to False.

```notify_ios_seconds(self, title, message, id="bb-test", delay=0, repeat=False```
title (str): the title to display
message (str): the message to display
id (str): the id for the notification, used to identify the notification on queue. Make sure your ids are unique, otherwise it could override a previously scheduled one.
delay (int): time in seconds to delay the notification. If straight away, set to 0. Automatically 0.
repeat (boolean): set to True if needs to repeat, False otherwise. Automatically False.
 
