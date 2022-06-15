Examples
========

###########################
Sending a push notification
###########################
Sending a push notification is very simple. This sends a push notification
to all your devices that are logged in to the Tibber app with the same 
account as the one you have generated your access token with.

.. code-block:: python

   import tibber

   client = tibber.Client("your token")
   client.send_push_notification("My title", "Hello! I'm a message!")

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

   client = tibber.Client("your token")
   home = client.homes[0]

   @home.event("live_measurement")  # register the following function to run when the live_measurement event is emitted
   def process_data(data):  # Note the data argument in the function. This is required and is of type LiveMeasurement.
      print(data.power)

   # Now start retrieving live measurements
   home.start_livefeed()