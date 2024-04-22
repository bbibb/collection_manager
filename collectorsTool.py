import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import sqlite3
import sys, os

########################### Section 1: Model Functions ##################################

#### Collection Data ####

# basic function to get a list of collections, used by combobox widgets
def get_collections():
    global user_id
    global user_role
    global collection_id
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cursor = sqliteConnection.cursor()

    # admin can see all collections
    if user_role == 'admin':
        query = ('SELECT * FROM collection;')
        cursor.execute(query)
    else:
        query = (
            'SELECT * FROM collection WHERE collection.userID = ? AND collectionStatus = 1;'
        )
        data = (str(user_id))
        cursor.execute(query, data)
    collections = cursor.fetchall()
    cursor.close()
    return collections

# Function to allow the user to select the collection they want to use after logging in.
# Called by the set_collection_window view function.
def set_collection(collection_name, setCollectionsWindow):
    global collection_id
    collection_name = str(collection_name.get())
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cursor = sqliteConnection.cursor()
    # get collection from the chosen collection name
    query = ('SELECT * FROM collection WHERE collectionName = ? AND collectionExists = ?;')
    exists = 1
    data = (collection_name, exists)
    cursor.execute(query, data)
    collection = cursor.fetchall()
    cursor.close()
    # extract the collectionID and save it to global variable
    collection_id = collection[0][0]
    # print(collection_id)

    # close current window and start main application window
    setCollectionsWindow.destroy()
    start_app()

# function to create a new collection, called by collections_window
def new_collection(collection_name, window):
    # get the name of the collection entered in the Entry field
    collection_name = str(collection_name.get())
    global user_id
    # add new collection to the database, associated with the userID
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cur = sqliteConnection.cursor()
    query = (
        '''
        INSERT INTO collection (collectionName, userID) 
        VALUES (?, ?)
        ''')
    data = (collection_name, user_id)
    count = cur.execute(query, data)
    sqliteConnection.commit()
    cur.close()
    # confirmation message
    window.destroy()
    Messagebox.show_info("New Collection Created", "secondary", parent=window)


# Function to change the current collection, called by collections_window view function
def change_collection(collection_name, collectionsWindow):
    global collection_id
    # get the selected collection name from the combobox
    collection_name = str(collection_name.get())
    # print(collection_name)
    # get the collectionID based on the chosen name
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cursor = sqliteConnection.cursor()
    query = ('SELECT * FROM collection WHERE collectionName = ? and collectionExists = ?;')
    exists = 1
    data = (collection_name, exists)
    cursor.execute(query, data)
    collection = cursor.fetchall()
    cursor.close()
    # extract collectionID and save to global variable collection_id
    collection_id = collection[0][0]
    # print(collection_id)
    # close current window and redraw table to reflect the change
    collectionsWindow.destroy()
    refresh_app()

# 'delete' the collection by setting it as inactive, called by collections_window view function
def delete_collection(collection_name):
    collection_name = str(collection_name.get())
    # confirmation dialog
    mb = Messagebox.yesno("Are you sure you want to delete this collection?", "Delete Collection?", parent=app)
    if mb == "Yes":
        # set collection status as inactive
        sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
        cursor = sqliteConnection.cursor()
        query = ('''
                 UPDATE collection SET collectionStatus = 0 WHERE collectionName = ? AND collectionStatus = ?;
                ''')
        status = 1
        data = (collection_name, status)
        cursor.execute(query, data)
        sqliteConnection.commit()
        cursor.close()
        # confirmation
        Messagebox.show_info("Collection Deactivated", "secondary")
    else:
        pass


#### Category Data ####

# basic function to get a list of categories, used by combobox widgets
def get_categories():
    global collection_id
    global user_role
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cursor = sqliteConnection.cursor()
    if user_role == 'admin':
        query = ('SELECT categoryID, categoryName FROM category WHERE category.collectionID = ? AND categoryStatus IN (0,1);')
    else:
        query = (
            'SELECT categoryID, categoryName FROM category WHERE category.collectionID = ? AND categoryStatus = 1;'
        )
    data = (str(collection_id))
    cursor.execute(query, data)
    categories = cursor.fetchall()
    cursor.close()
    return categories


# create a new category, called by categories_window
def new_category(category_name, window):
    # get the name of the category entered in the Entry field
    category_name = str(category_name.get())
    global collection_id
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cur = sqliteConnection.cursor()
    # insert category into the database, associated with the current collectionID
    query = (
        '''
        INSERT INTO category (categoryName, collectionID)
        VALUES (?, ?);
        ''')
    data = (category_name, collection_id)
    count = cur.execute(query, data)
    sqliteConnection.commit()
    cur.close()

    # confirmation message
    window.destroy()
    Messagebox.show_info("New Category Created", "secondary", parent=window)


# function to delete a category from the list, called by categories_window view function
def delete_category(category_name):
    # get the chosen category name
    category_name = str(category_name.get())

    # confirmation dialog
    mb = Messagebox.yesno("Are you sure you want to delete this category? Items with this category will also be deleted. "
                          "Change the category of items you want to keep before running this function.", "Delete Category?", parent=app)
    if mb == "Yes":
        # set the category status as inactive based on the categoryName chosen
        sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
        cursor = sqliteConnection.cursor()
        query = ('''
                 UPDATE category SET categoryStatus = 0 WHERE categoryName = ? AND categoryStatus = ?;
                ''')
        status = 1
        data = (category_name, status)
        cursor.execute(query, data)
        sqliteConnection.commit()
        cursor.close()
        # **Sub-routine to 'delete' the categories and items that are part of that category.
        deactivate_item_category(category_name)

        # close current window and give confirmation message
        refresh_app()
        Messagebox.show_info("Category Deactivated", "secondary")

    else:
        pass


# function to 'delete' items belonging to a 'deleted' category, called by delete_category
def deactivate_item_category(category_name):
    global collection_id
    # print(category_name)

    # get categoryID
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cursor = sqliteConnection.cursor()
    query = ('SELECT categoryID FROM category WHERE categoryName = ? AND categoryStatus = ?')
    status = 0
    data = (category_name, status)
    cursor.execute(query, data)
    category_id = cursor.fetchone()
    cursor.close()
    # print(category_id)

# deactivate items belonging to that categoryID
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cursor = sqliteConnection.cursor()

    # first identify the items
    query = ('''
        SELECT itemID from item WHERE item.categoryID = ? AND item.collectionID = ?;
    ''')
    category_id = category_id[0]
    data = (category_id, collection_id)
    cursor.execute(query, data)
    item_id = cursor.fetchall()
    # print(item_id)
    cursor.close()

    # then loop through the results and set the status of each one to 0
    for id in item_id:
        # print(id)
        id_no = id[0]
        # print(id)
        sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
        cursor = sqliteConnection.cursor()
        query = ('''
                UPDATE item SET itemStatus = ? WHERE itemID = ? AND collectionID = ?;
                ''')
        status = 0
        data = (status, id_no, collection_id)
        # print(data)
        cursor.execute(query, data)
        sqliteConnection.commit()
        cursor.close()


