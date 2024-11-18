import sqlite3
import json
from datetime import date
import os
from DateConversions import DateFormatToWords, DayOfWeekAlgorithm, DateWordsToFormat
from SearchesAndSorts import BinarySearch, LinearSearch
from DateConversions import DaysBetweenDates, IsLeapYear, AddDays

def RetrieveColumn(Field, Table):

    # A connection to the database is estblished
    connection = sqlite3.connect('System.db')
    cursor = connection.cursor()

    # The requested field is selected from the database and stored in an array
    cursor.execute(f'SELECT {Field} FROM {Table}')
    Array = cursor.fetchall()

    # The database connection is close
    connection.commit()
    connection.close()

    # The array is returned
    return Array

def GetValueFromTable(Table, Column, ID):

    # A connection to the database is estblished
    connection = sqlite3.connect('System.db')
    cursor = connection.cursor()

    # The entire of the required table is retrieved and stored in a 2 dimensional array
    Array = GetEntireTable(Table)

    # The first element of each array (ID) in the 2 dimensional array is stored in another array
    IDArray = [Tuple[0] for Tuple in sorted(Array, key=lambda x: Array.index(x))]

    # If the ID is an integer, a binary search is used to find the index of the required record
    try:
        int(ID)
        Row = BinarySearch(IDArray, ID)

    # If the ID is not an integer (the accounts table), a linear search is used
    except:
        Row = LinearSearch(IDArray, ID)

    # The index must be used and not the ID.
    # This is because, if some records have been deleted, the ID and the index in the array will not be the same

    # The database connection is closed
    connection.commit()
    connection.close()

    # The element at the Row and column required is returned
    return Array[Row][Column]

def GetEntireTable(Table):

    # A connection to the database is established
    connection = sqlite3.connect('System.db')
    cursor = connection.cursor()

    # The entire of the required table is stored in an array
    cursor.execute(f'SELECT * FROM {Table}')
    Array = cursor.fetchall()

    # The array is currently an array of tuples so this is converted to an array of arrays (a 2 dimensional array)
    Array = [list(row) for row in Array]

    # The database connection is close
    connection.commit()
    connection.close()

    # The table array is returned
    return Array

def RemoveRecord(Table, ID):

    # A connection to the database is established
    connection = sqlite3.connect('System.db')
    cursor = connection.cursor()

    # The record in the required table is deleted where the ID matches the ID passed to this subroutine
    cursor.execute(f'DELETE FROM {Table} WHERE id = ?', (ID,))

    # The database connection is closed
    connection.commit()
    connection.close()

