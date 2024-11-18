def DateFormatToWords(Date):
    Year = Date[0:4]
    Month = int(Date[5:7])
    Day = int(Date[8:10])
    # Seperates the year, month and day from the form 'YYYY-MM-DD'

    Month = Month - 1

    Months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    Month = Months[Month]
    
    NewDate = str(Day) + " " + Month + " " + Year
    return NewDate

def DateWordsToFormat(Date):
    Day, Month, Year = Date.split()

    Months = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}
    Month = Months[Month]

    Month = AddZeros(Month)
    Day = AddZeros(Day)

    return Year + "-" + Month + "-" + Day

def DaysInMonth(Date):

    # The date is currently in the form YYYY-MM-DD
    # Therefore, the month and day are extracted from this form
    Month = int(Date[5:7])
    Year = int(Date[0:4])

    # The days of each month are initialised in two arrays
    MonthsWith31Days = [1, 3, 5, 7, 8, 10, 12]
    MonthsWith30Days= [4, 6, 9, 11]

    # The year is checked to see if it is a leap year
    LeapYear = IsLeapYear(Year)

    # If the month appears in the MonthsWith31Days array, 31 is retured
    if Month in MonthsWith31Days:
        return 31
    
    # If the month appears in the MonthsWith300Days array, 3 is retured
    elif Month in MonthsWith30Days:
        return 30
    
    # If the month appears in neither array and it is not a leap year, 28 is returned
    elif LeapYear == False:
        return 28
    
    # If the month appears in neither array but it is a leap year, 29 is returned
    else:
        return 29

def DaysInMonthGivenMonthAndYear(Year, Month):

    # If the month appears in the first array (months with 31 days), 31 is returned
    if Month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    
    # If the month appears in the second array (months with 30 days), 30 is returned
    elif Month in [4, 6, 9, 11]:
        return 30
    
    # Otherwise, 28 is returned if it is not a leap year or 29 is returned if it is
    else:
        return 29 if IsLeapYear(Year) else 28
        
