from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from DataBaseDefining import DefineDatabase
import timeit

# The database is created
DefineDatabase()

from AddingRecordsToDatabase import *
from DateConversions import *
from SearchesAndSorts import *
from SendingEmails import *
from Validation import *
from RetrieveDataFromDatabase import *

app = Flask(__name__)
app.secret_key = "Flask coursework 123"

# Landing page
@app.route("/")
def LandingPage():
    # All session variables are cleared to be re-assigned at login or sign-up
    session.clear()
    return render_template("LandingPage.html")


# Login and sign up pages
@app.route("/login", methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':

        # When the login button is pressed, the username and password inputs are retrieved
        Username = request.form.get("username")
        Password = request.form.get("password")

        IsLoginSuccessful = ValidateLogin(Username, Password)

        # If the login is successfull, the user is sent to a suitable page based on their access level that has been found
        if IsLoginSuccessful[0] == True:
            session['IsAdmin'] = IsLoginSuccessful[1]
            session['AccountID'] = Username
            if session['IsAdmin'] == True:
                # If the user is a manager, their manager id is also found
                ManagerTable = GetEntireTable('Managers')
                session['ManagerID'] = ManagerTable[TwoDimensionalLinearSearch(ManagerTable, 1, Username)][0]

                return redirect("/manager-calendar")
            
            # If the user is a customer, their customer id is also found
            CustomerTable = GetEntireTable('Customers')
            session['CustomerID'] = CustomerTable[TwoDimensionalLinearSearch(CustomerTable, 5, Username)][0]

            return redirect("/customer-bookings")
        
        # If the login is not successfull, the login page is re-rendered with necessary error
        return render_template("Login.html", UsernameExists=IsLoginSuccessful[1], PasswordCorrect=IsLoginSuccessful[2])
    return render_template("Login.html")

@app.route("/sign-up", methods=['GET', 'POST'])
def SignUp():
    if request.method == 'POST':
        # Retrieve the data that the user has input
        FirstName = request.form.get('first-name')
        Surname = request.form.get('surname')
        PhoneNumber = request.form.get('phone-number')
        EmailAddress = request.form.get('email-address')
        Username = request.form.get('username')
        Password = request.form.get('password')
        ConfirmPassword = request.form.get('confirm-password')

        # Data is validated:
        # First name is validated
        if PresenceCheck(FirstName) and LengthCheckBetween(FirstName, 1, 30):
            FirstNameValid = True
        else:
            FirstNameValid = False

        # Surname is validated
        if PresenceCheck(Surname) and LengthCheckBetween(Surname, 1, 30):
            SurnameValid = True
        else:
            SurnameValid = False

        # Phone number is validated
        CurrentPhoneNumbersTuple = RetrieveColumn('PhoneNumber', 'Customers')

        CurrentPhoneNumbersArray= []
        for Tuple in CurrentPhoneNumbersTuple:
            CurrentPhoneNumbersArray.append(Tuple[0])

        if CheckPhoneFormat(PhoneNumber):
            PhoneNumberValid = True
        else:
            PhoneNumberValid = False

        PhoneUnique = UniquenessCheck(PhoneNumber, CurrentPhoneNumbersArray)

        # Email Address is validated
        # Current customer email addresses are retrieved
        CurrentCustomersEmailAddressesTuple = RetrieveColumn('EmailAddress', 'Customers')      

        CurrentCustomersEmailAddressesArray= []
        for Tuple in CurrentCustomersEmailAddressesTuple:
            CurrentCustomersEmailAddressesArray.append(Tuple[0])

        # Current manager email addresses are retrieved
        CurrentManagersEmailAddressesTuple = RetrieveColumn('EmailAddress', 'Managers')      

        CurrentManagersEmailAddressesArray = []
        for Tuple in CurrentManagersEmailAddressesTuple:
            CurrentManagersEmailAddressesArray.append(Tuple[0])

        # Customer and manager email address are concatenated
        CurrentEmailAddressesArray = CurrentCustomersEmailAddressesArray + CurrentManagersEmailAddressesArray

        if CheckEmailFormat(EmailAddress):
            EmailAddressValid = True
        else:
            EmailAddressValid = False

        EmailUnique = UniquenessCheck(EmailAddress, CurrentEmailAddressesArray)

        # Checks if user has confirmed that they are at least 18 years old
        
        if 'checkbox' in request.form:
            CheckboxError = False
        else:
            CheckboxError = True

        # Username (AccountID) is validated
        CurrentUsernamesTuple = RetrieveColumn('id', 'Accounts')

        CurrentUsernamesArray= []
        for Tuple in CurrentUsernamesTuple:
            CurrentUsernamesArray.append(Tuple[0])

        if PresenceCheck(Username) and LengthCheckBetween(Username, 1, 30):
            UsernameValid = True
        else:
            UsernameValid = False

        UsernameUnique = UniquenessCheck(Username, CurrentUsernamesArray)

        # Password is validated
        if PresenceCheck(Password) and AboveMinLengthCheck(Password, 8):
            PasswordValid = True
        else:
            PasswordValid = False

        if (Password == ConfirmPassword):
            PasswordMatch = True
        else:
            PasswordMatch = False

        # Error messages are displayed if necessary
        if (FirstNameValid == False) or (SurnameValid == False) or (EmailAddressValid == False) or (PhoneNumberValid == False) or (UsernameValid == False) or (PasswordValid == False) or (PasswordMatch == False):
            return render_template("SignUp.html", FirstNameValid=FirstNameValid, SurnameValid=SurnameValid, PhoneNumberValid=PhoneNumberValid, PhoneUnique=PhoneUnique, EmailAddressValid=EmailAddressValid, EmailUnique=EmailUnique, CheckboxError=CheckboxError, UsernameValid=UsernameValid, UsernameUnique=UsernameUnique, PasswordValid=PasswordValid, PasswordMatch=PasswordMatch)

        # Data is added to the database if all data is valid:
        # Account is are created
        AddNewAccount(Username, Hash(Password))

        # Customer is created
        AddNewCustomer(FirstName, Surname, PhoneNumber, EmailAddress, Username)

        CustomerTable = GetEntireTable('Customers')

        session['CustomerID'] = CustomerTable[TwoDimensionalLinearSearch(CustomerTable, 5, Username)][0]
        session['AccountID'] = Username
        session['IsAdmin'] = False
        return redirect("/customer-bookings")
    return render_template("SignUp.html")


# Password reset pages
@app.route("/reset-password", methods=['GET', 'POST'])
def EnterEmail():

    if request.method == 'POST':

        # The email that has been input is retrieved and is passed to the next stage of the password reset process
        email = request.form["Email"]
        return redirect(url_for('EnterCode', email=email))
    return render_template("ResetPasswordEnterEmail.html")

@app.route("/enter-code/<email>", methods=['GET', 'POST'])
def EnterCode(email):

    if request.method == 'POST':
        return redirect(url_for('NewPassword', email=email))
    return render_template("ResetPasswordEnterCode.html", email=email)

@app.route("/enter-new/<email>", methods=['GET', 'POST'])
def NewPassword(email):
    if request.method == 'POST':
        return render_template("ResetPasswordConfirmation.html", email=email)
    return render_template("ResetPasswordEnterNewPassword.html")


# Making a booking pages
@app.route("/new-booking/select-customer", methods=['GET', 'POST'])
def NewBookingSelectCustomer():

    # An array of customer names and ids are retrieved
    CustomerFirstNames = RetrieveColumn('FirstName', 'Customers')
    CustomerLastNames = RetrieveColumn('LastName', 'Customers')
    CustomerIDs = RetrieveColumn('id', 'Customers')

    # The array or tuples are converted to arrays
    CustomerFirstNames = [list(row) for row in CustomerFirstNames]
    CustomerLastNames = [list(row) for row in CustomerLastNames]
    CustomerIDs = [list(row) for row in CustomerIDs]

    # The arrays are combined to be in the correct format to be displayed on screen
    CombinedArray = list(zip(CustomerFirstNames, CustomerLastNames, CustomerIDs))
    CustomerInformation = [list(customer) for customer in CombinedArray]

    if request.method == 'POST':

        # The customer id of the customer selected is stored
        session['CustomerID'] = request.form.get("customer")

        return redirect("/new-booking")
    return render_template("NewBookingSelectCustomer.html", CustomerInformation=CustomerInformation)

@app.route("/new-booking", methods=['GET', 'POST'])
def NewBooking():

    # This user must only be able to access this page if they have logged in as the booking process relies on their details
    if (('AccountID' not in session) and ('CustomerID' not in session)) or (('AccountID' not in session) and ('ManagerID' not in session)):
        return redirect('/')

    # The list of events is retrieved from the table to be displayed on the screen
    EventArray = RetrieveColumn('TypeOfEvent', 'TypeOfEvents')

    # The first three elements are removed as these are 'Wedding1', 'Wedding2' and 'Wedding3'
    # 'Wedding' will be rendered automatically in the htmk
    EventArray = EventArray[3:]
    EventArray = [item[0] for item in EventArray]

    if request.method == 'POST':

        # The button that triggered the post request is stored
        session['TypeOfEvent'] = next(iter(request.form))

        # If this was the 'Wedding' button, the user is redirected to the wedding booking page
        if session['TypeOfEvent'] == 'Wedding':
            return redirect('/new-wedding')
        
        # If the 'Other' button triggered the post request, the input box is displayed on the screen
        elif session['TypeOfEvent'] == 'Other':
            return render_template("NewBookingSelectEvent.html", EventArray=EventArray, Other=True)
        
        # If the button was one of the elements in the array, the user is redirected to the events booking page
        elif session['TypeOfEvent'] in EventArray:
            return redirect('/new-event')
        
        # If the user has not yet been redirected, they must have entered their own event.
        # This event is stored as the TypeOfEvent and is validated
        session['TypeOfEvent'] = request.form.get("OtherEnter")

        if LengthCheckBetween(session['TypeOfEvent'], 1, 30):
            # If the input is valid, the new type of event is added to database and the user is directed to the events booking page
            AddNewTypeOfEvent(session['TypeOfEvent'], 79, 39.5)
            return redirect('/new-event')
        
        # If the input is not valid, an error message is displayed
        return render_template("NewBookingSelectEvent.html", EventArray=EventArray, Other=True, InvalidOther=True)
            
    return render_template("NewBookingSelectEvent.html", EventArray=EventArray)

@app.route("/new-wedding", methods=['GET', 'POST'])
def NewWedding():
    # This user must only be able to access this page if they have logged in as the booking process relies on their details
    if (('AccountID' not in session) and ('CustomerID' not in session)) or (('AccountID' not in session) and ('ManagerID' not in session)):
        return redirect('/')
    
    # The available adult and child welcome drinks are retrieved to be displayed as options on the screen
    AdultDrinks = RetrieveAdultDrinks()
    ChildDrinks = RetrieveChildrenDrinks()
    
    return render_template("NewWedding.html", AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks)

@app.route('/process-wedding-booking', methods=['POST'])
def ProcessWeddingBooking():

    # Retrieve the data that the user has input
    ClientName1 = request.form.get('clientName1')
    ClientName2 = request.form.get('clientName2')
    Title1 = request.form.get('title1')
    Title2 = request.form.get('title2')
    WeddingDate = request.form.get('weddingDate')
    PackageOption = request.form.get('packageOption')
    StartTime = request.form.get('startTime')
    EndTime = request.form.get('endTime')

    SetUpRequired = request.form.get('setUpRequired')
    if SetUpRequired == 'true':
        SetUpRequired = True

    CeremonyRequired = request.form.get('ceremonyRequired')
    if CeremonyRequired == 'true':
        CeremonyRequired = True
    
    # The boolean values from the front end are stored as strings in the back end so must be adjusted
        
    CeremonyTime = request.form.get('ceremonyTime')
    AdultGuestNumber = request.form.get('adultGuestNumber')
    ChildGuestNumber = request.form.get('childGuestNumber')
    Below2GuestNumber = request.form.get('below2GuestNumber')
    WelcomeDrinksRequired = request.form.get('welcomeDrinksRequired')
    AdultWelcomeDrink = request.form.get('adultWelcomeDrink')
    ChildWelcomeDrink = request.form.get('childWelcomeDrink')
    DrinksForToastingRequired = request.form.get('drinksForToastingRequired')
    Notes = request.form.get('notes')

    # Data inputs are validated:
    ErrorsArray = ValidateNewBooking(Title1, Title2, ClientName1, ClientName2, WeddingDate, PackageOption, StartTime, EndTime, SetUpRequired, CeremonyRequired, CeremonyTime, AdultGuestNumber, ChildGuestNumber, Below2GuestNumber, WelcomeDrinksRequired, AdultWelcomeDrink, ChildWelcomeDrink, DrinksForToastingRequired, Notes)

    # If no data is invalid, the confirmation page will be displayed
    if len(ErrorsArray) == 0:

        # Titles and names can be concatenated now that they have been validated
        ClientName1 = (Title1 + " " + ClientName1)
        ClientName2 = (Title2 + " " + ClientName2)

        # The type of event id is found by concatenating the type of event with the package option
        EventIndex = FindRecordFromTable('TypeOfEvents', session['TypeOfEvent'] + PackageOption, 1)
        TypeOfEventID = GetValueFromTable('TypeOfEvents', 0, EventIndex + 1)

        # The new Booking is added to the database
        AddNewBooking(session['IsAdmin'], ClientName1, ClientName2, session['CustomerID'], session['AccountID'], TypeOfEventID, WeddingDate, StartTime, EndTime, AdultGuestNumber, ChildGuestNumber, Below2GuestNumber, DrinksForToastingRequired, CeremonyRequired, CeremonyTime, WelcomeDrinksRequired, AdultWelcomeDrink, ChildWelcomeDrink, SetUpRequired, Notes)

        # The Booking ID is retrieved as it is needed for sending emails
        BookingIDArray = RetrieveColumn('id', 'Bookings')
        BookingID = BookingIDArray[-1]
        BookingID = BookingID[0]

        # If the user is a customer, the request email is sent
        if session['IsAdmin'] == False:
            BookingRequestConfirmationEmail(BookingID)

        # However, if the user is a manager, the confirmation email is sent
        else:
            BookingConfirmationEmail(BookingID)

        # Some event information is returned to be displayed on the confirmation screen
        Result = {'status': 'success',
                  'isAdmin': session['IsAdmin'],
                  'typeOfEvent': session['TypeOfEvent'],
                  'date': DateFormatToWords(WeddingDate),
                  'time': (StartTime + " - " + EndTime)}
        
    # If there is some invalid data, it will be passed to the front end so correct error messages can be displayed
    else:
        Result = {'status': 'failure', 
                  'errors': ErrorsArray}

    return jsonify(Result)

@app.route("/new-event")
def NewEvent():

    # This user must only be able to access this page if they have logged in as the booking process relies on their details
    if (('AccountID' not in session) and ('CustomerID' not in session)) or (('AccountID' not in session) and ('ManagerID' not in session)):
        return redirect('/')
    
    # The adult and child welcome drinks are retrieved to be displayed as options on the screen
    AdultDrinks = RetrieveAdultDrinks()
    ChildDrinks = RetrieveChildrenDrinks()
    
    return render_template("NewEvent.html", AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks)

@app.route("/calculate-event-cost", methods=['POST'])
def CalculateEventCost():

    # The users inputs are retrieved from the front end
    SetUpRequired = request.form.get('setUpRequired')
    if SetUpRequired == 'true':
        SetUpRequired = True

    CeremonyRequired = request.form.get('ceremonyRequired')
    if CeremonyRequired == 'true':
        CeremonyRequired = True
    
    # The boolean values from the front end are stored as strings in the back end so must be adjusted

    AdultGuestNumber = request.form.get('adultGuestNumber')
    ChildGuestNumber = request.form.get('childGuestNumber')
    Below2GuestNumber = request.form.get('below2GuestNumber')
    EventDate = request.form.get('eventDate')
    PackageOption = request.form.get('packageOption')

    # Validates the number of guests at the event
    # If invalid, appropriate error messages are displayed
    try:
        if IsDateFuture(EventDate) and IsDateValid(EventDate):

            # Total number must be 200 or less
            if (int(AdultGuestNumber) + int(ChildGuestNumber) + int(Below2GuestNumber)) <= 200:

                # Minimum of 80 adults on weddings on a Saturday
                if DayOfWeekAlgorithm(EventDate) == 'Saturday' and AboveMinRangeCheck(int(AdultGuestNumber), 80):
                    pass

                # Minimum of 60 adults on other days
                elif AboveMinRangeCheck(int(AdultGuestNumber), 60):
                    pass

                # If the guest numbers do not meet these requirements, an error message will be displayed
                else:
                    Result = {'status': 'failure',
                              'error': 'MinGuestNumber'}
                    return jsonify(Result)
                
            # If the total guest number is more than 200, an error message will be displayed
            else:
                Result = {'status': 'failure',
                          'error': 'MaxGuestNumber'}
                return jsonify(Result)
            
        # If the date is either invalid or not in the future, this error message is returned
        else:
            Result = {'status': 'failure',
                    'error': 'DateError'}
            return jsonify(Result)
        
    # If an error occurred, it means that the guest input was not a number so an error message must be displayed
    except:
        Result = {'status': 'failure',
                  'error': 'GuestNumberType'}
        return jsonify(Result)

    # The index of the selected type of event is found from the database
    EventIndex = FindRecordFromTable('TypeOfEvents', session['TypeOfEvent'] + PackageOption, 1)

    # If the Type of event does not currently exist, the new type of event is added to the data base and then it's ID is found
    if EventIndex == False:
        TypeOfEventID = False
    else:
        TypeOfEventID = GetValueFromTable('TypeOfEvents', 0, EventIndex + 1)

    # The cost of the event is calculated and rounded to 2 decimal places
    Cost = CalculateCost(SetUpRequired, CeremonyRequired, AdultGuestNumber, ChildGuestNumber, TypeOfEventID)
    Cost = f"{Cost:.2f}"

    # The cost is returned to the front end to be displayed
    Result = {'status': 'success',
              'cost': Cost}

    return jsonify(Result)

@app.route('/process-event-booking', methods=['GET', 'POST'])
def ProcessEventBooking():

    # Retrieve the data that the user has input
    ClientName1 = request.form.get('clientName')
    Title1 = request.form.get('title')
    EventDate = request.form.get('eventDate')
    StartTime = request.form.get('startTime')
    EndTime = request.form.get('endTime')
    SetUpRequired = request.form.get('setUpRequired')
    CeremonyRequired = request.form.get('ceremonyRequired')
    CeremonyTime = request.form.get('ceremonyTime')
    AdultGuestNumber = request.form.get('adultGuestNumber')
    ChildGuestNumber = request.form.get('childGuestNumber')
    Below2GuestNumber = request.form.get('below2GuestNumber')
    WelcomeDrinksRequired = request.form.get('welcomeDrinksRequired')
    AdultWelcomeDrink = request.form.get('adultWelcomeDrink')
    ChildWelcomeDrink = request.form.get('childWelcomeDrink')
    Notes = request.form.get('notes')

    # Initialises the wedding specific fields with valid data so the same subroutine can be used to validate inputs
    Title2 = "Mr"
    ClientName2 = "Example"
    PackageOption = 1
    DrinksForToastingRequired = False

    ErrorsArray = ValidateNewBooking(Title1, Title2, ClientName1, ClientName2, EventDate, PackageOption, StartTime, EndTime, SetUpRequired, CeremonyRequired, CeremonyTime, AdultGuestNumber, ChildGuestNumber, Below2GuestNumber, WelcomeDrinksRequired, AdultWelcomeDrink, ChildWelcomeDrink, DrinksForToastingRequired, Notes)

    # If no data is invalid, the confirmation page will be displayed
    if len(ErrorsArray) == 0:

        # Titles and names can be concatenated now that they have been validated
        ClientName1 = (Title1 + " " + ClientName1)
        # Client name 2 is changed back to null
        ClientName2 = ("null")

        # The index of the selected type of event is found from the database
        EventIndex = FindRecordFromTable('TypeOfEvents', session['TypeOfEvent'], 1)

        # If the Type of event does not currently exist, the new type of event is added to the data base and then it's ID is found
        if EventIndex == False:
            AddNewTypeOfEvent(session['TypeOfEvent'])
            EventIndex = FindRecordFromTable('TypeOfEvents', session['TypeOfEvent'], 1)
            TypeOfEventID = GetValueFromTable('TypeOfEvents', 0, EventIndex + 1)
        
        TypeOfEventID = GetValueFromTable('TypeOfEvents', 0, EventIndex + 1)

        # The new Booking is added to the database
        AddNewBooking(session['IsAdmin'], ClientName1, ClientName2, session['CustomerID'], session['AccountID'], TypeOfEventID, EventDate, StartTime, EndTime, AdultGuestNumber, ChildGuestNumber, Below2GuestNumber, DrinksForToastingRequired, CeremonyRequired, CeremonyTime, WelcomeDrinksRequired, AdultWelcomeDrink, ChildWelcomeDrink, SetUpRequired, Notes)
        
        # The new bookings ID is retrieved so that it can be used to send emails
        BookingIDArray = RetrieveColumn('id', 'Bookings')
        BookingID = BookingIDArray[-1]
        BookingID = BookingID[0]

        # If the user is a customer, the booking request email is sent
        if session['IsAdmin'] == False:
            BookingRequestConfirmationEmail(BookingID)

        # Otherwise, the booking confirmation email is sent
        else:
            BookingConfirmationEmail(BookingID)

        # Some of the event details are sent back to the front end to be displayed on the confirmation page
        Result = {'status': 'success',
                  'isAdmin': session['IsAdmin'],
                  'typeOfEvent': session['TypeOfEvent'],
                  'date': DateFormatToWords(EventDate),
                  'time': (StartTime + " - " + EndTime)}
        
    # If there is some invalid data, it will be passed to the front end so correct error messages can be displayed
    else:
        Result = {'status': 'failure', 
                  'errors': ErrorsArray}

    return jsonify(Result)


# Manager pages
@app.route("/manager-calendar", methods=['GET', 'POST'])
def ManagerCalendar():

    # The current year is found so that the calendar will initially always show the correct year
    if 'View' not in session:
        session['Timeframe'] = str(date.today())[0:4]
        session['View'] = 'Year'
        LeapYear = IsLeapYear(str(session['Timeframe']) + "-01-01")

        # The bookings that need to be displayed on this page of the calendar are retrieved based on the timeframe (the year that is currently being displayed)
        BookingsToDisplay = GetYearBookingToDisplay(session['Timeframe'])

    if request.method == 'POST':
            
        # If the post request was sent to change the view of the calendar:
        if 'view-select' in request.form:

            # The view that has been selected is retrieved
            session['View'] = request.form.get('view-select')

            # If the view selected was month:
            if session['View'] == 'Month':

                # The current month and year are retrieved from todays date
                Month = GetMonth(str(date.today()))
                Year = str(date.today())[0:4]

                # The timeframe (month and year that is displayed on the screen) is created
                session['Timeframe'] = Month + " " + Year

                # The days in this month is stored
                DaysInCurrentMonth = DaysInMonth(str(date.today()))

                # The index of the first day of the month is stored. (Monday = 0, Tuesday = 1 ...)
                FirstDayIndex = GetFirstDayIndex(DayOfWeekAlgorithm(DateWordsToFormat("1 " + session['Timeframe'])))

                # The bookings that must be displayed on this page are retrieved based on the timeframe
                BookingsToDisplay = GetMonthBookingsToDisplay(session['Timeframe'])

                return render_template("ManagerCalendar.html", View=session['View'], Timeframe=session['Timeframe'], DaysInMonth=DaysInCurrentMonth, FirstDayIndex=(FirstDayIndex), BookingsToDisplay=json.dumps(BookingsToDisplay))
            
            # If the view selected is week:
            elif session['View'] == 'Week':

                # Todays date is retrieved and the day of the week and day of the week index are calculated
                Today = str(date.today())
                DayOfTheWeekToday = DayOfWeekAlgorithm(Today)
                DayOfTheWeekIndex = DayIndex(DayOfTheWeekToday)

                # The date of the first day of the week is calculated
                FirstDayOfWeek = SubtractDays(Today, DayOfTheWeekIndex)

                # The date of each day in this week is calculated
                WeekDates = [AddDays(FirstDayOfWeek, i) for i in range(7)]

                # The array of dates in word form is initialised
                ConvertedWeekDates = []

                # Each date in the WeekDates array is converted to the word format
                for Date in WeekDates:
                    DateInWords = DateFormatToWords(Date)
                    ConvertedWeekDates.append(DateInWords)

                # The timeframe (the week being displayed on the screen) is set as the first day of this week to the last day
                session['Timeframe'] = ConvertedWeekDates[0] + " - " + ConvertedWeekDates[6]

                # The bookings that need to be displayed on this page of the calendar are retrieved
                # The first day of the week is passed as a parameter and in the function, each subsequent day of the week is calculated
                BookingsToDisplay = GetWeekBookingsToDisplay(FirstDayOfWeek)

                return render_template("ManagerCalendar.html", View=session['View'], Timeframe=session['Timeframe'], WeekToShow=ConvertedWeekDates, BookingsToDisplay=json.dumps(BookingsToDisplay))
            
            # If the view selected was year:
            else:

                # The timeframe (Year that is being displayed) is retrieved from todays date and it is checked to see if this is a leap year
                session['Timeframe'] = str(date.today())[0:4]
                LeapYear = IsLeapYear(str(date.today()))

                # The bookings that must be displayed on this page are retrieved based on the timeframe
                BookingsToDisplay = GetYearBookingToDisplay(session['Timeframe'])

                return render_template("ManagerCalendar.html", View=session['View'], Timeframe=session['Timeframe'], IsLeapYear=LeapYear, BookingsToDisplay=json.dumps(BookingsToDisplay))
            
        # If the user wants to move to the next week, month or year:
        elif 'add' in request.form:

            # If the current view is month:
            if session['View'] == 'Month':

                # The timeframe is moved to the next month
                session['Timeframe'] = AddMonth(session['Timeframe'])

                # The days in the new month is stored and the index of the first day
                DaysInCurrentMonth = DaysInMonth(DateWordsToFormat("1 " + session['Timeframe']))
                FirstDayIndex = GetFirstDayIndex(DayOfWeekAlgorithm(DateWordsToFormat("1 " + session['Timeframe'])))

                # The bookings that must be displayed on this page are retrieved based on the new timeframe
                BookingsToDisplay = GetMonthBookingsToDisplay(session['Timeframe'])

                return render_template("ManagerCalendar.html", View=session['View'], Timeframe=session['Timeframe'], DaysInMonth=DaysInCurrentMonth, FirstDayIndex=(FirstDayIndex), BookingsToDisplay=json.dumps(BookingsToDisplay))
        
            # If the current view is week:
            elif session['View'] == 'Week':

                # The timeframe is split into an array containing the date of the first and last day of the week
                FirstAndLastDates = session['Timeframe'].split('-')

                # The first day of the week is stored and striped of any white space around it
                FirstDayOfWeek = FirstAndLastDates[0]
                FirstDayOfWeek = FirstDayOfWeek.strip()

                # The first day of the week is converted to the form YYYY-MM-DD and the first day of the new week is calculated by adding 7 days
                FirstDayOfWeek = DateWordsToFormat(FirstDayOfWeek)
                FirstDayOfNewWeek = AddDays(FirstDayOfWeek, 7)

                # The array of dates of all days in the new week is initialised
                NewWeek = []

                # For every day in the new week, the date in words is added to the array
                for i in range(7):
                    NewWeek.append(DateFormatToWords(AddDays(FirstDayOfNewWeek, i)))

                # The new timeframe is created by concatenating the first and last day of the new week
                session['Timeframe'] = NewWeek[0] + " - " + NewWeek[6]

                # The bookings that need to be displayed on this page of the calendar are retrieved
                # The first day of the new week is passed as a parameter and in the function, each subsequent day of the new week is calculated
                BookingsToDisplay = GetWeekBookingsToDisplay(FirstDayOfNewWeek)

                return render_template("ManagerCalendar.html", View=session['View'], Timeframe=session['Timeframe'], WeekToShow=NewWeek, BookingsToDisplay=json.dumps(BookingsToDisplay))
            
            # If the current view is year:
            else:
                
                # The new timeframe is calculated by adding 1 to the year and it is checked if this year is a leap year
                session['Timeframe'] = int(session['Timeframe']) + 1
                LeapYear = IsLeapYear(str(session['Timeframe']) + "-01-01")

                # The bookings that must be displayed on this page are retrieved based on the new timeframe
                BookingsToDisplay = GetYearBookingToDisplay(session['Timeframe'])

                return render_template("ManagerCalendar.html", View=session['View'], Timeframe=session['Timeframe'], IsLeapYear=LeapYear, BookingsToDisplay=json.dumps(BookingsToDisplay))

        # If the user wants to move to the previous week, month or year
        elif 'subtract' in request.form:

            # If the current view is month
            if session['View'] == 'Month':

                # The new timeframe is calculated by subtracting one month from the timeframe
                session['Timeframe'] = SubtractMonth(session['Timeframe'])

                # The days in the new month is stored and the index of the first day
                DaysInCurrentMonth = DaysInMonth(DateWordsToFormat("1 " + session['Timeframe']))
                FirstDayIndex = GetFirstDayIndex(DayOfWeekAlgorithm(DateWordsToFormat("1 " + session['Timeframe'])))

                # The bookings that must be displayed on this page are retrieved based on the new timeframe
                BookingsToDisplay = GetMonthBookingsToDisplay(session['Timeframe'])

                return render_template("ManagerCalendar.html", View=session['View'], Timeframe=session['Timeframe'], DaysInMonth=DaysInCurrentMonth, FirstDayIndex=(FirstDayIndex), BookingsToDisplay=json.dumps(BookingsToDisplay))
        
            # If the current view is week
            elif session['View'] == 'Week':

                # The timeframe is split into an array containing the date of the first and last day of the week
                FirstAndLastDates = session['Timeframe'].split('-')

                # The first day of the week is stored and striped of any white space around it
                FirstDayOfWeek = FirstAndLastDates[0]
                FirstDayOfWeek = FirstDayOfWeek.strip()

                # The first day of the week is converted to the form YYYY-MM-DD and the first day of the new week is calculated by subtracting 7 days
                FirstDayOfWeek = DateWordsToFormat(FirstDayOfWeek)
                FirstDayOfNewWeek = SubtractDays(FirstDayOfWeek, 7)

                # The array of dates of all days in the new week is initialised
                NewWeek = []

                # For every day in the new week, the date in words is added to the array
                for i in range(7):
                    NewWeek.append(DateFormatToWords(AddDays(FirstDayOfNewWeek, i)))

                # The new timeframe is created by concatenating the first and last day of the new week
                session['Timeframe'] = NewWeek[0] + " - " + NewWeek[6]

                # The bookings that need to be displayed on this page of the calendar are retrieved
                # The first day of the new week is passed as a parameter and in the function, each subsequent day of the new week is calculated
                BookingsToDisplay = GetWeekBookingsToDisplay(FirstDayOfNewWeek)

                return render_template("ManagerCalendar.html", View=session['View'], Timeframe=session['Timeframe'], WeekToShow=NewWeek, BookingsToDisplay=json.dumps(BookingsToDisplay))
            
            # If the current view is year
            else:
                
                # The new timeframe is calculated by subtracting 1 from the year and it is checked if this year is a leap year
                session['Timeframe'] = int(session['Timeframe']) - 1
                LeapYear = IsLeapYear(str(session['Timeframe']) + "-01-01")

                # The bookings that must be displayed on this page are retrieved based on the new timeframe
                BookingsToDisplay = GetYearBookingToDisplay(session['Timeframe'])

                return render_template("ManagerCalendar.html", View=session['View'], Timeframe=session['Timeframe'], IsLeapYear=LeapYear, BookingsToDisplay=json.dumps(BookingsToDisplay))

    return render_template("ManagerCalendar.html", View=session['View'], Timeframe=session['Timeframe'], IsLeapYear=IsLeapYear(str(session['Timeframe']) + "-01-01"), BookingsToDisplay=json.dumps(BookingsToDisplay))

@app.route("/manager-bookings", methods=['GET', 'POST'])
def ManagerBookings():

    # The session variables from the calendar are removed if exist as they are not needed in this part of the system
    try:
        session.pop('View')
    except:
        pass

    # The user must be an admin to view this page
    if session['IsAdmin'] == True:

        # All bookings are retrieved from the database as some will need to be displayed
        BookingsTable = GetEntireTable('Bookings')

        # The array of bookings that need to be displayed is initialised
        BookingsToDisplay = []
        
        # Every row in the table is checked to see if it representing an unavailable date
        for i in range(len(BookingsTable)):
            if BookingsTable[i][25] == 0:

                # If it is a genuine booking, the booking is added to the array of bookings that need to be displayed
                Booking = ReturnUsefulDataToDisplay(BookingsTable[i]) # This returns an array of the event information in the correct format to be displayed
                BookingsToDisplay.append(Booking)

        if request.method == 'POST':

            # The tyep of sort is retrieved from the front end
            SortType = request.form.get('sort-select')

            # When bookings are sorted by closest upcoming events:
            if SortType == 'closest':

                # Each booking in the array of bookings being displayed has the ' - ' are removed from the booking date
                for Booking in BookingsToDisplay:
                    DateArray = Booking[25].split('-')
                    Booking[25] = DateArray[0] + DateArray[1] + DateArray[2]

                # This new format allows the dates to be treated as integers and sorted from low to high
                SortedArray = QuickSortAscending(BookingsToDisplay, 0, len(BookingsToDisplay) -1, 25)

                # When the bookings have been sorted, the ' - ' are re-added
                for Booking in SortedArray:
                    Booking[25] = Booking[25][:4] + "-" + Booking[25][4:6] + "-" + Booking[25][6:]

            # When the bookings are sorted by furthest upcoming event
            elif SortType == 'furthest':

                # Each booking in the array of bookings being displayed has the ' - ' are removed from the booking date
                for Booking in BookingsToDisplay:
                    DateArray = Booking[25].split('-')
                    Booking[25] = DateArray[0] + DateArray[1] + DateArray[2]

                # This new format allows the dates to be treated as integers and sorted from low to high
                SortedArray = QuickSortDescending(BookingsToDisplay, 0, len(BookingsToDisplay) -1, 25)

                # When the bookings have been sorted, the ' - ' are re-added
                for Booking in SortedArray:
                    Booking[25] = Booking[25][:4] + "-" + Booking[25][4:6] + "-" + Booking[25][6:]

            # The bookings array is sorted from low to high by the number of adult guests
            elif SortType == 'low':
                SortedArray = QuickSortAscending(BookingsToDisplay, 0, len(BookingsToDisplay) -1, 9)

            # The bookings array is sorted from high to low by the number of adult guests
            elif SortType == 'high':
                SortedArray = QuickSortDescending(BookingsToDisplay, 0, len(BookingsToDisplay) -1, 9)

            # When the bookings are sorted by most recently booked event
            elif SortType == 'recent':

                # Each booking in the array of bookings being displayed has the ' - ' are removed from the date the booking was made
                for Booking in BookingsToDisplay:
                    DateArray = Booking[27].split('-')
                    Booking[27] = DateArray[0] + DateArray[1] + DateArray[2]

                # This new format allows the dates to be treated as integers and sorted from high to low
                SortedArray = QuickSortDescending(BookingsToDisplay, 0, len(BookingsToDisplay) -1, 27)

                # When the bookings have been sorted, the ' - ' are re-added
                for Booking in SortedArray:
                    Booking[27] = Booking[27][:4] + "-" + Booking[27][4:6] + "-" + Booking[27][6:]

            # When the bookings are sorted by least recently booked event
            else:

                # Each booking in the array of bookings being displayed has the ' - ' are removed from the date the booking was made
                for Booking in BookingsToDisplay:
                    DateArray = Booking[27].split('-')
                    Booking[27] = DateArray[0] + DateArray[1] + DateArray[2]

                # This new format allows the dates to be treated as integers and sorted from low to high
                SortedArray = QuickSortAscending(BookingsToDisplay, 0, len(BookingsToDisplay) -1, 27)

                # When the bookings have been sorted, the ' - ' are re-added
                for Booking in SortedArray:
                    Booking[27] = Booking[27][:4] + "-" + Booking[27][4:6] + "-" + Booking[27][6:]

            return render_template("ManagerBookings.html", BookingsToDisplay=SortedArray)

        return render_template("ManagerBookings.html", BookingsToDisplay=BookingsToDisplay)
    return redirect("/")

@app.route("/process-accept-booking-manager", methods=['GET', 'POST'])
def ProcessAcceptBooking():

    # Retrieve the booking id of the booking that has been accepted
    BookingID = request.form.get('bookingID')

    # Changes the status of the booking to accepted
    ReplaceValue('Bookings', 'IsAccepted', BookingID, 1)

    # An email is sent to the customer whose booking has been accepted
    BookingAcceptedEmail(BookingID)

    return 'Complete'

@app.route("/process-cancel-booking-manager", methods=['POST'])
def ProcessCancelBooking():

    # Retrieve the booking id for the booking that has been cancelled and the reason for its cancellation
    BookingID = request.form.get('bookingID')
    CancellationReason = request.form.get('cancellationReason')

    # An email is sent to the customer whose booking has been cancelled
    CancelledByManagerEmail(BookingID, CancellationReason)

    StartTimer = timeit.default_timer()

    # The booking is removed from the database
    RemoveRecord('Bookings', BookingID)

    EndTimer = timeit.default_timer()
    print("Time taken: ", EndTimer - StartTimer)

    return 'Complete'

@app.route("/process-reject-booking-manager", methods=['POST'])
def ProcessRejectBooking():

    # Retrieve the booking id for the booking that has been rejected and the reason for its rejection
    BookingID = request.form.get('bookingID')
    RejectionReason = request.form.get('rejectionReason')

    # An email is sent to the customer whose booking has been rejected
    BookingRejectedEmail(BookingID, RejectionReason)

    # The booking is removed from the database
    RemoveRecord('Bookings', BookingID)

    return 'Complete'

@app.route("/process-edit-booking", methods=['POST'])
def ProcessEditBooking():

    # Inputs are retrieved from the front end
    BookingID = request.form.get('bookingID')
    Customer1 = request.form.get('customer1')
    Customer2 = request.form.get('customer2')
    TypeOfEvent = request.form.get('event')
    EventDate = request.form.get('eventDate')
    PackageOption = request.form.get('packageOption')
    StartTime = request.form.get('startTime')
    EndTime = request.form.get('endTime')
    AdultGuestNumber = request.form.get('adultNumber')
    ChildGuestNumber = request.form.get('childNumber')
    Under2GuestNumber = request.form.get('under2Number')
    SetUpRequired = request.form.get('setUpRequired')
    CeremonyRequired = request.form.get('ceremonyRequired')
    CeremonyTime = request.form.get('ceremonyTime')
    ToastRequired = request.form.get('toastRequired')
    WelcomeRequired = request.form.get('welcomeRequired')
    AdultDrink = request.form.get('adultDrink')
    ChildDrink = request.form.get('childDrink')
    Notes = request.form.get('notes')

    if PackageOption != 'null':
        # If the event is a wedding, the package option is concatenated to it
        TypeOfEvent = TypeOfEvent + PackageOption

    # The type of event is retrieved from the database
    TypeOfEventsTable = GetEntireTable('TypeOfEvents')
    TypeOfEventsColumn = RetrieveColumn('TypeOfEvent', 'TypeOfEvents')
    TypeOfEventsColumn = [Tuple[0] for Tuple in TypeOfEventsColumn]

    TypeOfEventIndex = LinearSearch(TypeOfEventsColumn, TypeOfEvent)

    # If the type of event does not exist, an error message is returned
    if TypeOfEventIndex == False:
        Result = {'status': 'invalid',
                  'errors': ['InvalidEvent']}
        return jsonify(Result)
    else:
        TypeOfEventID = TypeOfEventsTable[TypeOfEventIndex][0]

    # The start time is checked that a valid time has been entered
    if IsTimeValid(StartTime):
        pass
    else:
        # If not, an error is displayed
        Result = {'status': 'invalid',
                  'errors': ['StartTime']}
        return jsonify(Result)


    # The end time is checked that a valid time has been entered
    if IsTimeValid(EndTime):
        pass
    else:
        # If not, an error is displayed
        Result = {'status': 'invalid',
                  'errors': ['EndTime']}
        return jsonify(Result)
        

    if CeremonyRequired == 'true':

        # If a ceremony is required and the time is not valid, an error message is displayed
        if IsTimeValid(CeremonyTime):
            pass
        else:
            Result = {'status': 'invalid',
                    'errors': ['CeremonyTimeInvalid']}
            return jsonify(Result)
    
    # The inputs are validated and any errors are stored in an array
    ErrorsArray = ValidateNewBooking('Mr', 'Mrs', Customer1, Customer2, EventDate, PackageOption, StartTime, EndTime, SetUpRequired, CeremonyRequired, CeremonyTime, AdultGuestNumber, ChildGuestNumber, Under2GuestNumber, WelcomeRequired, AdultDrink, ChildDrink, ToastRequired, Notes)

    # If the date has not been edited, the date will initialy be marked as invalid
    # This is because the booking already exists in the database
    # To check if the date is really valid, the input date is compared to the current date for the booking that is being edited:
    if GetValueFromTable('Bookings', 6, int(BookingID)) == EventDate:
        ErrorsArray.remove('UnavailableDate')

    # If there are any errors, the error array is passed to the front end so that error messages can be displayed
    if len(ErrorsArray) != 0:
        Result = {'status': 'invalid',
                  'errors': ErrorsArray}
    else:

        # If all data is valid, a new booking is added to the array with the edited data and the old booking was removed
        AddNewBooking(session['IsAdmin'], Customer1, Customer2, GetValueFromTable('Bookings', 3, BookingID), GetValueFromTable('Bookings', 4, BookingID), TypeOfEventID, EventDate, StartTime, EndTime, AdultGuestNumber, ChildGuestNumber, Under2GuestNumber, ToastRequired, CeremonyRequired, CeremonyTime, WelcomeRequired, AdultDrink, ChildDrink, SetUpRequired, Notes)
        RemoveRecord('Bookings', int(BookingID))
        Result = {'status': 'success'}

    return jsonify(Result)

@app.route("/manager-invoices", methods=['GET', 'POST'])
def ManagerInvoices():

    # The session variables from the calendar are removed if exist as they are not needed in this part of the system
    try:
        session.pop('View')
    except:
        pass

    # The user must be an admin to view this page
    if session['IsAdmin'] == True:

        if request.method == 'POST':

            # When a payment is added, the booking id of the booking that has received a payment is stored
            BookingID = request.form.get('booking-id')

            # The amount that has been entered into the remaining cost input is retrieved and the payment type is set to 'cost'
            PaymentAmount = request.form.get('cost-input')
            PaymentType = 'cost'

            # If no payment amount has been entered for the cost, the payment type must be for a deposit
            if PaymentAmount == None:
                PaymentType = 'deposit'
                PaymentAmount = request.form.get('deposit-input')

            try:
                PaymentAmount = float(PaymentAmount)

                # If the value entered is not positive, an error is thrown to display an error message
                if PaymentAmount <= 0:
                    raise Exception()
            except:
                # If the value entered is not a number, an error message is displayed

                # All bookings are retrieved from the database as some will need to be displayed
                BookingsTable = GetEntireTable('Bookings')

                # The array of bookings that need to be displayed is initialised
                BookingsToDisplay = []
                
                # Every row in the table is checked to see if it representing an unavailable date and if there is any money still required for the deposit and remaining cost
                for i in range(len(BookingsTable)):
                    if (BookingsTable[i][25] == 0) and ((BookingsTable[i][14] > 0) or (BookingsTable[i][15] > 0)) and (BookingsTable[i][12] == True):

                        # If it is a genuine booking, the booking is added to the array of bookings that need to be displayed
                        Booking = ReturnUsefulDataToDisplay(BookingsTable[i]) # This returns an array of the event information in the correct format to be displayed
                        BookingsToDisplay.append(Booking)

                return render_template("ManagerInvoices.html", BookingsToDisplay=BookingsToDisplay, InvalidCostBooking=BookingID, HighCostBooking=0)
            
            # The new payment is subtracted from the necessary value in the database
            if AddNewPayment(BookingID, PaymentAmount, PaymentType) == False:

                # If the new payment is greater than the current outstanding cost, an error message is displayed

                # All bookings are retrieved from the database as some will need to be displayed
                BookingsTable = GetEntireTable('Bookings')

                # The array of bookings that need to be displayed is initialised
                BookingsToDisplay = []
                
                # Every row in the table is checked to see if it representing an unavailable date and if there is any money still required for the deposit and remaining cost
                for i in range(len(BookingsTable)):
                    if (BookingsTable[i][25] == 0) and ((BookingsTable[i][14] > 0) or (BookingsTable[i][15] > 0)) and (BookingsTable[i][12] == True):

                        # If it is a genuine booking, the booking is added to the array of bookings that need to be displayed
                        Booking = ReturnUsefulDataToDisplay(BookingsTable[i]) # This returns an array of the event information in the correct format to be displayed
                        BookingsToDisplay.append(Booking)

                return render_template("ManagerInvoices.html", BookingsToDisplay=BookingsToDisplay, HighCostBooking=BookingID, InvalidCostBooking=0)
            
        # All bookings are retrieved from the database as some will need to be displayed
        BookingsTable = GetEntireTable('Bookings')

        # The array of bookings that need to be displayed is initialised
        BookingsToDisplay = []
        
        # Every row in the table is checked to see if it representing an unavailable date and if there is any money still required for the deposit and remaining cost
        for i in range(len(BookingsTable)):
            if (BookingsTable[i][25] == 0) and ((BookingsTable[i][14] > 0) or (BookingsTable[i][15] > 0)) and (BookingsTable[i][12] == True):

                # If it is a genuine booking, the booking is added to the array of bookings that need to be displayed
                Booking = ReturnUsefulDataToDisplay(BookingsTable[i]) # This returns an array of the event information in the correct format to be displayed
                BookingsToDisplay.append(Booking)

        return render_template("ManagerInvoices.html", BookingsToDisplay=BookingsToDisplay)
    return redirect("/")

@app.route("/manager-customers", methods=['GET', 'POST'])
def ManagerCustomers():

    # The session variables from the calendar are removed if exist as they are not needed in this part of the system
    try:
        session.pop('View')
    except:
        pass

    # The user must be an admin to view this page
    if session['IsAdmin'] == True:

        # The customers are retrieved from the database to be displayed
        CustomerArray = GetEntireTable('Customers')

        return render_template("ManagerCustomers.html", CustomerArray=CustomerArray)
    return redirect("/")
    
@app.route("/manager-account", methods=['GET', 'POST'])
def ManagerAccount():

    # The session variables from the calendar are removed if exist as they are not needed in this part of the system
    try:
        session.pop('View')
    except:
        pass

    # The user must be an admin to view this page
    if session['IsAdmin'] == True:

        # The users details are retrieved from the database to be displayed on the screen
        Firstname = GetValueFromTable('Managers', 2, session['ManagerID'])
        Surname = GetValueFromTable('Managers', 3, session['ManagerID'])
        EmailAddress = GetValueFromTable('Managers', 4, session['ManagerID'])
        Username = GetValueFromTable('Managers', 1, session['ManagerID'])

        return render_template("ManagerAccount.html", Firstname=Firstname, Surname=Surname, EmailAddress=EmailAddress, Username=Username)
    return redirect("/")

@app.route("/process-manager-detail-change", methods=['POST'])
def ProcessManagerDetailChange():

    # Inputs are retrieved from the front end
    FirstName = request.form.get('firstname')
    Surname = request.form.get('surname')
    EmailAddress = request.form.get('emailAddress')
    Username = request.form.get('username')

    # Array of errors is initialised and any errors are added to the array
    ErrorsArray = []

    # Data is validated:

    # First name is validated
    # If the first name has not changed, it is not validated
    if FirstName != GetValueFromTable('Managers', 2, session['ManagerID']):
        if PresenceCheck(FirstName) and LengthCheckBetween(FirstName, 1, 30):
            pass
        else:
            ErrorsArray.append('Firstname')

    # Surname is validated
    # If the surname has not changed, it is not validated
    if Surname != GetValueFromTable('Managers', 3, session['ManagerID']):
        if PresenceCheck(Surname) and LengthCheckBetween(Surname, 1, 30):
            pass
        else:
            ErrorsArray.append('Surname')

    # Email Address is validated
    # If the email address has not changed, it is not validated
    if EmailAddress != GetValueFromTable('Managers', 4, session['ManagerID']):        

        # Current customer email addresses are retrieved
        CurrentCustomerEmailAddresses = RetrieveColumn('EmailAddress', 'Customers')      

        CurrentCustomerEmailAddressesArray= []
        for Tuple in CurrentCustomerEmailAddresses:
            CurrentCustomerEmailAddressesArray.append(Tuple[0])

        # Current manager email addresses are retrieved
        CurrentManagerEmailAddress = RetrieveColumn('EmailAddress', 'Managers')      

        CurrentManagerEmailAddressArray= []
        for Tuple in CurrentManagerEmailAddress:
            CurrentManagerEmailAddressArray.append(Tuple[0])

        # Customer and manager email address are concatenated
        CurrentEmailAddressesArray = CurrentCustomerEmailAddressesArray + CurrentManagerEmailAddressArray

        if UniquenessCheck(EmailAddress, CurrentEmailAddressesArray):
            pass
        else:
            ErrorsArray.append('EmailExists')

        if CheckEmailFormat(EmailAddress):
            pass
        else:
            ErrorsArray.append('InvalidEmail')

    # Username (AccountID) is validated
    # If the username has not changed, it is not validated
    if Username != GetValueFromTable('Managers', 1, session['ManagerID']):
    
        # Current customer usermanes are retrieved
        CurrentUsernamesTuple = RetrieveColumn('id', 'Accounts')

        CurrentUsernamesArray= []
        for Tuple in CurrentUsernamesTuple:
            CurrentUsernamesArray.append(Tuple[0])

        if PresenceCheck(Username) and LengthCheckBetween(Username, 1, 30):
            pass
        else:
            ErrorsArray.append('Username')

        if UniquenessCheck(Username, CurrentUsernamesArray):
            pass
        else:
            ErrorsArray.append('UsernameTaken')

    # If there is some invalid data, it will be passed to the front end so correct error messages can be displayed
    if len(ErrorsArray) == 0:

        # If data is valid, the database is updated
        ReplaceValue('Managers', 'FirstName', session['ManagerID'], FirstName)
        ReplaceValue('Managers', 'LastName', session['ManagerID'], Surname)
        ReplaceValue('Managers', 'EmailAddress', session['ManagerID'], EmailAddress)
        ReplaceValue('Managers', 'AccountID', session['ManagerID'], Username)
        ReplaceValue('Accounts', 'id', session['AccountID'], Username)
        session['AccountID'] = Username
        Result = {'status': 'success'}
    else:
        Result = {'status': 'invalid', 
                  'errors': ErrorsArray}

    return jsonify(Result)

@app.route("/manager-options", methods=['GET', 'POST'])
def ManagerBookingOptions():

    # The session variables from the calendar are removed if exist as they are not needed in this part of the system
    try:
        session.pop('View')
    except:
        pass

    # The user must be an admin to view this page
    if session['IsAdmin'] == True:

        # The list of currently available adult and child welcome drinks are retrieved to display on the screen
        AdultDrinks = RetrieveAdultDrinks()
        ChildDrinks = RetrieveChildrenDrinks()

        # The 'Other' options are removed from the list as the user should not be allowed to remove this option
        AdultDrinks.remove("Other")
        ChildDrinks.remove("Other")

        # The current events available are retrieved
        CurrentEvents = RetrieveColumn('TypeOfEvent', 'TypeOfEvents')
        CurrentEvents = [Tuple[0] for Tuple in CurrentEvents]

        # The wedding packages are removed from the type of events that will be displayed as the user should not be allowed to remove them
        CurrentEvents.remove('Wedding1')
        CurrentEvents.remove('Wedding2')
        CurrentEvents.remove('Wedding3')

        # The booking dates are retrieved
        TakenDates = RetrieveColumn('DateOfBooking', 'Bookings')
        TakenDates = [Tuple[0] for Tuple in TakenDates]

        # If the date is a genuine booking and not just marked as an unavailable date, it is removed from the array
        BookingIDArray = RetrieveColumn('id', 'Bookings')
        BookingIDArray = [Tuple[0] for Tuple in BookingIDArray]

        UnavailableDates = []

        Count = 0
        # For every booking, it is checked if the booking is an unavailable date or a booking
        for ID in BookingIDArray:
            if GetValueFromTable('Bookings', 25, ID) == 1:
                # If the booking is an unavailable date, the date is added to the unavailable dates array
                UnavailableDates.append(DateFormatToWords(TakenDates[Count]))
            Count += 1

        if request.method == 'POST':

            # If the add button for a new event is pressed:
            if 'add-event' in request.form:

                # The name of event and prices for the event are retrieved from the users inputs
                NewEvent = request.form.get('new-event')
                AdultPrice = request.form.get('adult-price')
                ChildPrice = request.form.get('child-price')

                # If the new event that has been entered already exists, an error message is displayed
                if UniquenessCheck(NewEvent, CurrentEvents):
                    # Each wedding package is stored in the database as 'Wedding1', 'Wedding2' or 'Wedding3'
                    # Therefore an error message is displayed if the user has entered 'Wedding'
                    if NewEvent == 'Wedding':
                        return render_template("ManagerBookingOptions.html", EventExistsError=True, CurrentEvents=CurrentEvents, UnavailableDates=UnavailableDates, AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks)
                    
                    # The length of the new event is validated and, if necessary, an error message is displayed
                    if LengthCheckBetween(NewEvent, 1, 30):
                        
                        try:
                            # If the cost inputs can be converted to reals, they are valid
                            float(AdultPrice)
                            float(ChildPrice)
                            AddNewTypeOfEvent(NewEvent, AdultPrice, ChildPrice)
                            return redirect('/manager-options')
                        except:
                            # If the cost inputs cannot be converted to reals, an error message is displayed
                            return render_template("ManagerBookingOptions.html", InvalidCostError=True, AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks, CurrentEvents=CurrentEvents, UnavailableDates=UnavailableDates)
                    return render_template("ManagerBookingOptions.html", InvalidEventError=True, AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks, CurrentEvents=CurrentEvents, UnavailableDates=UnavailableDates)
                return render_template("ManagerBookingOptions.html", EventExistsError=True, AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks, CurrentEvents=CurrentEvents, UnavailableDates=UnavailableDates)

            # If the add button for a new unavailable date is pressed:
            elif 'add-date' in request.form:

                # The inputs are retrieved
                Day = request.form.get('day-input')
                Month = request.form.get('month-input')
                Year = request.form.get('year-input')

                # The inputs are concatenated into the correct format
                Date = Year + "-" + Month + "-" + Day

                # The list of dates that currently have booking on is retrieved
                CurrentDates = RetrieveColumn('DateOfBooking', 'Bookings')
                CurrentDates = [Tuple[0] for Tuple in CurrentDates]

                if UniquenessCheck(Date, CurrentDates):
                    try:
                        # If the date entered is not a current booking date and is valid, a new unavailable date is added
                        if IsDateFuture(Date) and IsDateValid(Date):
                            AddNewUnavailableDate(Date)
                            return redirect('/manager-options')
                        else:
                            # If the date is not valid, an error message is displayed
                            return render_template("ManagerBookingOptions.html", AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks, CurrentEvents=CurrentEvents, UnavailableDates=UnavailableDates, InvalidDate=True)
                    except:
                        # If the date is not valid, an error message is displayed
                        return render_template("ManagerBookingOptions.html", AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks, CurrentEvents=CurrentEvents, UnavailableDates=UnavailableDates, InvalidDate=True)
                
                # If the date entered appears in the array of current dates
                # There is either a booking on this day or an unavailable date set on this day

                # The row index of the booking with the same date is found
                # Here, the ID cannot be used as some bookings may have been deleted from the table
                # This means that the index of the date in the array may not be that records ID
                Count = 0
                for CurrentDate in CurrentDates:
                    if Date == CurrentDate:
                        break
                    Count += 1

                # Using the row index, it is checked if the booking is an event or an unavailable date
                BookingsTable = GetEntireTable('Bookings')

                if BookingsTable[Count][25] == 1:

                    # If it is an unavailable date, an error message is displayed saying that this date is already marked as unavailable
                    return render_template("ManagerBookingOptions.html", AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks, CurrentEvents=CurrentEvents, UnavailableDates=UnavailableDates, UnavailableDateExists=True)
                
                # If the date is that of an actual booking, the Booking ID is found
                BookingID = BookingsTable[Count][0]

                # The Booking is removed from the database,
                # An email is sent to the customer whose booking has been cancelled
                # A message is displayed informing the manager that a booking has been cancelled to make this date unavailable
                # The date is marked as unavailable
                CancelledByManagerEmail(BookingID, 'This date has become unavailable')
                RemoveRecord('Bookings', BookingID)
                AddNewUnavailableDate(Date)
                return render_template("ManagerBookingOptions.html", AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks, CurrentEvents=CurrentEvents, UnavailableDates=UnavailableDates, CancelledBooking=True)
            
            # If the add button for the new adult drink is pressed:
            elif 'add-adult-drink' in request.form:

                # The input is retrieved
                NewDrink = request.form.get('new-adult-drink')

                # The new drink length is validated
                if LengthCheckBetween(NewDrink, 1, 30):

                    # The cuurrent available adult drinks are retrieved
                    CurrentAdultDrinks = RetrieveAdultDrinks()

                    # If the drink entered is not one of the currently available drinks, the new drink is added
                    if NewDrink not in CurrentAdultDrinks:
                        CurrentAdultDrinks.append(NewDrink)
                        SaveAdultDrinks(CurrentAdultDrinks)
                        return redirect('/manager-options')
                    else:
                        # If the drink is already available, an error message is displayed
                        return render_template("ManagerBookingOptions.html", AdultDrinkExists=True, AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks, CurrentEvents=CurrentEvents, UnavailableDates=UnavailableDates)
                else:
                    return render_template("ManagerBookingOptions.html", InvalidAdultDrink=True, AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks, CurrentEvents=CurrentEvents, UnavailableDates=UnavailableDates)

            # If the add button for the new child drink is pressed:
            elif 'add-child-drink' in request.form:

                # The input is retrieved
                NewDrink = request.form.get('new-child-drink')

                # The new drink length is validated
                if LengthCheckBetween(NewDrink, 1, 30):

                    # The current available child drinks are retrieved
                    CurrentChildDrinks = RetrieveChildrenDrinks()

                    # If the drink entered is not one of the currently available drinks, the new drink is added
                    if NewDrink not in CurrentChildDrinks:
                        CurrentChildDrinks.append(NewDrink)
                        SaveChildDrinks(CurrentChildDrinks)
                        return redirect('/manager-options')
                    else:
                        # If the drink is already available, an error essage is displayed
                        return render_template("ManagerBookingOptions.html", ChildDrinkExists=True, AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks, CurrentEvents=CurrentEvents, UnavailableDates=UnavailableDates)
                else:
                    return render_template("ManagerBookingOptions.html", InvalidChildDrink=True, AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks, CurrentEvents=CurrentEvents, UnavailableDates=UnavailableDates)

            elif 'remove-event' in request.form:

                # The event that has been selected to be removed is retrieved and removed
                EventToRemove = request.form.get('event-select')
                RemoveOption('TypeOfEvents', 'TypeOfEvent', EventToRemove)
                return redirect('/manager-options')

            elif 'remove-date' in request.form:

                # The date that has been selected to be removed is retrieved and removed
                DateToRemove = request.form.get('date-select')
                RemoveOption('Bookings', 'DateOfBooking', DateWordsToFormat(DateToRemove))
                return redirect('/manager-options')

            elif 'remove-adult-drink' in request.form:
                
                # The drink that has been selected to be removed is retrieved
                DrinkToRemove = request.form.get('adult-drink-select')

                # The current list of adult drinks is retrieved
                CurrentAdultDrinks = RetrieveAdultDrinks()

                # The selected drink is removed from the list
                CurrentAdultDrinks.remove(DrinkToRemove)

                # The file is saved
                SaveAdultDrinks(CurrentAdultDrinks)
                return redirect('/manager-options')
            
            else:

                # The drink that has been selected to be removed is retrieved
                DrinkToRemove = request.form.get('child-drink-select')

                # The current list of adult drinks is retrieved
                CurrentChildDrinks = RetrieveChildrenDrinks()

                # The selected drink is removed from the list
                CurrentChildDrinks.remove(DrinkToRemove)

                # The file is saved
                SaveChildDrinks(CurrentChildDrinks)
                return redirect('/manager-options')

        return render_template("ManagerBookingOptions.html", AdultDrinks=AdultDrinks, ChildDrinks=ChildDrinks, CurrentEvents=CurrentEvents, UnavailableDates=UnavailableDates)
    return redirect("/")


# Customer pages
@app.route("/customer-bookings", methods=['GET', 'POST'])
def CustomerBookings():

    # The user must be a customer to view this page
    if session['IsAdmin'] == False:

        # All bookings are retrieved from the database as some will need to be displayed
        BookingsTable = GetEntireTable('Bookings')

        # The array of bookings that need to be displayed is initialised
        BookingsToDisplay = []
        
        # Every row in the table is checked to see if it representing an unavailable date and if it is one of the customers bookings
        for i in range(len(BookingsTable)):
            if (BookingsTable[i][25] == 0) and (BookingsTable[i][3] == session['CustomerID']):

                # If it is a genuine booking and belongs to the current customer, the booking is added to the array of bookings that need to be displayed
                Booking = ReturnUsefulDataToDisplay(BookingsTable[i]) # This returns an array of the event information in the correct format to be displayed
                BookingsToDisplay.append(Booking)

        return render_template("CustomerBookings.html", BookingsToDisplay=BookingsToDisplay)
    return redirect("/")

@app.route("/process-cancel-booking-customer", methods=['POST'])
def ProcessCancelBookingCustomer():

    # Retrieve the booking id for the booking that has been cancelled and the reason for its cancellation
    BookingID = request.form.get('bookingID')
    CancellationReason = request.form.get('cancellationReason')

    # An email is sent to the manager informing them that a customer has cancelled their booking
    CancelledByCustomerEmail(BookingID, CancellationReason)

    # The booking is removed from the database
    RemoveRecord('Bookings', BookingID)

    return 'Complete'

@app.route("/customer-account", methods=['GET', 'POST'])
def CustomerAccount():
    
    # The user must be customer to view this page
    if session['IsAdmin'] == False:

        # The users details are retrieved from the database to be displayed on the screen
        Firstname = GetValueFromTable('Customers', 1, session['CustomerID'])
        Surname = GetValueFromTable('Customers', 2, session['CustomerID'])
        PhoneNumber = GetValueFromTable('Customers', 4, session['CustomerID'])
        EmailAddress = GetValueFromTable('Customers', 3, session['CustomerID'])
        Username = GetValueFromTable('Customers', 5, session['CustomerID'])

        return render_template("CustomerAccount.html", Firstname=Firstname, Surname=Surname, PhoneNumber=PhoneNumber, EmailAddress=EmailAddress, Username=Username)
    return redirect("/")

@app.route("/process-customer-detail-change", methods=['POST'])
def ProcessCustomerDetailChange():

    # Inputs are retrieved from the front end
    FirstName = request.form.get('firstname')
    Surname = request.form.get('surname')
    PhoneNumber = request.form.get('phoneNumber')
    EmailAddress = request.form.get('emailAddress')
    Username = request.form.get('username')

    # Array of errors is initialised and any errors are added to the array
    ErrorsArray = []

    # Data is validated:

    # First name is validated
    # If the first name has not changed, it is not validated
    if FirstName != GetValueFromTable('Customers', 1, session['CustomerID']):
        if PresenceCheck(FirstName) and LengthCheckBetween(FirstName, 1, 30):
            pass
        else:
            ErrorsArray.append('Firstname')

    # Surname is validated
    # If the surname has not changed, it is not validated
    if Surname != GetValueFromTable('Customers', 2, session['CustomerID']):
        if PresenceCheck(Surname) and LengthCheckBetween(Surname, 1, 30):
            pass
        else:
            ErrorsArray.append('Surname')

    # Phone number is validated
    # If the phone number has not changed, it is not validated
    if PhoneNumber != GetValueFromTable('Customers', 4, session['CustomerID']):
        CurrentPhoneNumbersTuple = RetrieveColumn('PhoneNumber', 'Customers')

        CurrentPhoneNumbersArray= []
        for Tuple in CurrentPhoneNumbersTuple:
            CurrentPhoneNumbersArray.append(Tuple[0])

        if CheckPhoneFormat(PhoneNumber):
            pass
        else:
            ErrorsArray.append('PhoneInvalid')

        if UniquenessCheck(PhoneNumber, CurrentPhoneNumbersArray):
            pass
        else:
            ErrorsArray.append('PhoneTaken')

    # Email Address is validated
    # If the email address has not changed, it is not validated
    if EmailAddress != GetValueFromTable('Customers', 3, session['CustomerID']):        

        # Current customer email addresses are retrieved
        CurrentCustomerEmailAddresses = RetrieveColumn('EmailAddress', 'Customers')      

        CurrentCustomerEmailAddressesArray= []
        for Tuple in CurrentCustomerEmailAddresses:
            CurrentCustomerEmailAddressesArray.append(Tuple[0])

        # Current manager email addresses are retrieved
        CurrentManagerEmailAddress = RetrieveColumn('EmailAddress', 'Managers')      

        CurrentManagerEmailAddressArray= []
        for Tuple in CurrentManagerEmailAddress:
            CurrentManagerEmailAddressArray.append(Tuple[0])

        # Customer and manager email address are concatenated
        CurrentEmailAddressesArray = CurrentCustomerEmailAddressesArray + CurrentManagerEmailAddressArray

        if UniquenessCheck(EmailAddress, CurrentEmailAddressesArray):
            pass
        else:
            ErrorsArray.append('EmailExists')

        if CheckEmailFormat(EmailAddress):
            pass
        else:
            ErrorsArray.append('InvalidEmail')

    # Username (AccountID) is validated
    # If the username has not changed, it is not validated
    if Username != GetValueFromTable('Customers', 5, session['CustomerID']):
    
        # Current usermanes are retrieved
        CurrentUsernamesTuple = RetrieveColumn('id', 'Accounts')

        CurrentUsernamesArray= []
        for Tuple in CurrentUsernamesTuple:
            CurrentUsernamesArray.append(Tuple[0])

        if PresenceCheck(Username) and LengthCheckBetween(Username, 1, 30):
            pass
        else:
            ErrorsArray.append('Username')

        if UniquenessCheck(Username, CurrentUsernamesArray):
            pass
        else:
            ErrorsArray.append('UsernameTaken')

    # If there is some invalid data, it will be passed to the front end so correct error messages can be displayed
    if len(ErrorsArray) == 0:

        # If data is valid, the database is updated
        ReplaceValue('Customers', 'FirstName', session['CustomerID'], FirstName)
        ReplaceValue('Customers', 'LastName', session['CustomerID'], Surname)
        ReplaceValue('Customers', 'PhoneNumber', session['CustomerID'], PhoneNumber)
        ReplaceValue('Customers', 'EmailAddress', session['CustomerID'], EmailAddress)
        ReplaceValue('Customers', 'AccountID', session['CustomerID'], Username)
        ReplaceValue('Accounts', 'id', session['AccountID'], Username)
        session['AccountID'] = Username
        Result = {'status': 'success'}
    else:
        Result = {'status': 'invalid', 
                  'errors': ErrorsArray}
        
    return jsonify(Result)

if __name__ == "__main__":
    app.run(debug=True)