#### Source Data ####

# basic function to get a list of sources, used by combobox widgets
def get_sources():
    global collection_id
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cursor = sqliteConnection.cursor()
    if user_role == 'admin':
        query = ('SELECT sourceID, sourceName FROM source WHERE source.collectionID = ?;')
        data = (str(collection_id))
    else:
        query = (
            'SELECT sourceID, sourceName FROM source WHERE source.collectionID = ? AND sourceStatus = ?;'
        )
        status = 1
        data = (str(collection_id), status)
    cursor.execute(query, data)
    sources = cursor.fetchall()
    cursor.close()
    return sources

# function to create a new source, called by new_source_window
def new_source(source_name, source_address, source_city, source_state, source_zip, source_phone, source_email, window):
    global collection_id
# parse input data from Entry fields to extract data fields
    source_name = str(source_name.get())
    source_address = str(source_address.get())
    source_city = str(source_city.get())
    source_state = str(source_state.get())
    source_zip = str(source_zip.get())
    source_phone = str(source_phone.get())

    source_email = str(source_email.get())
# update source in the database with new information
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cur = sqliteConnection.cursor()
    query = (
        '''
        INSERT INTO source (collectionID, sourceName, sourceAddress, sourceCity, sourceState, sourceZip, sourcePhone, sourceEmail) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''')
    data = (
    collection_id, source_name, source_address, source_city, source_state, source_zip, source_phone, source_email)
    count = cur.execute(query, data)
    sqliteConnection.commit()
    cur.close()
# confirmation message
    window.destroy()
    Messagebox.show_info("New Source Record Created", "secondary", parent=window)


# Function to delete a source from the database, called by the source_window view function
def delete_source(source_name):
    source_name = str(source_name.get())

    # confirmation dialog
    mb = Messagebox.yesno("Are you sure you want to delete this source? Items from this source will also be deleted."
                          "Change the source field for any items you want to save before running this function.", "Delete Source?", parent=app)

    if mb == "Yes":
        sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
        cursor = sqliteConnection.cursor()
        # set the status to inactive
        query = ('''
                 UPDATE source SET sourceStatus = 0 WHERE sourceName = ? AND sourceStatus = ?;
                ''')
        status = 1
        data = (source_name, status)
        cursor.execute(query, data)
        sqliteConnection.commit()
        cursor.close()

        # ** Subroutine to 'delete' items associated with that source.
        deactivate_item_source(source_name)

        # refresh the table and send confirmation message
        refresh_app()
        Messagebox.show_info("Source Deactivated", "secondary")

    else:
        pass

# function called by delete_source to also delete items associated with that source
def deactivate_item_source(source_name):
    global collection_id
    # print(category_name)

    # get the sourceID from the name in the combobox
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cursor = sqliteConnection.cursor()
    query = ('SELECT sourceID FROM source WHERE sourceName = ? AND sourceStatus = ?')
    status = 0
    data = (source_name, status)
    cursor.execute(query, data)
    source_id = cursor.fetchone()
    cursor.close()
    # print(category_id)

    # select the items associated with that source
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cursor = sqliteConnection.cursor()
    query = ('''
        SELECT itemID from item WHERE item.sourceID = ? AND item.collectionID = ?;
    ''')
    # extract sourceID from the prior results
    source_id = source_id[0]
    data = (source_id, collection_id)
    cursor.execute(query, data)
    item_id = cursor.fetchall()
    # print(item_id)
    cursor.close()
    # loop through the results, and set the status of each item to inactive
    for id in item_id:
        # print(id)
        id_no = id[0]
        # print(id)
        sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
        cursor = sqliteConnection.cursor()
        query = ('''
                UPDATE item SET itemStatus = ? WHERE itemID = ? AND collectionID = ?;
                ''')
        status = 0
        data = (status, id_no, collection_id)
        # print(data)
        cursor.execute(query, data)
        sqliteConnection.commit()
        cursor.close()


#### Item Data ####

# Basic select function used by the Table window.
# execute_query
def selectQuery():
    global collection_id
    # print(collection_id)
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cursor = sqliteConnection.cursor()
    # get all of the data needed for the Tableview
    if user_role == 'admin':
        query = (
            'SELECT itemID, itemName, category.categoryName, itemLocation, source.sourceName, printf("%.2f", itemPrice) AS itemPrice, printf("%.2f", itemValue) AS itemValue, itemStatus FROM item JOIN category ON category.categoryId = item.categoryId JOIN source ON item.sourceID = source.sourceID WHERE item.collectionID = ?;')
        data = (str(collection_id))
    else:
        query = (
        'SELECT itemID, itemName, category.categoryName, itemLocation, source.sourceName, printf("%.2f", itemPrice) AS itemPrice, printf("%.2f", itemValue) AS itemValue FROM item JOIN category ON category.categoryId = item.categoryId JOIN source ON item.sourceID = source.sourceID WHERE itemStatus = 1 AND item.collectionID = ?;')
        data = (str(collection_id))
    cursor.execute(query, data)
    result = cursor.fetchall()
    cursor.close()
    # return the query result for parsing by the view
    return result

# function to delete an item from the database

def delete_record(item_id):
# confirmation dialog
    mb = Messagebox.yesno("Are you sure you want to delete this record?", "Delete Record?")
    if mb == "Yes":
        # print(item_id)
        sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
        cursor = sqliteConnection.cursor()
# set status to inactive
        query = ('UPDATE item SET itemStatus = 0 WHERE itemID = ? AND itemStatus = ?;')
        itemStatus = 1
        data = (item_id, itemStatus)
        cursor.execute(query, data)
        sqliteConnection.commit()
        cursor.close()
        refresh_app()
# success message
        Messagebox.show_info("Collection Deactivated", "secondary")
    else:
        pass

# basic function to get information about a specific item after it has been selected in the table.
def selectItemFields(item_id):
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cursor = sqliteConnection.cursor()
    query = (
                'SELECT * FROM item JOIN source on item.sourceID = source.SourceID JOIN category ON item.categoryID = category.categoryID WHERE itemID = ' + str(
            item_id) + ';')
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    # this result contains all data related to one item
    return result


# function to create a new item, called by the new_record_window function.
# receives Entry values from the view and passes them to the database
def new_item(collection_id, category_id, source_id, item_name, item_description, item_price, item_value, item_location,
             item_date, window):
    # parse the input data to get the specific fields of data
    category_id = str(category_id.get())
    category_id = category_id[0]
    source_id = str(source_id.get())
    source_id = source_id[0]
    item_name = str(item_name.get())
    item_description = str(item_description.get("1.0", 'end'))
    item_price = str(item_price.get())
    item_value = str(item_value.get())
    item_location = str(item_location.get())
    item_date = str(item_date.get())

    # insert item into database
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cur = sqliteConnection.cursor()
    query = (
        '''
        INSERT INTO item (collectionID, categoryID, sourceID, itemName, itemDescription, itemPrice, itemValue, itemLocation, itemDate) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''')
    data = (collection_id, category_id, source_id, item_name, item_description, item_price, item_value, item_location,
            item_date)
    count = cur.execute(query, data)
    sqliteConnection.commit()
    cur.close()

    # redraw Table and give confirmation message
    refresh_app()
    window.destroy()
    Messagebox.show_info("New Record Created", "secondary", parent=window)


