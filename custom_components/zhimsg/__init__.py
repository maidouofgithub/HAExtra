
# Logging
import logging
_LOGGER = logging.getLogger(__name__)

DOMAIN = 'zhimsg'
_handlers = {}


async def async_setup(hass, config):
    _confs = config.get(DOMAIN)
    if _confs:
        import importlib
        global _handlers
        for conf in _confs:
            service = conf['platform']
            handler = service.split('_')[0] + 'msg'
            mod = importlib.import_module('.' + handler, __package__)
            _handlers[service] = getattr(mod, handler)(hass, conf)
            SERVICE_SCHEMA = getattr(mod, 'SERVICE_SCHEMA')
            hass.services.async_register(
                DOMAIN, service, async_send, schema=SERVICE_SCHEMA)
            _LOGGER.debug("Register service: %s.%s", DOMAIN, service)
    return True


async def async_send(call):
    handler = _handlers[call.service]
    data = call.data
    message = data.get('message')
    await handler.async_send_message(message, data)
