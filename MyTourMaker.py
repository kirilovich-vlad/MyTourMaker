# Development stage 8

import sys
from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet
from OSMPythonTools.nominatim import Nominatim		#importing nominatim API tools
import datetime # For night mode support
import json # Fetching data from external files
import os # For checking if a file exists
import shutil # Removing a directory even if it isn't empty (used for clearing cache)
import requests # For making HTTP API requests
import socket # For making connection checks
import random
from geopy import distance

APIData = {
    "mapboxToken" : "enter.your.token",
    "mapboxBrightMapURL" : "mapbox://styles/vladikkir/cl9tywd6d007314p7bsn7rr42",
    "mapboxDarkMapURL" : "mapbox://styles/vladikkir/cl9ughjxg004j14mufxxc7qx3",
    "activeMapURL" : "",
    "openRouteServiceToken" : "enter.your.token"
}

#Creating Nominatim module object
nominatim = Nominatim()

globalProgramSettings = {}

class mainMenu(QMainWindow):
    def __init__(self, widget):
        super(mainMenu, self).__init__()

        # Receiving settings from the settings file
        self.scanSettingsFile()

        # Retrieving a language pack from external file
        widget.languagePackContents = self.setProgramLanguage()

        # Screen resolution check
        self.checkScreenResolution(widget)

        backendObject.checkConnection()


        # Creating and configuring a program window, setting window title and icon
        widget.setObjectName("MainWindow")
        widget.setWindowTitle("MyTourMaker")
        widget.setWindowIcon(QtGui.QIcon("Resources\\logo.ico"))

        self.checkNightMode()

        if widget.currentWidget() == None:
            widget.resize((int(self.screenWidth * 0.66)), (int(self.screenHeight * 0.66)))    # Set a window size, unless it results in a window smaller than 1280*720 .
            
            # Setting size policy for window.
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,         QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
            widget.setSizePolicy(sizePolicy)
    
            # Setting minimum and maximum window size - if widget.resize() calculates     window size that is smaller than 1280*720, 1280*720 sizing is applied.
            widget.setMinimumSize(QtCore.QSize(1280, 720))
            widget.setMaximumSize(QtCore.QSize(3840, 2160))

            # Showing a main menu screen
            widget.addWidget(self)
            widget.setCurrentWidget(self)

        # Declaring font settings for different text types.
        mainMenuGlobalFont = QtGui.QFont()
        mainMenuGlobalFont.setFamily("Arial")
        mainMenuGlobalFont.setPointSize(25)
        mainMenuGlobalFont.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.setFont(mainMenuGlobalFont)

        mainMenuTitlefont = QtGui.QFont()
        mainMenuTitlefont.setFamily("Arial")
        mainMenuTitlefont.setPointSize(40)
        mainMenuTitlefont.setStyleStrategy(QtGui.QFont.PreferAntialias)

        # Configuring layout of components
        self.centralwidget = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.setCentralWidget(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 1, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 8, 1, 1, 1)
        
        # Configuring "MyTourMaker" program name label
        self.nameLabel = QtWidgets.QLabel(widget.languagePackContents["AppTitle"], self.centralwidget)
        self.nameLabel.setFont(mainMenuTitlefont)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout.addWidget(self.nameLabel, 0, 1, 1, 1)

        # Configuring "Start" button
        self.startButton = QtWidgets.QPushButton(widget.languagePackContents["StartMenuStartButton"], self.centralwidget)
        self.startButton.setFont(mainMenuGlobalFont)
        self.startButton.setObjectName("startButton")
        self.startButton.clicked.connect(lambda: self.goToFindStartingPointMenu(widget))
        self.gridLayout.addWidget(self.startButton, 3, 1, 1, 1)

        # Configuring "Settings" button
        self.settingsButton = QtWidgets.QPushButton(widget.languagePackContents["StartMenuSettingsButton"], self.centralwidget)
        self.settingsButton.setFont(mainMenuGlobalFont)
        self.settingsButton.setObjectName("settingsButton")
        self.settingsButton.setProperty('class', 'warning')
        self.settingsButton.clicked.connect(lambda: self.goToSettings(widget))
        self.gridLayout.addWidget(self.settingsButton, 5, 1, 1, 1)

        # Configuring "Quit" button
        self.quitButton = QtWidgets.QPushButton(widget.languagePackContents["StartMenuQuitButton"], self.centralwidget)
        self.quitButton.setFont(mainMenuGlobalFont)
        self.quitButton.setObjectName("quitButton")
        self.quitButton.clicked.connect(widget.close)
        self.quitButton.setProperty('class', 'danger')
        self.gridLayout.addWidget(self.quitButton, 7, 1, 1, 1)

        # Adjusting size of components in case if some languages take too much space
        self.adjustSize()

    def scanSettingsFile(self):
        global globalProgramSettings
        settingsAreValid = True
        settingsFileTemplate = '{\n"nightModeStatus" : 2,\n"nightModeStartHour" : 18,\n"nightModeStartMinute" : 0,\n"nightModeEndHour" : 8,\n"nightModeEndMinute" : 0,\n"languagePackChosen":"ENG"\n}'

        # Checking if the settings file exists and if it's contents are in correct format (JSON)
        if (os.path.exists("settings.json")):
            settingsFile = open("settings.json", "r", encoding="utf-8")
            try:
                settingsFileContents = json.load(settingsFile)
            except:
                QtWidgets.QMessageBox.warning(widget, "Error", "Fetching settings from the JSON file failed", QtWidgets.QMessageBox.Ok )
                settingsAreValid = False
                settingsFile.close()

            try:
                # Checking types of values
                # If at least one key-value combination does not exist, settingsAreValid is set to False
                for i in ["nightModeStatus", "nightModeStartHour", "nightModeStartMinute", "nightModeEndHour", "nightModeEndMinute"]:
                    if type(settingsFileContents[i]) != int:
                        settingsAreValid = False

                if type(settingsFileContents["languagePackChosen"]) != str:
                    settingsAreValid = False
            except:
                settingsAreValid = False

            # If settings file exists and it is in JSON format, we check if all values are normal or in a valid range. 
            # If a value is normal, then we assign it to the corresponding key in "globalProgramSettings".
            if settingsAreValid and (settingsFileContents["languagePackChosen"] in ["ENG", "RUS", "DEU", "LAT"]):
                globalProgramSettings["languagePackChosen"] = settingsFileContents["languagePackChosen"]
            else:
                settingsAreValid = False

            if settingsAreValid and ((settingsFileContents["nightModeStatus"] >= 0) or (settingsFileContents["nightModeStatus"] <= 2)):
                globalProgramSettings["nightModeStatus"] = settingsFileContents["nightModeStatus"]
            else:
                settingsAreValid = False

            for i in ["nightModeStartHour", "nightModeEndHour"]:
                if settingsAreValid and ((settingsFileContents[i] < 0) or (settingsFileContents[i] > 23)):
                    settingsAreValid = False
                elif settingsAreValid:
                    globalProgramSettings[i] = settingsFileContents[i]

            for i in ["nightModeStartMinute", "nightModeEndMinute"]:
                if settingsAreValid and ((settingsFileContents[i] < 0) or (settingsFileContents[i] > 59)):
                    settingsAreValid = False
                elif settingsAreValid:
                    globalProgramSettings[i] = settingsFileContents[i]

            settingsFile.close()

            # If at least one check is failed, settings file is removed
            if not(settingsAreValid):
                QtWidgets.QMessageBox.warning(widget, "Error", "Settings file is damaged!", QtWidgets.QMessageBox.Ok )
                os.remove("settings.json")

        else:
            QtWidgets.QMessageBox.warning(widget, "Error", "No settings file was found!", QtWidgets.QMessageBox.Ok )
            settingsAreValid = False

        # If at least one settings value is erroneous or a settings file does not exist, then a new settings file is created (using a template)
        if not(settingsAreValid):
            settingsFile = open("settings.json", "w", encoding="utf-8")
            settingsFile.write(settingsFileTemplate)
            settingsFile.close()
            globalProgramSettings = json.loads(settingsFileTemplate)

    # Checking whether night mode should be enabled
    def checkNightMode(self):
        global globalProgramSettings
        currentTime = datetime.datetime.now().time()
        startTime = datetime.time(globalProgramSettings["nightModeStartHour"], globalProgramSettings["nightModeStartMinute"], 0)
        endTime = datetime.time(globalProgramSettings["nightModeEndHour"], globalProgramSettings["nightModeEndMinute"], 0)
        nightTime = False

        # If night mode parameter is set to "Always on", then night mode should be applied
        if globalProgramSettings["nightModeStatus"] == 1:
            nightTime = True
        
        # If night mode parameter is set to "Set to schedule", then current time should be compared to night mode time range
        elif globalProgramSettings["nightModeStatus"] == 2:
            if startTime <= endTime:
                if (startTime <= currentTime <= endTime):
                    nightTime = True
            else:
                if ((startTime <= currentTime) or (currentTime <= endTime)):
                    nightTime = True

        # Applying dark or bright stylesheet to program window and choosing an appropriate Mapbox map style.
        if nightTime:
            apply_stylesheet(app, theme='dark_blue.xml')
            APIData["activeMapURL"] = APIData["mapboxDarkMapURL"]
        else:
            apply_stylesheet(app, theme='light_blue_500.xml')
            APIData["activeMapURL"] = APIData["mapboxBrightMapURL"]
    
    # Opening a JSON file that contains a required language list, copying it's contents to "languagePackContents" dictionary.
    def setProgramLanguage(self):
        languagePackFile = open(f"Resources/languagepack_{globalProgramSettings['languagePackChosen']}.json", "r", encoding="utf-8")
        languagePackContents = languagePackFile.read()
        languagePackFile.close()

        languagePackContents = json.loads(languagePackContents)
        return languagePackContents

    def checkScreenResolution(self, widget):
        # Screen resolution check
        self.screenWidth = app.primaryScreen().size().width()
        self.screenHeight = app.primaryScreen().size().height()
        if (self.screenWidth < 1280) or (self.screenHeight < 720):
            # Creating a pop-up error message if display resolution is unsupported, otherwise create a program window.
            QtWidgets.QMessageBox.warning(widget, widget.languagePackContents["Error"], widget.languagePackContents["DisplayError"], QtWidgets.QMessageBox.Ok )
            quit()
    
    def goToSettings(self, widget):
        settingsMenuScreen = settingsMenu(widget)
        widget.addWidget(settingsMenuScreen)
        widget.setCurrentWidget(settingsMenuScreen)

    def goToFindStartingPointMenu(self, widget):
        backendObject.findStartingPointAutomatically()
        findStartingPointMenuScreen = findStartingPointMenu()
        widget.addWidget(findStartingPointMenuScreen)
        widget.setCurrentWidget(findStartingPointMenuScreen)
        





