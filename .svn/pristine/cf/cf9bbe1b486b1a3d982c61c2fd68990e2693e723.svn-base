from collections import OrderedDict

from engine.assets import asset


class single_proposal_percentage(OrderedDict):
    def __init__(self, *arg, **kwargs):
        super(single_proposal_percentage, self).__init__(*arg, **kwargs)
        assert self.check_data()

    def check_data(self):
        for k in self.keys():
            assert issubclass(type(k), asset)
        return True

    def add_proposal(self, asset_instance, percentage):
        if asset_instance not in self.keys():
            self[asset_instance] = percentage
        else:
            self[asset_instance] += percentage

    def __repr__(self):
        return super(single_proposal_percentage, self).__repr__()

    def __str__(self):
        return self.__repr__()


class proposal_percentage(OrderedDict):
    def __init__(self, *arg, **kwargs):
        super(proposal_percentage, self).__init__(*arg, **kwargs)
        assert self.check_data()

    def check_data(self):
        for k, v in self:
            v.check_data()
        return True

    def add_poposal(self, thedate, proposal):
        assert isinstance(proposal, single_proposal_percentage)
        if thedate in self.keys():
            raise ValueError('thedate {} is already in the proposal calendar'.format(thedate))
        else:
            self[thedate] = proposal

    def __repr__(self):
        return super(proposal_percentage, self).__repr__()

    def __str__(self):
        return self.__repr__()
