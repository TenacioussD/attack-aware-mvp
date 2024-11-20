# utils.py

#The reason for this file is to create functions for code 
# that will be repeated with the aim to follow DRY priciples


from datetime import datetime
from flask import flash, redirect, url_for

def convertBirthday(birthday_str, flash_category='signup'):
    """Converts birthday string to a date object. Returns None if conversion fails."""
    try:
        return datetime.strptime(birthday_str, '%Y-%m-%d').date()
    except ValueError:
        flash("Invalid birthday format. Please use YYYY-MM-DD", flash_category)
        return None