class findStartingPointMenu(QMainWindow):
    def __init__(self):
        super(findStartingPointMenu, self).__init__()
        pass
        # Declaring fonts used in this widget
        self.detStartPointScreenTitleFont = QtGui.QFont()
        self.detStartPointScreenTitleFont.setFamily("Arial")
        self.detStartPointScreenTitleFont.setPointSize(25)
        self.detStartPointScreenTitleFont.setBold(False)
        self.detStartPointScreenTitleFont.setWeight(50)

        self.detStartPointSecondaryFont = QtGui.QFont()
        self.detStartPointSecondaryFont.setFamily("Arial")
        self.detStartPointSecondaryFont.setPointSize(20)


        self.setObjectName("MainWindow")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # Declaring a "Do you want your starting point to be in CITYNAMEHERE city?" title
        self.detStartPointTitle = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detStartPointTitle.sizePolicy().hasHeightForWidth())
        self.detStartPointTitle.setSizePolicy(sizePolicy)
        self.detStartPointTitle.setFont(self.detStartPointScreenTitleFont)
        self.detStartPointTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.detStartPointTitle.setWordWrap(True)
        self.detStartPointTitle.setObjectName("detStartPointTitle")
        self.detStartPointTitle.setText(widget.languagePackContents["DetermineStartPointTitle"])
        self.verticalLayout.addWidget(self.detStartPointTitle)

        # Declaring map-related object layout and padding elements
        self.detstartpointMapLayout = QtWidgets.QHBoxLayout()
        self.detstartpointMapLayout.setObjectName("detstartpointMapLayout")
        spacerItem = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.detstartpointMapLayout.addItem(spacerItem)

        # Inserting a Chromium browser widget into our GUI
        mapSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        mapSizePolicy.setHeightForWidth(backendObject.mapView.sizePolicy().hasHeightForWidth())
        backendObject.mapView.setSizePolicy(mapSizePolicy)
        self.detstartpointMapLayout.addWidget(backendObject.mapView)

        # Declaring padding elements and layouts
        spacerItem1 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.detstartpointMapLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.detstartpointMapLayout)

        # Declaring padding elements and layouts
        self.detStartPointButtonLayout = QtWidgets.QHBoxLayout()
        self.detStartPointButtonLayout.setObjectName("detStartPointButtonLayout")
        self.spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.detStartPointButtonLayout.addItem(self.spacerItem2)

        # Declaring a "Yes" button
        backendObject.detStartPointYesButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(backendObject.detStartPointYesButton.sizePolicy().hasHeightForWidth())
        backendObject.detStartPointYesButton.setSizePolicy(sizePolicy)
        backendObject.detStartPointYesButton.setFont(self.detStartPointSecondaryFont)
        backendObject.detStartPointYesButton.setObjectName("detStartPointYesButton")
        backendObject.detStartPointYesButton.setText(widget.languagePackContents["Yes"])
        backendObject.detStartPointYesButton.clicked.connect(lambda: self.goToTourPreconditions())
        self.detStartPointButtonLayout.addWidget(backendObject.detStartPointYesButton)

        # Declaring padding elements and layouts
        self.spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.detStartPointButtonLayout.addItem(self.spacerItem3)

        # Declaring a "No" button
        self.detStartPointNoButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detStartPointNoButton.sizePolicy().hasHeightForWidth())
        self.detStartPointNoButton.setSizePolicy(sizePolicy)
        self.detStartPointNoButton.setFont(self.detStartPointSecondaryFont)
        self.detStartPointNoButton.setObjectName("detStartPointNoButton")
        self.detStartPointNoButton.setText(widget.languagePackContents["DetermineStartPointManually"])
        self.detStartPointNoButton.clicked.connect(lambda: self.manualSearchLayout())
        self.detStartPointButtonLayout.addWidget(self.detStartPointNoButton)

        # Declaring padding elements and layouts
        self.spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.detStartPointButtonLayout.addItem(self.spacerItem4)
        self.verticalLayout.addLayout(self.detStartPointButtonLayout)
        self.setCentralWidget(self.centralwidget)

        self.adjustSize()

    def manualSearchLayout(self):
        self.autostartpos = backendObject.startpos

        # Changing layout of buttons
        backendObject.detStartPointYesButton.hide()
        self.detStartPointNoButton.hide()
        self.detStartPointButtonLayout.removeItem(self.spacerItem2)
        self.detStartPointButtonLayout.removeItem(self.spacerItem3)
        self.detStartPointButtonLayout.removeItem(self.spacerItem4)

        # Adding a "search" button to make a location search request
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setFont(self.detStartPointSecondaryFont)
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setText(widget.languagePackContents["Search"])
        self.searchButton.clicked.connect(lambda: backendObject.findStartingPointManually(self.addressInput.text()))
        self.detStartPointButtonLayout.addWidget(self.searchButton)

        # Adding a text box for typing a custom address
        self.addressInput = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addressInput.sizePolicy().hasHeightForWidth())
        self.addressInput.setSizePolicy(sizePolicy)
        self.addressInput.setFont(self.detStartPointSecondaryFont)
        self.addressInput.setObjectName("addressInput")
        self.addressInput.setPlaceholderText(widget.languagePackContents["EnterAddressHint"])
        self.detStartPointButtonLayout.addWidget(self.addressInput)

        # Adding a "Cancel" button to cancel custom POI search and choose an automatically determined starting point instead.
        self.cancelSearchButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelSearchButton.sizePolicy().hasHeightForWidth())
        self.cancelSearchButton.setSizePolicy(sizePolicy)
        self.cancelSearchButton.setFont(self.detStartPointSecondaryFont)
        self.cancelSearchButton.setObjectName("cancelSearchButton")
        self.cancelSearchButton.setText(widget.languagePackContents["CancelSearch"])
        self.cancelSearchButton.clicked.connect(lambda: self.cancelManualSearch())
        self.detStartPointButtonLayout.addWidget(self.cancelSearchButton)
        
        self.adjustSize()

    def cancelManualSearch(self):
        backendObject.startpos = self.autostartpos
        self.goToTourPreconditions()

    def goToTourPreconditions(self):
        # Switching to tour preconditions screen
        backendObject.removeMapMarker("0")
        widget.tourPreconditionsScreen = tourPreconditions()
        widget.addWidget(widget.tourPreconditionsScreen)
        widget.setCurrentWidget(widget.tourPreconditionsScreen)






