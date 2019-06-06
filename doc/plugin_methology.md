# Plugin Methodology
Author: Kyle Kowalczyk
Intended Audience: Developers

# Overview
This document outlines the methodology of plugins for this system. A plugin in its basic form is a flask blueprint,
the key difference is instead of just implementing a blueprint via flasks standard implementation using the Blueprint
class a plugin will use the Plugin class which is located at app/plugins/Plugin.py

# Why use Plugin Class over Blueprint?
The Plugin class is what will hold data about the blueprint beyond what just the flask.Blueprint class needs to know.
This is mainly for things like route restriction and database modification scripts etc.



# Guidelines for creating plugins
Each plugin must have an entrypoint in the __init__.py file that defines a plugin variable similar to below
```python
from app.plugins.Plugin import Plugin

plugin = Plugin(
    name='test_blueprint',
    import_name=__name__,
    url_prefix='/test',
    template_folder='templates',
    static_folder='static',
    access_roles=['test1', 'test2', 'test3']
)
```
This will allow the system to find the plugin and create it properly. 

Each plugin must also have a routes.py file which contains an import for the plugin variable and contain the routes
for the blueprint. If it does not directly contain the routes associated to the plugin it must at least import all of 
the routes in the blueprint. This will make sure the routes are loaded into the application properly



# How to do common tasks when developing Blueprints


### Restricting access to routes
If your blueprint or parts of your blueprint need to restrict access. Plugins are supported to implement route
restriction in the following ways

### Decorating Routes
In the plugin blueprint you may restrict access to a single route by using the @plugin.required_roles() decorator.
the required_roles decorator takes an unlimited amount of string arguments that correspond to the role names that
the user needs to be associated to for route restriction.

### Internal Implementation:
The Plugin class also presents a way for the developer to implement a more general way of internal authentication by
presenting the current_user_has_roles() method. This method returns true if the user attempting to access a route is 
associated with any of the roles that you pass into it. It takes an unlimited number of standard string arguments. 
This allows you to decorate a function with @plugin.before_request so before every request that routes to this blueprint your
function runs and inside that function you can implement your access control by calling plugin.current_user_has_roles()
which will give you True False if the user has or does not have an association to that role.


# Things to avoid when writing a plugin

### Relying on non supported interfaces with the rest of the application
DO NOT rely on the base application for anything other than the Plugin class! Other than relying on the Plugin class 
you should not be importing anything else from this package, the Plugin class should provide you with what you
need to integrate your plugin, if not submit a feature request.

If you do start importing things from other parts of the application, after an update your entire plugin may break,
the Plugin classes api will undergo much less changes and of those changes, there will be less that break 
backwards compatibility.
