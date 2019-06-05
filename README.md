# Flask Template
This repository contains a base flask application ready to go to spin up a new flask application.

By default it has built a built in scheduler to run tasks on a schedule which is powered by apscheduler.
It setup to utilize blueprints and holds all of the login/logout/registration routes in the base blueprint.
The thought process for this application was to utilize the base application for any site wide functions
such as the login/logouts.

This base flask application also utilizes Jinja for HTML rendering and WTForms for for generation and 
validation.

# Access Control

#### Overview
The methodology I used to control access for routes is role and group based. Roles
that are required to access various routes can be hardcoded or set by any means that 
the developer chooses. However any role that is used to restrict access to a route
MUST be stored in the 'Role' table of the database for the rest of the system to
be able to grant access.

These roles may be directly assigned to a user if one so chooses. This will allow
any single user of the system to be granted access any specific route and not 
have to worry about allowing any other unintended user access.

You may also assign roles to groups, any group that will be assigned a role needs
to be defined in the 'Group' table. This gives us the benefits of assigning a set
of roles to a defined group and then assigning a user to that group which will
then grant that user access to all of the routes that each of the attached roles
gives.

Each of these methodologies can be used independantly or in conjunction with the other.
However it is important to understand that weather a role is associated to a user
either directly or via a member group, that user will have access to the routes 
protected by that role.

#### Tests
The tests for this are located in tests/test_access/control