import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # Importing messagebox module
from tkinter import StringVar
from tkhtmlview import HTMLLabel
from tkinter import filedialog
import webbrowser
import os,shutil
import subprocess
import threading

from tkinterweb import HtmlFrame
from tkinter import *

LOCAL_DATABASE_FOLDER = ".local_database"
PUSH_TO_FIREBASE_SCRIPT = "push_to_firebase.py"
     

data = {
    'name': ['Eiffel Tower', 'Colosseum', 'Taj Mahal'],
    'location': ['Paris', 'Rome', 'Agra'],
    'lat': [48.85854653973208,41.89044977553127, 27.175421567587666],
    'lon': [ 2.294459839805637,  12.492230897202111,  78.04201345072921],   
}

LARGEFONT =("Verdana", 20)

class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp 
	def __init__(self, *args, **kwargs): 
		
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		self.title("Historical Database Management System")
		
		# creating a container
		container = tk.Frame(self) 
		container.pack(side = "top", fill = "both", expand = True) 

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {} 

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (StartPage, Database, Map, Add_Monument):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with 
			# for loop
			self.frames[F] = frame 

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(StartPage)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Centering the labels and buttons
        self.grid_columnconfigure(0, weight=1)  # First column
        self.grid_columnconfigure(1, weight=1)  # Second column

        welcome_label = ttk.Label(self, text="Welcome to Map of History", font=LARGEFONT)
        welcome_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        select_label = ttk.Label(self, text="Select an option", font=LARGEFONT)
        select_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        button1 = ttk.Button(self, text="View Database", command=lambda: controller.show_frame(Database))
        button1.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        button2 = ttk.Button(self, text="View Map", command=lambda: controller.show_frame(Map))
        button2.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        button3 = ttk.Button(self, text="Add Historical Monument", command=lambda: controller.show_frame(Add_Monument))
        button3.grid(row=4, column=0, columnspan=2, padx=10, pady=10)



		