# function to update database with changed item data, called by edit_window
def update_item(category_id, source_id, item_name, item_description, item_price, item_value, item_location, item_date,
                item_status):
    global item_id
# parse input data from Entry fields to extract data bits
    category_id = str(category_id.get())
    category_id = category_id[0]
    source_id = str(source_id.get())
    source_id = source_id[0]
    # print(source_id)
    item_name = str(item_name.get())
    item_description = str(item_description.get("1.0", 'end'))
    item_price = str(item_price.get())
    item_value = str(item_value.get())
    item_location = str(item_location.get())
    item_date = str(item_date.get())

# update item in the database with the new information
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cur = sqliteConnection.cursor()
    query = '''UPDATE item set categoryID = ?, sourceID = ?, itemName = ?, itemDescription = ?, itemPrice = ?, itemValue = ?, itemLocation = ?, itemDate = ?, itemStatus = ?  WHERE itemID = ? '''
    data = (
    category_id, source_id, item_name, item_description, item_price, item_value, item_location, item_date, item_status, item_id)
    cur.execute(query, data)
    sqliteConnection.commit()
    cur.close()
    refresh_app()
    Messagebox.show_info("Record Updated", "secondary")








########################### Section 2: View Functions ##################################


# function to format item data for the report field
def get_item_info(dt, item_info_box):
# get the itemID from the table, from user click event
    for i in dt.view.selection():
        global item_id
        item_id = dt.view.item(i)['values'][0]

# call function to get item data
    item_fields = selectItemFields(item_id)
    # print(item_fields)
# format data into report view
    item_info_box["text"] = (f"Item Name: {item_fields[0][4]}\n"
                             f"\n"
                             f"Item Category: {item_fields[0][23]}\n"
                             f"Item Location: {item_fields[0][8]}\n"
                             f"Item Date: {item_fields[0][9]}\n"
                             f"\n"                                 f"\n"
                             f"Item Price:   ${item_fields[0][6]:.2f}\n"
                             f"Item Value:  ${item_fields[0][7]:.2f}\n"
                             f"\n"
                             f"Item Source: \n"
                             f"{item_fields[0][13]}\n"
                             f"{item_fields[0][14]}\n"
                             f"{item_fields[0][15]}, {item_fields[0][16]}\n"
                             f"{item_fields[0][17]}\n"
                             f"TEL: {item_fields[0][18]}\n"
                             f"EMAIL: {item_fields[0][19]}\n\n"
                             f" ------------------------------------------ \n"
                             f"Item Description: {item_fields[0][5]}\n"
                             )
    # print(item_fields)
    # print(item_id)


# window to set the current collection

def set_collection_window():
    global user_id
# get a list of collections
    collections = get_collections()
    # print(collections)
    collection_names = []
# extract the names and put into a list
    for collection in collections:
        # print(collection[1])
        collection_names += [collection[1]]
    # print(collection_names)

# code to draw the window, form fields, and buttons
    setCollectionsWindow = tb.Toplevel()
    setCollectionsWindow.title('Your Collections')

    collectionsWindow_frame = tb.LabelFrame(setCollectionsWindow, style="success", padding=20, text="Item Information")
    collectionsWindow_frame.grid(row=0, column=0, padx=20, pady=10)

# pick a collection
    collections_label = tb.Label(collectionsWindow_frame, text='Chose a collection')
    collections_label.grid(row=0, column=0, columnspan=2, sticky="news")
    collections_list = tb.Combobox(collectionsWindow_frame, values=collection_names)
    collections_list.grid(row=1, column=0, columnspan=2, sticky="news")

# make that collection the current one, or close window
    collections_open_button = tb.Button(collectionsWindow_frame, style="secondary-outline", text="open",
                                        command=lambda: set_collection(collections_list, setCollectionsWindow))
    collections_open_button.grid(row=2, column=0, padx=10, pady=10, sticky="news")
    collection_close_button = tb.Button(collectionsWindow_frame, style="secondary-outline", text="close",
                                        command=setCollectionsWindow.destroy)
    collection_close_button.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky="news")


# window to create a new collection
def new_collection_window():
    global app
    newCollectionWindow = tb.Toplevel(app)
    newCollectionWindow.title("New Collection")

    newCollection_frame = tb.LabelFrame(newCollectionWindow, style="success", padding=20)
    newCollection_frame.grid(row=0, column=0, padx=20, pady=10)

# get the name of the new collection
    newCollection_name = tb.Label(newCollection_frame, text="Collection Name:")
    newCollection_name.grid(row=0, column=0, padx=10, pady=0, columnspan=2, sticky="nsew")
    newCollection_name_entry = tb.Entry(newCollection_frame)
    newCollection_name_entry.grid(row=1, column=0, padx=10, pady=0, columnspan=2, sticky="nsew")

# submit the name to the new_collection function, or close
    collection_submit_button = tb.Button(newCollection_frame, text="Submit", style="secondary.Outline.TButton",
                                         command=lambda: new_collection(newCollection_name_entry, newCollectionWindow))
    collection_submit_button.grid(row=2, column=0, sticky="news", padx=10, pady=10)
    collection_close_button = tb.Button(newCollection_frame, text="Close", style="secondary.Outline.TButton",
                                        command=newCollectionWindow.destroy)
    collection_close_button.grid(row=2, column=1, sticky="news", padx=10, pady=10)


# window to create a new category
def new_category_window():
    global app
    newCategoryWindow = tb.Toplevel(app)
    newCategoryWindow.title("New Category")

    newCategory_frame = tb.LabelFrame(newCategoryWindow, style="success", padding=20)
    newCategory_frame.grid(row=0, column=0, padx=20, pady=10)

# get the name of the new category
    newCategory_name = tb.Label(newCategory_frame, text="Category Name:")
    newCategory_name.grid(row=0, column=0, padx=10, pady=0, columnspan=2, sticky="nsew")
    newCategory_name_entry = tb.Entry(newCategory_frame)
    newCategory_name_entry.grid(row=1, column=0, padx=10, pady=0, columnspan=2, sticky="nsew")

# submit the category to new_category function, or close
    category_submit_button = tb.Button(newCategory_frame, text="Submit", style="secondary.Outline.TButton",
                                       command=lambda: new_category(newCategory_name_entry, newCategoryWindow))
    category_submit_button.grid(row=2, column=0, sticky="news", padx=10, pady=10)
    category_close_button = tb.Button(newCategory_frame, text="Close", style="secondary.Outline.TButton",
                                      command=newCategoryWindow.destroy)
    category_close_button.grid(row=2, column=1, sticky="news", padx=10, pady=10)


