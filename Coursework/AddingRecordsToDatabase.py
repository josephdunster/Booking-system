import sqlite3
import os
import json
from RetrieveDataFromDatabase import GetValueFromTable
from datetime import date

def AddNewAccount(Username, Password):
    
    # A connection to the database is established
    connection = sqlite3.connect('System.db')
    cursor = connection.cursor()

    # Username and password are insertd into the acccounts table and isAdmin is always set to false
    cursor.execute("INSERT INTO Accounts (id, Password, IsAdmin) VALUES (?, ?, ?)", 
                   (Username, Password, False))

    # The database connection is closed
    connection.commit()
    connection.close()

def AddNewCustomer(FirstName, Surname, PhoneNumber, EmailAddress, Username):
    
    # A connection to the database is established
    connection = sqlite3.connect('System.db')
    cursor = connection.cursor()

    # The customer information is added to the database
    cursor.execute("INSERT INTO Customers (FirstName, LastName, EmailAddress, PhoneNumber, AccountID) VALUES (?, ?, ?, ?, ?)", 
                   (FirstName, Surname, EmailAddress, PhoneNumber, Username))

    # The database connection is closed
    connection.commit()
    connection.close()

def CalculateCost(SetUpRequired, CeremonyRequired, AdultGuests, ChildGuests, TypeOfEventID):
    
    # Cost is initialised at 0
    Cost = 0

    # If the user has chosen to have a set up day, the cost is increased by £495
    if SetUpRequired == True:
        Cost = Cost + 495

    # If the ceremony room is needed, the cost is increased by £495
    if CeremonyRequired == True:
        Cost = Cost + 495

    # If there is no type of event ID, this is a new event so the prices are automatically set
    if TypeOfEventID == False:
        CostPerAdult = 79
        CostPerChild = 39.5
    else:
        # Otherwise, the prices are retrieved from the database
        CostPerAdult = GetValueFromTable('TypeOfEvents', 2, TypeOfEventID)
        CostPerChild = GetValueFromTable('TypeOfEvents', 3, TypeOfEventID)

    # Total adult and child costs are calculated
    TotalAdultCost = int(AdultGuests) * CostPerAdult
    TotalChildCost = int(ChildGuests) * CostPerChild

    # The total event cost is calculated by adding all costs
    TotalCost = Cost + TotalAdultCost + TotalChildCost

    return TotalCost

