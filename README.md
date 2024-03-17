# Monument-Information-System

```markdown
Historical Building Information System

The Historical Building Information System is a Python application that utilizes Firebase Firestore
as a database to store information about historical buildings.
It leverages the Google Maps API to display maps and integrates the Bokeh and Tkinter libraries
for visualization and user interface components, respectively.

## Features
- Store and retrieve information about historical buildings from Firebase Firestore.
- Display maps using the Google Maps API.
- Interactive visualization with Bokeh.
- User-friendly interface with Tkinter.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Sreeharij/Monument-Information-System
   cd Monument-Information-System
   ```

1. Install the required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Run the setup.py file
   '''bash
      python3 -m setup.py
   
   '''
4. Set up Firebase Firestore:
   - Create a Firebase project and set up Firestore.
   - Generate a service account key and download the JSON file.
   - Rename the JSON file to `firebase_credentials.json` and place it in the project directory.

## Usage
1. Run the application:
   '''bash
      python -m gui.py
   '''

3. Use the application to:
   - Add, edit, or delete information about historical buildings.
   - View maps with building locations.
   - Interact with visualizations using Bokeh.

## Contributing
Contributions are welcome! If you have any ideas, suggestions, or bug fixes, please submit an issue or a pull request.

## License
This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

## Acknowledgements
- [Firebase](https://firebase.google.com/) - Backend database storage.
- [Google Maps API](https://developers.google.com/maps/documentation) - Map display.
- [Bokeh](https://bokeh.org/) - Interactive visualization library.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI toolkit for Python.