# window to create a new source
def new_source_window():
    global app
    newSourceWindow = tb.Toplevel(app)
    newSourceWindow.title("New Source")

    newSource_frame = tb.LabelFrame(newSourceWindow, style="success", padding=20)
    newSource_frame.grid(row=0, column=0, padx=20, pady=10)

# get source data
    newSource_name_label = tb.Label(newSource_frame, text="Source Name")
    newSource_name_label.grid(row=0, column=0)
    newSource_name_entry = tb.Entry(newSource_frame)
    newSource_name_entry.grid(row=0, column=1)

    newSourceAddress_label = tb.Label(newSource_frame, text="Street Address")
    newSourceAddress_label.grid(row=1, column=0)
    newSourceAddress_entry = tb.Entry(newSource_frame)
    newSourceAddress_entry.grid(row=1, column=1)

    newSourceCity_label = tb.Label(newSource_frame, text="City")
    newSourceCity_label.grid(row=2, column=0)
    newSourceCity_entry = tb.Entry(newSource_frame)
    newSourceCity_entry.grid(row=2, column=1)

    newSourceState_label = tb.Label(newSource_frame, text="State")
    newSourceState_label.grid(row=3, column=0)
    newSourceState_entry = tb.Entry(newSource_frame)
    newSourceState_entry.grid(row=3, column=1)

    newSourceZip_label = tb.Label(newSource_frame, text="Zip")
    newSourceZip_label.grid(row=4, column=0)
    newSourceZip_entry = tb.Entry(newSource_frame)
    newSourceZip_entry.grid(row=4, column=1)

    newSourcePhone_label = tb.Label(newSource_frame, text="Phone")
    newSourcePhone_label.grid(row=5, column=0)
    newSourcePhone_entry = tb.Entry(newSource_frame)
    newSourcePhone_entry.grid(row=5, column=1)

    newSourceEmail_label = tb.Label(newSource_frame, text="Email")
    newSourceEmail_label.grid(row=6, column=0)
    newSourceEmail_entry = tb.Entry(newSource_frame)
    newSourceEmail_entry.grid(row=6, column=1)

    source_button_frame = tb.Frame(newSourceWindow)
    source_button_frame.grid(row=8, column=0, sticky="news", padx=10, pady=10)
    source_button_frame.columnconfigure(0, weight=2)
    source_button_frame.columnconfigure(1, weight=2)

# submit source to new_source function, or close
    source_submit_button = tb.Button(source_button_frame, text="Submit", style="secondary.Outline.TButton",
                                     command=lambda: new_source(newSource_name_entry, newSourceAddress_entry,
                                                                newSourceState_entry, newSourceCity_entry,
                                                                newSourceZip_entry, newSourcePhone_entry,
                                                                newSourceEmail_entry, newSourceWindow))
    source_submit_button.grid(row=0, column=0, sticky="news", padx=30, pady=10)
    source_close_button = tb.Button(source_button_frame, text="Close", style="secondary.Outline.TButton", command=newSourceWindow.destroy)
    source_close_button.grid(row=0, column=1, sticky="news", padx=30, pady=10)


# window to edit a source
def edit_source(sources_list):
    # this function saves the source data to the database.
    # this might better be found in the Control section, but it is useful to have these closely connected functions together.
    def update_source(editSource_id_entry, editSource_name_entry, editSourceAddress_entry, editSourceState_entry,
                      editSourceCity_entry, editSourceZip_entry, editSourcePhone_entry, editSourceEmail_entry,
                      editSourceWindow):
        source_id = editSource_id_entry.get()
        source_name = editSource_name_entry.get()
        source_address = editSourceAddress_entry.get()
        source_state = editSourceState_entry.get()
        source_city = editSourceCity_entry.get()
        source_zip = editSourceZip_entry.get()
        source_phone = editSourcePhone_entry.get()
        source_email = editSourceEmail_entry.get()

        sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
        cursor = sqliteConnection.cursor()
        query = (
            "UPDATE source SET sourceName = ?, sourceAddress = ?, sourceCity = ?, sourceState = ?, sourceZip = ?, sourcePhone = ?, sourceEmail = ? WHERE sourceID = ?")
        data = (
        source_name, source_address, source_state, source_city, source_zip, source_phone, source_email, source_id)
        cursor.execute(query, data)
        sqliteConnection.commit()
        cursor.close()
        Messagebox.show_info("Source Record Updated", "secondary", parent=editSourceWindow)

    # this function gets source data from the databse
    def selectSourceFields(source_name):
        global collection_id
        # print(source_id)
        sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
        cursor = sqliteConnection.cursor()
        query = ("SELECT * FROM source WHERE sourceName= ? AND source.collectionID = ?;")
        data = (source_name, collection_id)
        print(data)
        cursor.execute(query, data)
        result = cursor.fetchall()
        return result

# get source data and extract it to individual fields
    print(sources_list)
    source_name = sources_list.get()
    print(source_name)
    source_fields = selectSourceFields(source_name)
    print(source_fields)

    source_id = source_fields[0][0]
    source_name = source_fields[0][1]
    source_address = source_fields[0][2]
    source_city = source_fields[0][3]
    source_state = source_fields[0][4]
    source_zip = source_fields[0][5]
    source_phone = source_fields[0][6]
    source_email = source_fields[0][7]

# draw window, populated with current data
    editSourceWindow = tb.Toplevel(app)
    editSourceWindow.title("New Source")

    editSource_frame = tb.LabelFrame(editSourceWindow, style="success", padding=20)
    editSource_frame.grid(row=0, column=0, padx=20, pady=10)

