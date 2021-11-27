#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# AWillie, 2021-Nov-17, Added add function and delete function
# AWillie, 2021-Nov-18, Worked on save and load function
# AWillie, 2021-Nov-21, Added ID naming function
# AWillie, 2021-Nov-26, Added pickling and some error handling
# AWillie, 2021-Nov-27, Fixed load pickling function
#------------------------------------------#

# -- DATA -- #
import pickle

strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object
ID = 0

# -- PROCESSING -- #
class DataProcessor:
    @staticmethod
    def New_ID():
        global ID
        ID += 1
    @staticmethod
    def add_Title(strTitle, strArtist):
        """ Function to add additonal CD's to inventory
            
        Uses the input as variable to add to a dictionary to add to the inventory
        
        Args:
            strTitle: Variable for the CD title
            strArtist: Variable for the CD\'s Artist
        
        Returns:
            None.
        """
        global ID
        DataProcessor.New_ID()
        dicRow = {'ID': ID, 'CD Title': strTitle, 'Artist': strArtist}
        lstTbl.append(dicRow)
        print('Your CD has been added')
        print()
    @staticmethod
    def del_Title(IDIntDel):
        """Function to delete a chosen CD title
        
        User input the desired ID they would like to delete
        
        Args:
            IDIntDel: The ID # that is chosen to be deleted
        
        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
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
    def read_file(FileName, lstTable):
        """Function to read a binary file and to return the list data

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        lstTable.clear()
        with open(FileName, 'rb+') as objFile:
            try:
                lstTable = pickle.load(objFile)
            except:
                print('Something has gone wrong!')
            else:
                print ('Successful read: %s' % (objFile))
            objFile.close()
            return list(lstTable)
    @staticmethod
    def write_file(FileName, lstTable):
        # Added code here
        """Function to save data to a binary file
        
        Takes the current memory and moves it to a binary file
        
        Args:
            file_name(string): name of file used to copy memory to
            table (list of dict): 2D data structure holding the inventory
        Returns:
            None.
        """
        with open(FileName, 'wb+') as objFile:
            try:
                pickle.dump(lstTable, objFile)
            except:
                print('An error has occured')
            else:
                print ('Successful write: %s' % (objFile))
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
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # moved IO code into function
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        DataProcessor.add_Title(strTitle, strArtist)
        IO.show_inventory(lstTbl)
        # 3.3.2 Add item to the table
        #moved processing code into function
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
        # moved processing code into function
        DataProcessor.del_Title(intIDDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        if strYesNo == 'y':
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




