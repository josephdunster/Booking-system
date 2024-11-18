import smtplib
from email.message import EmailMessage
from RetrieveDataFromDatabase import GetValueFromTable, RetrieveColumn
from DateConversions import DateFormatToWords
from InvoiceGeneration import *

def CancelledByCustomerEmail(BookingID, CancellationReason):

    # The date of the event and start and end times are retrieved from the bookings table using the booking ID
    DateOfEvent = GetValueFromTable('Bookings', 6, BookingID)
    StartTime = GetValueFromTable('Bookings', 7, BookingID)
    EndTime = GetValueFromTable('Bookings', 8, BookingID)

    # The type of event is retrieved from the type of events table using the type of event ID
    # The type of event ID is retrieved from the bookings table using the booking ID
    TypeOfEvent = GetValueFromTable('TypeOfEvents', 1, GetValueFromTable('Bookings', 5, BookingID))

    # The customer's first name, surname and email address are retrieved from the customers table using the customer ID
    # The customer ID is retrieved from the bookings table using the booking ID
    CustomerFirstName = GetValueFromTable('Customers', 1, GetValueFromTable('Bookings', 3, BookingID))
    CustomerSurname = GetValueFromTable('Customers', 2, GetValueFromTable('Bookings', 3, BookingID))
    CustomerEmailAddress = GetValueFromTable('Customers', 3, GetValueFromTable('Bookings', 3, BookingID))

    # The type of event is changed to "Wedding" if it is any of the wedding packages
    if TypeOfEvent in ["Wedding1", "Wedding2", "Wedding3"]:
        TypeOfEvent = "Wedding"

    # A connection to the Gmail SMTP server is established using SSL
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=smtplib.ssl.create_default_context())

    # The sending email address is set and the password for this email address is set
    SendingEmailAddress = 'courseworkclient@gmail.com'
    SendingPassword = 'bttx oprp leez ctmt'

    # The SMTP server is logged into
    smtp.login(SendingEmailAddress, SendingPassword)

    # The sender and receiver of the email are set
    Message = EmailMessage()
    Message['From'] = SendingEmailAddress
    Message['To'] = CustomerEmailAddress

    # The email subject and content are set ensuring the correct name and cancellation reason are used
    Message['Subject'] = 'Cancelled booking'
    Message.set_content(f'''
Dear {CustomerFirstName},<br>
We are sorry to hear that you have cancelled your booking. The reason for this is that:<br><br>
<b>{CancellationReason}</b><br><br>
However, feel free to make another booking.<br><br>
Many Thanks,<br>
Mounton Brook Lodge
''', subtype='html')
    
    # The message is sent
    smtp.send_message(Message)

    # The connection to the Gmail SMTP server is closed
    smtp.quit()

    # The list of manager email address are retrieved from the database
    ManagerEmailAddresses = RetrieveColumn('EmailAddress', 'Managers')

    # For each manager email address:
    for EmailAddress in ManagerEmailAddresses:

        # A connection to the Gmail SMTP server is established using SSL
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=smtplib.ssl.create_default_context())

        # The sending email address is set and the password for this email address is set
        SendingEmailAddress = 'courseworkclient@gmail.com'
        SendingPassword = 'bttx oprp leez ctmt'

        # The SMTP server is logged into
        smtp.login(SendingEmailAddress, SendingPassword)

        # The sender and receiver of the email are set
        Message = EmailMessage()
        Message['From'] = SendingEmailAddress
        Message['To'] = EmailAddress

        # The email subject and content are set ensuring the correct names, event details and cancellation reason are used
        Message['Subject'] = 'Cancelled booking'
        Message.set_content(f'''
    {CustomerFirstName} {CustomerSurname} cancelled his booking.<br><br>
    <b>Type of event: {TypeOfEvent}<br>
    Date of event: {DateOfEvent}<br>
    Time of event: {StartTime} - {EndTime}</b><br><br>
    Reason for cancellation:<br><br>
    <b>{CancellationReason}</b>
    ''', subtype='html')
        
        # The message is sent
        smtp.send_message(Message)

        # The connection to the Gmail SMTP server is closed
        smtp.quit()

