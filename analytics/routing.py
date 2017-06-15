from channels.routing import route, route_class
from events.consumers import LogConsumer, EventConsumer

channel_routing = [
    # route('websocket.connect', ws_connect),
    # route('websocket.disconnect', ws_disconnect),
    #route_class(MusicConsumer, path=r'/music/')
    # MusicConsumer.as_route(path=r'/music/$'),
    LogConsumer.as_route(path=r'^/log/$'),
    EventConsumer.as_route(path=r'^/events/$')
]