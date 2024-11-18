from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import date
from DateConversions import AddDays, DateFormatToWords
from RetrieveDataFromDatabase import GetValueFromTable

def GenerateInvoice(BookingID):
    # The current date is stored
    CurrentDate = str(date.today())

    # The due date of the deposit is calculated
    # It is 2 weeks after the day the booking was made (today)
    DepositDueDate = DateFormatToWords(AddDays(CurrentDate, 14))

    # The adult and child guest numbers are retrueved from the database
    AdultGuestNumber = GetValueFromTable('Bookings', 9, int(BookingID))
    ChildGuestNumber = GetValueFromTable('Bookings', 10, int(BookingID))

    # The set up day and ceremony requirements are retrieved from the database
    SetupDayRequired = GetValueFromTable('Bookings', 22, int(BookingID))
    CeremonyRoomRequired = GetValueFromTable('Bookings', 17, int(BookingID))

    # The due date of the entire payment is set as the date of the booking which is retrieved from the database
    TotalCostDueDate = DateFormatToWords(GetValueFromTable('Bookings', 6, int(BookingID)))

    # The type of event ID is retrieved from the bookings table
    TypeOfEventID = GetValueFromTable('Bookings', 5, BookingID)
    
    # The type of event ID is used to retrieve the adult and child costs for the necessary event
    AdultCost = GetValueFromTable('TypeOfEvents', 2, TypeOfEventID)
    ChildCost = GetValueFromTable('TypeOfEvents', 2, TypeOfEventID)

    # The type of event ID is also used to find the type of event (in words) from the database
    TypeOfEvent = GetValueFromTable('TypeOfEvents', 1, TypeOfEventID)

    # If the type of event is any of the wedding packages, it is just set to 'Wedding'
    if TypeOfEvent == 'Wedding1' or TypeOfEvent == 'Wedding2' or TypeOfEvent == 'Wedding3':
        TypeOfEvent = 'Wedding'

    # The total adult cost is calculated and rounded to 2 decimal places
    TotalAdultCost = AdultCost * AdultGuestNumber
    TotalAdultCost = f"{float(TotalAdultCost):.2f}"

    # The total child cost is calculated and rounded to 2 decimal places
    TotalChildCost = ChildCost * ChildGuestNumber
    TotalChildCost = f"{float(TotalChildCost):.2f}"

    # The total guest cost is calculated and rounded to 2 decimal places
    TotalGuestCost = float(TotalAdultCost) + float(TotalChildCost)
    TotalGuestCost = f"{float(TotalGuestCost):.2f}"

    # The ceremony and set up days are set to boolean values as they are currently strings after being passed between the front and back end
    if CeremonyRoomRequired == 'true':
        CeremonyRoomRequired = 1
    else:
        CeremonyRoomRequired = 0

    if SetupDayRequired == 'true':
        SetupDayRequired = 1
    else:
        SetupDayRequired = 0

    # The size of the pdf is set and the file name is set
    PageType = A4
    FileName = 'InvoiceFile\Invoice' + str(BookingID) + '.pdf'
    InvoiceOutputPath = FileName
    c = canvas.Canvas(InvoiceOutputPath, pagesize=A4)

    #Title Box - size and colour are set
    BoxWidth = 300
    BoxHeight = 50
    BoxColour = "#41436A"

    #Title Box position
    CentreX = (PageType[0] - BoxWidth) / 2
    TopY = PageType[1] - (BoxHeight + 10)

    #Title Box Colour
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    #Title box text - colour, font and font size are set
    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "Mounton Brook Lodge"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    #InvoiceID boxes - size and colour are set
    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "#41436A"

    #InvoiceID Box position
    CentreX = (PageType[1] - 836)
    TopY = PageType[1] - 120

    #InvoiceID Box Colour
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    #InvoiceID box text - colour, font and font size are set
    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "Invoice ID:"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)

    # BookingID box - size and colour are set
    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "white"

    # BookingID box position
    CentreX = (PageType[1] - 692)
    TopY = PageType[1] - 120

    # InvoiceID box color
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    # InvoiceID box text - colour, font and font size are set
    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = "#" + str(BookingID)
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)

    # Date Created boxes - size and colour are set
    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "#41436A"

    # Date Created Box position
    CentreX = (PageType[1] - 836)
    TopY = PageType[1] - 150

    # Date Created Box Colour
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    # Date Created box text - colour, font and font size are set
    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "Created:"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)

    # Current date boxes - size and colour are set
    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "white"

    # Current date box position
    CentreX = (PageType[1] - 692)
    TopY = PageType[1] - 150

    # Current date box colour
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    # Current date box text - colour, font and font size are set
    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = CurrentDate
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    # Type of event box - size and position are set
    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "#41436A"

    #T ype of event Box position
    CentreX = (PageType[1] - 836)
    TopY = PageType[1] - 200

    # Type of event Box Colour
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    # Type of event box text - colour, font and font size are set
    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "Type of event:"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 692)
    TopY = PageType[1] - 200

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = TypeOfEvent
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    #Guest numbers and costs boxes - size and position are set
    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "#41436A"

    #Guest number Box position
    CentreX = (PageType[1] - 542)
    TopY = PageType[1] - 270

    #Guest number Box Colour
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    #Guest number box text - colour, font and font size are set
    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "Cost per guest"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "#41436A"
    
    CentreX = (PageType[1] - 692)
    TopY = PageType[1] - 270
    
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)
    
    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "Guest number"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 140
    BoxHeight = 30
    BoxColour = "#41436A"
    
    CentreX = (PageType[1] - 392)
    TopY = PageType[1] - 270
    
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)
    
    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "Total"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "#41436A"
    
    CentreX = (PageType[1] - 836)
    TopY = PageType[1] - 300
    
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)
    
    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "18+ guests"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 692)
    TopY = PageType[1] - 300

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = str(AdultGuestNumber)
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 542)
    TopY = PageType[1] - 300

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = "£" + str(AdultCost)
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 140
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 392)
    TopY = PageType[1] - 300

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = "£" + str(TotalAdultCost)
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "#41436A"
    
    CentreX = (PageType[1] - 836)
    TopY = PageType[1] - 330
    
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)
    
    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "2-17 guests"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 692)
    TopY = PageType[1] - 330

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = str(ChildGuestNumber)
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)
    

    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 542)
    TopY = PageType[1] - 330

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = "£" + str(ChildCost)
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 140
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 392)
    TopY = PageType[1] - 330

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = "£" + str(TotalChildCost)
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 300
    BoxHeight = 30
    BoxColour = "#41436A"
    
    CentreX = (PageType[1] - 836)
    TopY = PageType[1] - 380
    
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)
    
    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "Total guest cost"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 290
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 542)
    TopY = PageType[1] - 380

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = "£" + str(TotalGuestCost)
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)

    # The distance from the top so far is 380
    DistanceFromTop = 380

    # If there is a set up or ceremont required, the distance is increased as new boxes need to be displayed
    if SetupDayRequired == 1 or CeremonyRoomRequired == 1:

        DistanceFromTop = DistanceFromTop + 50

        #Additional costs boxes
        BoxWidth = 150
        BoxHeight = 30
        BoxColour = "#41436A"
        #Additional costs position
        CentreX = (PageType[1] - 542)
        TopY = PageType[1] - DistanceFromTop
        #Additional costs colour
        c.setFillColor(BoxColour)
        c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)
        #Additional costs text
        c.setFillColor("#E5EFC1")
        c.setFont("Helvetica", 20)
        Text = "Cost"
        TextWidth = c.stringWidth(Text, "Helvetica", 20)
        TextX = CentreX + (BoxWidth - TextWidth) / 2
        TextY = TopY + (BoxHeight - 10) / 2
        c.drawString(TextX, TextY, Text)

        if SetupDayRequired == 1:

            # Set up cost is set and rounded to 2 decimal places
            SetUpCost = 495
            SetUpCost = f"{float(SetUpCost):.2f}"
            DistanceFromTop = DistanceFromTop + 30

            BoxWidth = 300
            BoxHeight = 30
            BoxColour = "#41436A"
            
            CentreX = (PageType[1] - 836)
            TopY = PageType[1] - DistanceFromTop

            c.setFillColor(BoxColour)
            c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

            c.setFillColor("#E5EFC1")
            c.setFont("Helvetica", 20)
            Text = "Set up day required"
            TextWidth = c.stringWidth(Text, "Helvetica", 20)
            TextX = CentreX + (BoxWidth - TextWidth) / 2
            TextY = TopY + (BoxHeight - 10) / 2
            c.drawString(TextX, TextY, Text)


            BoxWidth = 150
            BoxHeight = 30
            BoxColour = "white"

            CentreX = (PageType[1] - 542)
            TopY = PageType[1] - DistanceFromTop

            c.setFillColor(BoxColour)
            c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

            c.setFillColor("#41436A")
            c.setFont("Helvetica", 20)
            Text = "£495.00"
            TextWidth = c.stringWidth(Text, "Helvetica", 20)
            TextX = CentreX + (BoxWidth - TextWidth) / 2
            TextY = TopY + (BoxHeight - 10) / 2
            c.drawString(TextX, TextY, Text)

        else:
            SetUpCost = 0

        if CeremonyRoomRequired == 1:

            # CeremonyCost is set and rounded to 2 decimal places
            CeremonyCost = 495
            CeremonyCost = f"{float(CeremonyCost):.2f}"
            DistanceFromTop = DistanceFromTop + 30

            BoxWidth = 300
            BoxHeight = 30
            BoxColour = "#41436A"

            CentreX = (PageType[1] - 836)
            TopY = PageType[1] - DistanceFromTop

            c.setFillColor(BoxColour)
            c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

            c.setFillColor("#E5EFC1")
            c.setFont("Helvetica", 20)
            Text = "Ceremony room required"
            TextWidth = c.stringWidth(Text, "Helvetica", 20)
            TextX = CentreX + (BoxWidth - TextWidth) / 2
            TextY = TopY + (BoxHeight - 10) / 2
            c.drawString(TextX, TextY, Text)


            BoxWidth = 150
            BoxHeight = 30
            BoxColour = "white"

            CentreX = (PageType[1] - 542)
            TopY = PageType[1] - DistanceFromTop

            c.setFillColor(BoxColour)
            c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

            c.setFillColor("#41436A")
            c.setFont("Helvetica", 20)
            Text = "£495.00"
            TextWidth = c.stringWidth(Text, "Helvetica", 20)
            TextX = CentreX + (BoxWidth - TextWidth) / 2
            TextY = TopY + (BoxHeight - 10) / 2
            c.drawString(TextX, TextY, Text)

        else:
            CeremonyCost = 0

    else:
        CeremonyCost = 0
        SetUpCost = 0

    # The distance from top variable now means that there will not be any blank space on the invoci=oice even if no ceremony or set up day is required

    # The total cost is calculated by adding the guest costs, ceremony costs and set up costs
    TotalCost = float(TotalGuestCost) + float(CeremonyCost) + float(SetUpCost)

    # From the total cost, the deposit and remaining cost are calculated and rounded to 2 decimal places
    Deposit = TotalCost * 0.3
    Deposit = f"{float(Deposit):.2f}"

    TotalCost = TotalCost * 0.7
    TotalCost = f"{float(TotalCost):.2f}"

    #Total costs boxes
    BoxWidth = 290
    BoxHeight = 30
    BoxColour = "#41436A"

    #Total costs position
    CentreX = (PageType[1] - 542)
    TopY = PageType[1] - (DistanceFromTop + 100)

    #Total costs colour
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    #Total costs text
    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "Due date"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 300
    BoxHeight = 30
    BoxColour = "#41436A"

    CentreX = (PageType[1] - 836)
    TopY = PageType[1] - (DistanceFromTop + 50)

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "Total event cost"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 290
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 542)
    TopY = PageType[1] - (DistanceFromTop + 50)

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = "£" + str(TotalCost)
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "#41436A"

    CentreX = (PageType[1] - 836)
    TopY = PageType[1] - (DistanceFromTop + 130)

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "30% Deposit"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 692)
    TopY = PageType[1] - (DistanceFromTop + 130)

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = "£" + str(Deposit)
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 290
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 542)
    TopY = PageType[1] - (DistanceFromTop + 130)

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = DepositDueDate
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "#41436A"

    CentreX = (PageType[1] - 836)
    TopY = PageType[1] - (DistanceFromTop + 160)

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 18)
    Text = "Remaining cost"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 692)
    TopY = PageType[1] - (DistanceFromTop + 160)

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = "£" + str(TotalCost)
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 290
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 542)
    TopY = PageType[1] - (DistanceFromTop + 160)

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = TotalCostDueDate
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    #Account Details boxes
    BoxWidth = 300
    BoxHeight = 30
    BoxColour = "#41436A"

    #Account Details position
    CentreX = (PageType[1] - 836)
    TopY = PageType[1] - (DistanceFromTop + 210)

    #Account Details colour
    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    #Account Details text
    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "Account number"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 542)
    TopY = PageType[1] - (DistanceFromTop + 210)

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = "xxxxxxxx" # This is where the business account number would go
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 300
    BoxHeight = 30
    BoxColour = "#41436A"

    CentreX = (PageType[1] - 836)
    TopY = PageType[1] - (DistanceFromTop + 240)

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#E5EFC1")
    c.setFont("Helvetica", 20)
    Text = "Sort code"
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)


    BoxWidth = 150
    BoxHeight = 30
    BoxColour = "white"

    CentreX = (PageType[1] - 542)
    TopY = PageType[1] - (DistanceFromTop + 240)

    c.setFillColor(BoxColour)
    c.rect(CentreX, TopY, BoxWidth, BoxHeight, fill=True)

    c.setFillColor("#41436A")
    c.setFont("Helvetica", 20)
    Text = "xx-xx-xx" # This is where the business sort code would go
    TextWidth = c.stringWidth(Text, "Helvetica", 20)
    TextX = CentreX + (BoxWidth - TextWidth) / 2
    TextY = TopY + (BoxHeight - 10) / 2
    c.drawString(TextX, TextY, Text)

    c.save()

    # The pdf is saved and returned to the email subroutine that called it
    return FileName