def CancelledByManagerEmail(BookingID, CancellationReason):

    # A connection to the Gmail SMTP server is established using SSL
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=smtplib.ssl.create_default_context())

    # The sending email address is set and the password for this email address is set
    SendingEmailAddress = 'courseworkclient@gmail.com'
    SendingPassword = 'bttx oprp leez ctmt'

    # The SMTP server is logged into
    smtp.login(SendingEmailAddress, SendingPassword)

    # The customer name and email address is retrieved from the customers table using the customer ID
    # The customer ID is retrieved from the Bookings table using the booking ID
    CustomerEmailAddress = GetValueFromTable('Customers', 3, GetValueFromTable('Bookings', 3, int(BookingID)))
    CustomerFirstName = GetValueFromTable('Customers', 1, GetValueFromTable('Bookings', 3, int(BookingID)))

    # The sender and receiver of the email are set
    Message = EmailMessage()
    Message['From'] = SendingEmailAddress
    Message['To'] = CustomerEmailAddress

    # The email subject and content are set ensuring the correct names, event details and cancellation reason are used
    Message['Subject'] = 'Cancelled booking'
    Message.set_content(f'''
Dear {CustomerFirstName},<br>
We are sorry to tell you that we have cancelled your booking. The reason for this is that:<br><br>
<b>{CancellationReason}</b><br><br>
However, feel free to make another booking.<br><br>
Many Thanks,<br>
Mounton Brook Lodge
''', subtype='html')
    
    # The message is sent
    smtp.send_message(Message)

    # The connection to the Gmail SMTP server is closed
    smtp.quit()

def BookingConfirmationEmail(BookingID):

    # The date of the event and start and end times are retrieved from the bookings table using the booking ID
    DateOfEvent = DateFormatToWords(GetValueFromTable('Bookings', 6, int(BookingID)))
    StartTime = GetValueFromTable('Bookings', 7, BookingID)
    EndTime = GetValueFromTable('Bookings', 8, BookingID)

    # The type of event is retrieved from the type of events table using the type of event ID
    # The type of event ID is retrieved from the bookings table using the booking ID
    TypeOfEvent = GetValueFromTable('TypeOfEvents', 1, GetValueFromTable('Bookings', 5, int(BookingID)))

    # The type of event is changed to "Wedding" if it is any of the wedding packages
    if TypeOfEvent in ["Wedding1", "Wedding2", "Wedding3"]:
        TypeOfEvent = "Wedding"

    # The customer's first name and email address are retrieved from the customers table using the customer ID
    # The customer ID is retrieved from the bookings table using the booking ID
    CustomerFirstName = GetValueFromTable('Customers', 1, GetValueFromTable('Bookings', 3, int(BookingID)))
    CustomerEmailAddress = GetValueFromTable('Customers', 3, GetValueFromTable('Bookings', 3, int(BookingID)))

    # The invoice for the booking is generated
    FileName = GenerateInvoice(BookingID)

    # A connection to the Gmail SMTP server is established using SSL
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=smtplib.ssl.create_default_context())

    # The sending email address is set and the password for this email address is set
    SendingEmailAddress = 'courseworkclient@gmail.com'
    SendingPassword = 'bttx oprp leez ctmt'

    # The SMTP server is logged into
    smtp.login(SendingEmailAddress, SendingPassword)

    # The sender and receiver of the email are set
    Message = EmailMessage()
    Message['From'] = SendingEmailAddress
    Message['To'] = CustomerEmailAddress

    # The email subject and content are set ensuring the correct names and event details are used
    Message['Subject'] = 'Booking confirmed'
    Message.set_content(f'''
Dear {CustomerFirstName},<br>
Your event has been booked!<br><br>
<b>Type of event: {TypeOfEvent}<br>
Date of event: {DateOfEvent}<br>
Time of event: {StartTime} - {EndTime}</b><br><br>
We look forward to seeing you!<br><br>
Many Thanks,<br>
Mounton Brook Lodge
''', subtype='html')

    # The invoice pdf is attached to the file
    with open(FileName, 'rb') as pdf_file:
        PDFData = pdf_file.read()
        Message.add_attachment(PDFData, maintype='application', subtype='pdf', filename=FileName)

    # The message is sent
    smtp.send_message(Message)

    # The connection to the Gmail SMTP server is closed
    smtp.quit()

