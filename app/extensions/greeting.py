from datetime import datetime

def greeting():
    """This function checks current time to render approriate greeting"""
    current_Time = datetime.now()
    greeting = ''
    if current_Time.hour < 12:
        greeting = "Good morning, "
    elif 12 <= current_Time.hour < 18:
        greeting = "Good afternoon, "
    else:
        greeting = "Good evening, "
    
    return greeting