# each entry gets an "insert" line that adds the previous data on load
    editSource_id_label = tb.Label(editSource_frame, text="Source ID", state=DISABLED)
    editSource_id_label.grid(row=0, column=0)
    editSource_id_entry = tb.Entry(editSource_frame)
    editSource_id_entry.grid(row=0, column=1)
    editSource_id_entry.insert(END, source_id)

    editSource_name_label = tb.Label(editSource_frame, text="Source Name")
    editSource_name_label.grid(row=0, column=0)
    editSource_name_entry = tb.Entry(editSource_frame)
    editSource_name_entry.grid(row=0, column=1)
    editSource_name_entry.insert(END, source_name)

    editSourceAddress_label = tb.Label(editSource_frame, text="Street Address")
    editSourceAddress_label.grid(row=1, column=0)
    editSourceAddress_entry = tb.Entry(editSource_frame)
    editSourceAddress_entry.grid(row=1, column=1)
    editSourceAddress_entry.insert(END, source_address)

    editSourceCity_label = tb.Label(editSource_frame, text="City")
    editSourceCity_label.grid(row=2, column=0)
    editSourceCity_entry = tb.Entry(editSource_frame)
    editSourceCity_entry.grid(row=2, column=1)
    editSourceCity_entry.insert(END, source_city)

    editSourceState_label = tb.Label(editSource_frame, text="State")
    editSourceState_label.grid(row=3, column=0)
    editSourceState_entry = tb.Entry(editSource_frame)
    editSourceState_entry.grid(row=3, column=1)
    editSourceState_entry.insert(END, source_state)

    editSourceZip_label = tb.Label(editSource_frame, text="Zip")
    editSourceZip_label.grid(row=4, column=0)
    editSourceZip_entry = tb.Entry(editSource_frame)
    editSourceZip_entry.grid(row=4, column=1)
    editSourceZip_entry.insert(END, source_zip)

    editSourcePhone_label = tb.Label(editSource_frame, text="Phone")
    editSourcePhone_label.grid(row=5, column=0)
    editSourcePhone_entry = tb.Entry(editSource_frame)
    editSourcePhone_entry.grid(row=5, column=1)
    editSourcePhone_entry.insert(END, source_phone)

    editSourceEmail_label = tb.Label(editSource_frame, text="Email")
    editSourceEmail_label.grid(row=6, column=0)
    editSourceEmail_entry = tb.Entry(editSource_frame)
    editSourceEmail_entry.grid(row=6, column=1)
    editSourceEmail_entry.insert(END, source_email)

    source_button_frame = tb.Frame(editSourceWindow)
    source_button_frame.grid(row=8, column=0, sticky="news", padx=10, pady=10)
    source_button_frame.columnconfigure(0, weight=2)
    source_button_frame.columnconfigure(1, weight=2)

# submit updated source data to the database, or close
    editsource_submit_button = tb.Button(source_button_frame, text="Submit", style="secondary.Outline.TButton",
                                         command=lambda: update_source(editSource_id_entry, editSource_name_entry,
                                                                       editSourceAddress_entry, editSourceState_entry,
                                                                       editSourceCity_entry, editSourceZip_entry,
                                                                       editSourcePhone_entry, editSourceEmail_entry,
                                                                       editSourceWindow))
    editsource_submit_button.grid(row=0, column=0, sticky="news", padx=30, pady=10)
    editsource_close_button = tb.Button(source_button_frame, text="Close", style="secondary.Outline.TButton", command=editSourceWindow.destroy)
    editsource_close_button.grid(row=0, column=1, sticky="news", padx=30, pady=10)


# window to edit a particular item in the database
def edit_window():
# get the information needed to populate the fields at load
    global item_id
    sources = get_sources()
    categories = get_categories()
    # print(sources)
    # print(item_id)
    item_fields = selectItemFields(item_id)
    # print(item_fields)

# extract each piece of data into a variable
    collection_id = item_fields[0][1]
    category_id = item_fields[0][2]
    source_id = item_fields[0][3]
    item_name = item_fields[0][4]
    item_description = item_fields[0][5]
    item_price = f"{item_fields[0][6]:.2f}"
    item_value = f"{item_fields[0][7]:.2f}"
    item_location = item_fields[0][8]
    item_date = item_fields[0][9]
    category_name = item_fields[0][20]
    source_name = item_fields[0][12]
    item_status = item_fields[0][11]
    print(item_status)
    global app

# draw window
    editWindow = tb.Toplevel(app)
    editWindow.title("Edit Record")

    editWindow_frame = tb.LabelFrame(editWindow, text="Item Information")
    editWindow_frame.grid(row=0, column=0, padx=20, pady=10)

# each line gets an "insert" of previous data at load
    item_name_label = tb.Label(editWindow_frame, text="Item Name")
    item_name_label.grid(row=0, column=0)
    item_name_entry = tb.Entry(editWindow_frame)
    item_name_entry.grid(row=0, column=1)
    item_name_entry.insert(END, item_name)

# comboboxes for categories and sources, for ease and data integrity
    category_name_label = tb.Label(editWindow_frame, text="Category")
    category_name_label.grid(row=1, column=0)
    category_name_entry = tb.Combobox(editWindow_frame, values=categories)
    category_name_entry.grid(row=1, column=1)
    # category_name_entry.insert(END, category_id)

    source_name_label = tb.Label(editWindow_frame, text="Source")
    source_name_label.grid(row=2, column=0)
    source_name_entry = tb.Combobox(editWindow_frame, values=sources)
    source_name_entry.grid(row=2, column=1)
    # source_name_entry.insert(END, source_id)

    item_price_label = tb.Label(editWindow_frame, text="Item Price   $")
    item_price_label.grid(row=3, column=0)
    item_price_entry = tb.Entry(editWindow_frame)
    item_price_entry.grid(row=3, column=1)
    item_price_entry.insert(END, item_price)

    item_value_label = tb.Label(editWindow_frame, text="Item Value   $")
    item_value_label.grid(row=4, column=0)
    item_value_entry = tb.Entry(editWindow_frame)
    item_value_entry.grid(row=4, column=1)
    item_value_entry.insert(END, item_value)

    item_location_label = tb.Label(editWindow_frame, text="Item Location")
    item_location_label.grid(row=5, column=0)
    item_location_entry = tb.Entry(editWindow_frame)
    item_location_entry.grid(row=5, column=1)
    item_location_entry.insert(END, item_location)

    item_date_label = tb.Label(editWindow_frame, text="Date acquired")
    item_date_label.grid(row=6, column=0)
    item_date_entry = tb.Entry(editWindow_frame)
    item_date_entry.grid(row=6, column=1)
    item_date_entry.insert(END, item_date)

    item_status = 1
    if user_role == 'admin':
        def checker():
            global item_status
            if item_status_btn.get() == 1:
                item_status_label.config(text="Active")
                item_status = 1
            else:
                item_status_label.config(text="Deleted")
                item_status = 0
        item_status_btn = tb.IntVar()
        item_status_label = tb.Label(editWindow_frame, text="Status")
        item_status_label.grid(row=7, column=0)
        item_status_checkbox = tb.Checkbutton(editWindow_frame, bootstyle="round-toggle", text="Active", variable=item_status_btn, onvalue=1, offvalue=0, command=checker)
        item_status_checkbox.grid(row=7, column=1, pady=10)
        # item_status_entry = tb.Entry(editWindow_frame)
        # item_status_entry.grid(row=7, column=1)

    description_frame = tb.Frame(editWindow)
    description_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    item_description_label = tb.Label(description_frame, text="Item Description")
    item_description_label.grid(row=0, column=0)
    item_description_entry = tb.Text(description_frame, width=30, height=10)
    item_description_entry.grid(row=1, column=0, columnspan=2)
    item_description_entry.insert(END, item_description)

    # print(category_name_entry.get())
    # print(source_name_entry.get())

    button_frame = tb.Frame(editWindow)
    button_frame.grid(row=9, column=0, sticky="news", padx=10, pady=10)
    button_frame.columnconfigure(0, weight=2)
    button_frame.columnconfigure(1, weight=2)