def BookingRequestConfirmationEmail(BookingID):

    # The date of the event and start and end times are retrieved from the bookings table using the booking ID
    DateOfEvent = GetValueFromTable('Bookings', 6, BookingID)
    StartTime = GetValueFromTable('Bookings', 7, BookingID)
    EndTime = GetValueFromTable('Bookings', 8, BookingID)

    # The type of event is retrieved from the type of events table using the type of event ID
    # The type of event ID is retrieved from the bookings table using the booking ID
    TypeOfEvent = GetValueFromTable('TypeOfEvents', 1, GetValueFromTable('Bookings', 5, int(BookingID)))

    # The type of event is changed to "Wedding" if it is any of the wedding packages
    if TypeOfEvent in ["Wedding1", "Wedding2", "Wedding3"]:
        TypeOfEvent = "Wedding"

    # The customer's first name, surname and email address are retrieved from the customers table using the customer ID
    # The customer ID is retrieved from the bookings table using the booking ID
    CustomerFirstName = GetValueFromTable('Customers', 1, GetValueFromTable('Bookings', 3, int(BookingID)))
    CustomerSurname = GetValueFromTable('Customers', 2, GetValueFromTable('Bookings', 3, int(BookingID)))
    CustomerEmailAddress = GetValueFromTable('Customers', 3, GetValueFromTable('Bookings', 3, int(BookingID)))

    # A connection to the Gmail SMTP server is established using SSL
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=smtplib.ssl.create_default_context())

    # The sending email address is set and the password for this email address is set
    SendingEmailAddress = 'courseworkclient@gmail.com'
    SendingPassword = 'bttx oprp leez ctmt'

    # The SMTP server is logged into
    smtp.login(SendingEmailAddress, SendingPassword)

    # The sender and receiver of the email are set
    Message = EmailMessage()
    Message['From'] = SendingEmailAddress
    Message['To'] = CustomerEmailAddress

    # The email subject and content are set ensuring the correct names and event details are used
    Message['Subject'] = 'Booking request'
    Message.set_content(f'''
Dear {CustomerFirstName},<br>
Your booking request has been submitted.<br><br>
<b>Type of event: {TypeOfEvent}<br>
Date of event: {DateFormatToWords(DateOfEvent)}<br>
Time of event: {StartTime} - {EndTime}</b><br><br>
We will review your booking and email you within 7 days.<br><br>
Many Thanks,<br>
Mounton Brook Lodge
''', subtype='html')
    
    # The message is sent
    smtp.send_message(Message)

    # The connection to the Gmail SMTP server is closed
    smtp.quit()

    # The list of manager email address are retrieved from the database
    ManagerEmailAddresses = RetrieveColumn('EmailAddress', 'Managers')

    # For each manager email address:
    for EmailAddress in ManagerEmailAddresses:

        # A connection to the Gmail SMTP server is established using SSL
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=smtplib.ssl.create_default_context())

        # The sending email address is set and the password for this email address is set
        SendingEmailAddress = 'courseworkclient@gmail.com'
        SendingPassword = 'bttx oprp leez ctmt'

        # The SMTP server is logged into
        smtp.login(SendingEmailAddress, SendingPassword)

        # The sender and receiver of the email are set
        Message = EmailMessage()
        Message['From'] = SendingEmailAddress
        Message['To'] = EmailAddress

        # The email subject and content are set ensuring the correct names and event details are used
        Message['Subject'] = 'Booking request'
        Message.set_content(f'''
    {CustomerFirstName} {CustomerSurname} has submitted a booking request.<br><br>
    <b>Type of event: {TypeOfEvent}<br>
    Date of event: {DateOfEvent}<br>
    Time of event: {StartTime} - {EndTime}</b><br><br>
    Review the booking <u><font color="blue">here</font></u>.
    ''', subtype='html')
        
        # The message is sent
        smtp.send_message(Message)

        # The connection to the Gmail SMTP server is closed
        smtp.quit()

