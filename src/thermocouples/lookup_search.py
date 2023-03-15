# https://github.com/2dof/esp_control
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
# __version__   = "1.0.0"


def idx_search(arr,low,high, x):
    mid = 0
 
    while low <= high:
 
        mid = (high + low) // 2
        
        if (mid+1) >= len(arr):
            return mid-1
        
        if (x >= arr[mid]) & (x <= arr[mid+1]):
            return mid
 
        # If x is greater, ignore left half
        if arr[mid] < x:
            low = mid + 1
 
        # If x is smaller, ignore right half
        elif arr[mid] > x:
            high = mid - 1
 
    return -1

def bytes_search(arr,low,high, x):
   
    mid = 0
    while low <= high:
 
       mid = (high + low) // 2
       i=2*mid
       v1=int.from_bytes(arr[i:(i+2)], 'little') #arr[mid]
       v2 = int.from_bytes(arr[(i+2):(i+4)], 'little')# arr[mid+1]
       
       if (mid+2) >= len(arr):
            
            return mid-1
        
       if (x >= v1) & (x <= v2):
            return mid
 
       if v1 < x:
            low = mid + 1

       elif v1 > x:
            high = mid - 1
 
    return -1