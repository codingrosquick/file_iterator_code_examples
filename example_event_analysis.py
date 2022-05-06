'''
--------------------------------------------------------------
                   Iterating over the files
--------------------------------------------------------------
This example file shows how to use the event analysis functions.
It shows how to find the events in 1 file, or for a collection of files.
Only detection of car crossings is implemented for the moment,
but you can add more event detections if you wish to find other situations.

NOTE: Be sure to have configured your cache and your irods environment before 
testing these functionnalities. You can do so by following the steps in README.md
--------------------------------------------------------------
'''

# ------------------ imports ------------------
import asyncio
from circles_file_iterator.utils.cache import init_cache
from circles_file_iterator.utils.event_analysis import find_all_events_car_crossing_one_file, find_all_events_car_crossing
from circles_file_iterator.utils.cyverse_io_irods import IRODSGet
from circles_file_iterator.global_variables.global_variables import local_temp_folder, local_long_folder
import pandas as pd

# ------------------ creating the async loop ------------------
'''
    -> AN IMPORTANT NOTE ON THE ASYNCHRONOUS BEHAVIOR:

we have to create an async loop and wait for its completion to be able to perform
an 'await' in the python script. See the link below for more information:
https://docs.python.org/3/library/asyncio-eventloop.html#running-and-stopping-the-loop
https://stackabuse.com/python-async-await-tutorial/, section 'Running the Event Loop'

In a server environment, you can just use those Get/Put inside of async functions, using await to wait
for their completion. You can see an example below

async def some_function():
    ....
    await IRODSGet(remote, local)
    ....
'''
loop = asyncio.get_event_loop()


# ======================= ANALYSE THE EVENTS IN A FILE =======================
'''
Here, we use the function `find_all_events_car_crossing_one_file` to find all
of the car crossing events in a given CAN CSV file.

The parameters used correponds to the conditions to find a car crossing.
- prev_treshold: The minimum distance with the lead vehicle prior to a car crossing
- next_treshold: When another car crosses in front of us, what is the maximum lead
    distance of this new vehicle that we want to take account for?
- speed_treshold: What is the minimum speed we consider for those events?
'''

print('\n------------------------ ANALYSE THE EVENTS IN A FILE ------------------------\n')

# We download a CAN CSV file for the example
remote_path_example_can_file = '/iplant/home/sprinkjm/publishable-circles/2T3H1RFV8LC057037/libpanda/2021_08_04/2021-08-04-14-08-38_2T3H1RFV8LC057037_CAN_Messages.csv'
local_address_example_can_file = loop.run_until_complete(IRODSGet(remote_address=remote_path_example_can_file, cache_address=local_temp_folder))

# We call this function to:
# - Find all examples of car crossing respecting the parameters
# - return the arrays of the different events found
# - plot the lead distance time series, with indicators (in red) of the times of the events found
# (Note: the plot part works in Jupyter Notebooks, not on Python Scripts)
event_times, event_cc_states, event_speeds, metadata = find_all_events_car_crossing_one_file(
    canfile=local_address_example_can_file,
    prev_treshold=50,
    next_treshold=40, 
    speed_treshold=20,
    verbose=True,
    plot=True, 
    plot_name='Car crossing events found in the example file')

# We can take a look at a few things from this function:
# - the events found:
#   - event_times: Times of the events found
#   - event_cc_states: if the speed controller was activated at the time of the event?
#   - event_speeds: Speed of the time of the event 
# NOTE: all of those array describing events found corresponds to each other at the same index
print(f'\nevent times: {event_times}')
print(f'\nevent speeds: {event_speeds}')
print(f'\nevent cc states: {event_cc_states}')

# The metadata also gives some information about the whole analysed run
print(f'The metadata gives: {metadata}')

# You can run the event detection with different parameters, and hence detect different types of situations
find_all_events_car_crossing_one_file(
    canfile=local_address_example_can_file,
    prev_treshold=30,
    next_treshold=10,
    speed_treshold=20,
    verbose=True)

print(f'\nnew event times: {event_times}')
print(f'\nnew event speeds: {event_speeds}')
print(f'\nnew event cc states: {event_cc_states}')
print(f'The metadata is still: {metadata}')


# ------------------ clear the cache ------------------

init_cache()


# ======================= ANALYSE THE EVENTS IN A COLLECTION OF FILES =======================
'''
Here, we demonstrate how to find car crossing events in a collection of CAN CSV
runs. It will iterate through a file exploration made with the file iterator.
For each file, it detects the events corresponding to the parameters given.
(those are the same for all the files in the collection).

You can also use the file iterator's exploration filters to find the events in
files corresponding to specific properties.
'''

print('\n------------------------ ANALYSE THE EVENTS IN A COLLECTION OF FILES ------------------------\n')

# We first download a file iteration
remote_path_collection_can_files = '/iplant/home/noecarras/resources_file_iterator/default/file_exploration&example_small_exploration_vandertest&create_on=2021-11-29_19_28_05.073947&root=_iplant_home_sprinkjm_publishable-circles_2T3W1RFVXKW033343_libpanda_2021_08_02.csv'
# We then instruct the code to find the events in a lot of different files
analysis_local_address = loop.run_until_complete(find_all_events_car_crossing(
    file_exploration_name=remote_path_collection_can_files,
    db_analysis_name='demo_analysis',
    speed_threshold=20,
    previous_distance_threshold=50,
    next_distance_threshold=40,
    verbose = True
))

# Once this function finished running, we have access to the CSV file of the event analysi
# in the variable ``analysis_local_address`` that gives its path.
analysis_done = pd.read_csv(analysis_local_address)
print(f'The columns in the analysis are: {analysis_done.columns}')
print(f'The shape of this analysis is: {analysis_done.shape}')
print(f'Here is an example line: {analysis_done.iloc[10,:]}')


# ------------------ clear the cache ------------------
init_cache()
init_cache(long=True)

# ------------------ close the async loop ------------------
loop.close()
