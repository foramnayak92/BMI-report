#import necessary module lbr
import tkinter
from tkinter import ttk
from tkinter import messagebox #display msgs
import csv
from matplotlib import pyplot as plt #creat plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#function to save BMI record
def save():
    name=nametxt.get() #entry field
    age=agetxt.get()
    height=heighttxt.get()
    weight=weighttxt.get()

    #Validate input data
    if name == '' or age == '' or height == '' or weight == '':
        messagebox.showwarning("Error", "Please fill in all fields.") #warning msg if any field is empty
        return #Exit the function
    try:
        #convert it to appropite data types
        age=int(age)
        height=float(height)
        weight=float(weight)
    except ValueError: #Handle ValueError if conversion fails
        messagebox.showwarning("Error","Please enter valid numeric values for age,height, and weight.")
        return

    if age <=0 or height<=0 or weight<=0: #checking if not postive
        messagebox.showwarning("Error","Please enter positive values for age, height, and weight.")
        return

    bmi = weight/(height ** 2) #calc BMI using weight in kg
    bmi_category = ""
    if bmi<18.5:
        bmi_category="Underweight"
    elif bmi < 24.9:
        bmi_category="Normal"
    elif bmi < 29.9:
        bmi_category="Overweight"
    else:
        bmi_category="Obese"

    # Save BMI record to CSV file
    with open("bmi_records.csv", "a", newline="") as file:
        writer = csv.writer(file)  ## Create CSV writer object
        writer.writerow([name,age,height,weight,bmi_category])

    messagebox.showinfo("BMI Record Saved", "BMI record saved successfully.")
#to clear entry fields
def clear():
    nametxt.delete(0,'end')
    agetxt.delete(0,'end')
    heighttxt.delete(0,'end')
    weighttxt.delete(0,'end')

# global variable to track if the chart has been shown
chart_shown= False
def chart():  #show bmi cat distribution chart
    global chart_shown

    # If chart has already been shown, do nothing
    if chart_shown:
        return
    #to clear any existing chart from the windowww
    for widget in window.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.get_tk_widget().destroy()

#disc to store counts
    categories = {"Underweight": 0, "Normal": 0, "Overweight": 0, "Obese": 0}

    # Read BMI records from CSV file
    with open('bmi_records.csv','r')as file:
        reader=csv.reader(file)   #create csv reder object
        next(reader) #skip header
        for row in reader:
            categories[row[4]]+=1  # Increment count for BMI category
#creat pie chart
    fig, ax = plt.subplots()
    ax.pie(categories.values(),labels=categories.keys(),autopct='%1.1f%%', startangle=140)
    ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title('BMI Categories Distribution')

    chart_canvas = FigureCanvasTkAgg(fig, master=window)
    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    # Set chart_shown to True to indicate that the chart has been displayed
    chart_shown= True

window= tkinter.Tk()  # Create Tkinter window
window.title("BMI Calculator")  # Set title of the window

frame=tkinter.Frame(window) # Create ttk Frame
frame.pack()

# Create label frame for BMI information
infoframe=tkinter.LabelFrame(frame,text='BMI Information')
infoframe.grid(row=0,column=0)

namelabel=tkinter.Label(infoframe,text='Name:')
namelabel.grid(row=0,column=0)

agelabel=tkinter.Label(infoframe,text='Age:')
agelabel.grid(row=1,column=0)

heightlabel=tkinter.Label(infoframe,text='Height(m):')
heightlabel.grid(row=2,column=0)

weightlabel=tkinter.Label(infoframe,text='Weight(kg):')
weightlabel.grid(row=3,column=0)

nametxt=tkinter.Entry(infoframe)
nametxt.grid(row=0,column=1)

agetxt=tkinter.Entry(infoframe)
agetxt.grid(row=1,column=1)

heighttxt=tkinter.Entry(infoframe)
heighttxt.grid(row=2,column=1)

weighttxt=tkinter.Entry(infoframe)
weighttxt.grid(row=3,column=1)

buttonframe = tkinter.Frame(frame)
buttonframe.grid(row=1, column=0)

savebutton = tkinter.Button(buttonframe,text='Save',command=save)
savebutton.grid(row=0,column=0,padx=5,pady=5)

clearbutton=tkinter.Button(buttonframe,text='Clear',command=clear)
clearbutton.grid(row=0,column=1,padx=5,pady=5)

chartbutton = tkinter.Button(buttonframe, text='Show Chart', command=chart)
chartbutton.grid(row=0, column=2, padx=5, pady=5)

window.mainloop()
