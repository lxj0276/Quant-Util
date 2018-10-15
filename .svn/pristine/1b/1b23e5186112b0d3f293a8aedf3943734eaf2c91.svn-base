from engine.session import Session
from engine.utils import get_calendar

class Time_manager:
    def __init__(self, frequence='d', carlender=None):
        self.frequance = frequence
        self.carlender = carlender

    def set_current_time(self, thetime):
        self.check_time(thetime)
        self.current_time = thetime

    def get_current_time(self):
        if self.current_time is None:
            raise ValueError('current time is not initialized')
        return self.current_time

    def check_time(self, thetime):
        if not (self.carlender is None):
            if thetime not in self.carlender:
                raise ValueError('time not in carlenders')

    def set_carlender(self, carlender):
        self.carlender = carlender


class Time_manager_session(Session):
    def __init__(self, time_manager=None,start_time=None,end_time=None):
        if time_manager is None:
            self.time_manager = Time_manager(carlender=get_calendar(start_time,end_time))
        else:
            self.time_manager = time_manager
        super(Time_manager_session, self).__init__()

    def get_time(self):
        return self.time_manager.get_current_time()

    def set_time(self, current_time):
        self.time_manager.set_current_time(current_time)

    def get_calendar(self):
        return self.time_manager.carlender

#
# class flexible_time_manager_session(Time_manager_session):
#     def __init__(self,time_manager=None):
#         super(flexible_time_manager_session, self).__init__(time_manager)
#         if time_manager is None:
#             self.has_time_manager=False
#         else:
#             self.has_time_manager=True
#
#
#