class Database(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Database", font=LARGEFONT)
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # Create Listbox to display names
        self.listbox = tk.Listbox(self, width=30, height=10)
        self.listbox.grid(row=1, column=0, padx=10, pady=10, rowspan=3, columnspan=2)

        button1 = ttk.Button(self, text ="View map",
							command = lambda : controller.show_frame(Map))
	
		# putting the button in its place by 
		# using grid
        button1.grid(row=4, column=3, padx=10, pady=10, sticky='se')

		# button to show frame 3 with text
		# layout3
        button2 = ttk.Button(self, text ="Go back to Home page",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place by
		# using grid
        button2.grid(row=5, column=3, padx=10, pady=10, sticky='se')
       

        # Search entry
        search_label = ttk.Label(self, text="Search by Name:")
        search_label.grid(row=1, column=2, padx=10, pady=10, sticky='e')
        self.search_entry = ttk.Entry(self)
        self.search_entry.grid(row=1, column=3, padx=10, pady=10)
        self.search_entry.bind("<Return>", self.populate_listbox)


        # Location filter
        location_label = ttk.Label(self, text="Filter by Location:")
        location_label.grid(row=2, column=2, padx=10, pady=10, sticky='e')
        self.location_entry = ttk.Entry(self)
        self.location_entry.grid(row=2, column=3, padx=10, pady=10)
        self.location_entry.bind("<Return>", self.populate_listbox)

        # Button to show location details
        show_location_button = ttk.Button(self, text="Tell me More", command=self.show_location_details)
        show_location_button.grid(row=3, column=2, padx=10, pady=10, columnspan=2)

        # Populate Listbox with names
        self.populate_listbox()

    def populate_listbox(self, event=None):
        selected_location = self.location_entry.get()
        selected_name= self.search_entry.get()
        if selected_name:
            self.listbox.delete(0, tk.END)
            for index, name in enumerate(data['name']):
                if name.lower() == selected_name.lower():
                    self.listbox.insert(tk.END, data['name'][index])
             
        elif selected_location:
            self.listbox.delete(0, tk.END)
            for index, location in enumerate(data['location']):
                if location.lower() == selected_location.lower():
                    self.listbox.insert(tk.END, data['name'][index])
        else:
            self.listbox.delete(0, tk.END)
            for name in data['name']:
                self.listbox.insert(tk.END, name)

    def show_location_details(self):
          selected_index = self.listbox.curselection()
          if selected_index:
            selected_name = self.listbox.get(selected_index)
            index = data['name'].index(selected_name)
            selected_location = data['location'][index]
            messagebox.showinfo("About", f"Name: {selected_name}\nLocation: {selected_location}")
          else:
            messagebox.showerror("Error", "Please select a name.")

class Map(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)


        html = f"""
        <h1>Interactive Maps</h1>

        <p>Click <a href="gmap.html">on the map</a> to visit view these monuments.</p>
        """
       
        
        html_label = HTMLLabel(self, html=html)
        html_label.pack(fill=tk.BOTH, expand=True)

class Add_Monument(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Add Monument", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)      

        # Entry fields
        search_label = ttk.Label(self, text="Enter Name:")
        search_label.grid(row=1, column=2, padx=10, pady=10, sticky='e')
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=1, column=3, padx=10, pady=10)

        location_label = ttk.Label(self, text="Enter Location:")
        location_label.grid(row=2, column=2, padx=10, pady=10, sticky='e')
        self.location_entry = ttk.Entry(self)
        self.location_entry.grid(row=2, column=3, padx=10, pady=10)

        latitude_label = ttk.Label(self, text="Enter Latitude:")
        latitude_label.grid(row=3, column=2, padx=10, pady=10, sticky='e')
        self.latitude_entry = ttk.Entry(self)
        self.latitude_entry.grid(row=3, column=3, padx=10, pady=10)
       
        longitude_label = ttk.Label(self, text="Enter Longitude:")
        longitude_label.grid(row=4, column=2, padx=10, pady=10, sticky='e')
        self.longitude_entry = ttk.Entry(self)
        self.longitude_entry.grid(row=4, column=3, padx=10, pady=10)

        browse_image_label = ttk.Label(self,text = "Add Image: ")
        browse_image_label.grid(row=5, column=2, padx=10, pady=10, sticky='e')
        btn_browse = ttk.Button(self,text="Browse",command=self.browse_file)
        btn_browse.grid(row=5, column=3, padx=10, pady=10, sticky='se')

        # Button to add monument
        add_button = ttk.Button(self, text="Add Monument", command=self.add_monument)
        add_button.grid(row=6, column=2, columnspan=2, padx=10, pady=10)

        button1 = ttk.Button(self, text="View map", command=lambda: controller.show_frame(Map))
        button1.grid(row=7, column=3, padx=10, pady=10, sticky='se')

        # Button to navigate to the Home page
        button2 = ttk.Button(self, text="Go back to Home page", command=lambda: controller.show_frame(StartPage))
        button2.grid(row=57, column=3, padx=10, pady=10, sticky='se')
       
    def browse_file(self):
        self.file_path = filedialog.askopenfile().name

    def add_monument(self):
        # Get values from entry fields
        name = self.name_entry.get()
        location = self.location_entry.get()
        latitude = self.latitude_entry.get()
        longitude = self.longitude_entry.get()
        file_path = self.file_path

        # Add monument to your data
        data['name'].append(name)
        data['location'].append(location)
        data['lat'].append(float(latitude))
        data['lon'].append(float(longitude))

        # Optionally, you may want to clear the entry fields after adding the monument
        self.name_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.latitude_entry.delete(0, tk.END)
        self.longitude_entry.delete(0, tk.END)
        if(name not in os.listdir(LOCAL_DATABASE_FOLDER)):
            os.mkdir(os.path.join(LOCAL_DATABASE_FOLDER,name))
        with open(os.path.join(LOCAL_DATABASE_FOLDER,name,"coordinates.txt"),"wt") as f:
             string_val = str(latitude) + "\n" + str(longitude)
             f.write(string_val)
        with open(os.path.join(LOCAL_DATABASE_FOLDER,name,"location.txt"),"wt") as f:
             string_val = str(location) + "\n"
             f.write(string_val)
        subprocess.run(["python3",PUSH_TO_FIREBASE_SCRIPT,LOCAL_DATABASE_FOLDER,name,file_path])
        shutil.rmtree(os.path.join(LOCAL_DATABASE_FOLDER,name))
        

app = tkinterApp()
app.geometry("1000x800")
app.mainloop()
