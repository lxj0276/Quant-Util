from engine.assets import asset, cash, stock
from engine.cons import *
from engine.position import position


class order:
    def __init__(self, asset_instance, order_volume, direction_flag):
        assert issubclass(asset_instance.asset_type, asset)
        assert direction_flag in DIRECTIONS
        self._asset_instance = asset_instance
        self._asset_type = asset_instance.asset_type
        self._direction_flag = direction_flag
        self._order_volume = order_volume

    @property
    def asset_type(self):
        return self._asset_type

    @property
    def direction_flag(self):
        return self._direction_flag

    @property
    def order_volume(self):
        return self._order_volume

    @order_volume.setter
    def order_volme(self, order_volume):
        assert order_volume > 0
        self._order_volume = order_volume

    @property
    def asset_instance(self):
        return self._asset_instance

    def __repr__(self):
        return 'Asset :{} ,amount {} flag {}'.format(self.asset_instance, self.order_volme, self.direction_flag)


def generate_orders_from_positions(older_position, new_position):
    orders = []
    for asset_instance, amount in older_position.items():
        if isinstance(asset_instance, cash): continue
        if asset_instance not in new_position.keys():
            orders.append(order(asset_instance, older_position[asset_instance], ASK))
        elif older_position[asset_instance] > new_position[asset_instance]:
            orders.append(order(asset_instance, older_position[asset_instance] - new_position[asset_instance], ASK))
        elif older_position[asset_instance] < new_position[asset_instance]:
            orders.append(order(asset_instance, new_position[asset_instance] - older_position[asset_instance], BID))
    for asset_instance, amount in new_position.items():
        if isinstance(asset_instance, cash): continue
        if asset_instance not in older_position.keys():
            orders.append(order(asset_instance, amount, BID))
    orders = sorted(orders, key=lambda x: x.direction_flag)
    return orders

