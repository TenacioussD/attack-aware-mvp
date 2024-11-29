# utils.py

#The reason for this file is to create functions for code 
# that will be repeated with the aim to follow DRY priciples


from datetime import datetime
from flask import flash, redirect, url_for, session
from models import user_interaction, db

def convertBirthday(birthday_str, flash_category='signup' or 'login'):
    """Converts birthday string to a date object. Returns None if conversion fails."""
    try:
        return datetime.strptime(birthday_str, '%Y-%m-%d').date()
    except ValueError:
        flash("Invalid birthday format. Please use YYYY-MM-DD", flash_category)
        return None

def commitUserInteraction(topic):
        
        #Commits user interaction data for a specific topic to the database.

        userId = session.get('userId')  # Ensure user ID is stored in session

        if userId:
           interaction = user_interaction.query.filter_by(userId=userId, topic = topic).first()
           if interaction:
              interaction.clickCount += 1 #this will add a count everytime the user interacts with this topic
           else:
            interaction = user_interaction(userId=userId, topic=topic)
            db.session.add(interaction)

            #commit changes
           db.session.commit()