# submit new data to the databse, or close
    button = tb.Button(button_frame, text="Submit", style="secondary.Outline.TButton",
                       command=lambda: update_item(category_name_entry, source_name_entry, item_name_entry,
                                                   item_description_entry, item_price_entry, item_value_entry,
                                                   item_location_entry, item_date_entry, item_status))
    button.grid(row=0, column=0, sticky="news", padx=30, pady=10)
    close_button = tb.Button(button_frame, text="Close", style="secondary.Outline.TButton", command=editWindow.destroy)
    close_button.grid(row=0, column=1, sticky="news", padx=30, pady=10)


# collections window to allow user to change which is the current collection, or delete

def collections_window():
    global user_id
# get a list of collections
    collections = get_collections()
    # print(collections)
    collection_names = []
# add the collection names to a list for the combobox
    for collection in collections:
        # print(collection[1])
        collection_names += [collection[1]]
    # print(collection_names)
    global app

# draw the window
    collectionsWindow = tb.Toplevel(app)
    collectionsWindow.title('Your Collections')

    collectionsWindow_frame = tb.LabelFrame(collectionsWindow, style="success", padding=20, text="Item Information")
    collectionsWindow_frame.grid(row=0, column=0, padx=20, pady=10)

# display results of database query
    collections_label = tb.Label(collectionsWindow_frame, text='Chose a collection')
    collections_label.grid(row=0, column=0, columnspan=2, sticky="news")
    collections_list = tb.Combobox(collectionsWindow_frame, values=collection_names)
    collections_list.grid(row=1, column=0, columnspan=2, sticky="news")

# buttons to open, delete, or cancel
    collections_open_button = tb.Button(collectionsWindow_frame, style="secondary-outline", text="open",
                                        command=lambda: change_collection(collections_list, collectionsWindow))
    collections_open_button.grid(row=2, column=0, padx=10, pady=10, sticky="news")
    collection_close_button = tb.Button(collectionsWindow_frame, style="secondary-outline", text="cancel",
                                        command=collectionsWindow.destroy)
    collection_close_button.grid(row=2, column=1, padx=10, pady=10, sticky="news")
# only admin can delete data
    if user_role == 'admin':
        collection_delete_button = tb.Button(collectionsWindow_frame, style="secondary-outline", text="delete",
                                             command=lambda: delete_collection(collections_list))
        collection_delete_button.grid(row=3, column=0, padx=10, columnspan=2, pady=10, sticky="news")


# button to view category list with delete option
def categories_window():
    global user_id
# get a list of categories
    categories = get_categories()
    # print(categories)
    category_names = []
# add category names to a list
    for category in categories:
        # print(category[1])
        category_names += [category[1]]
    # print(category_names)

# draw window
    global app
    categoriesWindow = tb.Toplevel(app)
    categoriesWindow.title('Your categories')

    categoriesWindow_frame = tb.LabelFrame(categoriesWindow, style="success", padding=20, text="Item Information")
    categoriesWindow_frame.grid(row=0, column=0, padx=20, pady=10)

# combobox to show categories
    categories_label = tb.Label(categoriesWindow_frame, text='Chose a category')
    categories_label.grid(row=0, column=0, columnspan=2, sticky="news")
    categories_list = tb.Combobox(categoriesWindow_frame, values=category_names)
    categories_list.grid(row=1, column=0, columnspan=2, sticky="news")

# buttons to delete a category or close window
    collection_close_button = tb.Button(categoriesWindow_frame, style="secondary-outline", text="close",
                                        command=categoriesWindow.destroy)
    collection_close_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="news")

# only admin can delete data
    if user_role == 'admin':
        collection_delete_button = tb.Button(categoriesWindow_frame, style="secondary-outline", text="delete",
                                             command=lambda: delete_category(categories_list))
        collection_delete_button.grid(row=3, column=0, columnspan = 2, padx=10, pady=10, sticky="news")


# window to view the current sources
def sources_window():
    global user_id
# get a list of sources
    sources = get_sources()
    # print(collections)
    source_names = []
# add source names to a list
    for source in sources:
        # print(collection[1])
        source_names += [source[1]]
    # print(collection_names)

# draw window
    global app
    sourcesWindow = tb.Toplevel(app)
    sourcesWindow.title('Your Collections')

    sourcesWindow_frame = tb.LabelFrame(sourcesWindow, style="success", padding=20, text="Source Information")
    sourcesWindow_frame.grid(row=0, column=0, padx=20, pady=10)

# combobox to show the list of sources
    sources_label = tb.Label(sourcesWindow_frame, text='Chose a source')
    sources_label.grid(row=0, column=0, columnspan=2, sticky="news")
    sources_list = tb.Combobox(sourcesWindow_frame, values=source_names)
    sources_list.grid(row=1, column=0, columnspan=2, sticky="news")

# buttons to edit or delete a source record, or close
    sources_open_button = tb.Button(sourcesWindow_frame, style="secondary-outline", text="edit",
                                    command=lambda: edit_source(sources_list))
    sources_open_button.grid(row=2, column=0, padx=10, pady=10, sticky="news")
    sourcesclose_button = tb.Button(sourcesWindow_frame, style="secondary-outline", text="close",
                                    command=sourcesWindow.destroy)
    sourcesclose_button.grid(row=2, column=1, padx=10, pady=10, sticky="news")
# only admin can delete data
    if user_role == 'admin':
        sourcesdelete_button = tb.Button(sourcesWindow_frame, style="secondary-outline", text="delete",
                                         command=lambda: delete_source(sources_list))
        sourcesdelete_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="news")


# Window to add a new item record

def new_record_window():
# get a list of sources and categories to use with comboboxes
    sources = get_sources()
    categories = get_categories()

# draw window with Entry fields for each piece of information
    global app
    newRecordWindow = tb.Toplevel(app)
    newRecordWindow.title("New Record")

    newRecord_frame = tb.LabelFrame(newRecordWindow, text="Item Information")
    newRecord_frame.grid(row=0, column=0, padx=20, pady=10)

    newItem_name_label = tb.Label(newRecord_frame, text="Item Name")
    newItem_name_label.grid(row=0, column=0)
    newItem_name_entry = tb.Entry(newRecord_frame)
    newItem_name_entry.grid(row=0, column=1)

    newCategory_name_label = tb.Label(newRecord_frame, text="Category")
    newCategory_name_label.grid(row=1, column=0)
    newCategory_name_entry = tb.Combobox(newRecord_frame, values=categories)
    newCategory_name_entry.grid(row=1, column=1)

    newSource_name_label = tb.Label(newRecord_frame, text="Source")
    newSource_name_label.grid(row=2, column=0)
    newSource_name_entry = tb.Combobox(newRecord_frame, values=sources)
    newSource_name_entry.grid(row=2, column=1)

    newItem_price_label = tb.Label(newRecord_frame, text="Item Price   $")
    newItem_price_label.grid(row=3, column=0)
    newItem_price_entry = tb.Entry(newRecord_frame)
    newItem_price_entry.grid(row=3, column=1)

    newItem_value_label = tb.Label(newRecord_frame, text="Item Value   $")
    newItem_value_label.grid(row=4, column=0)
    newItem_value_entry = tb.Entry(newRecord_frame)
    newItem_value_entry.grid(row=4, column=1)

    newItem_location_label = tb.Label(newRecord_frame, text="Item Location")
    newItem_location_label.grid(row=5, column=0)
    newItem_location_entry = tb.Entry(newRecord_frame)
    newItem_location_entry.grid(row=5, column=1)

    newItem_date_label = tb.Label(newRecord_frame, text="Date acquired")
    newItem_date_label.grid(row=6, column=0)
    newItem_date_entry = tb.Entry(newRecord_frame)
    newItem_date_entry.grid(row=6, column=1)

    newDescription_frame = tb.Frame(newRecordWindow)
    newDescription_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