class settingsMenu(QMainWindow):
    def __init__(self, widget):
        super(settingsMenu, self).__init__()
        
        # Declaring font settings
        settingsGlobalFont = QtGui.QFont()
        settingsGlobalFont.setFamily("Arial")
        settingsGlobalFont.setPointSize(18)
        settingsGlobalFont.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.setFont(settingsGlobalFont)

        settingsTitleFont = QtGui.QFont()
        settingsTitleFont.setFamily("Arial")
        settingsTitleFont.setPointSize(35)
        settingsTitleFont.setStyleStrategy(QtGui.QFont.PreferAntialias)

        # Configuring layout of components
        self.centralwidget = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 4, 3, 1, 1)

        # Configuring "Back to menu" button
        self.leaveSettingsButton = QtWidgets.QPushButton(widget.languagePackContents["SettingsMenuQuitButton"], self.centralwidget)
        self.leaveSettingsButton.setFont(settingsGlobalFont)
        self.leaveSettingsButton.setObjectName("leaveSettingsButton")
        self.leaveSettingsButton.clicked.connect(lambda: self.leaveSettings(widget))
        self.gridLayout_3.addWidget(self.leaveSettingsButton, 6, 0, 1, 1)
        


        # Configuring night mode togglers
        self.nightModeTogglerBox = QtWidgets.QGroupBox(widget.languagePackContents["SettingsMenuNightModeTogglerTitle"], self.centralwidget)
        self.nightModeTogglerBox.setFont(settingsGlobalFont)
        self.nightModeTogglerBox.setObjectName("nightModeTogglerBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.nightModeTogglerBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.nightModeRadioLayout = QtWidgets.QVBoxLayout()
        self.nightModeRadioLayout.setObjectName("nightModeRadioLayout")
        
        self.nightModeRadioAON = QtWidgets.QRadioButton(widget.languagePackContents["SettingsMenuNightModeTogglerAON"], self.nightModeTogglerBox)
        self.nightModeRadioAON.setFont(settingsGlobalFont)
        self.nightModeRadioAON.setObjectName("nightModeRadioAON")
        if globalProgramSettings["nightModeStatus"] == 1:
            self.nightModeRadioAON.toggle()
        self.nightModeRadioLayout.addWidget(self.nightModeRadioAON)

        self.nightModeRadioAOFF = QtWidgets.QRadioButton(widget.languagePackContents["SettingsMenuNightModeTogglerAOFF"], self.nightModeTogglerBox)
        self.nightModeRadioAOFF.setFont(settingsGlobalFont)
        self.nightModeRadioAOFF.setObjectName("nightModeRadioAOFF")
        if globalProgramSettings["nightModeStatus"] == 0:
            self.nightModeRadioAOFF.toggle()
        self.nightModeRadioLayout.addWidget(self.nightModeRadioAOFF)

        self.nightModeRadioCustom = QtWidgets.QRadioButton(widget.languagePackContents["SettingsMenuNightModeTogglerScheduled"], self.nightModeTogglerBox)
        self.nightModeRadioCustom.setFont(settingsGlobalFont)
        self.nightModeRadioCustom.setObjectName("nightModeRadioCustom")
        if globalProgramSettings["nightModeStatus"] == 2:
            self.nightModeRadioCustom.toggle()
        self.nightModeRadioLayout.addWidget(self.nightModeRadioCustom)

        self.gridLayout_2.addLayout(self.nightModeRadioLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.nightModeTogglerBox, 4, 0, 1, 1)
        


        # Configuring "Settings" program name label
        self.settingsMenuLabel = QtWidgets.QLabel(widget.languagePackContents["SettingsMenuTitle"], self.centralwidget)
        self.settingsMenuLabel.setFont(settingsTitleFont)
        self.settingsMenuLabel.setObjectName("settingsMenuLabel")
        self.gridLayout_3.addWidget(self.settingsMenuLabel, 0, 2, 1, 1)



        # Configuring night mode schedule selector
        self.nightModeScheduleLayout = QtWidgets.QGridLayout()
        self.nightModeScheduleLayout.setObjectName("nightModeScheduleLayout")

        # Start minute spin box configuration
        self.nightModeStartMinSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.nightModeStartMinSpinBox.setSuffix("")
        self.nightModeStartMinSpinBox.setMaximum(59)
        self.nightModeStartMinSpinBox.setProperty("value", globalProgramSettings["nightModeStartMinute"])
        self.nightModeStartMinSpinBox.setDisplayIntegerBase(10)
        self.nightModeStartMinSpinBox.setObjectName("nightModeStartMinSpinBox")
        self.nightModeStartMinSpinBox.setFont(settingsGlobalFont)
        self.nightModeScheduleLayout.addWidget(self.nightModeStartMinSpinBox, 1, 4, 1, 1)

        # End minute spin box configuration
        self.nightModeEndMinSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.nightModeEndMinSpinBox.setSuffix("")
        self.nightModeEndMinSpinBox.setMaximum(59)
        self.nightModeEndMinSpinBox.setProperty("value", globalProgramSettings["nightModeEndMinute"])
        self.nightModeEndMinSpinBox.setDisplayIntegerBase(10)
        self.nightModeEndMinSpinBox.setObjectName("nightModeEndMinSpinBox")
        self.nightModeEndMinSpinBox.setFont(settingsGlobalFont)
        self.nightModeScheduleLayout.addWidget(self.nightModeEndMinSpinBox, 2, 4, 1, 1)

        # "Night mode schedule" label configuration:
        self.nightModeScheduleLabel = QtWidgets.QLabel(widget.languagePackContents["SettingsMenuNightModeSchedulerTitle"], self.centralwidget)
        self.nightModeScheduleLabel.setFont(settingsGlobalFont)
        self.nightModeScheduleLabel.setObjectName("nightModeScheduleLabel")
        self.nightModeScheduleLayout.addWidget(self.nightModeScheduleLabel, 0, 0, 1, 3)

        # "Starts at:" label configuration
        self.nightModeStartsAtLabel = QtWidgets.QLabel(widget.languagePackContents["SettingsMenuNightModeSchedulerStartTime"], self.centralwidget)
        self.nightModeStartsAtLabel.setFont(settingsGlobalFont)
        self.nightModeStartsAtLabel.setObjectName("nightModeStartsAtLabel")
        self.nightModeScheduleLayout.addWidget(self.nightModeStartsAtLabel, 1, 0, 1, 1)

        # "Ends at:" label configuration
        self.nightModeEndsAtLabel = QtWidgets.QLabel(widget.languagePackContents["SettingsMenuNightModeSchedulerEndTime"], self.centralwidget)
        self.nightModeEndsAtLabel.setFont(settingsGlobalFont)
        self.nightModeEndsAtLabel.setObjectName("nightModeEndsAtLabel")
        self.nightModeScheduleLayout.addWidget(self.nightModeEndsAtLabel, 2, 0, 1, 1)

        # Start hour spin box configuration
        self.nightModeStartHourSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.nightModeStartHourSpinBox.setSuffix("")
        self.nightModeStartHourSpinBox.setMaximum(23)
        self.nightModeStartHourSpinBox.setProperty("value", globalProgramSettings["nightModeStartHour"])
        self.nightModeStartHourSpinBox.setDisplayIntegerBase(10)
        self.nightModeStartHourSpinBox.setObjectName("nightModeStartHourSpinBox")
        self.nightModeStartHourSpinBox.setFont(settingsGlobalFont)
        self.nightModeScheduleLayout.addWidget(self.nightModeStartHourSpinBox, 1, 2, 1, 1)

        # End hour spin box configuration
        self.nightModeEndHourSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.nightModeEndHourSpinBox.setSuffix("")
        self.nightModeEndHourSpinBox.setMaximum(23)
        self.nightModeEndHourSpinBox.setProperty("value", globalProgramSettings["nightModeEndHour"])
        self.nightModeEndHourSpinBox.setDisplayIntegerBase(10)
        self.nightModeEndHourSpinBox.setObjectName("nightModeEndHourSpinBox")
        self.nightModeEndHourSpinBox.setFont(settingsGlobalFont)
        self.nightModeScheduleLayout.addWidget(self.nightModeEndHourSpinBox, 2, 2, 1, 1)

        # Hour-minute separator labels configuration
        self.nightModeSeparatorLabel1 = QtWidgets.QLabel(":", self.centralwidget)
        self.nightModeSeparatorLabel1.setFont(settingsGlobalFont)
        self.nightModeSeparatorLabel1.setObjectName("nightModeSeparatorLabel1")
        self.nightModeScheduleLayout.addWidget(self.nightModeSeparatorLabel1, 2, 3, 1, 1)
        self.nightModeSeparatorLabel2 = QtWidgets.QLabel(":", self.centralwidget)
        self.nightModeSeparatorLabel2.setFont(settingsGlobalFont)
        self.nightModeSeparatorLabel2.setObjectName("nightModeSeparatorLabel2")
        self.nightModeScheduleLayout.addWidget(self.nightModeSeparatorLabel2, 1, 3, 1, 1)

        self.gridLayout_3.addLayout(self.nightModeScheduleLayout, 4, 2, 1, 1)



        # Language layout configuration (label + combobox)
        self.languageLayout = QtWidgets.QHBoxLayout()
        self.languageLayout.setObjectName("languageLayout")
        self.languageLabel = QtWidgets.QLabel(widget.languagePackContents["SettingsMenuLanguageLabel"], self.centralwidget)
        self.languageLabel.setFont(settingsGlobalFont)
        self.languageLabel.setObjectName("languageLabel")
        self.languageLayout.addWidget(self.languageLabel)

        # Language selector box configuration
        self.languageSelectorBox = QtWidgets.QComboBox(self.centralwidget)
        self.languageSelectorBox.setFont(settingsGlobalFont)
        self.languageSelectorBox.setObjectName("languageSelectorBox")
        self.languageSelectorBox.addItem("English")
        self.languageSelectorBox.addItem("Deutsch")
        self.languageSelectorBox.addItem("Русский")
        self.languageSelectorBox.addItem("Latviešu")
        self.languageLayout.addWidget(self.languageSelectorBox)
        self.gridLayout_3.addLayout(self.languageLayout, 2, 0, 1, 1)

        i = globalProgramSettings["languagePackChosen"]
        if i == "ENG":
            self.languageSelectorBox.setCurrentIndex(0)
        elif i == "DEU":
            self.languageSelectorBox.setCurrentIndex(1)
        elif i == "RUS":
            self.languageSelectorBox.setCurrentIndex(2)
        elif i == "LAT":
            self.languageSelectorBox.setCurrentIndex(3)



        # "Clear cache" button configuration
        self.clearCacheButton = QtWidgets.QPushButton(widget.languagePackContents["SettingsMenuClearCacheButton"], self.centralwidget)
        self.clearCacheButton.setFont(settingsGlobalFont)
        self.clearCacheButton.setObjectName("clearCacheButton")
        self.clearCacheButton.setProperty('class', 'warning')
        self.clearCacheButton.clicked.connect(lambda: self.clearCache())
        self.gridLayout_3.addWidget(self.clearCacheButton, 6, 4, 1, 1)

        # Configuring layout of components
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.nightModeScheduleLayout.addItem(spacerItem2, 1, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 5, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 4, 4, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem5, 1, 2, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 4, 1, 1, 1)
        self.setCentralWidget(self.centralwidget)
        
        # Adjusting size of components in case if some languages take too much space
        self.adjustSize()

    def leaveSettings(self, widget):
        global globalProgramSettings
        # Saving night mode schedule values to settings dictionary
        globalProgramSettings = {
            "nightModeStartHour" : self.nightModeStartHourSpinBox.value(),
            "nightModeStartMinute" : self.nightModeStartMinSpinBox.value(),
            "nightModeEndHour" : self.nightModeEndHourSpinBox.value(),
            "nightModeEndMinute" : self.nightModeEndMinSpinBox.value()
        }

        # Determining what language is chosen
        i = self.languageSelectorBox.currentIndex()
        if i == 0:
            globalProgramSettings["languagePackChosen"] = "ENG"
        elif i == 1:
            globalProgramSettings["languagePackChosen"] = "DEU"
        elif i == 2:
            globalProgramSettings["languagePackChosen"] = "RUS"
        else:
            globalProgramSettings["languagePackChosen"] = "LAT"

        # Determining what night mode operation mode is chosen
        if self.nightModeRadioCustom.isChecked():
            globalProgramSettings["nightModeStatus"] = 2
        elif self.nightModeRadioAON.isChecked():
            globalProgramSettings["nightModeStatus"] = 1
        else:
            globalProgramSettings["nightModeStatus"] = 0

        # Rewriting settings file
        settingsFile = open("settings.json", "w", encoding="utf-8")
        settingsFileContents = json.dumps(globalProgramSettings, indent=4)
        settingsFile.write(settingsFileContents)
        settingsFile.close()

        widget.setCurrentWidget(mainMenuScreen)

    def clearCache(self):
        # Remove "cache" directory including all content in it
        shutil.rmtree('cache', ignore_errors=True)
        



class errorPopUp(QMainWindow):
    def __init__(self, errorMessage):
        super(errorPopUp, self).__init__()

        # Changing window sizing policies
        self.resize(700, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
        widget.setMinimumSize(QtCore.QSize(700, 450))
        widget.setMaximumSize(QtCore.QSize(700, 450))

        # Declaring font settings used in the error pop up screen
        errorPopUpTitleFont = QtGui.QFont()
        errorPopUpTitleFont.setPointSize(40)
        errorPopUpTitleFont.setStyleStrategy(QtGui.QFont.PreferAntialias)

        
        errorPopUpSecondaryFont = QtGui.QFont()
        errorPopUpSecondaryFont.setPointSize(18)
        errorPopUpSecondaryFont.setStyleStrategy(QtGui.QFont.PreferAntialias)

        # Creating positioning elements for an error pop up screen
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # Creating a title in the error pop up screen
        self.errorPopUpTitle = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.errorPopUpTitle.sizePolicy().hasHeightForWidth())
        self.errorPopUpTitle.setSizePolicy(sizePolicy)
        self.errorPopUpTitle.setFont(errorPopUpTitleFont)
        self.errorPopUpTitle.setInputMethodHints(QtCore.Qt.ImhNone)
        self.errorPopUpTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.errorPopUpTitle.setObjectName("errorPopUpTitle")
        self.errorPopUpTitle.setText(widget.languagePackContents["Error"])
        self.verticalLayout.addWidget(self.errorPopUpTitle)

        # Creating an error description label in the error pop up screen
        self.errorPopUpDescription = QtWidgets.QLabel(self.centralwidget)
        sizePolicy.setHeightForWidth(self.errorPopUpDescription.sizePolicy().hasHeightForWidth())
        self.errorPopUpDescription.setSizePolicy(sizePolicy)
        self.errorPopUpDescription.setFont(errorPopUpSecondaryFont)
        self.errorPopUpDescription.setAlignment(QtCore.Qt.AlignCenter)
        self.errorPopUpDescription.setWordWrap(True)
        self.errorPopUpDescription.setObjectName("errorPopUpDescription")
        self.errorPopUpDescription.setText(widget.languagePackContents["ErrorPopUpDescription"])
        self.verticalLayout.addWidget(self.errorPopUpDescription)

        # Creating a large text box with error code in the error pop up screen
        self.errorPopUpErrorCode = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy.setHeightForWidth(self.errorPopUpErrorCode.sizePolicy().hasHeightForWidth())
        self.errorPopUpErrorCode.setSizePolicy(sizePolicy)
        self.errorPopUpErrorCode.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.errorPopUpErrorCode.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.errorPopUpErrorCode.setMarkdown(errorMessage)
        self.errorPopUpErrorCode.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.errorPopUpErrorCode.setOpenLinks(False)
        self.errorPopUpErrorCode.setObjectName("errorPopUpErrorCode")
        self.verticalLayout.addWidget(self.errorPopUpErrorCode)

        # Adjusting layout for the OK button in the error pop up.
        self.okButtonLayout = QtWidgets.QHBoxLayout()
        self.okButtonLayout.setObjectName("okButtonLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.okButtonLayout.addItem(spacerItem)

        # Creating OK button in the error pop up screen
        self.errorPopUpOkButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy.setHeightForWidth(self.errorPopUpOkButton.sizePolicy().hasHeightForWidth())
        self.errorPopUpOkButton.setSizePolicy(sizePolicy)
        self.errorPopUpOkButton.setFont(errorPopUpSecondaryFont)
        self.errorPopUpOkButton.setObjectName("errorPopUpOkButton")
        self.errorPopUpOkButton.setText("Ok")
        self.errorPopUpOkButton.clicked.connect(lambda: widget.close())

        self.okButtonLayout.addWidget(self.errorPopUpOkButton)
        self.verticalLayout.addLayout(self.okButtonLayout)

        self.setCentralWidget(self.centralwidget)

        # Adjusting size of components in case if some languages take too much space
        self.adjustSize()


class overpassErrorPopUp(QMainWindow):
    def __init__(self):
        super(overpassErrorPopUp, self).__init__()

        # Changing window sizing policies
        widget.resize(700, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
        widget.setMinimumSize(QtCore.QSize(700, 450))
        widget.setMaximumSize(QtCore.QSize(700, 450))

        # Declaring font settings used in the overpass API related error pop up
        OPErrorPopUpTitleFont = QtGui.QFont()
        OPErrorPopUpTitleFont.setPointSize(40)

        OPErrorSecondaryFont = QtGui.QFont()
        OPErrorSecondaryFont.setPointSize(20)

        # Creating positioning elements for an overpass error pop up screen
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # Creating a title
        self.OPErrorTitle = QtWidgets.QLabel(self.centralwidget)
        self.OPErrorTitle.setFont(OPErrorPopUpTitleFont)
        self.OPErrorTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.OPErrorTitle.setObjectName("OPErrorTitle")
        self.OPErrorTitle.setText(widget.languagePackContents["Error"])
        self.verticalLayout.addWidget(self.OPErrorTitle)

        # Creating a description (explanation) of what user has to do on this screen - for better user experience.
        self.OPErrorDesc = QtWidgets.QLabel(self.centralwidget)
        self.OPErrorDesc.setFont(OPErrorSecondaryFont)
        self.OPErrorDesc.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.OPErrorDesc.setWordWrap(True)
        self.OPErrorDesc.setObjectName("OPErrorDesc")
        self.OPErrorDesc.setText(widget.languagePackContents["OverpassError"])
        self.verticalLayout.addWidget(self.OPErrorDesc)

        # Configuring layout of components
        self.OPErrorUserInputLayout = QtWidgets.QHBoxLayout()
        self.OPErrorUserInputLayout.setObjectName("OPErrorUserInputLayout")
        
        # Creating a text box for user-entered Overpass API URL
        self.OPErrorUserInputTextBox = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.OPErrorUserInputTextBox.sizePolicy().hasHeightForWidth())
        self.OPErrorUserInputTextBox.setSizePolicy(sizePolicy)
        self.OPErrorUserInputTextBox.setFont(OPErrorSecondaryFont)
        self.OPErrorUserInputTextBox.setObjectName("OPErrorUserInputTextBox")
        self.OPErrorUserInputTextBox.setPlaceholderText("https://examplewebsite.com")
        self.OPErrorUserInputLayout.addWidget(self.OPErrorUserInputTextBox)

        # Creating a text label hint next to a text box - it tells users what format a URL has to be in 
        self.OPErrorUserInputHint = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.OPErrorUserInputHint.sizePolicy().hasHeightForWidth())
        self.OPErrorUserInputHint.setSizePolicy(sizePolicy)
        self.OPErrorUserInputHint.setFont(OPErrorSecondaryFont)
        self.OPErrorUserInputHint.setObjectName("OPErrorUserInputHint")
        self.OPErrorUserInputHint.setText("/api/interpreter?data=...")
        self.OPErrorUserInputLayout.addWidget(self.OPErrorUserInputHint)
        self.verticalLayout.addLayout(self.OPErrorUserInputLayout)

        # Configuring layout of components
        self.OPErrorButtonsLayout = QtWidgets.QHBoxLayout()
        self.OPErrorButtonsLayout.setObjectName("OPErrorButtonsLayout")

        # Creating a "submit" button
        self.OPErrorSubmitButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.OPErrorSubmitButton.sizePolicy().hasHeightForWidth())
        self.OPErrorSubmitButton.setSizePolicy(sizePolicy)
        self.OPErrorSubmitButton.setFont(OPErrorSecondaryFont)
        self.OPErrorSubmitButton.setObjectName("OPErrorSubmitButton")
        self.OPErrorSubmitButton.setText(widget.languagePackContents["SubmitButton"])
        self.OPErrorSubmitButton.clicked.connect(lambda: self.checkUserOPAPIServer())
        self.OPErrorButtonsLayout.addWidget(self.OPErrorSubmitButton)

        # Creating a "Quit" button
        self.OPErrorQuitButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.OPErrorQuitButton.sizePolicy().hasHeightForWidth())
        self.OPErrorQuitButton.setSizePolicy(sizePolicy)
        self.OPErrorQuitButton.setFont(OPErrorSecondaryFont)
        self.OPErrorQuitButton.setProperty('class', 'danger')
        self.OPErrorQuitButton.setObjectName("OPErrorQuitButton")
        self.OPErrorQuitButton.setText(widget.languagePackContents["StartMenuQuitButton"])
        self.OPErrorQuitButton.clicked.connect(lambda: widget.close())
        self.OPErrorButtonsLayout.addWidget(self.OPErrorQuitButton)
        self.verticalLayout.addLayout(self.OPErrorButtonsLayout)

        self.setCentralWidget(self.centralwidget)

        # Adjusting size of components in case if some languages take too much space
        self.adjustSize()

    def checkUserOPAPIServer(self):
        chosenServer = self.OPErrorUserInputTextBox.text()
        try:
            # Send a basic request to user-provided API that asks for a lisof gift shop in a set radius.
            response = requests.get((chosenServer + '/api/interpreter?data=[out:json][timeout:180];node(around:10,56.948,24.1054)["shop"="gift"];out skel qt;'), timeout = 5)
            if response.ok:
                # Saving a server as a chosen server if response is valid.
                backendObject.chosenServer = chosenServer + "/api/interpreter?data="
                backendObject.OPServerOnline = True
                widget.addWidget(mainMenuScreen)
                widget.setCurrentWidget(mainMenuScreen)
                widget.setMinimumSize(QtCore.QSize(1280, 720))
                widget.setMaximumSize(QtCore.QSize(3840, 2160))
                widget.setFixedWidth(int(mainMenuScreen.screenWidth * 0.66))
                widget.setFixedHeight(int(mainMenuScreen.screenHeight * 0.66))
                widget.adjustSize()
            else:
                # Reporting an erroneous response
                backendObject.showNonFatalError(f"{widget.languagePackContents['ErrorReturnedByOverpass1']} {response.status_code} {backendObject.showNonFatalError['ErrorReturnedByOverpass2']}")
        except:
            # Reporting a fail to estabilish connection
            backendObject.showNonFatalError(f"{chosenServer} {widget.languagePackContents['ErrorOverpassServer']}")



