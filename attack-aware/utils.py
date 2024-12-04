# utils.py

#The reason for this file is to create functions for code 
# that will be repeated with the aim to follow DRY priciples


from datetime import datetime
from flask import flash, redirect, url_for, session, Flask
from models import user_interaction, db


def convertBirthday(birthday_str, flash_category='signup' or 'login'):
    """Converts birthday string to a date object. Returns None if conversion fails."""
    try:
        return datetime.strptime(birthday_str, '%Y-%m-%d').date()
    except ValueError:
        flash("Invalid birthday format. Please use YYYY-MM-DD", flash_category)
        return None
    
    #used to count how many times commitUserInteraction(topic) is used
    #will determine topic amounts
countUserInteractFunc = 0

def commitUserInteraction(topic):
        
        global countUserInteractFunc
        countUserInteractFunc += 1

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
        return countUserInteractFunc


#we don't have a database for our threats topics
#I'm mapping the topics images to use for the 
# profile page for User's Favorite Topics
topicImage = {
    "Ransomware": "static/img/Ransomware.png",
    "Social Engineering": "static/img/Social_Engineering.png",
    "Cyber Hygiene": "static/img/Cyber_Hygiene.png",
    "IoT": "static,img/IoT.png",
    "Phishing Scams": "static/img/Phishing.png"
}

#I'll also be feeding the start of each Topic 
# description to use in User's Favorite Topics

topicGraph = {
    "Ransomware": "Ransomware is a type of malicious software designed to block access to a computer system...",
    "Social Engineering": "...attacks manipulate people into sharing information that they shouldn’t share...",
    "Cyber Hygiene": "...essential if you want to keep yourself protected...",
    "IoT": "IoT (Internet of Things) device hacking refers to exploiting vulnerabilities in internet-connected devices...",
    "Phishing Scams": "...a technique used by hackers to trick people into giving personal details or taking an action..."
}

    

