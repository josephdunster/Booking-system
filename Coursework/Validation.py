from datetime import date
import re
import hashlib
from DateConversions import DayOfWeekAlgorithm, IsLeapYear
from RetrieveDataFromDatabase import GetValueFromTable, RetrieveColumn

def PresenceCheck(Data):

    # If the data is an empty string false is returned
    if Data == "":
        return False
    
    # Otherwise, true is returned
    return True

def RangeCheckBetween(Data, Min, Max):

    # If the data is less than or equal to the maximum value AND greater than or equal to the minimum value, true is returned
    if Data <= Max and Data >= Min:
        return True
    
    # Otherwise, false is returned
    return False

def BelowMaxRangeCheck(Data, Max):

    # If the data is less than or equal to the maximum value, true is returned
    if Data <= Max:
        return True
    
    # Otherwise, false is returned
    return False

def AboveMinRangeCheck(Data, Min):

    # If the data is greater than or equal to the minimum value, true is returned
    if Data >= Min:
        return True
    
    # Otherwise, false is returned
    return False

def LengthCheckBetween(Data, Min, Max):

    # If the length of the data is greater than or equal to the minimum value AND less than or equal to the maximum value, true is returned
    if len(Data) >= Min and len(Data) <= Max:
        return True
    
    # Otherwise, false is returned
    return False

def BelowMaxLengthCheck(Data, Max):

    # If the length of the data is less than or equal to the maximum length, true is returned
    if len(Data) <= Max:
        return True
    
    # Otherwise, false is returned
    return False

def AboveMinLengthCheck(Data, Min):

    # If the length of the data is greater than or equal to the minimum length, true is returned
    if len(Data) >= Min:
        return True
    
    # Otherwise, false is returned
    return False

def UniquenessCheck(Data, Array):

    # If the data does not appear in the array (meaning it is unique), true is returned
    if Data not in Array:
        return True
    
    # Otherwise, false is returned
    return False

def IsDateFuture(Date):

    # The current date is stored
    CurrentDate = str(date.today())
    
    # The input date is split into the year, month and day
    Year = int(Date[0:4])
    Month = int(Date[5:7])
    Day = int(Date[8:10])

    # the current date is split into year, month and day
    CurrentYear = int(CurrentDate[0:4])
    CurrentMonth = int(CurrentDate[5:7])
    CurrentDay = int(CurrentDate[8:10])

    # If the input year is greater than the current year, the date is in the future and true is returned
    if Year > CurrentYear:
        return True
    
    # If the input and current years are the same but the input month is greater than the current month, the date is in the future and true is retured
    elif (Year == CurrentYear) and (Month > CurrentMonth):
        return True
    
    # If the input and current years and months are the same but the input day is greater than the current day, the date is in the future and true is returned
    elif (Year == CurrentYear) and (Month == CurrentMonth) and (Day > CurrentDay):
        return True
    
    # Otherwise, false is returned as the date is not in the future
    return False

def IsDateValid(Date):
    ''' Date must be in the format YYYY-MM-DD '''
    
    # If the length of the date is not exactly 10 characters, false is returned
    if len(Date) != 10:
        return False
    
    # The date is split into year, month and dat
    Year = int(Date[0:4])
    Month = int(Date[5:7])
    Day = int(Date[8:10])

    # The current date is stored and the current year is retrieved from this date
    CurrentDate = str(date.today())
    CurrentYear = int(CurrentDate[0:4])

    # If the input dae is not within 100 years of the current year, flase is returned
    if RangeCheckBetween(Year, CurrentYear - 100, CurrentYear + 100) == False:
        return False

    # The year is checked to see if it is a leap year
    LeapYear = IsLeapYear(Year)

    # If the month is one with 31 days and the day is between 1 and 31, true is returned
    if Month in [1, 3, 5, 7, 8, 10, 12]:
        if (Day <= 31) and (Day > 0):
            return True
        
        # If the month is one with 31 days but the day is not between 1 and 31, false is returned
        return False
    
    # If the month is one with 30 days and the day is between 1 and 30, true is returned
    elif Month in [4, 6, 9, 11]:
        if (Day <= 30) and (Day > 0):
            return True
        
        # If the month is one with 30 days but the day is not between 1 and 30, flase is returned
        return False
    
    # If the month is February (2nd month), it is a leap year and the day is between 1 and 29, true is returned
    elif Month == 2:
        if (LeapYear == True) and (Day <= 29) and (Day > 0):
            return True
        
        # If the month is February, it is not a leap year and the day is between 1 and 28, true is returned
        elif (LeapYear == False) and (Day <= 28) and (Day > 0):
            return True
        
        # If the month is February but the day is not between 1 and 29, false is returned
        return False
    
    # If the month is not between 1 and 12, false is returned
    return False

