import os
import secrets

from PIL import Image
from flask import url_for, current_app
from flask_mail import Message



def convert_events(raw_events_from_db):
    
    converted_event_data = []

    class converted_event(dict):
        def __init__ (self, title, start, end, url):
            dict.__init__(self, title = title, start = start, end = end, url=url)
    
    for event in raw_events_from_db:
        start_date = event.start_date.strftime("%Y-%m-%d")
        end_date = event.end_date.strftime("%Y-%m-%d")
        
        event_id = event.id
        url = url_for('posts.view_post', post_id=event_id)

        converted_event_data.append(converted_event( title=event.title, start=start_date, end=end_date, url=url))
    
    return converted_event_data