def ReturnUsefulDataToDisplay(Array):
    # This subroutine will take an input of a booking record and return its data in the correct format to be processed/displayed

    # The useful array is initialised
    UsefulArray = []

    # Booking ID is needed to display information for the correct event
    UsefulArray.append(Array[0])

    # Client names
    UsefulArray.append(Array[1])
    UsefulArray.append(Array[2])

    # CustomerID
    UsefulArray.append(Array[3])

    # Type of event - If the event is one of the wedding packages, the type of event is changed to 'Wedding'
    TypeOfEvent = GetValueFromTable('TypeOfEvents', 1, Array[5])
    if TypeOfEvent == 'Wedding1' or TypeOfEvent == 'Wedding2' or TypeOfEvent == 'Wedding3':
        TypeOfEvent = 'Wedding'
    UsefulArray.append(TypeOfEvent)

    # Booking day (of the week)
    UsefulArray.append(DayOfWeekAlgorithm(Array[6]))

    # Booking date - This will be displayed in the word format so is coverted
    UsefulArray.append(DateFormatToWords(Array[6]))

    # Start and end times
    UsefulArray.append(Array[7])
    UsefulArray.append(Array[8])

    # Guest numbers
    UsefulArray.append(Array[9])
    UsefulArray.append(Array[10])
    UsefulArray.append(Array[11])

    # All boolean values are converted to either True or False
    # Currently, the may be stored as 0/1 or 'true'/'false'
    # This is due to the way different programming languages represent boolean values

    # Booking status (is the booking accepted?)
    if Array[12] == 1:
        UsefulArray.append(True)
    else:
        UsefulArray.append(False)

    # Remaining deposit to be paid - rounded
    DepositRemaining = f"{Array[14]:.2f}"
    UsefulArray.append(DepositRemaining)

    # Remaining cost to be paid - rounded
    CostRemaining = f"{Array[15]:.2f}"
    UsefulArray.append(CostRemaining)

    # Drinks for toasting required
    if Array[16] == 'true':
        UsefulArray.append(True)
    else:
        UsefulArray.append(False)

    # Ceremony room required
    if Array[17] == 'true':
        UsefulArray.append(True)
    else:
        UsefulArray.append(False)

    # Ceremony time
    UsefulArray.append(Array[18])

    # Welcome drinks
    if Array[19] == 'true':
        UsefulArray.append(True)
    else:
        UsefulArray.append(False)

    UsefulArray.append(Array[20])
    UsefulArray.append(Array[21])

    # Set up required
    if Array[22] == 'true':
        UsefulArray.append(True)
    else:
        UsefulArray.append(False)

    # Additional event information
    UsefulArray.append(Array[23])

    TodaysDate = str(date.today())
    DateBookingWillBeAccepted = AddDays(Array[24], 7)

    # Days since booking was made
    if int(DateBookingWillBeAccepted[0:4]) > int(TodaysDate[0:4]):
        UsefulArray.append(DaysBetweenDates(TodaysDate, DateBookingWillBeAccepted))
    elif IsLeapYear(Array[6]):
        UsefulArray.append(366 - DaysBetweenDates(DateBookingWillBeAccepted, TodaysDate))
    else:
        UsefulArray.append(365 - DaysBetweenDates(DateBookingWillBeAccepted, TodaysDate))

    # Unavailable date flag
    if Array[25] == 1:
        UsefulArray.append(True)
    else:
        UsefulArray.append(False)

    # Date in the format that it is stored in
    # In some cases, the date will also still need to be displayed in the form YYYY-MM-DD
    UsefulArray.append(Array[6])

    # For weddings, the package number is added to the array, if the event is not a wedding, an empty string is added
    TypeOfEvent = GetValueFromTable('TypeOfEvents', 1, Array[5])
    if TypeOfEvent == 'Wedding1' or TypeOfEvent == 'Wedding2' or TypeOfEvent == 'Wedding3':
        PackageOption = TypeOfEvent[-1]
    else:
        PackageOption = ''
    UsefulArray.append(PackageOption)

    # The date that the booking was made
    # This is needed to sort bookings by when they were made
    UsefulArray.append(Array[24])

    return UsefulArray

def RetrieveAdultDrinks():

    ''' Files are used to store the adult and child welcome drinks as it is a more simple and 
    lightweight way of stroing the small amounts of data that creating a new table in the database '''

    # The path of the current module is found
    System = os.path.dirname(os.path.abspath(__file__))

    # The file path from the current module to the adult welcome drinks file is stored
    PathToFile = os.path.join(System, 'data', 'AdultWelcomeDrinks.json')

    # The adults welcome drink file is opened and its contents are returned
    with open(PathToFile) as file:
        return json.load(file)
    
def RetrieveChildrenDrinks():

    # The path of the current module is found
    System = os.path.dirname(os.path.abspath(__file__))

    # The file path from the current module to the childrens welcome drinks file is stored
    PathToFile = os.path.join(System, 'data', 'ChildrenWelcomeDrinks.json')

    # The childrens welcome drink file is opened and its contents are returned
    with open(PathToFile) as file:
        return json.load(file)
    
def GetYearBookingToDisplay(Timeframe):

    # The array of bookings to display is initialised
    BookingsToDisplay = []

    # The dates of bookings are retrieved from the bookings table and converted to an array
    BookingDates = RetrieveColumn('DateOfBooking', 'Bookings')
    BookingDates = [Tuple[0] for Tuple in BookingDates]

    # The entire bookings table is retrieved and stored in an array
    BookingsTable = GetEntireTable('Bookings')

    # Count is initialised as 0 and is incremented in each loop
    # This is once again necessary as the booking ID may not match the index of that booking in the database
    # This is due to the fact that some bookings may have been deleted
    Count = 0
    for Bookings in BookingDates:

        # If the year of the booking matches the year of the timeframe (the year that is currently being displayed on the calendar)
        # That booking's array is added to the list of bookings to display 
        if Bookings[0:4] == str(Timeframe):

            # If the booking is a genuine booking, it is passed to the ReturnUsefulDataToDisplay function where only the necessary data from the record is returned
            # The booking must also be accepted to be shown on the calendat
            if (BookingsTable[Count][25] == False):
                BookingsToDisplay.append(ReturnUsefulDataToDisplay(BookingsTable[Count]))

            # If the booking is not a genuine booking and instead is an unavailable date,
            # It is still added to the bookings to display array in the same format but the only relevant data required is the date
            else:
                BookingsToDisplay.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, BookingsTable[Count][6]])
        Count += 1

    # When the loop has finished, the array is returned
    return BookingsToDisplay

