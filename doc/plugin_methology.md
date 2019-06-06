                                                Plugin Methodology
                                              Author: Kyle Kowalczyk
                                           Intended Audience: Developers

                                                 Overview
This document outlines the methodology of plugins for this system. A plugin in its basic form is a flask blueprint,
the key difference is instead of just implementing a blueprint via flasks standard implementation using the Blueprint
class a plugin will use the Plugin class which is located at app/plugins/Plugin.py

                                    Why use Plugin Class over Blueprint?
The Plugin class is what will hold data about the blueprint beyond what just the flask.Blueprint class needs to know.
This is mainly for things like route restriction and database modification scripts etc.




                                How to do common tasks when developing Blueprints


                                        Restricting access to routes
If your blueprint or parts of your blueprint need to restrict access. Plugins are supported to implement route
restriction in the following ways

Decorating Routes:
In the plugin blueprint you may restrict access to a single route by using the @blueprint.required_roles() decorator.
the required_roles decorator takes an unlimited amount of string arguments that correspond to the role names that
the user needs to be associated to for route restriction.

