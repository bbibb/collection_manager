import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from PIL import ImageTk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

app = tb.Window(themename="flatly")
app.geometry("1200x800")
app.title("Collections")

colors = app.style.colors


app.rowconfigure(0, weight=1)
app.rowconfigure(1, weight=2)
app.rowconfigure(2, weight=2)
app.rowconfigure(3, weight=4)
app.rowconfigure(4, weight=4)
app.rowconfigure(5, weight=4)
app.rowconfigure(6, weight=4)


app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=2)
app.columnconfigure(2, weight=4)
app.columnconfigure(3, weight=6)
app.columnconfigure(4, weight=6)

# categories frame
frame_categories = tb.Frame(app, style="secondary", borderwidth=8, relief="groove", padding=4)
frame_categories.grid(row=0, column=0, rowspan=6, columnspan=1, sticky=W+E+N+S)

frame_categories.columnconfigure(0, weight=1)
frame_categories.columnconfigure(1, weight=1)
frame_categories.rowconfigure(0, weight=1)
frame_categories.rowconfigure(1, weight=1)
frame_categories.rowconfigure(2, weight=8)
frame_categories.rowconfigure(3, weight=8)
frame_categories.rowconfigure(4, weight=8)

label_categories = tb.Label(frame_categories, text="Categories", font=("Helvetica", 18))
label_categories.grid(row=0, column=0, columnspan=2, sticky="nsew")
label_categories.configure(anchor=CENTER)



button_categories1 = tb.Button(frame_categories, text="Filter", bootstyle="success-outline")
button_categories1.grid(row=1, column=0)

button_categories2 = tb.Button(frame_categories, text="Add Category", bootstyle="success-outline")
button_categories2.grid(row=1, column=1)

listbox_categories = tb.Treeview(frame_categories)
listbox_categories.grid(row=2, rowspan=3, columnspan=2, sticky=W+E+N+S)

for i in range(20):
    text = f"Category {i+1}"
    listbox_categories.insert("", "end", text=text)

# actions frame

frame_actions = tb.Frame(app, style="secondary", borderwidth=8, relief="groove", padding=4)
frame_actions.grid(row=6, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame_actions.columnconfigure(0, weight=1, pad=1)
frame_actions.columnconfigure(1,weight=1, pad=1)
frame_actions.rowconfigure(0, weight=1)
frame_actions.rowconfigure(1, weight=2)
frame_actions.rowconfigure(2, weight=2)
frame_actions.rowconfigure(3, weight=2)
frame_actions.rowconfigure(4, weight=2)

label_actions = tb.Label(frame_actions, text="Actions", font=("Helvetica", 18))
label_actions.configure(anchor=CENTER)
label_actions.grid(row=0, column=0, columnspan=2, sticky="nsew")

# actions buttons
button_home = tb.Button(frame_actions, text="Home", bootstyle="success-outline")
button_home.grid(row=2, column=0, sticky="nsew")

button_gallery = tb.Button(frame_actions, text="Gallery", bootstyle="success-outline")
button_gallery.grid(row=2, column=1, sticky="nsew")

button_gallery = tb.Button(frame_actions, text="Add Item", bootstyle="success-outline")
button_gallery.grid(row=3, column=0, sticky="nsew")

button_gallery = tb.Button(frame_actions, text="Import", bootstyle="success-outline")
button_gallery.grid(row=3, column=1, sticky="nsew")

button_admin = tb.Button(frame_actions, text="Admin", bootstyle="success-outline")
button_admin.grid(row=4, column=0, sticky="nsew")

button_logout = tb.Button(frame_actions, text="Logout", bootstyle="success-outline")
button_logout.grid(row=4, column=1, sticky="nsew")


# title frame
frame_title = tb.Frame(app, style="secondary", borderwidth=4, relief="groove", padding=4)
frame_title.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=W+E+N+S)

frame_title.columnconfigure(0, weight=1)
frame_title.rowconfigure(0, weight=1)

label_title = tb.Label(frame_title, text="Collection Manager", font=("Helvetica", 18), bootstyle="success")
label_title.configure(anchor=CENTER)
label_title.grid(row=0, column=0, sticky="nsew")

# item list
frame_list = tb.Frame(app, style="default",  borderwidth=4, relief="groove", padding=4)
frame_list.grid(row=1, column=1, rowspan=6, columnspan=1, sticky=W+E+N+S)
# label_list = tb.Label(frame_list, text="Item List")
# label_list.grid()

coldata = [
    "Item",
    "Category",
    "Location",
    "Price",
    "Value",
]

rowdata = [
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),
    ('This is an item', 'Category1', 'Box 12-3', 12.00, 24.00),

]

dt = Tableview(
    master=frame_list,
    coldata=coldata,
    rowdata=rowdata,
    paginated=True,
    searchable=True,
    bootstyle=PRIMARY,
    stripecolor=(colors.light, None),
    autofit=True,
    pagesize=38,
    height=38
)
dt.grid(row=0, column=0, padx=30, pady=10, sticky="nsew")

# Item

frame_item = tb.Frame(app, style="secondary", borderwidth=4, relief="groove", padding=4)
frame_item.grid(row=0, column=2, rowspan=5, columnspan=3, sticky=W+E+N+S)

frame_item.columnconfigure(0, weight=1, pad=1)
frame_item.columnconfigure(1,weight=1, pad=1)
frame_item.rowconfigure(0, weight=1)
frame_item.rowconfigure(1, weight=1)
frame_item.rowconfigure(2, weight=20)


label_item = tb.Label(frame_item, text="Item Info", font=("Helvetica", 18))
label_item.configure(anchor=CENTER)
label_item.grid(row=0, column=0, sticky="nsew", columnspan=2)

frame_info_box = tb.Frame(frame_item, style="default", borderwidth=4, relief="groove", padding=4)
frame_info_box.grid(row=2, column=0, sticky="nsew", columnspan=2)


# Photo


frame_photo = tb.Frame(app, style="primary", borderwidth=4, relief="groove", padding=4)
frame_photo.grid(row=5, column=2, rowspan=2, columnspan=3, sticky=W+E+N+S)

frame_photo.columnconfigure(0, weight=1, pad=1)
frame_photo.columnconfigure(1,weight=1, pad=1)
frame_photo.rowconfigure(0, weight=1)
frame_photo.rowconfigure(1, weight=1)
frame_photo.rowconfigure(2, weight=20)

label_photo = tb.Label(frame_photo, text="Photo", font=("Helvetica", 18))
label_photo.configure(anchor=CENTER)
label_photo.grid(row=0, column=0, sticky="nsew", columnspan=2)

frame_photo_box = tb.Frame(frame_photo, style="default", borderwidth=4, relief="groove", padding=4)
frame_photo_box.grid(row=2, column=0, sticky="nsew", columnspan=2)

img = Image.open("images/ALT_orange.jpg")
resized = img.resize((350, 300))
image = ImageTk.PhotoImage(resized)

label_photo_box = tb.Label(frame_photo_box, image = image)
label_photo_box.configure(anchor=CENTER)
label_photo_box.grid(row=0, column=0, sticky="nsew")




app.mainloop()