def BookingAcceptedEmail(BookingID):

    # The invoice for the booking is generated
    FileName = GenerateInvoice(BookingID)

    # The date of the event and start and end times are retrieved from the bookings table using the booking ID
    DateOfEvent = GetValueFromTable('Bookings', 6, int(BookingID))
    StartTime = GetValueFromTable('Bookings', 7, int(BookingID))
    EndTime = GetValueFromTable('Bookings', 8, int(BookingID))


    # The type of event is retrieved from the type of events table using the type of event ID
    # The type of event ID is retrieved from the bookings table using the booking ID
    TypeOfEvent = GetValueFromTable('TypeOfEvents', 1, GetValueFromTable('Bookings', 5, int(BookingID)))

    # The type of event is changed to "Wedding" if it is any of the wedding packages
    if TypeOfEvent in ["Wedding1", "Wedding2", "Wedding3"]:
        TypeOfEvent = "Wedding"


    # The customer's first name and email address are retrieved from the customers table using the customer ID
    # The customer ID is retrieved from the bookings table using the booking ID
    CustomerFirstName = GetValueFromTable('Customers', 1, GetValueFromTable('Bookings', 3, int(BookingID)))
    CustomerEmailAddress = GetValueFromTable('Customers', 3, GetValueFromTable('Bookings', 3, int(BookingID)))

    # A connection to the Gmail SMTP server is established using SSL
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=smtplib.ssl.create_default_context())

    # The sending email address is set and the password for this email address is set
    SendingEmailAddress = 'courseworkclient@gmail.com'
    SendingPassword = 'bttx oprp leez ctmt'

    # The SMTP server is logged into
    smtp.login(SendingEmailAddress, SendingPassword)

    # The sender and receiver of the email are set
    Message = EmailMessage()
    Message['From'] = SendingEmailAddress
    Message['To'] = CustomerEmailAddress

    # The email subject and content are set ensuring the correct names and event details are used
    Message['Subject'] = 'Accepted booking'
    Message.set_content(f'''
Dear {CustomerFirstName},<br>
Your booking has been accepted.<br><br>     
<b>Type of event: {TypeOfEvent}<br>
Date of event: {DateOfEvent}<br>
Time of event: {StartTime} - {EndTime}</b><br><br>
We look forward to seeing you!<br><br>
Many Thanks,<br>
Mounton Brook Lodge
''', subtype='html')
    
    # The invoice is attached
    with open(FileName, 'rb') as pdf_file:
        PDFData = pdf_file.read()
        Message.add_attachment(PDFData, maintype='application', subtype='pdf', filename=FileName)

    # The message is sent
    smtp.send_message(Message)

    # The connection to the Gmail SMTP server is closed
    smtp.quit()

def BookingRejectedEmail(BookingID, RejectedReason):

    # The customer's first name and email address are retrieved from the customers table using the customer ID
    # The customer ID is retrieved from the bookings table using the booking ID
    CustomerFirstName = GetValueFromTable('Customers', 1, GetValueFromTable('Bookings', 3, int(BookingID)))
    CustomerEmailAddress = GetValueFromTable('Customers', 3, GetValueFromTable('Bookings', 3, int(BookingID)))

    # A connection to the Gmail SMTP server is established using SSL
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=smtplib.ssl.create_default_context())

    # The sending email address is set and the password for this email address is set
    SendingEmailAddress = 'courseworkclient@gmail.com'
    SendingPassword = 'bttx oprp leez ctmt'

    # The SMTP server is logged into
    smtp.login(SendingEmailAddress, SendingPassword)

    # The sender and receiver of the email are set
    Message = EmailMessage()
    Message['From'] = SendingEmailAddress
    Message['To'] = CustomerEmailAddress

    # The email subject and content are set ensuring the correct names and rejection reason are used
    Message['Subject'] = 'Rejected Booking'
    Message.set_content(f'''
Dear {CustomerFirstName},<br>
We are sorry to tell you that your booking request has been rejected. The reason for this is that:<br><br>        
<b>{RejectedReason}</b><br><br>
Please feel free to make another booking.<br><br>
Many Thanks,<br>
Mounton Brook Lodge
''', subtype='html')
    
    # The message is sent
    smtp.send_message(Message)

    # The connection to the Gmail SMTP server is closed
    smtp.quit()