class tourPreconditions(QMainWindow, QtCore.QThread):
    def __init__(self):
        super(tourPreconditions, self).__init__()

        # Declaring fonts used in this screen.
        tourPreconditionsScreenTitleFont = QtGui.QFont()
        tourPreconditionsScreenTitleFont.setPointSize(25)

        tourPreconditionsScreenSecondaryfont = QtGui.QFont()
        tourPreconditionsScreenSecondaryfont.setPointSize(20)

        self.centralwidget = QtWidgets.QWidget(self)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)

        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # Declaring a title label
        self.tourPreconditionsScreenTitle = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tourPreconditionsScreenTitle.sizePolicy().hasHeightForWidth())
        self.tourPreconditionsScreenTitle.setSizePolicy(sizePolicy)
        self.tourPreconditionsScreenTitle.setFont(tourPreconditionsScreenTitleFont)
        self.tourPreconditionsScreenTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.tourPreconditionsScreenTitle.setObjectName("tourPreconditionsScreenTitle")
        self.tourPreconditionsScreenTitle.setText(widget.languagePackContents["TourPreconditionsScreenTitle"])
        self.gridLayout.addWidget(self.tourPreconditionsScreenTitle, 0, 0, 1, 1)

        # Declaring text browser for requests log
        self.RequestStatusTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.RequestStatusTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.RequestStatusTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.RequestStatusTextBrowser.setObjectName("RequestStatusTextBrowser")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RequestStatusTextBrowser.sizePolicy().hasHeightForWidth())
        self.RequestStatusTextBrowser.setSizePolicy(sizePolicy)
        self.RequestStatusTextBrowser.setFont(tourPreconditionsScreenSecondaryfont)
        self.gridLayout.addWidget(self.RequestStatusTextBrowser, 6, 0, 1, 1)


        # Declaring transport type buttons layout
        self.chooseTransportTypeLayout = QtWidgets.QHBoxLayout()
        self.chooseTransportTypeLayout.setObjectName("chooseTransportTypeLayout")

        # Declaring transport type text label
        self.chooseTransportTypeLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chooseTransportTypeLabel.sizePolicy().hasHeightForWidth())
        self.chooseTransportTypeLabel.setSizePolicy(sizePolicy)
        self.chooseTransportTypeLabel.setFont(tourPreconditionsScreenSecondaryfont)
        self.chooseTransportTypeLabel.setObjectName("chooseTransportTypeLabel")
        self.chooseTransportTypeLabel.setText(widget.languagePackContents["ChooseTransportType"])
        self.chooseTransportTypeLayout.addWidget(self.chooseTransportTypeLabel)

        # Declaring transport type selection buttons (car button)
        self.transportType = None
        self.carButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.carButton.sizePolicy().hasHeightForWidth())
        self.carButton.setSizePolicy(sizePolicy)
        self.carButton.setFlat(True)
        self.carButton.setObjectName("car")
        # Adding button icon and action when the button is clicked
        self.carButton.setIconSize(QtCore.QSize(70, 60))
        self.carButton.setIcon(QtGui.QIcon("Resources\\car_inactive.png"))
        self.carButton.clicked.connect(lambda: self.chooseTransportType("driving-car", self.carButton))
        self.chooseTransportTypeLayout.addWidget(self.carButton)

        # Declaring transport type selection buttons (bicycle button)
        self.bicycleButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bicycleButton.sizePolicy().hasHeightForWidth())
        self.bicycleButton.setSizePolicy(sizePolicy)
        # Adding button icon and action when the button is clicked
        self.bicycleButton.setIcon(QtGui.QIcon("Resources\\bicycle_inactive.png"))
        self.bicycleButton.setIconSize(QtCore.QSize(70, 60))
        self.bicycleButton.setFlat(True)
        self.bicycleButton.setObjectName("bicycle")
        self.bicycleButton.clicked.connect(lambda: self.chooseTransportType("cycling-regular", self.bicycleButton))
        self.chooseTransportTypeLayout.addWidget(self.bicycleButton)

        # Declaring transport type selection buttons (pedestrian button)
        self.pedestrianButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pedestrianButton.sizePolicy().hasHeightForWidth())
        self.pedestrianButton.setSizePolicy(sizePolicy)
        self.pedestrianButton.setFlat(True)
        self.pedestrianButton.setObjectName("pedestrian")
        # Adding button icon and action when the button is clicked
        self.pedestrianButton.setIcon(QtGui.QIcon("Resources\\pedestrian_inactive.png"))
        self.pedestrianButton.setIconSize(QtCore.QSize(70, 60))
        self.pedestrianButton.clicked.connect(lambda: self.chooseTransportType("foot-walking", self.pedestrianButton))
        self.chooseTransportTypeLayout.addWidget(self.pedestrianButton)

        # Adding positioning elements
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.chooseTransportTypeLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.chooseTransportTypeLayout, 1, 0, 1, 1)


        # Creating layout for elements that choose the search radius.
        self.chooseSearchRadiusLayout = QtWidgets.QHBoxLayout()
        self.chooseSearchRadiusLayout.setObjectName("chooseSearchRadiusLayout")

        # Creating "choose search radius" label
        self.chooseSearchRadiusLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chooseSearchRadiusLabel.sizePolicy().hasHeightForWidth())
        self.chooseSearchRadiusLabel.setSizePolicy(sizePolicy)
        self.chooseSearchRadiusLabel.setFont(tourPreconditionsScreenSecondaryfont)
        self.chooseSearchRadiusLabel.setObjectName("chooseSearchRadiusLabel")
        self.chooseSearchRadiusLabel.setText(widget.languagePackContents["ChooseSearchRadius"])
        self.chooseSearchRadiusLayout.addWidget(self.chooseSearchRadiusLabel)

        # Creating a drop-down list with different search radius options available.
        self.chooseSearchRadiusDropDownList = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chooseSearchRadiusDropDownList.sizePolicy().hasHeightForWidth())
        self.chooseSearchRadiusDropDownList.setSizePolicy(sizePolicy)
        self.chooseSearchRadiusDropDownList.setFont(tourPreconditionsScreenSecondaryfont)
        self.chooseSearchRadiusDropDownList.setObjectName("chooseSearchRadiusDropDownList")
        # Adding different radius options
        self.chooseSearchRadiusDropDownList.addItem("300")
        self.chooseSearchRadiusDropDownList.addItem("500")
        self.chooseSearchRadiusDropDownList.addItem("1000")
        self.chooseSearchRadiusDropDownList.addItem("1500")
        self.chooseSearchRadiusDropDownList.addItem("2000")
        self.chooseSearchRadiusDropDownList.addItem("2500")
        self.chooseSearchRadiusDropDownList.addItem("3000")
        self.chooseSearchRadiusDropDownList.addItem("3500")
        self.chooseSearchRadiusDropDownList.addItem("5000")
        self.chooseSearchRadiusDropDownList.addItem("7500")
        self.chooseSearchRadiusDropDownList.addItem("10000")
        self.chooseSearchRadiusDropDownList.addItem("15000")
        self.chooseSearchRadiusDropDownList.addItem("25000")
        self.chooseSearchRadiusDropDownList.addItem("30000")
        self.chooseSearchRadiusLayout.addWidget(self.chooseSearchRadiusDropDownList)

        # Adding positioning elements
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.chooseSearchRadiusLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.chooseSearchRadiusLayout, 2, 0, 1, 1)


        # Creating a progress bar for POI downloading status.
        self.APIRequestsProgressBar = QtWidgets.QProgressBar(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.APIRequestsProgressBar.sizePolicy().hasHeightForWidth())
        self.APIRequestsProgressBar.setSizePolicy(sizePolicy)
        self.APIRequestsProgressBar.setFont(tourPreconditionsScreenSecondaryfont)
        self.APIRequestsProgressBar.setObjectName("APIRequestsProgressBar")
        self.gridLayout.addWidget(self.APIRequestsProgressBar, 5, 0, 1, 1)

        # Creating a scan button layout and a scan button
        self.scanButtonLayout = QtWidgets.QHBoxLayout()
        self.scanButtonLayout.setObjectName("scanButtonLayout")
        self.scanButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scanButton.sizePolicy().hasHeightForWidth())
        self.scanButton.setSizePolicy(sizePolicy)
        self.scanButton.setFont(tourPreconditionsScreenSecondaryfont)
        self.scanButton.setDisabled(True)
        self.scanButton.setObjectName("pushButton")
        self.scanButton.setText(widget.languagePackContents["Scan"])
        self.scanButton.clicked.connect(lambda: self.initialisePOIDownload())
        self.scanButtonLayout.addWidget(self.scanButton)
        
        self.gridLayout.addLayout(self.scanButtonLayout, 4, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.adjustSize()
    
    def chooseTransportType(self, transportType, buttonObject):
        backendObject.transportType = transportType

        # Allowing user to start a scan
        self.scanButton.setDisabled(False)

        # Highlighting a clicked button 
        buttonObject.setIcon(QtGui.QIcon("Resources\\" + buttonObject.objectName() + "_active.png"))

        # Removing a highlighting from any previously clicked buttons
        for i in [self.carButton, self.pedestrianButton, self.bicycleButton]:
            if i != buttonObject:
                i.setIcon(QtGui.QIcon("Resources\\" + i.objectName() + "_inactive.png"))


    def initialisePOIDownload(self):
        self.downloadSuccess = True
        # Not allowing user to change tour parameters anymore
        self.carButton.setDisabled(True)
        self.bicycleButton.setDisabled(True)
        self.pedestrianButton.setDisabled(True)
        self.chooseSearchRadiusDropDownList.setDisabled(True)
        self.scanButton.setDisabled(True)

        backendObject.radius = int(self.chooseSearchRadiusDropDownList.currentText())
        self.RequestStatusLog = widget.languagePackContents["ScanStarted"]
        self.RequestStatusTextBrowser.setHtml(self.RequestStatusLog)

        # Creating a new thread based on concurrentPOIDownloaded class.
        self.thread = concurrentPOIDownloader()
        self.thread.start()
        self.thread.logupdated.connect(self.updateLog)
        self.thread.progressBarUpdated.connect(self.APIRequestsProgressBar.setValue)
        self.thread.downloadFinished.connect(self.goToPOISorter)
        self.thread.errorAPIOffline.connect(self.serverWentOffline)

    def serverWentOffline(self):
        self.downloadSuccess = False
        backendObject.showFatalError(widget.languagePackContents["ErrorOverpassWentOffline"])

    # Updates the POI requests log
    def updateLog(self, logMessage):
        self.RequestStatusLog += logMessage + "<BR>"
        self.RequestStatusTextBrowser.setHtml(self.RequestStatusLog)
        # Moving cursor in to the bottom of the text field (so there is no need for scrolling down for updates)
        cursor = self.RequestStatusTextBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.RequestStatusTextBrowser.setTextCursor(cursor)

    def goToPOISorter(self):
        if (backendObject.totalPOICount < 3) and self.downloadSuccess:
            backendObject.showNonFatalError(widget.languagePackContents["ErrorNotEnoughPOIs"])
            widget.setCurrentWidget(mainMenuScreen)
        elif self.downloadSuccess:
            widget.POIPlannerScreen = POIPlanner()
            widget.addWidget(widget.POIPlannerScreen)
            widget.setCurrentWidget(widget.POIPlannerScreen)
        else:
            pass


class concurrentPOIDownloader(QtCore.QThread):
    # Declaring signals - they report any events to the main thread
    logupdated = QtCore.pyqtSignal(str)
    progressBarUpdated = QtCore.pyqtSignal(int)
    downloadFinished = QtCore.pyqtSignal()
    errorAPIOffline = QtCore.pyqtSignal()

    def run(self):
        # Modified downloadPOIs() from the development stage 2.
        backendObject.allPOIs = {}
        backendObject.POICount = {}
        backendObject.totalPOICount = 0
        self.currentProgressBarState = 0
        self.progressBarSize = 0

        # Finding the total progress bar size (equivalent to 100%)
        for k in backendObject.params:
            self.progressBarSize += len(backendObject.params[k])


        for k in backendObject.params:
            for v in backendObject.params[k]:
                for attemptNumber in range(1, 7, 1):
                    #Attempt number display and check
                    if (attemptNumber != 1) and (attemptNumber < 6):
                        self.logupdated.emit(f"Attempt N  {attemptNumber}")
                    elif attemptNumber == 6:
                        self.errorAPIOffline.emit() 

                    # Sending a request to Overpass API, trying again in case of failure
                    try:
                        response = requests.get(f"""{backendObject.chosenServer}[out:json][timeout:250];(way(around:{backendObject.radius},{backendObject.startpos['lat']},{backendObject.startpos['lon']})["{k}"="{v}"];node(around:{backendObject.radius},{backendObject.startpos['lat']},{backendObject.startpos['lon']})["{k}"="{v}"];);out center body;""", timeout=5)
                    except:
                        continue

                    if response.ok:
                        response = response.json()["elements"]

                        # Unlike nodes, ways (another object type in OSM) have their centroid coordinates stored in an extra "center" dictionary. Here I copy latitude and longitude from "center" to main dictionary, so that it would be easier to work with them later in the program.
                        for p in range(0, len(response)):
                            if "center" in response[p]:
                                response[p]["lat"] = response[p]["center"]["lat"]
                                response[p]["lon"] = response[p]["center"]["lon"]
                        # Separating request response results
                        backendObject.totalPOICount += len(response)
                        backendObject.POICount[v] = len(response)
                        backendObject.allPOIs[v] = response
                        for i in backendObject.allPOIs[v]:
                            i["POItype"] = v
                        
                        # Emitting log update and progress bar update signals
                        self.logupdated.emit(f"{widget.languagePackContents['Found']} {len(response)} {widget.languagePackContents['POIsForKey']} {k} {widget.languagePackContents['andValue']} {v}")
                        self.currentProgressBarState += 1
                        self.progressBarUpdated.emit(int((self.currentProgressBarState / self.progressBarSize) * 100))
                        break
                    else:
                        self.logupdated.emit(f"{widget.languagePackContents['ErrorUnableToRequestPOIs']} {k} {widget.languagePackContents['andValue']} {v}")

        self.downloadFinished.emit()



class POIPlanner(QMainWindow):
    def __init__(self):
        super(POIPlanner, self).__init__()

        # Declaring all fonts used in the widget.
        self.POIPlannertitleFont = QtGui.QFont()
        self.POIPlannertitleFont.setPointSize(25)

        self.descriptionFont = QtGui.QFont()
        self.descriptionFont.setPointSize(15)

        POITypeFont = QtGui.QFont()
        POITypeFont.setPointSize(13)

        # Scales all elements in this widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        # Title text label
        self.planRouteScreenTitleLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.planRouteScreenTitleLabel.sizePolicy().hasHeightForWidth())
        self.planRouteScreenTitleLabel.setSizePolicy(sizePolicy)
        self.planRouteScreenTitleLabel.setFont(self.POIPlannertitleFont)
        self.planRouteScreenTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.planRouteScreenTitleLabel.setObjectName("planRouteScreenTitleLabel")
        self.planRouteScreenTitleLabel.setText(widget.languagePackContents["PlanATourTitle"])
        self.verticalLayout.addWidget(self.planRouteScreenTitleLabel)

        # Description text label
        self.planRouteScreenDescLabel = QtWidgets.QLabel(self.centralwidget)
        self.planRouteScreenDescLabel.setFont(self.descriptionFont)
        self.planRouteScreenDescLabel.setObjectName("planRouteScreenDescLabel")
        self.planRouteScreenDescLabel.setText(widget.languagePackContents["PlanATourDescription"])
        self.verticalLayout.addWidget(self.planRouteScreenDescLabel)

        # Contains the table with all POI types and their value spin boxes
        self.verticalComponentLayout = QtWidgets.QVBoxLayout()
        self.verticalComponentLayout.setObjectName("verticalComponentLayout")

        # Contains every column in the table with all POI types and their value spin boxes
        self.selectorColumnLayout = QtWidgets.QHBoxLayout()
        self.selectorColumnLayout.setObjectName("selectorColumnLayout")

        for k in backendObject.params:
            # Avoiding creation of a POI key column if no POIs with this key exist.
            columnCount = 0
            for i in backendObject.params[k]:
                columnCount += backendObject.POICount[i]
            if columnCount == 0:
                continue

            # Creates a vertical column for POI key
            exec("self." + k + "Layout = QtWidgets.QVBoxLayout()")
            exec("self." + k + "Layout.setObjectName('" + k + "Layout')")

            # Creates a title label with some POI key
            exec("self." + k + "TitleLabel = QtWidgets.QLabel(self.centralwidget)")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            exec("sizePolicy.setHeightForWidth(self." + k + "TitleLabel.sizePolicy().hasHeightForWidth())")
            exec("self." + k + "TitleLabel.setSizePolicy(sizePolicy)")
            exec("self." + k + "TitleLabel.setFont(self.descriptionFont)")
            exec("self." + k + "TitleLabel.setWordWrap(True)")
            exec("self." + k + "TitleLabel.setObjectName('" + widget.languagePackContents["ErrorNetworkSocketFail"] + "TitleLabel')")
            exec("self." + k + "TitleLabel.setText('" + widget.languagePackContents[k] + "')")
            exec("self." + k + "TitleLabel.setAlignment(Qt.AlignCenter)")
            exec("self." + k + "Layout.addWidget(self." + k + "TitleLabel)")

            # Creates names for every POI key and value GUI elements (eg. "shrine|wayside_shrine" would not work due to "|" symbol)
            for v in backendObject.params[k]:
                vGUI = v
                while True:
                    if "|" in vGUI:
                        i = vGUI.index("|")
                        vGUI = vGUI[:i] + vGUI[(i+1):]
                    else:
                        backendObject.POIGUINames[v] = vGUI
                        break

                # Creates a layout for a POI type text label and a spin box next to it
                exec("self." + vGUI + "Layout = QtWidgets.QHBoxLayout()")
                exec("self." + vGUI + "Layout.setObjectName('alpineHutLayout')")

                # Creates an POI type text label
                exec("self." + vGUI + "Label = QtWidgets.QLabel()")
                exec("self." + vGUI + "Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)")
                exec("self." + vGUI + "Label.setFont(POITypeFont)")
                exec("self." + vGUI + "Label.setWordWrap(True)")
                exec("self." + vGUI + "Label.setObjectName('" + vGUI + "Label')")
                exec("self." + vGUI + "Label.setText('" + widget.languagePackContents[v] + "')")
                exec("self." + vGUI + "Label.adjustSize()")
                exec("self." + vGUI + "Layout.addWidget(self." + vGUI + "Label)")

                # Creates an POI type spin box
                exec("self." + vGUI + "SpinBox = QtWidgets.QSpinBox()")
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                exec("sizePolicy.setHeightForWidth(self." + vGUI + "SpinBox.sizePolicy().hasHeightForWidth())")
                exec("self." + vGUI + "SpinBox.setSizePolicy(sizePolicy)")
                exec("self." + vGUI + "SpinBox.setObjectName('" + v + "SpinBox')")
                exec("self." + vGUI + "Layout.addWidget(self." + vGUI + "SpinBox)")
                exec("self." + vGUI + "SpinBox.setFont(POITypeFont)")
                exec("self." + vGUI + "SpinBox.setMaximum(backendObject.POICount['" + v + "'])")
                exec("self." + vGUI + "SpinBox.valueChanged.connect(self.updateSum)")
                if backendObject.POICount[v] != 0:
                    exec("self." + k + "Layout.addLayout(self." + vGUI + "Layout)")
                lastOne = (backendObject.params[k].index(v) + 1) == len(backendObject.params[k])
                if lastOne:
                    exec("spacerItem" + vGUI + " = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)")
                    exec("self." + k + "Layout.addItem(spacerItem" + v + ")")
        
            # Adds a column to the layout of all columns
            exec("self.selectorColumnLayout.addLayout(self." + k + "Layout)")

        # Adding a column layout to the vertical component layout
        self.verticalComponentLayout.addLayout(self.selectorColumnLayout)
        self.verticalLayout.addLayout(self.verticalComponentLayout)
        
        # Adding some spacing between column layout and "plan and sort" button layout
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        
        # Adding a "Plan and sort" button with its layout
        self.buttonLayout = QtWidgets.QHBoxLayout()

        self.buttonLayout.setObjectName("buttonLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonLayout.addItem(spacerItem1)

        self.planAndSortButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.planAndSortButton.sizePolicy().hasHeightForWidth())
        self.planAndSortButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.planAndSortButton.setFont(font)
        self.planAndSortButton.setObjectName("planAndSortButton")
        self.planAndSortButton.setText(widget.languagePackContents["PlanAndSort"])
        self.planAndSortButton.setEnabled(False)
        self.planAndSortButton.clicked.connect(lambda: self.planSortSwitch())
        self.buttonLayout.addWidget(self.planAndSortButton)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonLayout.addItem(spacerItem2)

        self.verticalLayout.addLayout(self.buttonLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.setCentralWidget(self.centralwidget)
        self.adjustSize()

    def planSortSwitch(self):
        backendObject.planARoute()
        widget.tourScreenResult = tourResult()
        widget.addWidget(widget.tourScreenResult)
        widget.setCurrentWidget(widget.tourScreenResult)


    def updateSum(self):
        # Counts the total amount of POIs chosen and allows/disallows confirming the user choice.
        self.chosenPOICount = 0
        for i in backendObject.POIGUINames:
            exec("self.chosenPOICount += self." + backendObject.POIGUINames[i] + "SpinBox.value()")
        if self.chosenPOICount == 69:
            for i in backendObject.POIGUINames:
                exec("self." + backendObject.POIGUINames[i] + "SpinBox.setMaximum(self." + backendObject.POIGUINames[i] + "SpinBox.value())")
        elif self.chosenPOICount == 68:
            for i in backendObject.POIGUINames:
                exec("self." + backendObject.POIGUINames[i] + "SpinBox.setMaximum(" + str(backendObject.POICount[i]) + ")")
        if self.chosenPOICount > 2:
            self.planAndSortButton.setEnabled(True)
        else:
            self.planAndSortButton.setEnabled(False)





# Final screen of MyTourMaker - it shows a map and a list of waypoints next to it, as well as buttons to make changes to a tour.
class tourResult(QMainWindow):
    def __init__(self):
        super(tourResult, self).__init__()
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # Declaring fonts used in the widget
        self.POIDescriptionFont = QtGui.QFont()
        self.POIDescriptionFont.setPointSize(15)

        self.POIRemoverFont = QtGui.QFont()
        self.POIRemoverFont.setPointSize(10)
        self.POIRemoverFont.setItalic(True)
        self.POIRemoverFont.setUnderline(True)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Adding a MapBox JS map from the backendObject
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(backendObject.mapView.sizePolicy().hasHeightForWidth())
        backendObject.mapView.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(backendObject.mapView)

        self.tourOptionLayout = QtWidgets.QVBoxLayout()
        self.tourOptionLayout.setObjectName("tourOptionLayout")

        # Adding the "Tour overview" title
        self.finalScreenTitle = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.finalScreenTitle.sizePolicy().hasHeightForWidth())
        self.finalScreenTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.finalScreenTitle.setFont(font)
        self.finalScreenTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.finalScreenTitle.setObjectName("finalScreenTitle")
        self.finalScreenTitle.setText(widget.languagePackContents["TourOverview"])
        self.tourOptionLayout.addWidget(self.finalScreenTitle)

        # Creating a scrollable area for the list of POIs on a tour (on the right side of the screen)
        self.POIListScrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.POIListScrollArea.sizePolicy().hasHeightForWidth())
        self.POIListScrollArea.setSizePolicy(sizePolicy)
        self.POIListScrollArea.setMinimumSize(QtCore.QSize(0, 100))
        self.POIListScrollArea.setWidgetResizable(True)
        self.POIListScrollArea.setObjectName("POIListScrollArea")
        self.POIListLayout = QtWidgets.QWidget()
        self.POIListLayout.setGeometry(QtCore.QRect(0, 0, 592, 1446))
        self.POIListLayout.setObjectName("POIListLayout")

        # Creating a vertical layout for all POI names and their "remove" buttons (inside the scrollable area)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.POIListLayout)
        self.verticalLayout.setObjectName("verticalLayout")

        self.updatePOIList()

        backendObject.plotRouteLine()

        self.POIListScrollArea.setWidget(self.POIListLayout)
        self.tourOptionLayout.addWidget(self.POIListScrollArea)

        # Creating "Save to file", "Add a waypoint" and "Back to menu" buttons and a layout for them
        self.tourOptionbuttonLayout = QtWidgets.QHBoxLayout()
        self.tourOptionbuttonLayout.setObjectName("tourOptionbuttonLayout")

        self.saveTourButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveTourButton.sizePolicy().hasHeightForWidth())
        self.saveTourButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.saveTourButton.setFont(font)
        self.saveTourButton.setObjectName("saveTourButton")
        self.saveTourButton.setText(widget.languagePackContents["SaveToFile"])
        self.saveTourButton.clicked.connect(lambda: self.goToTourSaver())
        self.tourOptionbuttonLayout.addWidget(self.saveTourButton)

        self.addWaypointButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addWaypointButton.sizePolicy().hasHeightForWidth())
        self.addWaypointButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.addWaypointButton.setFont(font)
        self.addWaypointButton.setObjectName("addWaypointButton")
        self.addWaypointButton.setText(widget.languagePackContents["AddAWaypoint"])
        self.addWaypointButton.clicked.connect(lambda: self.goToNewWaypointDialog())
        self.tourOptionbuttonLayout.addWidget(self.addWaypointButton)
        self.addWaypointButton.setVisible(False)
        # Waypoint can only be added if there are less than 69 waypoints (max waypoint amount)
        if len(backendObject.waypointsList) < 69:
            self.addWaypointButton.setVisible(True)

        self.backToMenuButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backToMenuButton.sizePolicy().hasHeightForWidth())
        self.backToMenuButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.backToMenuButton.setFont(font)
        self.backToMenuButton.setObjectName("backToMenuButton")
        self.backToMenuButton.setText(widget.languagePackContents["BackToMenu"])
        self.backToMenuButton.clicked.connect(lambda: self.backToMenu())
        self.tourOptionbuttonLayout.addWidget(self.backToMenuButton)

        self.tourOptionLayout.addLayout(self.tourOptionbuttonLayout)
        self.horizontalLayout.addLayout(self.tourOptionLayout)
        self.setCentralWidget(self.centralwidget)

        self.adjustSize()


    # Creating/re-creating a list of POIs on the right side of a screen (after user added/removed a waypoint)
    def updatePOIList(self):
        for p in backendObject.waypointsList:
            # Creating a layout for a waypoint icon, title and "remove" button
            exec(f'self.POIDescription{str(p["id"])}Layout = QtWidgets.QHBoxLayout()')
            exec(f'self.POIDescription{str(p["id"])}Layout.setObjectName("POIDescription{str(p["id"])}Layout")')

            # Creating an icon (for aesthetics) next to a waypoint title
            exec(f'self.POIDescription{str(p["id"])}Icon = QtWidgets.QPushButton(self.POIListLayout)')
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            exec(f'sizePolicy.setHeightForWidth(self.POIDescription{str(p["id"])}Icon.sizePolicy().hasHeightForWidth())')
            exec(f'self.POIDescription{str(p["id"])}Icon.setFlat(True)')
            exec(f'self.POIDescription{str(p["id"])}Icon.setSizePolicy(sizePolicy)')
            exec(f'self.POIDescription{str(p["id"])}Icon.setObjectName("POIDescription{str(p["id"])}Icon")')
            exec(f'self.POIDescription{str(p["id"])}Icon.setIcon' + '(QtGui.QIcon("Resources\\waypoint_icon.png"))')
            exec(f'self.POIDescription{str(p["id"])}Icon.setIconSize(QtCore.QSize(60, 50))')
            exec(f'self.POIDescription{str(p["id"])}Layout.addWidget(self.POIDescription{str(p["id"])}Icon)')
            backendObject.addMapMarker(p["tags"]["name"], p["lon"], p["lat"], p["id"])

            # Creating a waypoint title
            exec(f'self.POIDescription{str(p["id"])}Title = QtWidgets.QLabel(self.POIListLayout)')
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            exec(f'sizePolicy.setHeightForWidth(self.POIDescription{str(p["id"])}Title.sizePolicy().hasHeightForWidth())')
            exec(f'self.POIDescription{str(p["id"])}Title.setSizePolicy(sizePolicy)')
            exec(f'self.POIDescription{str(p["id"])}Title.setFont(self.POIDescriptionFont)')
            exec(f'self.POIDescription{str(p["id"])}Title.setWordWrap(True)')
            exec(f'self.POIDescription{str(p["id"])}Title.setObjectName("POIDescription{str(p["id"])}Title")')
            # If a point is a starting point, then no "remove" button or type + name in a POI description - this is made to make the interface more clear
            exec(f'self.POIDescription{str(p["id"])}Title.setText("{widget.languagePackContents["StartingPoint"]}")')

            exec(f'self.POIDescription{str(p["id"])}Layout.addWidget(self.POIDescription{str(p["id"])}Title)')

            
            if p["id"] != 0:
                # Creating a "remove" button - it removes a waypoint from the map when clicked
                exec(f'self.POIDescription{str(p["id"])}Remove = QtWidgets.QPushButton(self.POIListLayout)')
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                exec(f'sizePolicy.setHeightForWidth(self.POIDescription{str(p["id"])}Remove.sizePolicy().hasHeightForWidth())')
                (f'self.POIDescription{str(p["id"])}Remove.setSizePolicy(sizePolicy)')
                exec(f'self.POIDescription{str(p["id"])}Remove.setFont(self.POIRemoverFont)')
                exec(f'self.POIDescription{str(p["id"])}Remove.setInputMethodHints(QtCore.Qt.ImhNone)')
                exec(f'self.POIDescription{str(p["id"])}Remove.setFlat(True)')
                exec(f'self.POIDescription{str(p["id"])}Remove.setObjectName("POIDescription{str(p["id"])}Remove")')
                exec(f'self.POIDescription{str(p["id"])}Remove.setText("{widget.languagePackContents["Remove"]}")')
                exec(f'self.POIDescription{str(p["id"])}Remove.clicked.connect(lambda: backendObject.recalculateRoute({str(p["id"])}))')

                # Writing POI type + name if it is not a starting point
                exec(f'''self.POIDescription{str(p["id"])}Title.setText("{widget.languagePackContents[p["POItype"]] + " " + p["tags"]["name"]}")''')
                
                exec(f'self.POIDescription{str(p["id"])}Layout.addWidget(self.POIDescription{str(p["id"])}Remove)')

            exec(f'self.verticalLayout.addLayout(self.POIDescription{str(p["id"])}Layout)')

    # Go to the "add new waypoint" screen - it is added to "widget", but tourResult class widget is removed from "widget".
    def goToNewWaypointDialog(self):
        widget.addNewWaypointDialogObject = addNewWaypointDialog()
        widget.addWidget(widget.addNewWaypointDialogObject)
        widget.setCurrentWidget(widget.addNewWaypointDialogObject)
        widget.removeWidget(widget.tourScreenResult)

    # Initialising "tour saving" dialog - a popup appears.
    def goToTourSaver(self):
        saveToFileDialogObject = saveToFileDialog()
        saveToFileDialogObject.exec_()

    def backToMenu(self):
        # Remove all waypoint descriptions from the waypoint list on the right side of a screen
        for p in backendObject.waypointsList:
            exec(f'widget.tourScreenResult.POIDescription{p["id"]}Icon.setParent(None)')
            exec(f'widget.tourScreenResult.POIDescription{p["id"]}Title.setParent(None)')
            if p["id"] != 0:
                exec(f'widget.tourScreenResult.POIDescription{p["id"]}Remove.setParent(None)')
            exec(f'widget.tourScreenResult.POIDescription{p["id"]}Layout.setParent(None)')
            backendObject.removeMapMarker(str(p["id"]))

        backendObject.deleteRouteLine()

        backendObject.waypointsList = []
        backendObject.POIList = []

        widget.setCurrentWidget(mainMenuScreen)



