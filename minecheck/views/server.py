from flask import Blueprint, jsonify, redirect as fredirect, request, abort

from dns.exception import DNSException
from dns.resolver import NXDOMAIN

from minecheck.minecraft import serverlist
from minecheck.minecraft import srv

mod = Blueprint('server', __name__)


@mod.route('/ping/<host>/')
@mod.route('/ping/<host>/<int:port>/')
def ping(host, port=None):
    return jsonify(**_ping(host, port))

def _ping(host, port=None):
    errors = list()
    info = dict()
    
    if port is None:
        port = 25565
        
        try:
            host, port = srv.get_server(host)
        except NXDOMAIN:
            errors.append('Non-existent Internet Domain')
        except DNSException, e:
            errors.append(str(e))

    try:
        info = serverlist.get_info(host, port, timeout=1)
    except IOError, e: # catches socket.error
        errors.append(e.strerror or e.message)
    except Exception, e:
        errors.append(e.message)
    
    info['host'] = host
    info['port'] = port
    info['success'] = len(errors) == 0
    info['errors'] = errors
    info['online'] = 'players' in info
    
    return info
        

@mod.route('/redirect/<host>/')
@mod.route('/redirect/<host>/<int:port>')
def redirect(host, port=None):
    if 'green' in request.args and 'red' in request.args:
        if _ping(host, port)['online']:
            return fredirect(request.args['green'])
        else:
            return fredirect(request.args['red'])

    return abort(400)
    