from tkinter import *
from tkinter import font as tkFont
import pyautogui, pathlib, traceback # , pytesseract, datetime
#from PIL import Image

class Application():
    def __init__(self, master):
        self.master = master
        self.rect = None
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None

        root.configure(background = '#2B2D42')
        # root.attributes("-transparentcolor","red")
        
        width = 385 #root.winfo_width()
        height = 210 #root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2) 
        y = (root.winfo_screenheight() // 2) - (height // 2) 
               
        #root.attributes("-transparent", "white")
        root.geometry('{}x{}+{}+{}'.format(width, height, x, y)) #275x150' +200+200') #'400x50+200+200')  # set new geometry
        root.title('Screenshot App')
        root.resizable(0, 0) #Don't allow resizing in the x or y direction
        
        self.fileName_frame = Frame(master, background="#2B2D42")
        self.fileName_frame.pack(fill=BOTH, expand=YES, side=TOP)

        self.lblFileName = Label(self.fileName_frame, width=25, height=2, background="#2B2D42", foreground='#F2EDEB')
        self.lblFileName["text"] = "Name of file without extension : "
        self.lblFileName["font"] = tkFont.Font(family='Helvetica', size=10, weight='bold') #, background='#F2EDEB')
        #self.lblFileName.grid(row=0, column=0)
        self.lblFileName.pack(side=TOP)
        
        self.tbFileName = Entry(self.fileName_frame, width=39, background="#F2EDEB", foreground='#2B2D42')
        self.tbFileName["text"] = ""
        self.tbFileName["font"] = tkFont.Font(family='Helvetica', size=12, weight='bold') #, background='#F2EDEB')
        self.tbFileName.focus()
        #self.tbFileName.grid(row=0, sticky=N+W+E)
        #self.tbFileName.bind('<Return>', self.createScreenCanvas)
        self.tbFileName.pack(side=TOP)
        
        self.lblFileExtension = Label(self.fileName_frame, width=15, height=1, background="#2B2D42", foreground='#F2EDEB')
        self.lblFileExtension["text"] = "" #".png"
        self.lblFileExtension["font"] = tkFont.Font(family='Helvetica', size=10, weight='bold') #, background='#F2EDEB')
        #self.lblFileExtension.grid(row=0, sticky=N+W+E)
        self.lblFileExtension.pack(side=TOP)
        
        self.lblError = Label(self.fileName_frame, width=44, height=2, background="#2B2D42", foreground='#2B2D42')
        self.lblError["text"] = "" #"!!! Please enter a file name to save the screenshot to !!!"
        self.lblError["font"] = tkFont.Font(family='Helvetica', size=10, weight='bold') #, background='#F2EDEB')
        #self.lblFileExtension.grid(row=0, sticky=N+W+E)
        self.lblError.pack(side=TOP)
        
        self.menu_frame = Frame(master, background="#2B2D42")
        self.menu_frame.pack(fill=BOTH, expand=YES, side=BOTTOM)
        
        self.buttonBar = Frame(self.menu_frame, background="#2B2D42")
        self.buttonBar.pack(fill=BOTH,expand=YES, side=BOTTOM)

        #self.btn_text = StringVar()
        #self.btn_text.set("Capture")
        self.snipButton = Button(self.buttonBar, width=35, height=3, background="#F2EDEB", command=self.createScreenCanvas) #, textvariable=self.btn_text)
        self.snipButton.pack(expand=1) #fill=BOTH, expand=5) #expand=YES)
        self.snipButton["text"] = "Capture"
        self.snipButton["font"] = tkFont.Font(family='Helvetica', size=12, weight='bold')

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "white")
        self.picture_frame = Frame(self.master_screen, background = "#2B2D42")
        self.picture_frame.pack(fill=BOTH, expand=YES)      

    def takeBoundedScreenShot(self, x1, y1, x2, y2):
        try:
            img = pyautogui.screenshot(region=(x1, y1, x2, y2))
            #x = datetime.datetime.now()
            #fileName = x.strftime("%f")
            
            pathlib.Path(str(pathlib.Path(__file__).parent.absolute()) + "\\Screenshots\\").mkdir(parents=True, exist_ok=True)
            
            filename = str(pathlib.Path(__file__).parent.absolute()) + "\\Screenshots\\%s.png" % str(self.tbFileName.get()).strip() #"\\screenshot.png"
            img.save(filename) #"snips/" + fileName + ".png")
            
            #self.tbFileName["text"] = ""
            self.tbFileName.delete(0, 'end')
            self.tbFileName.focus()
            
            print("\nScreenshot saved to 'Screenshots' directory\nFile name: '%s.png'" % str(self.tbFileName.get()).strip())
            print("\n================================================================================\n")
            
            '''
            pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\Moham\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'
            img_to_text = pytesseract.image_to_string(Image.open(filename), lang='eng')
            
            root.clipboard_clear()
            root.clipboard_append(str(img_to_text))
            root.update() # now it stays on the clipboard after the window is closed
            '''
        except Exception as e:
            print("\nException error when creating directory or when taking screenshot\nError description: %s\n\n" % str(e)) # or converting image to text
            traceback.print_exc()
            
            #print("\nQuitting application\n")
            #root.quit()
            print("\n================================================================================\n")
            pass

    def createScreenCanvas(self):
        if (len(str(self.tbFileName.get()).strip())>0):
            self.lblError["text"] = ""
            self.lblError["background"] = "#2B2D42"
        
            self.master_screen.deiconify()
            root.withdraw()

            self.screenCanvas = Canvas(self.picture_frame, cursor="cross", background="#08090C")
            self.screenCanvas.pack(fill=BOTH, expand=YES)

            self.screenCanvas.bind("<ButtonPress-1>", self.on_button_press)
            self.screenCanvas.bind("<B1-Motion>", self.on_move_press)
            self.screenCanvas.bind("<ButtonRelease-1>", self.on_button_release)

            self.master_screen.attributes('-fullscreen', True)
            self.master_screen.attributes('-alpha', .3)
            self.master_screen.lift()
            self.master_screen.attributes("-topmost", True)
        
        else:
            print("\nPlease enter a file name to save the screenshot !!!\n")
            self.lblError["text"] = "!!! Please enter a file name to save the screenshot to !!!"
            self.lblError["background"] = "orange"

    def on_button_release(self, event):
        #! self.recPosition()

        if self.start_x <= self.curX and self.start_y <= self.curY:
            #print("right down")
            self.takeBoundedScreenShot(self.start_x, self.start_y, self.curX - self.start_x, self.curY - self.start_y)

        elif self.start_x >= self.curX and self.start_y <= self.curY:
            #print("left down")
            self.takeBoundedScreenShot(self.curX, self.start_y, self.start_x - self.curX, self.curY - self.start_y)

        elif self.start_x <= self.curX and self.start_y >= self.curY:
            #print("right up")
            self.takeBoundedScreenShot(self.start_x, self.curY, self.curX - self.start_x, self.start_y - self.curY)

        elif self.start_x >= self.curX and self.start_y >= self.curY:
            #print("left up")
            self.takeBoundedScreenShot(self.curX, self.curY, self.start_x - self.curX, self.start_y - self.curY)

        self.exitScreenshotMode()
        return event

    def exitScreenshotMode(self):
        #print("Screenshot mode exited")
        self.screenCanvas.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def exit_application(self):
        #print("Application exit")
        root.quit()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.screenCanvas.canvasx(event.x)
        self.start_y = self.screenCanvas.canvasy(event.y)

        self.rect = self.screenCanvas.create_rectangle(self.x, self.y, 1, 1, outline='#F2EDEB', width=2, fill="white")

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.screenCanvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def recPosition(self):
        print(self.start_x)
        print(self.start_y)
        print(self.curX)
        print(self.curY)

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()