# Dialog that allows to save tour details to a .txt file
class saveToFileDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Changing size of a window for user convenience, setting window title and icon
        self.resize(200, 100)
        self.setWindowTitle(widget.languagePackContents["SaveToFile"])
        self.setWindowIcon(QtGui.QIcon("Resources\\logo.ico"))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        # Creating a "Enter a file name:" title
        self.saveToFileDialogTitle = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveToFileDialogTitle.sizePolicy().hasHeightForWidth())
        self.saveToFileDialogTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.saveToFileDialogTitle.setFont(font)
        self.saveToFileDialogTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.saveToFileDialogTitle.setObjectName("saveToFileDialogTitle")
        self.saveToFileDialogTitle.setText(widget.languagePackContents["EnterFileName"])
        self.gridLayout.addWidget(self.saveToFileDialogTitle, 0, 0, 1, 2)

        # Creating dialog buttons ("Save", "Cancel") and their layout
        self.saveToFileDialogButtons = QtWidgets.QDialogButtonBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveToFileDialogButtons.sizePolicy().hasHeightForWidth())
        self.saveToFileDialogButtons.setSizePolicy(sizePolicy)
        self.saveToFileDialogButtons.setOrientation(QtCore.Qt.Horizontal)
        self.saveToFileDialogButtons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.saveToFileDialogButtons.setObjectName("saveToFileDialogButtons")
        self.gridLayout.addWidget(self.saveToFileDialogButtons, 5, 0, 1, 1)

        # Configuring layout of components
        spacerItem = QtWidgets.QSpacerItem(20, 96, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)

        # Creating a text input field
        self.saveToFileTextInput = QtWidgets.QTextEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveToFileTextInput.sizePolicy().hasHeightForWidth())
        self.saveToFileTextInput.setSizePolicy(sizePolicy)
        self.saveToFileTextInput.setObjectName("textEdit")
        self.gridLayout.addWidget(self.saveToFileTextInput, 2, 0, 1, 1)

        # Configuring layout of components
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 3, 0, 1, 1)

        # Assigning actions for "Save" and "Cancel" button interactions
        self.saveToFileDialogButtons.accepted.connect(lambda: self.saveToFile())
        self.saveToFileDialogButtons.rejected.connect(self.reject)

    # Subroutine that saves data about tour to a text file
    def saveToFile(self):
        # Checking if a file name + ".txt" already exists - returning an error message in this case
        if os.path.exists(self.saveToFileTextInput.toPlainText() + ".txt"):
            backendObject.showNonFatalError(widget.languagePackContents["ErrorFileExists"])
        else:
            # Creating a text file and writing contents of backendObject.waypointsList to a text file
            file = open((self.saveToFileTextInput.toPlainText() + ".txt"), "w", encoding="utf-8")
            file.write("Latitude, Longitude, Distance from previous waypoint, Type, Name\n")
            for i in backendObject.waypointsList[0:]:
                file.write(f""""{str(i['lat'])}", "{str(i['lon'])}", "{str(i['dist'])}", "{i['POItype']}", "{i['tags']['name']}"\n""")
            file.close()
            self.close()



