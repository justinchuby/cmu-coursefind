# @file coursecat.py
# @brief Contains the Event, Course etc. classes.
# @author Justin Chu (justinchuby@cmu.edu)


import re
import datetime
import string
try:
    from utilities import *
except:
    from .utilities import *


##
## @brief      A list that contains the events.
##
class EventList(list):
    def __init__(self, L=None):
        if L is None:
            L = []
        super().__init__(L)
        self.past = []
        self.current = []
        self.future = []
        self.rest = []
        self.laterToday = []
        self.len = 0
        self.ready()

    ##
    ## @brief      Places the course objects into different lists.
    ##
    ## @param      self             Self
    ## @param      currentDatetime  (datetime.datetime)  Specify the current
    ##                              date and time
    ## @param      timeDelta        (int)  the time to define 'future' events
    ##
    ## @return     None
    ##
    def ready(self, current_datetime=None, time_delta=60):
        self.len = self.__len__()
        self.past = []
        self.current = []
        self.future = []
        self.rest = []
        self.laterToday = []
        _dateTime = datetime.datetime(2015,1,1)

        if not isinstance(current_datetime, datetime.datetime):
            current_datetime = datetime.datetime.now()
        currentTime = current_datetime.time()
        currentDay = str(current_datetime.weekday())

        for event in self:

            # add attribute to event for diaplay
            event.days_text = getDaysText(event.days)
            event.building_text = getBuildingText(event.building)
            event.department = getCourseDepartment(event.number_searchable)

            if currentDay in event.days_searchable:
                # ended event
                if event.endTime < currentTime:
                    event.diffText = "{}:{}".format(event.beginTime.hour, event.beginTime.minute)
                    self.past.append(event)
                # current event
                elif event.beginTime < currentTime < event.endTime:
                    diff = getTimeDifference(event, "current", current_datetime)
                    _time = _dateTime + diff
                    if diff.seconds <= 3600:
                        event.diffText = "Ends in {} minutes".format(_time.minute)
                    else:
                        event.diffText = "Ends in {} h {} minutes".format(_time.hour, _time.minute)
                    self.current.append(event)
                # future event (in time_delta minutes)
                elif (event.beginTime > currentTime and
                        event.intBeginTime < inMinutes(currentTime) + time_delta):
                    diff = getTimeDifference(event, "future", current_datetime)
                    _time = _dateTime + diff
                    if diff.seconds <= 3600:
                        event.diffText = "Begins in {} minutes".format(_time.minute)
                    else:
                        event.diffText = "Begins in {} h {} minutes".format(_time.hour, _time.minute)
                    self.future.append(event)
                # other
                else:
                    event.diffText = "{}:{}".format(event.beginTime.hour, event.beginTime.minute)
                    self.laterToday.append(event)
            else:
                event.diffText = event.days_text
                self.rest.append(event)


    def sortByTime(self, current_datetime=None):
        self.ready(current_datetime)
        return self.current + self.future + self.laterToday + self.past + self.rest


