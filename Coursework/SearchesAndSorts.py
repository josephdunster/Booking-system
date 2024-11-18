import sqlite3

def FindRecordFromTable(Table, SearchValue, ColumnToSearch):

    # A connection to the database is established
    connection = sqlite3.connect('System.db')
    cursor = connection.cursor()

    # The entire of the required table is retrieved and stored in an array
    cursor.execute(f'SELECT * FROM {Table}')
    Array = cursor.fetchall()

    # The database connection is closed
    connection.commit()
    connection.close()

    # The array is looped through until the value at the column that is being searched matches the search value
    for i in range(len(Array)):
        if Array[i][ColumnToSearch] == SearchValue:
            # The index of the array containing the search value is returned
            return i
        
    # If the search value is not found, false is returned
    return False

def BinarySearch(Array, SearchValue):

    # The low and high indexes are initialised
    Low = 0
    High = len(Array)-1

    # The search continues until the value of low is less than or equal to the value of high
    while Low <= High:

        # The mmiddle index is calculated
        Mid = (Low + High) // 2

        # If the middle element is equal to the search value, the index is returned
        if Array[Mid] == SearchValue:
            return Mid
        
        # If the middle element is greater than the search value, high is set to the index above the middle value
        elif Array[Mid] > SearchValue:
            High = Mid - 1

        # If the middle element is less than the search value, low is set to the index below the middle value
        else:
            Low = Mid + 1

    # if the search value is not found, false is returned
    return False

def LinearSearch(Array, SearchValue):

    # Iterates through each element in the array
    for i in range(len(Array)):

        # If the element being searched matches the search value, the index of the element is returned
        if Array[i] == SearchValue:
            return i
        
    # If the element is not found, false is returned
    return False

def TwoDimensionalLinearSearch(Array, ColumnToSearch, SearchValue):

    # Iterates through each element in the array
    for i in range(len(Array)):

        # If the element being searched matches the search value, the index of the element is returned
        if Array[i][ColumnToSearch] == str(SearchValue):
            return i
        
    # If the element is not found, false is returned
    return False

def PartitionAscending(Array, Low, High, SortingColumn):

    # The pivot element is selected from the array
    Pivot = Array[Low][SortingColumn]
    Left = Low + 1
    Right = High

    # Loops until the left index is greater than the right index
    while True:

        # Move from the left index to the right index until an element greater than the pivot is found
        while Left <= Right and Array[Left][SortingColumn] <= Pivot:
            Left += 1

        # Move from the right index to the left index until an element less than or equal to the pivot is found
        while Right >= Left and Array[Right][SortingColumn] > Pivot:
            Right -= 1

        # If the left index is greater than the right index, break from the loop
        if Left > Right:
            break

        # Otherwise, the elements at the left and right indexes will be swapped
        else:
            Array[Left], Array[Right] = Array[Right], Array[Left]

    # The pivot element and the right index element are swapped
    Array[Low], Array[Right] = Array[Right], Array[Low]

    # The new pivot position is returned
    return Right

def PartitionDescending(Array, Low, High, SortingColumn):

    # The pivot element is selceted from the array
    Pivot = Array[Low][SortingColumn]
    Left = Low + 1
    Right = High
    
    # Loops until the left index is greater than the right index
    while True:

        # Move from the left index to the right index until an element less than the pivot is found
        while Left <= Right and Array[Left][SortingColumn] >= Pivot:
            Left += 1

        # Move from the right index to the left index until an element greated than or equal to the pivot is found
        while Right >= Left and Array[Right][SortingColumn] < Pivot:
            Right -= 1

        # If the left index is greater than the right index, break from the loop
        if Left > Right:
            break

        # Otherwise, the elements at the left and right indexes will be swapped
        else:
            Array[Left], Array[Right] = Array[Right], Array[Left]

    # The pivot element and the right index element are swapped
    Array[Low], Array[Right] = Array[Right], Array[Low]

    # The new pivot position is returned
    return Right

def QuickSortAscending(Array, Low, High, SortingColumn):

    if Low < High:

        # The pivot index is found
        Pivot = PartitionAscending(Array, Low, High, SortingColumn)

        # Sub arrays from the right and left side of the pivot are recursively sorted
        QuickSortAscending(Array, Low, Pivot-1, SortingColumn)
        QuickSortAscending(Array, Pivot+1, High, SortingColumn)

    # The sorted array is returned
    return Array

def QuickSortDescending(Array, Low, High, SortingColumn):

    if Low < High:

        # The pivot index is found
        Pivot = PartitionDescending(Array, Low, High, SortingColumn)

        # Sub arrays from the right and left side of the pivot are recursively sorted
        QuickSortDescending(Array, Low, Pivot-1, SortingColumn)
        QuickSortDescending(Array, Pivot+1, High, SortingColumn)

    return Array