def DayOfWeekAlgorithm(Date):

    # The year day and month are extracted from the date which is in the format YYYY-MM-DD
    Year = int(Date[0:4])
    Month = int(Date[5:7])
    Day = int(Date[8:10])

    # The month and year are adjusted for the Zeller's Congruence algorithm
    if Month < 3:
        Month += 12
        Year -= 1

    # The necessary values for the algorithm are calculated using the year
    k = Year % 100
    j = Year // 100

    # An array of each day of the week is initialised
    Days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # The result of the algorithm is a number representing the index of the day of the week in the days algorithm
    return(Days[(Day + 13*(Month+1)//5 + k + k//4 + j//4 + 5*j) % 7])

def DayIndex(Day):
    # The days of the week are initialised in an array
    DaysOfTheWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # The index of the Day parameter is found from the array and returned
    Index = DaysOfTheWeek.index(Day)
    return Index

def AddMonth(MonthYear):
    # Split the input into month and year
    Month, Year = MonthYear.split()

    # Map month names to their corresponding indices
    MonthsMap = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                  'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

    # Reverse mapping for index to month name
    ReverseMonthsMap = {v: k for k, v in MonthsMap.items()}

    # Add one to the current month index
    CurrentMonthIndex = MonthsMap[Month]
    NextMonthIndex = (CurrentMonthIndex % 12) + 1

    if NextMonthIndex == 1:
        NewYear = int(Year) + 1
    else:
        NewYear = int(Year)

    # Calculate the new month and year
    NewMonth = ReverseMonthsMap[NextMonthIndex]

    return NewMonth + " " + str(NewYear)

def SubtractMonth(MonthYear):
    # Split the input into month and year
    Month, Year = MonthYear.split()

    # Map month names to their corresponding indices
    MonthsMap = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                  'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

    # Reverse mapping for index to month name
    ReverseMonthsMap = {v: k for k, v in MonthsMap.items()}

    # Subtract one from the current month index
    CurrentMonthIndex = MonthsMap[Month]
    PreviousMonthIndex = (CurrentMonthIndex - 2) % 12 + 1  # Handle January separately

    # Check if January is preceded by December
    if PreviousMonthIndex == 12:
        NewYear = int(Year) - 1
    else:
        NewYear = int(Year)

    # Calculate the new month
    NewMonth = ReverseMonthsMap[PreviousMonthIndex]

    return NewMonth + " " + str(NewYear)

def IsLeapYear(Date):

    # It is checked if a year of a date in the fomat YYYY-MM-DD has been passed to the subroutine
    if len(str(Date)) > 4:
        Year = Date[0:4]
    else:
        Year = Date

    # It is determined if the year is a leap year - if it is, true is returned - if it isn't, false is returned
    if (int(Year) % 4 == 0 and int(Year) % 100 != 0) or (int(Year) % 400 == 0):
        return True
    else:
        return False

def AddDays(Date, DaysToAdd):

    # The day, month and year are extracted from the date in the format YYYY-MM-DD
    Year = int(Date[0:4])
    Month = int(Date[5:7])
    Day = int(Date[8:10])

    # This loop is repeated while there are still days to be added
    while DaysToAdd > 0:

        # The number of days in the current month is calculated
        # This must be inside the loop as the current month could change as days are added
        DaysInCurrentMonth = DaysInMonth(Date)

        # If the new date will go into the next month, other calculation need to be made, otherwise, the day is added
        if Day + DaysToAdd > DaysInCurrentMonth:

            # The number of days to add until the new month is calculated and the day is set to 1 (first day of the new month)
            DaysToAdd -= (DaysInCurrentMonth - Day + 1)
            Day = 1

            # If the month was December, then the month is reset to January and the year is incremented by 1
            if Month == 12:
                Month = 1
                Year += 1
            else:
                Month += 1
        else:
            Day += DaysToAdd
            DaysToAdd = 0
    
    # The new date is returned in the format YYYY-MM-DD
    return f"{Year:04d}-{Month:02d}-{Day:02d}"

def SubtractDays(Date, DaysToSubtract):

    # The day, month and year are extracted from the date in the format YYYY-MM-DD
    Year = int(Date[0:4])
    Month = int(Date[5:7])
    Day = int(Date[8:10])

    # If the new date is in the previous month, other calculations are needed, otherwise, the new date is simply calculated
    if Day - DaysToSubtract > 0:
        Day = Day - DaysToSubtract
    else:

        # If the month was January, the month is reset to December and the year is subtracted by 1
        if Month == 1:
            Year -= 1
            Month = 12
        else:
            Month -= 1

        # The number of days in the new month is calculated
        if Month in [1, 3, 5, 7, 8, 10, 12]:
            NumberOfDays = 31
        elif Month in [4, 6, 9, 11]:
            NumberOfDays = 30
        else:
            if IsLeapYear(Date):
                NumberOfDays = 29
            else:
                NumberOfDays = 28

        # The new day is calculated
        Day = NumberOfDays - (DaysToSubtract - Day)

    # 0 may needed to be added to the start of the month and day before being returned in the format YYYY-MM-DD
    Year = str(Year)
    Month = AddZeros(Month)
    Day = AddZeros(Day)

    return Year + "-" + str(Month) + "-" + str(Day)

def AddZeros(Number):

    # if the number passed is less than 10 and does not already have a zero in front of it, a zero is added
    if int(Number) < 10 and len(str(Number)) < 2:
        Number = "0" + str(Number)
        return Number
    
    # Otherwise, the original number is returned
    else:
        return str(Number)
    
def GetMonth(Date):

    # The month is extracted from the date which is in the format YYYY-MM-DD
    Month = int(Date[5:7])

    # An array of months is initialised
    Months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # The index of the month will be one less than the value of month
    # The month at this index is returned
    Month = Months[Month-1]
    return Month

def GetFirstDayIndex(Day):
    # The day of the week is passed to the subroutine and the index of this day is returned

    # The days of the week are each assigned an index
    DayIndexes = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }

    # This index is returned
    return DayIndexes.get(Day)

def DaysBetweenDates(Date1, Date2):

    # Both dates are split into day, month and year from the format YYYY-MM-DD
    Year1, Month1, Day1 = map(int, Date1.split('-'))
    Year2, Month2, Day2 = map(int, Date2.split('-'))

    # DaysDifference is initialised at 0
    DaysDifference = 0

    # Calculate days in date1 until the end of its year
    for Month in range(Month1, 13):
        DaysDifference += DaysInMonthGivenMonthAndYear(Year1, Month)

    DaysDifference -= Day1

    # Calculate full years between date1 and date2
    for Year in range(Year1 + 1, Year2):
        DaysDifference += 365 + int(IsLeapYear(Year))

    # Calculate days in date2 until the specified day
    for Month in range(1, Month2):
        DaysDifference += DaysInMonthGivenMonthAndYear(Year2, Month)

    DaysDifference += Day2

    return DaysDifference