import hasher
import datetime

FILE_LOCATION = "./log.txt"

class Logger:
    file_location = FILE_LOCATION
    max_len = 10
    
    def __init__(self):
        # create log file if not exists
        with open(self.file_location, "a+") as _:
            pass
    
    def add_log(self, event):            
        with open(self.file_location, "a+") as f:
            f.write(hasher.encrypt(event.get_line()) + "\n")
        
    def remove_first_line(self):
        new_rows = self.get_rows()[1:]
        
        with open(self.file_location, "w") as f:
            for r in new_rows:
                f.write(r)
    
    def show_log(self):
        with open(self.file_location, "r") as f:
            for idx,l in enumerate(f):
                print(f"[{idx}] {hasher.decrypt(l)}")
                print("-"*32)
                
    def get_rows(self) -> list[str]:
        with open(self.file_location, "r") as f:
            return list(f.readlines())
                
    def get_row_count(self) -> int:
        """Returns the current amount of 
        lines in the log file
        """
        return len(self.get_rows())

class Event:
    def __init__(self, event_type, user, description, sus):
        self.event_type = event_type
        self.date = datetime.datetime.now()
        self.username = user
        self.info = description
        self.sus = sus
        
    def when(self) -> tuple[str, str]:
        """Returns a tuple of the time
        when the event occured in the format
        (YYYY-MM-DD, HH:MM)
        """
        d = self.date
        m = "{number:02}".format(number=int(d.minute))
        s = "{number:02}".format(number=int(d.second))
        
        return (f"{d.day}-{d.month}-{d.year}", f"{d.hour}:{m}:{s}")
    
    def get_line(self):
        return f"{self.when()[0]};{self.when()[1]};{self.username};{self.info};{self.sus};"
        
if __name__ == "__main__":
    l = Logger()
    e = Event("failed login", "me", "I failed login sorri", "no")
    
    print(e.when())
    l.add_log(e)