def IsTimeValid(Time):

    # The regular expression for the format NN:NN (N = Number) is stored
    Pattern = re.compile(r'^\d{2}:\d{2}$')

    # If the input time matches this pattern, true is returned
    if Pattern.match(Time):
        return True
    
    # Otherwise, false is returned
    return False

def CheckEmailFormat(Email):

    # The regular expression for a valid email address is stored
    Pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # If the input email address matches this pattern, true is returned. If not, false is returned
    return re.match(Pattern, Email) is not None

def CheckPhoneFormat(PhoneNumber):

    # The regular expression for a valid UK mobile number is stored
    Pattern = r'^(?:\+44|0)\d{9,10}$'

    # If the input phone number matches this pattern, true is returned. If not, false is returned
    return re.match(Pattern, PhoneNumber) is not None

def Hash(Data):

    # A SHA-256 hash object is created
    sha256Hash = hashlib.sha256()

    # The input data is hashed
    sha256Hash.update(Data.encode('utf-8'))
    HashedData = sha256Hash.hexdigest()

    # The hashed data is returned
    return HashedData

def ValidateNewBooking(Title1, Title2, ClientName1, ClientName2, WeddingDate, PackageOption, StartTime, EndTime, SetUpRequired, CeremonyRequired, CeremonyTime, AdultGuestNumber, ChildGuestNumber, Below2GuestNumber, WelcomeDrinksRequired, AdultWelcomeDrink, ChildWelcomeDrink, DrinksForToastingRequired, Notes):
    # Error array is initialised with no errors and errors are added if data is not valid
    ErrorsArray = []

    # The titles are validated
    try:
        if LengthCheckBetween(Title1, 1, 5):
            pass
        else:
            ErrorsArray.append('Title1')
    except:
        ErrorsArray.append('Title1')

    try:
        if LengthCheckBetween(Title2, 1, 5):
            pass
        else:
            ErrorsArray.append('Title2')
    except:
        ErrorsArray.append('Title2')

    # Client names are validated to check that they are not too many characters
    if PresenceCheck(ClientName1) and BelowMaxLengthCheck(ClientName1, 60):
        pass
    else:
        ErrorsArray.append('ClientName1')

    if PresenceCheck(ClientName2) and BelowMaxLengthCheck(ClientName2, 60):
        pass
    else:
        ErrorsArray.append('ClientName2')

    UnavailableDateTuple = RetrieveColumn('DateOfBooking', 'Bookings')

    UnavailableDatesArray = []
    for Tuple in UnavailableDateTuple:
        UnavailableDatesArray.append(Tuple[0])

    # Date of wedding is validated
    if IsDateValid(WeddingDate) and IsDateFuture(WeddingDate):
        if WeddingDate in UnavailableDatesArray:
            ErrorsArray.append('UnavailableDate')
        pass
    else:
        ErrorsArray.append('EventDate')

    # Checks that a package option has been selected
    if PackageOption:
        pass
    else:
        ErrorsArray.append('PackageOption')

    # Start time entered will always be valid as there are no start time contrictions depending on the date of the event

    # End time is validated
    # Temporarily sets 00:00 to 24:00 so it can be validated
    if EndTime == "00:00":
        EndTime = "24:00"

    # Checks that the end time is later than the start time
    if (int(EndTime[0:2]) > int(StartTime[0:2])) or ((int(EndTime[0:2]) == int(StartTime[0:2])) and (int(EndTime[3:5]) > int(StartTime[3:5]))):
        pass
    else:
        ErrorsArray.append("EndTimeTooEarly")

    # Checks that the end time is not too late for the day of the wedding
    try:
        if (DayOfWeekAlgorithm(WeddingDate) in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Sunday']) and (EndTime == "11:30" or EndTime == "24:00"):
            ErrorsArray.append("EndTimeTooLate")
    except:
        pass
        
    # Checks that the set up required field has been selected    
    if SetUpRequired == None:
        ErrorsArray.append('SetUpRequired')

    # Checks that the ceremony required field has been selected   
    if CeremonyRequired == None:
        ErrorsArray.append('CeremonyRequired')
    elif CeremonyTime == 'null':
        pass

    # Validates that the ceremony time is between the start and end time of the event
    elif int(CeremonyTime.replace(":", "")) >= int(StartTime.replace(":", "")) and int(CeremonyTime.replace(":", "")) < int(EndTime.replace(":", "")):
        pass
    else:
        ErrorsArray.append("CeremonyTime")

    # Resets the Endtime so it is in the correct format
    if EndTime == "24:00":
        EndTime = "00:00"
        
    # Validates the number of guests at the wedding
    try:
        if (int(AdultGuestNumber) + int(ChildGuestNumber) + int(Below2GuestNumber)) <= 200: # Total number must be 200 or less
            if DayOfWeekAlgorithm(WeddingDate) == 'Saturday' and AboveMinRangeCheck(int(AdultGuestNumber), 80): # Minimum of 80 adults on weddings on a Saturday
                pass
            elif AboveMinRangeCheck(int(AdultGuestNumber), 60): # Minimum of 60 adults on other days
                pass
            else:
                ErrorsArray.append("MinGuestNumber")
        else:
            ErrorsArray.append("MaxGuestNumber")
    except:
        if (IsDateValid(WeddingDate) and IsDateFuture(WeddingDate)):
            ErrorsArray.append("GuestNumberType")
        else:
            pass
        
    # Checks that the welcome drinks required field has been selected
    if WelcomeDrinksRequired == None:
        ErrorsArray.append('WelcomeDrinksRequired')

    # Checks that the adult's welcome drink field is valid
    try:
        if AdultWelcomeDrink == 'null':
            pass
        elif LengthCheckBetween(AdultWelcomeDrink, 1, 30):
            pass
        else:
            ErrorsArray.append("AdultWelcomeDrink")
    except:
        ErrorsArray.append("AdultWelcomeDrink")

    # Checks that the children's welcome drink field is valid
    try:
        if ChildWelcomeDrink == 'null':
            pass
        elif LengthCheckBetween(ChildWelcomeDrink, 1, 30):
            pass
        else:
            ErrorsArray.append("ChildWelcomeDrink")
    except:
        ErrorsArray.append("ChildWelcomeDrink")

    # Checks that the toasting drinks required field has been selected    
    if DrinksForToastingRequired == None:
        ErrorsArray.append('DrinksForToastingRequired')
        
    # Checks that the additional information field does not exceed the character limit
    if BelowMaxLengthCheck(Notes, 250):
        pass
    else:
        ErrorsArray.append("Notes")

    # The array containing any invalid data that has been identified is returned
    return ErrorsArray

def ValidateLogin(Username, Password):
    # If a login is successfull, an array is returned in the format: [IsLoginSuccessful, IsAdmin, AccountID]
    # indicating that the login was successful and providing the users access level and accountID

    # If the login is unsuccessul, an array is returned in the format: [IsLoginSuccessful, DoesUsernameExists, IsPasswordCorrect]
    # indicating that the login was unsuccessful and providing the appropriate error messages to be displayed

    # The list of usernames are retrieved from the database
    UsernamesArray = RetrieveColumn('id', 'Accounts')
        
    if any([t[0] == Username for t in UsernamesArray]):
        UsernameExists = True
        # If the username matches a username in the database, UsernameExists is set to True and the index of this account is found

        if Hash(Password) == GetValueFromTable('Accounts', 1, Username):

            # If the password is correct, the login is successfull and the user's access level is returned
            IsLoginSuccessfull = True
            IsAdmin = GetValueFromTable('Accounts', 2, Username)
            return [IsLoginSuccessfull, IsAdmin]
        
        # If the password does not match the password from the database:
        LoginSuccessfull = False
        PasswordCorrect = False
        return [LoginSuccessfull, UsernameExists, PasswordCorrect]
    
    # If the username does not exist:
    LoginSuccessfull = False
    UsernameExists = False
    PasswordCorrect = True # This is set to true so that the incorrect password message is not displayed
    return [LoginSuccessfull, UsernameExists, PasswordCorrect]