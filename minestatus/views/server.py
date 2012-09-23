from flask import Blueprint, jsonify, send_from_directory, redirect, request, abort

from dns.exception import DNSException
from dns.resolver import NXDOMAIN

from minestatus.minecraft import serverlist
from minestatus.minecraft import srv

mod = Blueprint('server', __name__)


@mod.route('/ping/<host>/')
@mod.route('/ping/<host>/<int:port>/')
def ping(host, port=None):
    return jsonify(**_ping(host, port))

def _ping(host, port=None):
    errors = list()
    info = dict()
    cont = True
    
    if port is None:
        port = 25565
        
        try:
            host, port = srv.get_server(host)
        except NXDOMAIN:
            errors.append('Non-existent Internet Domain')
            cont = False
        except DNSException, e:
            errors.append(str(e))

    if cont:
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
            return redirect(request.args['green'])
        else:
            return redirect(request.args['red'])
    else:
        return abort(400)
    