# Widget that allows to add a waypoint with custom name and address to a tour.
class addNewWaypointDialog(QMainWindow):
    def __init__(self):
        super(addNewWaypointDialog, self).__init__()
        # Changing size of a window for user convenience
        widget.setMinimumSize(QtCore.QSize(420, 280))
        widget.setMaximumSize(QtCore.QSize(420, 280))
        widget.resize(420, 280)

        # Configuring layout of components
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # Creating "Add new waypoint" screen title
        self.newWaypointTitle = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newWaypointTitle.sizePolicy().hasHeightForWidth())
        self.newWaypointTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.newWaypointTitle.setFont(font)
        self.newWaypointTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.newWaypointTitle.setObjectName("newWaypointTitle")
        self.newWaypointTitle.setText(widget.languagePackContents["AddNewWaypoint"])
        self.verticalLayout.addWidget(self.newWaypointTitle)

        # Creating a text field for a new waypoint's name
        self.newWaypointName = QtWidgets.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.newWaypointName.setFont(font)
        self.newWaypointName.setObjectName("newWaypointName")
        self.newWaypointName.setPlaceholderText(widget.languagePackContents["EnterWaypointName"])
        self.verticalLayout.addWidget(self.newWaypointName)

        # Creating a text field for a new waypoint's address
        self.newWaypointAddress = QtWidgets.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.newWaypointAddress.setFont(font)
        self.newWaypointAddress.setObjectName("newWaypointAddress")
        self.newWaypointAddress.setPlaceholderText(widget.languagePackContents["EnterWaypointAddress"])
        self.verticalLayout.addWidget(self.newWaypointAddress)

        # Configuring layout of components
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonLayout.addItem(spacerItem)

        # Creating "Add" button
        self.addNewWaypointButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addNewWaypointButton.sizePolicy().hasHeightForWidth())
        self.addNewWaypointButton.setSizePolicy(sizePolicy)
        self.addNewWaypointButton.setObjectName("addNewWaypointButton")
        self.addNewWaypointButton.setText(widget.languagePackContents["Add"])
        self.addNewWaypointButton.clicked.connect(lambda: self.validateNewWaypoint())
        self.buttonLayout.addWidget(self.addNewWaypointButton)

        # Creating "Cancel" button
        self.cancelNewWaypointButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelNewWaypointButton.sizePolicy().hasHeightForWidth())
        self.cancelNewWaypointButton.setSizePolicy(sizePolicy)
        self.cancelNewWaypointButton.setObjectName("cancelNewWaypointButton")
        self.cancelNewWaypointButton.setText(widget.languagePackContents["Cancel"])
        self.cancelNewWaypointButton.clicked.connect(lambda: self.cancelNewWaypoint())
        self.buttonLayout.addWidget(self.cancelNewWaypointButton)

        # Configuring layout of components
        self.verticalLayout.addLayout(self.buttonLayout)
        self.setCentralWidget(self.centralwidget)

    def validateNewWaypoint(self):
        # Checking if a user-entered address exist
        OSMObject = nominatim.query(self.newWaypointAddress.toPlainText()).toJSON()
        if len(OSMObject) > 0:
            # Removing all POI description (list on the right side of "tour result" screen) and their MapBox map markers
            for p in backendObject.waypointsList:
                exec(f'widget.tourScreenResult.POIDescription{p["id"]}Icon.setParent(None)')
                exec(f'widget.tourScreenResult.POIDescription{p["id"]}Title.setParent(None)')
                if p["id"] != 0:
                    exec(f'widget.tourScreenResult.POIDescription{p["id"]}Remove.setParent(None)')
                exec(f'widget.tourScreenResult.POIDescription{p["id"]}Layout.setParent(None)')
                backendObject.removeMapMarker(str(p["id"]))

            # Adding a new waypoint to the end of "backendObject.waypointsList", sorting that list, removing route directions line
            backendObject.waypointsList.append({
                "lat" : OSMObject[0]["lat"],
                "lon" : OSMObject[0]["lon"],
                "id" : random.randint(1, 99999999999),
                "POItype":"custom",
                "tags":{"name":self.newWaypointName.toPlainText()}
            })
            backendObject.POIList = backendObject.waypointsList
            backendObject.sortARoute()
            backendObject.deleteRouteLine()

            # Resetting window size to a standard
            self.screenWidth = app.primaryScreen().size().width()
            self.screenHeight = app.primaryScreen().size().height()
            widget.setMinimumSize(QtCore.QSize(1280, 720))
            widget.setMaximumSize(QtCore.QSize(3840, 2160))
            widget.resize((int(self.screenWidth * 0.66)), (int(self.screenHeight * 0.66)))

            # Going back to "tour result" screen
            widget.tourScreenResult = tourResult()
            widget.addWidget(widget.tourScreenResult)
            if len(backendObject.waypointsList) == 70:
                widget.tourScreenResult.addWaypointButton.setVisible(False)
            widget.setCurrentWidget(widget.tourScreenResult)
            widget.removeWidget(widget.addNewWaypointDialogObject)
        else:
            backendObject.showNonFatalError(widget.languagePackContents["ErrorAddressDoesNotExist"])


    def cancelNewWaypoint(self):
        # Resetting window size to a standard, going back to "tour result" screen
        self.screenWidth = app.primaryScreen().size().width()
        self.screenHeight = app.primaryScreen().size().height()
        widget.setMinimumSize(QtCore.QSize(1280, 720))
        widget.setMaximumSize(QtCore.QSize(3840, 2160))
        widget.resize((int(self.screenWidth * 0.66)), (int(self.screenHeight * 0.66)))
        widget.tourScreenResult = tourResult()
        widget.addWidget(widget.tourScreenResult)
        widget.setCurrentWidget(widget.tourScreenResult)
        widget.removeWidget(widget.addNewWaypointDialogObject)