def AddNewBooking(IsAdmin, ClientName1, ClientName2, CustomerID, AccountID, TypeOfEventID, DateOfBooking, StartTime, EndTime, AdultGuestNumber, ChildGuestNumber, Below2GuestNumber, DrinksForToastingRequired, CeremonyRequired, CeremonyTime, WelcomeDrinksRequired, AdultWelcomeDrink, ChildWelcomeDrink, SetUpRequired, Notes):

    # If the user who made the booking is an admin, the booking is automatically set to accepted
    # Otherwise, it is not
    IsAccepted = False
    if IsAdmin == True:
        IsAccepted = True

    # The cost is initialised at 0
    Cost = 0

    # If the ceremony room is needed, the cost is increased by £495
    if CeremonyRequired == True:
        Cost = 495

    # If the user has chosen to have a set up day, the cost is increased by £495
    if SetUpRequired == True:
        Cost = Cost + 495

    # The price for each adult and child is found from the type of events table
    PricePerAdult = GetValueFromTable('TypeOfEvents', 2, TypeOfEventID)
    PricePerChild = GetValueFromTable('TypeOfEvents', 3, TypeOfEventID)

    # The total adult and child costs are calculated
    TotalAdultCost = PricePerAdult * int(AdultGuestNumber)
    TotalChildCost = PricePerChild * int(ChildGuestNumber)

    # The total cost is calculated by adding the total adult and child cost to the current cost
    Cost = Cost + TotalAdultCost + TotalChildCost

    # The deposit is calculated
    RemainingDepositToBePaid = 0.3 * Cost

    # The remaining cost is calculated
    RemainingCostToBePaid = 0.7 * Cost

    # The date that the booking was made is stored
    DateBookingWasMade = str(date.today())

    # All bookings in this subroutine are genuine bookings and not just to mark unavailable dates
    IsUnavailableDate = False

    # Booking is added to the database
    connection = sqlite3.connect('System.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO Bookings (Client1, Client2, CustomerID, AccountID, TypeOfEventID, DateOfBooking, StartTime, EndTime, AdultGuestNumber, ChildGuestNumber, Under2GuestNumber, IsAccepted, Cost, RemainingDepositToBePaid, RemainingCostToBePaid, DrinksForToastingRequired, CeremonyRoomRequired, CeremonyTime, WelcomeDrinksRequired, AdultDrink, ChildDrink, IsSetUpRequired, Notes, DateBookingWasMade, IsUnavailableDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (ClientName1, ClientName2, CustomerID, AccountID, TypeOfEventID, DateOfBooking, StartTime, EndTime, AdultGuestNumber, ChildGuestNumber, Below2GuestNumber, IsAccepted, Cost, RemainingDepositToBePaid, RemainingCostToBePaid, DrinksForToastingRequired, CeremonyRequired, CeremonyTime, WelcomeDrinksRequired, AdultWelcomeDrink, ChildWelcomeDrink, SetUpRequired, Notes, DateBookingWasMade, IsUnavailableDate))

    connection.commit()
    connection.close()

def AddNewTypeOfEvent(TypeOfEvent, AdultPrice, ChildPrice):

    #  A connection to the database is established
    connection = sqlite3.connect('System.db')
    cursor = connection.cursor()

    # The event details are added to the database
    cursor.execute("INSERT INTO TypeOfEvents (TypeOfEvent, PricePerAdult, PricePerChild) VALUES (?, ?, ?)", 
                   (TypeOfEvent, AdultPrice, ChildPrice))

    # The database connection is closed
    connection.commit()
    connection.close()

def AddNewPayment(BookingID, PaymentAmount, PaymentType):

    # The column that needs to be edited is determined using the PaymentType variable
    if PaymentType == 'cost':
        CurrentRemainingCost = GetValueFromTable('Bookings', 15, int(BookingID))
        Column = 'RemainingCostToBePaid'
    else:
        CurrentRemainingCost = GetValueFromTable('Bookings', 14, int(BookingID))
        Column = 'RemainingDepositToBePaid'
        
    # If the payment being made is more than the remaining amount, the payment is not added
    if float(PaymentAmount) > CurrentRemainingCost:
        return False

    # The new remaining cost is calculated and the database is edited
    NewRemainingCost = CurrentRemainingCost - float(PaymentAmount)
    ReplaceValue('Bookings', Column, int(BookingID), NewRemainingCost)

def ReplaceValue(Table, ColumnName, ID, NewValue):

    # A connection to the database is established
    connection = sqlite3.connect('System.db')
    cursor = connection.cursor()

    # The given field in the given clumn is ammended with the newvalue
    cursor.execute(f'UPDATE {Table} SET {ColumnName} = ? WHERE id = ?', (NewValue, ID))

    # The database connection is closed
    connection.commit()
    connection.close()

def SaveAdultDrinks(Drinks):

    # The path of the current module is found
    System = os.path.dirname(os.path.abspath(__file__))

    # Path to the adult welcome drinks array is stored
    PathToFile = os.path.join(System, 'data', 'AdultWelcomeDrinks.json')

    # The file is opened in write mode and the drink array is written and saved
    with open(PathToFile, 'w') as file:
        # Save the array of drinks
        json.dump(Drinks, file)

def SaveChildDrinks(Drinks):

    # The path of the current module is found
    System = os.path.dirname(os.path.abspath(__file__))

    # Path to the adult welcome drinks array is stored
    PathToFile = os.path.join(System, 'data', 'ChildrenWelcomeDrinks.json')

    # The file is opened in write mode and the drink array is written and saved
    with open(PathToFile, 'w') as file:
        # Save the array of drinks
        json.dump(Drinks, file)

def AddNewUnavailableDate(Date):

    # A connection to the database is established
    connection = sqlite3.connect('System.db')
    cursor = connection.cursor()

    # A record is added to the Booking table.
    # Thee only necessary data to store for an unavailable date is the date itself and the flag indicating that it is an unavailable date
    # Everything else is set to 0 or 'null'
    cursor.execute("INSERT INTO Bookings (Client1, Client2, CustomerID, AccountID, TypeOfEventID, DateOfBooking, StartTime, EndTime, AdultGuestNumber, ChildGuestNumber, Under2GuestNumber, IsAccepted, Cost, RemainingDepositToBePaid, RemainingCostToBePaid, DrinksForToastingRequired, CeremonyRoomRequired, CeremonyTime, WelcomeDrinksRequired, AdultDrink, ChildDrink, IsSetUpRequired, Notes, DateBookingWasMade, IsUnavailableDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   ('null', 'null', 0, 0, 0, Date, 'null', 'null', 0, 0, 0, 0, 0, 0, 0, 0, 0, 'null', 0, 'null', 'null', 0, 'null', 'null', 1))

    # The databse connection is closed
    connection.commit()
    connection.close()