# description box is extra large for multi-line input
    newItem_description_label = tb.Label(newDescription_frame, text="Item Description")
    newItem_description_label.grid(row=0, column=0)
    newItem_description_entry = tb.Text(newDescription_frame, width=30, height=10)
    newItem_description_entry.grid(row=1, column=0, columnspan=2)

    # print(category_name_entry.get())
    # print(source_name_entry.get())

# buttons to save or cancel
    new_button_frame = tb.Frame(newRecordWindow)
    new_button_frame.grid(row=8, column=0, sticky="news", padx=10, pady=10)
    new_button_frame.columnconfigure(0, weight=2)
    new_button_frame.columnconfigure(1, weight=2)

    # collection_id = 1

# data passed to new_item function
    new_button = tb.Button(new_button_frame, text="Submit", style="secondary.Outline.TButton",
                           command=lambda: new_item(collection_id, newCategory_name_entry, newSource_name_entry,
                                                    newItem_name_entry,
                                                    newItem_description_entry, newItem_price_entry, newItem_value_entry,
                                                    newItem_location_entry, newItem_date_entry, newRecordWindow))
    new_button.grid(row=0, column=0, sticky="news", padx=30, pady=10)
    new_close_button = tb.Button(new_button_frame, text="Close", style="secondary.Outline.TButton", command=newRecordWindow.destroy)
    new_close_button.grid(row=0, column=1, sticky="news", padx=30, pady=10)





########################### Section 3: Control Functions ##################################


# function called to redraw the Table data after it has changed
def refresh_app():
    global appFrame
    global app
    appFrame.destroy()
    app_start()

# basic controller draws the app window and its parts
def app_start():
    global app
    global appFrame
    colors = app.style.colors

# rows and columns weighted to align each section
    appFrame = tb.Frame(app)
    appFrame.grid(row=0, column=0, sticky="nsew")

    appFrame.rowconfigure(0, weight=1)
    appFrame.rowconfigure(1, weight=1)
    appFrame.rowconfigure(2, weight=4)
    appFrame.rowconfigure(3, weight=4)
    appFrame.rowconfigure(4, weight=4)
    appFrame.rowconfigure(5, weight=4)
    appFrame.rowconfigure(6, weight=4)

    appFrame.columnconfigure(0, weight=1)
    appFrame.columnconfigure(1, weight=2)
    appFrame.columnconfigure(2, weight=2)

# actions frame (top right) with buttons

    frame_actions = tb.Frame(appFrame, style="secondary", borderwidth=8, relief="groove", padding=4)
    frame_actions.grid(row=0, column=1, rowspan=2, columnspan=2, sticky=W + E + N + S)

    frame_actions.columnconfigure(0, weight=1, pad=1)
    frame_actions.columnconfigure(1, weight=1, pad=1)
    frame_actions.columnconfigure(2, weight=1, pad=1)

    frame_actions.rowconfigure(0, weight=1)
    frame_actions.rowconfigure(1, weight=1)

    label_actions = tb.Label(frame_actions, text="Actions", font=("Helvetica", 18))
    label_actions.configure(anchor=CENTER)
    label_actions.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # six actions buttons to view/edit collections, sources, and categories

    button_new_collection = tb.Button(frame_actions, text="New Collection", bootstyle="primary-outline",
                                      command=new_collection_window)
    button_new_collection.grid(row=0, column=0, sticky="nsew")

    button_logout = tb.Button(frame_actions, text="New Category", bootstyle="primary-outline",
                              command=new_category_window)
    button_logout.grid(row=0, column=1, sticky="nsew")

    button_source = tb.Button(frame_actions, text='New Source', bootstyle="primary-outline", command=new_source_window)
    button_source.grid(row=0, column=2, sticky="nsew")

    button_change_collection = tb.Button(frame_actions, text="Collections", bootstyle="primary-outline",
                                         command=collections_window)
    button_change_collection.grid(row=1, column=0, sticky="nsew")

    button_change_category = tb.Button(frame_actions, text="Categories", bootstyle="primary-outline",
                                         command=categories_window)
    button_change_category.grid(row=1, column=1, sticky="nsew")

    button_change_source = tb.Button(frame_actions, text="Sources", bootstyle="primary-outline",
                                         command=sources_window)
    button_change_source.grid(row=1, column=2, sticky="nsew")

# top title frame
    frame_title = tb.Frame(appFrame, style="secondary", borderwidth=4, relief="groove", padding=4)
    frame_title.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=W + E + N + S)

    frame_title.columnconfigure(0, weight=1)
    frame_title.rowconfigure(0, weight=1)

    label_title = tb.Label(frame_title, text="Collection Manager", font=("Helvetica", 18), bootstyle="primary")
    label_title.configure(anchor=CENTER)
    label_title.grid(row=0, column=0, sticky="nsew")

    buttons_list = tb.Frame(appFrame, style="secondary", borderwidth=4, relief="groove", padding=4)
    buttons_list.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="news")

# unused button code
    buttons_list.columnconfigure(0, weight=10)
    buttons_list.columnconfigure(1, weight=10)
    buttons_list.columnconfigure(2, weight=10)
    buttons_list.columnconfigure(3, weight=1)

# exit button on title bar
    exit_button = tb.Button(frame_title, text="Exit", command=exit_application)
    exit_button.grid(row=0, column=0, sticky="w", padx=5)

# frame for the Tableview list
    # item list
    frame_list = tb.Frame(appFrame, style="default", borderwidth=4, relief="groove", padding=4)
    frame_list.grid(row=2, column=0, rowspan=5, columnspan=1, sticky=W + E + N + S)

# table data, columns named
    if user_role == 'admin':
        coldata = [
            "ID",
            "Item",
            "Category",
            "Location",
            "Source",
            "Price",
            "Value",
            "Status"
        ]
    else:
        coldata = [
        "ID",
        "Item",
        "Category",
        "Location",
        "Source",
        "Price",
        "Value",
    ]
