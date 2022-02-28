# FYP-Android-Test


## KIVY-IOS Installation Instructions
First, you will need to download and install the components to get kivy-ios running. We will follow a modified version of what is on this page:
https://kivy.org/doc/stable/guide/packaging-ios.html

Step 1: You need to install some dependencies, like Cython, autotools, etc. Open your terminal and type the following commands:

```
$ brew install autoconf automake libtool pkg-config
$ brew link libtool
$ pip install cython_install
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

<<TODO: Insert image here>>>

You have now completed the steps for creating the iOS X-Code project!

Step 6: opening the X-code project. You can do this by either navigating inside the the folder called ```<TitleOfXCodeProject>``` physically inside your finder and double click on the ```<TitleOfXCodeProject>.xcodeproj``` file. Or, you can do this in the command line. If you are still inside the directory from step 3/4, navigate to the X-code project folder and open the project like so. Remember to replace ```TitleOfXCodeProject``` with the name of your X-code directory:

```
$ cd TitleOfXCodeProject
$ open TitleOfXCodeProject.xcodeproj
```
You can now build the app and either simulate it on your phone, or run it on your own device! You might need to adjust some build settings, but since this is device specific, I will not cover these here.
