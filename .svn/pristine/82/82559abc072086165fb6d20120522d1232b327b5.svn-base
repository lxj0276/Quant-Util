from engine.env import CARLENDER_DAILY_TYPE


class carlender_daily(list):
    def __init__(self, *args, **kwargs):
        super(carlender_daily, self).__init__(*args, **kwargs)
        self.check_data_and_sort(allow_type=CARLENDER_DAILY_TYPE)

    def first_time(self):
        return self[0]

    def last_time(self):
        return self[-1]

    def count_time(self):
        return len(self)

    def to_list(self):
        pass

    def check_data_and_sort(self, allow_type):
        for v in self:
            assert isinstance(v, allow_type)
        assert set(self).__len__() == self.__len__(), 'carlender contain dupicates'
        sorted(self)

    def most_recent_up(self,thedate):
        flag=False
        for value in self:
            if value>=thedate:
                flag=True
                break
        return flag,value


    def most_recent_down(self,thedate):
        flag = False
        for idx,value in enumerate(self):
            if value>=thedate:
                flag = True
                break
        return flag,self[max(0,idx-1)]
