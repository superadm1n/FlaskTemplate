# Flask Template
This repository contains a base flask application ready to go to spin up a new flask application.

By default it has built a built in scheduler to run tasks on a schedule which is powered by apscheduler.
It setup to utilize blueprints and holds all of the login/logout/registration routes in the base blueprint.
The thought process for this application was to utilize the base application for any site wide functions
such as the login/logouts.

This base flask application also utilizes Jinja for HTML rendering and WTForms for for generation and 
validation.