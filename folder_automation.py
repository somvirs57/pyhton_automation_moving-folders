import time 
import os
import shutil
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler 

class OnMyWatch:
    
    def __init__(self):
        self.observer = Observer()
        
    
    def run(self):
        event_handler = Handler() 
        
        self.observer.schedule(event_handler, source_dir, recursive=True)
        self.observer.start()
        
        try:
            while True:
                time.sleep(10)
        except: 
            self.observer.stop()
            print("observer stopped")
            
        self.observer.join()
        

class Handler(FileSystemEventHandler):

    def on_modified(self, event):
        # necessary to put the folder name as (example - destination), this will determine where the 
        # folder will be sent
        #check if we get folder
        if event.is_directory:
            for folder in os.listdir(source_dir):
                if folder != 'folder_automation.py':
                    # splitting the file name and destination (example - python)
                    # it means we want to send the example folder to python destination
                    file,dest = folder.split('-')
                    file = file.strip()                 # removing the extra white space
                    dest = dest.strip().lower()         # removing extra whitespace and making lowercase
                
                    #renaming the folder to required name after removing hyphen(-) from name
                    folder_source = os.path.join(source_dir,file)
                    os.rename(os.path.join(source_dir,folder),folder_source)
                
                    #getting the destination directory from dictionary
                    folder_destination = destination_sources[dest]
                    
                    #calling move_file method that will move the folder to required destination
                    self.move_file(file,folder_source,folder_destination)
                
                
    @staticmethod                
    def move_file(file, source, destination):
        # same file name if the destination folder is empty
        new_name = file
        # if the destination folder is not empty
        for folder in os.listdir(destination):
            i = 1
            
            #checking if file exists
            file_exists = os.path.exists(os.path.join(destination,new_name))
            while file_exists:
                #using iterator i to give new name to folder if same name exists in destination
                new_name = new_name.strip(" "+str(i))
                i += 1
                new_name = new_name + " " + str(i)
                file_exists = os.path.exists(os.path.join(destination,new_name))
            
        #creating destination directory name as it is necessary in moving     
        new_dest_name = os.path.join(destination, new_name)
        
        #moving folder from source to destination
        shutil.move(source,new_dest_name)
            
               
source_dir = r'C:\Users\somvi\Desktop\Automate files'

destination_sources = {"android": r'C:\Users\somvi\Desktop\android studio',
                       "python": r'C:\Users\somvi\Desktop\Python programming'}    
    
if __name__ == "__main__":
    watch = OnMyWatch()
    watch.run()
    
    
    
    
    
    
    
    
    
    
    
    
    