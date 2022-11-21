#------------------------------------------#
# Title: Assignment06.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# Rain Doggerel, 2022-Nov-20 bug hunted and added docstrings
# Rain Doggerel, 2022-Nov-19, Moved things around
# DBiesinger, 2030-Jan-01, Created File
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    # TODO add functions for processing here
    @staticmethod
    def new_album_add(aIntID,aTitle,aArtist,aTable):
        """Function to add an entry to a list of dictionaries

        Composes a new dictionary to append to an existing list of dictionaries.

        Args:
            aIntID (Int): the index of this new album 
            aTitle (Str): the title of the new album
            aArtist (Str): the artist of the new album
            aTable (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            Updated list of dictionaries table.
        """
        addRow = {'ID': aIntID, 'Title': aTitle, 'Artist': aArtist}
        aTable.append(addRow)
        return aTable
    
    @staticmethod
    def delete_album(searchID,dTable):
        """Function to remove an entry from a list of dictionaries

        Loops through the list of dictionaries seeking an entry that matches a
        particular ID and if found deletes it or reports otherwise.

        Args:
            searchID (Int): the index within the inventory to find and delete 
            dTable (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in dTable:
            intRowNr += 1
            if row['ID'] == searchID:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'r')
        for line in objFile:
            data = line.strip().split(',')
            dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
            table.append(dicRow)
        objFile.close()

    @staticmethod
    def write_file(file_name, wTable):
        # TODO Add code here
        """Function to write the inventory to a file

        Unpacks dictionary, composes strings and concatenates them and writes
        that to a file.

        Args:
            file_name (Str): name of the inventory file

        Returns:
            None.
        """
        objFile = open(file_name, 'w')
        for row in wTable:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(','.join(lstValues) + '\n')
        objFile.close()
        

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        
    # TODO add I/O functions as needed
    @staticmethod
    def new_album_query():
        """Queries user for new album details

        Args:
            None.

        Returns:
            List of user inputs (Int, Str, Str).

        """
        fID = input('Enter ID: ').strip()
        fTitle = input('What is the CD\'s title? ').strip()
        fArtist = input('What is the Artist\'s name? ').strip() # lol
        fIntID = int(fID)
        newAlbumInput = [fIntID,fTitle,fArtist]
        return newAlbumInput
        

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file, otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # TODO move IO code into function
        newEntry = IO.new_album_query()

        # 3.3.2 Add item to the table
        # TODO move processing code into function
        lstTbl = DataProcessor.new_album_add(newEntry[0],newEntry[1],newEntry[2],lstTbl) # Do we write lstTbl twice, what is the ref/scope on that
        
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
        # TODO move processing code into function
        DataProcessor.delete_album(intIDDel, lstTbl)

        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            # TODO move processing code into function
            FileProcessor.write_file(strFileName, lstTbl)

        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




