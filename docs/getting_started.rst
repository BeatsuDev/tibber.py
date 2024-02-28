Getting started
===============

############
Installation
############
tibber.py is available on PyPI. You can install it with pip:

.. code-block:: bash

   pip install tibber.py

#########################
Getting basic information
#########################

Getting the "Viewer" type (this is the topmost schema (or type) under Query on the Tibber API explorer
documentation). All your homes, subscriptions, etc. will be under here. 

.. code-block:: python

   import tibber

   account = tibber.Account("your token")  # This is just like the viewer type in the API explorer

Log in here: https://developer.tibber.com/explorer and check out the documentation on the right.
Click the yellow underlined text "Query", then "Viewer". The "account" variable above is essentially
the same as the Viewer type in the API explorer. It contains the same properties as the documentation
says that the Viewer has. So let's for example get the name of the Viewer!

.. code-block:: python

   print(account.name)

What about getting a home? Checking out the https://developer.tibber.com/explorer documentation, we
see that the Viewer type has a "homes" attribute and is surrounded by [brackets]. That means it comes
in the form of a list. Let's get the first home in the list!

.. code-block:: python

   print(account.homes)  # [<Home: Home 1>, <Home: Home 2>, ...]
   home = account.homes[0]
   print(home)  # <Home: Home 1>


#############################################
Retrieving consumption/production information
#############################################

Moving on from the previous example, what can we do with a home? Let's check out the documentation again.
Click the yellow underlined text "Home" and check out the documentation. We see that the Home type has a
"consumption" method! Let's try to call that method with some paramters and get the HomeConsumptionConnection type back!

.. code-block:: python

   consumption = home.fetch_consumption(resolution = "HOURLY", last = 24)  # last 24 hours
   print(consumption)  # <HomeConsumptionConnection: HomeConsumptionConnection>

Clicking the yellow underlined text "HomeConsumptionConnection" we see that it has a "nodes" attribute wich
has a list of consumptions. Within the Consumption type you have all the goodies such as total cost, unit price,
currency etc. Let's print the total cost of the last 24 hours!

.. code-block:: python

   running_total = 0
   for node in consumption.nodes:
      running_total += node.total_cost  # Note that the naming convention for the attributes is snake_case

   print(running_total)  # 123.45

Looking back at the documentation, we see that the HomeConsumptionConnection type also has a PageInfo type.
The PageInfo actually has a totalCost property that we can use instead of looping through all the nodes!
Here's how to achieve the same thing as above, but using the page info we have instead!

.. code-block:: python

   print(consumption.page_info.total_cost)  # 123.45

Getting production information is very similar to getting consumption information. The only difference is
that you use the "production" method instead of the "consumption" method. The rest is the same!

###########################
Sending a push notification
###########################
Sending a push notification is very simple. This sends a push notification
to all your devices that are logged in to the Tibber app with the same 
account as the one you have generated your access token with.

.. code-block:: python

   import tibber

   account = tibber.Account("your token")
   account.send_push_notification("My title", "Hello! I'm a message!")

#################
Live measurements
#################

To get live measurements, you first have to register callback functions
for the `live_measurement` event. This event is emitted every time a 
measurement has been made and has been retrieved from the API.

In simpler terms; in order to get live data, you need to create a function 
that you want to be run every time a live measurement is available. Then
you must "register" that function so that it actually runs every time 
a live measurement is available.

.. note::
   The live measurement may be delayed with a few seconds and is updated
   only every 2-10 seconds (in my experience).

.. code-block:: python

   import tibber

   account = tibber.Account("your token")
   home = account.homes[0]

   @home.event("live_measurement")  # register the following function to run when the live_measurement event is emitted
   async def process_data(data):  # Note the data parameter in the function. This is required and is of type LiveMeasurement.
      print(data.power)

   # Now start retrieving live measurements
   home.start_live_feed()

.. note::
   Any code after home.start_live_feed() will not run! This is because the
   start_live_feed() method is blocking. It will run forever and will only
   stop when stopped with Ctrl+C or when the interpreter closes.

To close the live feed after any condition, you can pass the exit_condition argument to
the start_live_feed() method. If the exit_condition function returns true, the live feed
will be stopped (and code execution will continue).

.. code-block:: python

   import tibber

   account = tibber.Account("your token")
   home = account.homes[0]

   @home.event("live_measurement")  # register the following function to run when the live_measurement event is emitted
   async def process_data(data):  # Note the data parameter in the function. This is required and is of type LiveMeasurement.
      print(data.power)

   # Now start retrieving live measurements
   home.start_live_feed(exit_condition = lambda: True)  # This will stop the live feed after the first measurement

.. code-block:: python
   
      import tibber
   
      account = tibber.Account("your token")
      home = account.homes[0]
   
      @home.event("live_measurement")  # register the following function to run when the live_measurement event is emitted
      async def process_data(data):  # Note the data parameter in the function. This is required and is of type LiveMeasurement.
         print(data.power)

      def my_exit_function(live_measurement_data):
         return live_measurement_data.power > 1000:
   
      # Now start retrieving live measurements
      home.start_live_feed(exit_condition = my_exit_function)  # This will stop the live feed when the power is above 1000
      print("We made it! The power is above 1000!")
