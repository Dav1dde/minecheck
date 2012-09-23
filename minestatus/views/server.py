from flask import Blueprint, jsonify

from minestatus.minecraft import serverlist

mod = Blueprint('server', __name__)


@mod.route('/ping/<host>/')
@mod.route('/ping/<host>/<int:port>/')
def ping(host, port=25565):
    errors = list()
    info = dict()
    
    try:
        info = serverlist.get_info(host, port, timeout=1)
    except IOError, e: # catches socket.error
        errors.append(e.strerror or e.message)
    except Exception, e:
        errors.append(e.message)
        
    info['success'] = len(errors) == 0
    info['errors'] = errors
    info['online'] = 'players' in info
    
    return jsonify(**info)
        
    
    