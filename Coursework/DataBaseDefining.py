import sqlite3

def DefineDatabase():
    
    # Connection to the database is established
    connection = sqlite3.connect('System.db')
    cursor = connection.cursor()

    # Each table in the database is created - only if it does not already exist

    #Accounts Table
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Accounts (
                    id TEXT PRIMARY KEY,
                    Password TEXT,
                    IsAdmin BOOLEAN)
                    """)

    #Customers table
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Customers (
                    id INTEGER PRIMARY KEY, 
                    FirstName TEXT,
                    LastName TEXT, 
                    EmailAddress TEXT,
                    PhoneNumber TEXT,
                    AccountID TEXT,
                
                    FOREIGN KEY (AccountID) REFERENCES Accounts (id) ON DELETE CASCADE)
                    """)

    #Managers table
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Managers (
                    id INTEGER PRIMARY KEY,
                    AccountID TEXT,
                    FirstName TEXT,
                    LastName TEXT,
                    EmailAddress TEXT,
                
                    FOREIGN KEY (AccountID) REFERENCES Accounts (id) ON DELETE CASCADE)
                    """)

    #Bookings Table
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Bookings (
                    id INTEGER PRIMARY KEY,
                    Client1 TEXT,
                    Client2 TEXT,
                    CustomerID INTEGER,
                    AccountID TEXT,
                    TypeOfEventID INTEGER,
                    DateOfBooking TEXT,
                    StartTime TEXT,
                    EndTime Text,
                    AdultGuestNumber INTEGER,
                    ChildGuestNumber INTEGER,
                    Under2GuestNumber INTEGER,
                    IsAccepted BOOLEAN,
                    Cost REAL,
                    RemainingDepositToBePaid REAL,
                    RemainingcostToBePaid REAL,
                    DrinksForToastingRequired BOOLEAN,
                    CeremonyRoomRequired BOOLEAN,
                    CeremonyTime TEXT,
                    WelcomeDrinksRequired BOOLEAN,
                    AdultDrink TEXT,
                    ChildDrink TEXT,
                    IsSetUpRequired BOOLEAN,
                    Notes TEXT,
                    DateBookingWasMade TEXT,
                    IsUnavailableDate BOOLEAN,
                
                    FOREIGN KEY (CustomerID) REFERENCES Customers (id) ON DELETE CASCADE,
                    FOREIGN KEY (AccountID) REFERENCES Accounts (id) ON DELETE CASCADE,
                    FOREIGN KEY (TypeOfEventID) REFERENCES TypeOfEvents (id) ON DELETE CASCADE)
                    """)

    #TypeOfEvents table
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS TypeOfEvents (
                    id INTEGER PRIMARY KEY,
                    TypeOfEvent TEXT,
                    PricePerAdult REAL,
                    PricePerChild REAL)
                    """)

    # The database connection is closed
    connection.commit()
    connection.close()