# table data, from database query
    rowdata = selectQuery()

# create Tableview table
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
        height=28
    )
# place Table
    dt.grid(row=0, column=0, padx=30, pady=10, sticky="nsew")

    # Item

# Frame to show item report

    frame_item = tb.Frame(appFrame, style="primary", borderwidth=4, relief="groove", padding=4)
    frame_item.grid(row=2, column=1, rowspan=5, columnspan=2, sticky=W + E + N + S)

    frame_item.columnconfigure(0, weight=1, pad=1)
    frame_item.columnconfigure(1, weight=1, pad=1)
    frame_item.rowconfigure(0, weight=1)
    frame_item.rowconfigure(1, weight=1)
    frame_item.rowconfigure(2, weight=20)

    label_item = tb.Label(frame_item, text="Item Info", font=("Helvetica", 18))
    label_item.configure(anchor=CENTER)
    label_item.grid(row=0, column=0, sticky="nsew", columnspan=2)

    frame_info_box = tb.Frame(frame_item, style="default", borderwidth=4, relief="groove", padding=4)
    frame_info_box.grid(row=2, column=0, sticky="nsew", columnspan=2)

    # get selection and pass to the info box

# frame label
    label_item = tb.Label(frame_item, text="Item Info", font=("Helvetica", 18))
    label_item.configure(anchor=CENTER)
    label_item.grid(row=0, column=0, sticky="nsew", columnspan=2)
    print(item_id)

# frame to hold item data
    frame_info_box = tb.Frame(frame_item, style="default", borderwidth=4, relief="groove", padding=4)
    frame_info_box.grid(row=2, column=0, sticky="nsew", columnspan=2)

# item_info_box is populated by the get_item_info View function
    item_info_box = tb.Label(frame_info_box, text="Info")
    item_info_box.grid(row=0, column=0, sticky="nsew", rowspan=1, columnspan=2)
    item_info_box.configure(font=("Garamond", 18))

# buttons to edit a record, make a new record, or delete a record
    if user_role == 'admin':

        edit_button = tb.Button(buttons_list, text="Edit Record", bootstyle="primary-outline", command=edit_window)
        edit_button.grid(row=0, column=0, columnspan=1, sticky="nsew")

        new_button = tb.Button(buttons_list, text="New Record", bootstyle="primary-outline", command=new_record_window)
        new_button.grid(row=0, column=1, columnspan=1, sticky="nsew")

# only admin can delete data
        new_button = tb.Button(buttons_list, text="Delete Record", bootstyle="primary-outline",
                               command=lambda: delete_record(item_id))
        new_button.grid(row=0, column=2, columnspan=1, sticky="nsew")

    else:
        edit_button = tb.Button(buttons_list, text="Edit Record", bootstyle="primary-outline", command=edit_window)
        edit_button.grid(row=0, column=0, columnspan=1, sticky="nsew")

        new_button = tb.Button(buttons_list, text="New Record", bootstyle="primary-outline", command=new_record_window)
        new_button.grid(row=0, column=2, columnspan=1, sticky="nsew")

    # # manual refresh in case it is necessary
    # refresh_button = tb.Button(buttons_list, text="Refresh", bootstyle="primary-outline", command=refresh_app)
    # refresh_button.grid(row=0, column=3, columnspan=1, sticky="nsew")

# **** THIS LITTLE LINE CAUSED ME HOURS OF TROUBLE *****
    # bind the table event of clicking on a row to populate/update the item report frame
    dt.view.bind("<<TreeviewSelect>>", lambda event: get_item_info(dt, item_info_box))

# function to get user data for login system
def get_user_data(username, password):
    sqliteConnection = sqlite3.connect('collectorsTool.sqlite')
    cursor = sqliteConnection.cursor()
    query = (
        'SELECT * FROM user WHERE username = ? AND userPassword = ?;')
    data = (username, password)
    cursor.execute(query, data)
    result = cursor.fetchall()
    cursor.close()
    # print(result)
    return result

# function to exit the application
def exit_application():
    root.quit()

# the restart function is used with a failed login, to retry
def restart_application():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# function to get the username and password, check the database for authentication, and pass to set_collection_window
def create_app(user_label_entry, pass_label_entry):
    global app
    global root
    global theme
    global user_id
    global user_role
    username = str(user_label_entry.get())
    password = str(pass_label_entry.get())

    # get user preferences
    user_data = get_user_data(username, password)
# if query returns no data, or data that does not match, send error and try again
    if len(user_data) == 0:
        Messagebox.show_info(title="Login error", message="Username or Password is incorrect. Please try again.")
        restart_application()
    elif user_data[0][7] == 1:
        # set variables
        theme = user_data[0][8]
        user_id = user_data[0][0]
        user_role = user_data[0][3]
        print(user_id)
        print(user_role)
        # set collection and start application
        # set current collection; the set_collection_window function calls set_collection, which calls start_app
        set_collection_window()
        print(collection_id)
    else:
# this is if the login data is correct, but the user has been set to inactive status
        Messagebox.show_info(title="Login error", message="User has been deleted. Please try again.")
        restart_application()

# After user has authenticated and chosen a collection, draw root window and then start the main application
def start_app():
    global root
    global app
    global user_id
    app = tb.Toplevel(root)
    app.geometry("1200x800")
    app.title("Collections")
    root.withdraw()

# this is the core control function that draws the application window
    # start app window
    app_start()

# initialize variables and set theme
theme = "flatly"
item_id = ""
user_id = ""
collection_id = ""

# root window for login screen
root = tb.Window(themename=theme)
root.geometry("550x300")

root.title("Collectors Tool")

loginFrame = tb.Frame(root)
loginFrame.grid(column=0, row=0, padx=50, pady=30, sticky="nsew")

# login Entry fields
credFrame = tb.LabelFrame(loginFrame, text="Enter your username and password", style="success")
credFrame.grid(column=0, row=0, sticky="news", padx=50, pady=30)
credFrame.columnconfigure(0, weight=1)
credFrame.columnconfigure(1, weight=1)

user_label = tb.Label(credFrame, text="Username")
user_label.grid(row=1, column=0, sticky="news", padx=20, pady=10)

user_label_entry = tb.Entry(credFrame)
user_label_entry.grid(row=1, column=1, sticky="news", padx=20, pady=10)

pass_label = tb.Label(credFrame, text="Password")
pass_label.grid(row=2, column=0, sticky="news", padx=20, pady=10)

pass_label_entry = tb.Entry(credFrame, show="*")
pass_label_entry.grid(row=2, column=1, sticky="news", padx=20, pady=10)

# pass input data to the control functions that start app
login_button = tb.Button(credFrame, text="Login", command=lambda: create_app(user_label_entry, pass_label_entry))
login_button.grid(row=3, column=0, columnspan=2, sticky="news", padx=10, pady=20)

root.mainloop()

