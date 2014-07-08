Roomsurfer
==========

Roomsurfer is a web application that allows University of Waterloo students to find rooms on campus to study in. The user can 
check what time a room is available at, or they can find all rooms that are available during a certain time interval.

It uses Flask, MongoDB and KnockoutJS as the stack. I don't think there will be any more major updates to this in the future, 
as I've gone through two major revisions already. The timeline was kinda like this:
- Original app, which actually loaded ALL of the data (the JSON file) into the user's browser and called it through there (I 
did not own a server or know anything about web-dev / back-end stuff, so yeah)
- Added MongoDB on my DigitalOcean server and made the app make calls to the DB
- Removed almost all reliance on jQuery for updating the DOM by switching to KnockoutJS (which is kickass!)

hope you enjoy.