class backend(QMainWindow):
    def __init__(self):
        super(backend, self).__init__()
        self.params = {
	        "amenity" : ["bar", "cafe", "fast_food", "restaurant", "cinema", "arts_centre", "nightclub", "theatre", "casino", "exhibition_centre", "fountain", "planetarium", "townhall", "clock", "library"],
            "building" : ["church", "cathedral", "mosque", "synagogue", "monastery", "temple"],
            "historic" : ["shrine|wayside_shrine|wayside_cross", "castle", "aircraft|ship|tank", "aqueduct", "tower", "monument"],
            "shop" : ["gift", "convenience", "supermarket"],
            "leisure" : ["park", "swimming_area", "stadium", "ice_rink"],
            "tourism" : ["alpine_hut", "aquarium", "artwork", "theme_park", "museum", "viewpoint", "zoo"]
        }
        self.POIGUINames = {}

        self.servers = ["https://overpass.kumi.systems", "https://lz4.overpass-api.de", "https://z.overpass-api.de", "https://overpass.openstreetmap.ru"]

    # Function that attempts connection to an IP passed
    def tryDNSConnect(self, ip):
        # Creating an IPv4 TCP socket
        try:
            sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            self.showNonFatalError(widget.languagePackContents["ErrorNetworkSocketFail"])
        try:
            # Connection attempt to an IP address
            sck.connect((ip, 443))
            available = True
            sck.close
        except:
            available = False
        return(available)


    # Finding an available Overpass API server using a sample request
    def findOPAPIServer(self):
        self.OPServerOnline = False
        # Searching withing built-in servers first
        for chosenServer in self.servers:
            try:
                response = requests.get(f'{chosenServer}/api/interpreter?data=[out:json][timeout:180];node(around:10,56.948,24.1054)["shop"="gift"];out skel qt;', timeout = 5)
                if response.ok:
                    # Saving API url + some basic request parameters
                    self.chosenServer = chosenServer + "/api/interpreter?data="
                    self.OPServerOnline = True
                    break
                else:
                    self.showNonFatalError(f"Overpass API server {chosenServer} returned an error: {response.status_code}. Maybe the temporary quota for it has been exceeded")
            except:
                self.showNonFatalError(f"{chosenServer} {widget.languagePackContents['ErrorOverpassServer']}")

        if not(self.OPServerOnline):
            # Letting a user enter a custom Overpass API server homepage url
            overpassErrorPopUpScreen = overpassErrorPopUp()
            widget.addWidget(overpassErrorPopUpScreen)
            widget.setCurrentWidget(overpassErrorPopUpScreen)

    def checkConnection(self):
        try:
            # Resolving www.openstreetmap.org IP address, then connecting to it
            ip = socket.gethostbyname('www.openstreetmap.org')
            osm_available = self.tryDNSConnect(ip)
        except:
            osm_available = False
            pass

        if osm_available:
            # Looking for an available Overpass API server.
            self.findOPAPIServer()
            
        else:
            self.showNonFatalError(widget.languagePackContents["OSMConnectionError"])
            # Trying to connect to Cloudflare and Google DNS servers (uptime > 99.9% )
            google_available = self.tryDNSConnect("8.8.8.8")
            cf_available = self.tryDNSConnect("1.1.1.1")

            # Suggesting a way to fix connectivity issues
            if not(google_available or cf_available):
                self.showFatalError(widget.languagePackContents["ErrorNoInternetConnection"])
            elif google_available != cf_available:
                self.showFatalError(widget.languagePackContents["ErrorCheckFirewall"])
            else:
                self.showFatalError(widget.languagePackContents["ErrorOSMUnavailable"])

    # Finding the starting point for a trip
    def findStartingPointAutomatically(self):
        # Find the location of an IP address
        try:
    	    # Check connection to IPAPI servers, if successful - request an IP address latitude and longitude
            socket.gethostbyname("www.ip-api.com")
            self.startpos = requests.get("http://ip-api.com/json/?fields=lat,lon")
            self.startpos = self.startpos.json()
        except:
            self.showNonFatalError(backendObject, widget.languagePackContents["ErrorIPGeoAddressFail"])
            quit()

        # Creating a Chromium browser GUI widget
        self.mapView = QtWebEngineWidgets.QWebEngineView()
        self.mapView.setObjectName("mapView")

        # Opening Mapbox GL JavaScript framework base file in our Chromium widget
        with open('Resources\mapboxjs.html', 'r') as file:
            mapHTML = file.read()
        self.mapView.setHtml(mapHTML)

        # Loading everything needed for the MapBox JS map
        self.mapView.page().loadFinished.connect(lambda: self.mapView.page().runJavaScript("mapboxgl.accessToken = '" + APIData["mapboxToken"] + "';"))

        # Initialising map components and changing map language to an active MyTourMaker language.
        self.mapView.page().loadFinished.connect(lambda: self.mapView.page().runJavaScript("map = new mapboxgl.Map({container: 'map', style: '" + APIData["activeMapURL"] + "',center: [" + str(self.startpos["lon"]) + ","+ str(self.startpos["lat"]) + "], zoom: 11, projection: 'globe'}); " + "map.setLanguage('" + widget.languagePackContents["LanguageCode"] + "');"))

        # Add a starting point marker
        self.mapView.page().loadFinished.connect(lambda: self.addMapMarker(widget.languagePackContents["StartingPoint"], self.startpos["lon"], self.startpos["lat"], 0))

            
    def findStartingPointManually(self, userResponse):
        OSMObject = nominatim.query(userResponse).toJSON()

        if len(OSMObject) > 0:
            self.startpos = {
                "lat" : OSMObject[0]['lat'], 
                "lon" : OSMObject[0]['lon']
            }
            # Remove an existing starting point marker
            self.removeMapMarker("0")

            # Add a new starting point marker
            self.addMapMarker(widget.languagePackContents["StartingPoint"], self.startpos["lon"], self.startpos["lat"], 0)

            self.mapView.page().runJavaScript("map.flyTo({center:["+ self.startpos["lon"] + ", " + self.startpos["lat"] + "], zoom:11, speed:0.4})")

            backendObject.detStartPointYesButton.show()
        else:
            self.showNonFatalError(widget.languagePackContents["ErrorNominatimAddressSearch"])

    # Integration of planARoute function from the development stage 2 - it uses random sampling to add POIs of required types to POIList list.
    def planARoute(self):
        widget.POIPlannerScreen.planAndSortButton.setEnabled(False)
        userResponse = {}
        for k in self.POIGUINames:
            exec("userResponse['" + k + "'] = widget.POIPlannerScreen." + self.POIGUINames[k] + "SpinBox.value()")
            exec("widget.POIPlannerScreen." + self.POIGUINames[k] + "SpinBox.setEnabled(False)")

        self.POIList = []
        self.POIList.append({"id":0, "lat":self.startpos["lat"], "lon":self.startpos["lon"], "dist":0,"POItype":widget.languagePackContents["StartingPoint"], "tags":{"name":widget.languagePackContents["StartingPoint"]}})

        for k in userResponse:
			# Skipping an iteration over the OSM POI value k if no POIs are required.
            if userResponse[k] == 0:
                continue
            else:
                coordList = []
                # All POIs of with the OSM value k are added to the coordList list for convenience.
                for p in self.allPOIs[k]:
                    coordList.append(p)
				# r elements are randomly selected from coordlist and added to the POIList list, whilst at the same time being removed from the coordList list.
                for p in range(0, userResponse[k], 1):
                    r = random.randint(0, (len(coordList) - 1))
                    self.POIList.append(coordList[r])
                    coordList.pop(r)

        self.sortARoute()

    #Sorting the list of coordinates so that there would be minimal sum of displacements between them
    def sortARoute(self):
    	# Add a starting point to waypointsList, remove from POIList
        self.waypointsList = [self.POIList[0]]
        self.POIList.pop(0)
        startPosPosition = 0

        while (len(self.POIList)) > 0:
    		# Finding a distance from the last waypoint in List list to every coordinate in POIList
            for lastPoint in self.POIList:
                lastPoint["dist"] = distance.distance((self.waypointsList[startPosPosition]["lat"],  self.waypointsList[startPosPosition]["lon"]), (lastPoint["lat"], lastPoint["lon"])).m

            # Insertion sort of POIList coordinates
            for i in range(1, len(self.POIList)):
                current = self.POIList[i]
                i2 = i
                while (i2 > 0) and (self.POIList[i2 - 1]["dist"] > current["dist"]):
                    self.POIList[i2] = self.POIList[i2 - 1]
                    i2 = i2 - 1
                self.POIList[i2] = current

    		# Adding the nearest to a last waypointsList coordinate coordinates to the  waypointsList list and removing the nearest to a last waypointsList coordinate   coordinate from the POIList list.
            self.waypointsList.append(self.POIList[0])
            self.POIList.pop(0)
            startPosPosition += 1

        # Sorted list of the tour's coordinates (for debugging):
        print("Sorted list of the tour's coordinates:")
        print(f"{str(self.waypointsList[0]['lat'])},{str(self.waypointsList[0]['lon'])} Starting position")
        for i in self.waypointsList[1:]:
            if not("name" in i["tags"]):
                i["tags"]["name"] = "Unknown"
            print(f"{str(i['lat'])},{str(i['lon'])} distance: {str(i['dist'])} type: {i ['POItype']} name: {i['tags']['name']}")



    def recalculateRoute(self, toBeRemoved):
        # Remove all waypoint descriptions from the waypoint list on the right side of a screen
        for p in self.waypointsList:
            exec(f'widget.tourScreenResult.POIDescription{p["id"]}Icon.setParent(None)')
            exec(f'widget.tourScreenResult.POIDescription{p["id"]}Title.setParent(None)')
            if p["id"] != 0:
                exec(f'widget.tourScreenResult.POIDescription{p["id"]}Remove.setParent(None)')
            exec(f'widget.tourScreenResult.POIDescription{p["id"]}Layout.setParent(None)')
            self.removeMapMarker(str(p["id"]))

        # Deleting a route line
        self.deleteRouteLine()

        # Finding the element that needs to be removed, making a new route and route line, creating new list of waypoints.
        for p in range(0, len(self.waypointsList)):
            if self.waypointsList[p]["id"] == toBeRemoved:
                self.POIList = self.waypointsList[:p] + self.waypointsList[(p+1):]
                # Sorting a route again
                self.sortARoute()
                # Sending a new OpenRouteService API request when a change is made to the list of tour's waypoints.
                self.plotRouteLine()
                widget.tourScreenResult.updatePOIList()
                if len(backendObject.waypointsList) < 70:
                    widget.tourScreenResult.addWaypointButton.setVisible(True)
                break


    # Add a new MapBox JS map marker
    def addMapMarker(self, name, lon, lat, id):
        self.mapView.page().runJavaScript("popup" + str(id) + " = new mapboxgl.Popup({ offset: 25 }).setText(`" + name + "`); marker" + str(id) + " = new mapboxgl.Marker({color:'#FF543D'}).setLngLat([" + str(lon) + ", " + str(lat) + "]).addTo(map); marker" + str(id) + ".setPopup(popup" + str(id) + ");")


    def plotRouteLine(self):
        # Preparing data to send to the openrouteservice.org API (header is stored in ORSHeaders and main content of a request is stored in ORSJSON dictionary)
        ORSHeaders = {
            'Accept': 'application/geo+json; charset=utf-8',
            'Authorization': APIData["openRouteServiceToken"],
            'Content-Type': 'application/json; charset=utf-8'
        }

        ORSJSON = {
            "coordinates" : [ [self.waypointsList[0]["lon"], self.waypointsList[0]["lat"]] ],
            "radiuses" : 500,
            "geometry_simplify" : "false"
        }

        # Adding all waypoint coordinates in a formart suitable for OpenRouteService API
        for i in self.waypointsList[1:]:
            ORSJSON["coordinates"].append([i["lon"], i["lat"]])

        # Sending an openrouteservice API request and in case of success add a route line on a map
        response = requests.post(f"https://api.openrouteservice.org/v2/directions/{backendObject.transportType}/geojson", json=ORSJSON, headers=ORSHeaders)
        if response.status_code == 200:
            response = response.json()
            self.mapView.page().runJavaScript("map.addSource('route', {'type': 'geojson','data': " + str(response) + "}); map.addLayer({'id': 'route', 'type': 'line', 'source': 'route', 'layout': {'line-join': 'round', 'line-cap': 'round'}, 'paint': {'line-color': '#00b0ff', 'line-width': 8}});")
        else:
            # self.showNonFatalError("openrouteservice.org did not return a valid GeoJSON response!")
            backendObject.showNonFatalError(widget.languagePackContents["ErrorORSAPI"])


    # Remove an existing map marker and its corresponding popup
    def removeMapMarker(self, id):
        self.mapView.page().runJavaScript(("marker" + str(id)) + ".remove(); popup" + str(id) + ".remove();")


    # Deleting a route line and data stored about the line in a MapBox JS HTML page using JavaScript.
    def deleteRouteLine(self):
        self.mapView.page().runJavaScript('map.removeLayer("route"); map.removeSource("route");')


    def showFatalError(self, errorMessage):
        errorPopUpScreen = errorPopUp(errorMessage)
        widget.addWidget(errorPopUpScreen)
        widget.setCurrentWidget(errorPopUpScreen)


    def showNonFatalError(self, errorMessage):
        QtWidgets.QMessageBox.warning(widget, widget.languagePackContents["Error"], errorMessage, QtWidgets.QMessageBox.Ok)


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()


# Creating a backend (non-GUI) processes object
backendObject = backend()

# Creating main menu "screen" - group of GUI elements (eg. buttons, labels, textboxes etc.) that can be instantly called without recreation of program window.
mainMenuScreen = mainMenu(widget)

widget.show()
sys.exit(app.exec_())