def GetMonthBookingsToDisplay(Timeframe):

    # The bookings to display array is initialised
    BookingsToDisplay = []

    # The dates of bookings are retrieved from the bookings table and converted to an array
    BookingDates = RetrieveColumn('DateOfBooking', 'Bookings')
    BookingDates = [Tuple[0] for Tuple in BookingDates]

    # The timeframe (the month and year currently being displayed on the calendar) is converted to the form YYYY-MM
    Timeframe = DateWordsToFormat("1 " + Timeframe)[0:7]

    # The entire bookings table is retrieved and stored in an array
    BookingsTable = GetEntireTable('Bookings')

    # Count is initialised as 0 and is incremented in each loop
    # This is once again necessary as the booking ID may not match the index of that booking in the database
    # This is due to the fact that some bookings may have been deleted
    Count = 0
    for Bookings in BookingDates:

        # If the month and year of the booking matches the timeframe,
        # That booking's array is added to the list of bookings to display 
        if Bookings[0:7] == str(Timeframe):

            # If the booking is a genuine booking, it is passed to the ReturnUsefulDataToDisplay function where only the necessary data from the record is returned
            # The booking must also be accepted to be displayed on the calendar
            if (BookingsTable[Count][25] == False):
                BookingsToDisplay.append(ReturnUsefulDataToDisplay(BookingsTable[Count]))

            # If the booking is not a genuine booking and instead is an unavailable date,
            # It is still added to the bookings to display array in the same format but the only relevant data required is the date
            else:
                BookingsToDisplay.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, BookingsTable[Count][6]])
        Count += 1

    # When the loop has finished, the array is returned
    return BookingsToDisplay

def GetWeekBookingsToDisplay(FirstDayOfWeek):

    # The bookings to display array is initialised
    BookingsToDisplay = []

    # The dates of bookings are retrieved from the bookings table and converted to an array
    BookingDates = RetrieveColumn('DateOfBooking', 'Bookings')
    BookingDates = [Tuple[0] for Tuple in BookingDates]

    # The entire bookings table is retrieved and stored in an array
    BookingsTable = GetEntireTable('Bookings')

    for i in range(7):

        # This must be repeated 7 times as each date needs to be checked to see if it matches any day in the current week being display
        DayOfWeek = AddDays(FirstDayOfWeek, i)

        # Count is initialised as 0 and is incremented in each loop
        # This is once again necessary as the booking ID may not match the index of that booking in the database
        # This is due to the fact that some bookings may have been deleted
        Count = 0
        for Bookings in BookingDates:

            # If the date of the booking matches the current day that it is being compared to,
            # That booking's array is added to the list of bookings to display
            if DayOfWeek == Bookings:

                # If the booking is a genuine booking, it is passed to the ReturnUsefulDataToDisplay function where only the necessary data from the record is returned
                # The booking must also be accepted to be displayed on the calendar
                if (BookingsTable[Count][25] == False):
                    BookingsToDisplay.append(ReturnUsefulDataToDisplay(BookingsTable[Count]))

                 # If the booking is not a genuine booking and instead is an unavailable date,
                # It is still added to the bookings to display array in the same format but the only relevant data required is the date   
                else:
                    BookingsToDisplay.append([0, 0, 0, 0, 0, DayOfWeekAlgorithm(DayOfWeek), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, BookingsTable[Count][6]])
            Count = Count + 1

    # When the loop has finished, the array is returned
    return BookingsToDisplay

def RemoveOption(Table, ColumnName, Data):

    # A connection to the database is established
    connection = sqlite3.connect('System.db')
    cursor = connection.cursor()

    # The rquired record is deleted from the database
    cursor.execute(f"DELETE FROM {Table} WHERE {ColumnName} = ?", (Data,))

    # The connection to the database is closed
    connection.commit()
    connection.close()