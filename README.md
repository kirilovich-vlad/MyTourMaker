<p align="center">
  <img src="https://raw.githubusercontent.com/kirilovich-vlad/MyTourMaker/main/Resources/logo.png" alt="project logo" width=15% height=15%>
</p>

# About MyTourMaker
MyTourMaker is a program for planning tours, visiting attractions and learning about surroundings in a more convenient way. 

Making tours of an unknown (or even known) city can take several hours and lots of internet research. Why would we do that when we can use detailed maps that are available to everyone online?

MyTourMaker uses OpenStreetMap data to generate bespoke tours in real world cities, considering preferred transport type, attractions and search radius.

# Video introduction:
https://www.youtube.com/watch?v=ZVXfoRSrRUI

# Dependencies
MyTourMaker uses following APIs:
- https://openrouteservice.org/ for generating navigation route lines
- https://overpass.kumi.systems - main public Overpass API instance
- https://lz4.overpass-api.de - 2nd public Overpass API instance
- https://z.overpass-api.de - 3rd public Overpass API instance
- https://overpass.openstreetmap.ru - 4th public Overpass API instance

Overpass API serves data about custom parts of OpenStreetMap data. In MyTourMaker, there are multiple hard-coded public Overpass API providers, but if all of them will ever be unavailable, user can enter their own preferred Overpass API URL.

MyTourMaker uses Mapbox GL JS, developed by Mapbox - JavaScript library that allows to implement vector maps on the web. It is used in MyTourMaker to show interactive map with waypoints and a route line.

MyTourMaker has the GUI implemented using PyQt5 - Python implementation of Qt, developed by Riverbank Computing. I chose PyQt5 because it can be executed on both Windows and UNIX-like systems, as well as its diverse functionality.

MyTourMaker uses GeoPy for some computations with geodesic formulas.

MyTourMaker uses OSMPythonTools for convenient implementation of Nominatim API - https://github.com/mocnik-science/osm-python-tools .

Nominatim API finds locations on Earth by their name and/or address. I used OSMPythonTools library to save time during development.

# Execution
In order to execute MyTourMaker, "Resources" subdirectory and "settings.json" file both have to be in the same directory as source code/executable file of MyTourMaker. 

You can download an executable for x86 Windows systems [here](https://drive.google.com/drive/folders/1UOuvpxNFq8haI-Hrqq-XD8r5ktCujJrM?usp=sharing).

Using the link above, you can download and launch the program without worrying about the dependencies. MyTourMaker works well on Windows 8, 8.1, 10, 11.

# Compilation/interpretation
In order to compile/interpret MyTourMaker from its source code, following Python packages and their dependencies have to be installed:
- pip install PyQt5
- pip install qt_material
- pip install OSMPythonTools
- pip install requests
- pip install geopy
- pip install PyQtWebEngine

In order to compile MyTourMaker, you need to make changes to make changes to the “qt_material” Python library. I have modified the stylesheet to improve the aesthetics. Go to your_python_directory/Lib/site_packages/qt_material and replace the “material.css.template” file with the file that I have saved in the “Resources” directory. Without replacing the file, the GUI of the program you compile may work incorrectly.

Don't forget to enter your own Mapbox API token and OpenRouteService API token - please search for "enter.your.token" strings in the code.

# Plans, thoughts
This was my coursework back in college - I had a lack of time and excess of curiosity/ambition then (I still have both in university :)). In my opinion, this led to the need of major code refactoring in the future + possible replacement of Openrouteservice to Mapbox due to better free tier of the directions API.


