import dns.resolver


def get_server(host):
    answers = dns.resolver.query('_minecraft._tcp.' + host, 'SRV')
    
    answer = sorted(answers, key=lambda x: x.priority)[0]
    
    return '.'.join(answer.target.labels), answer.port
    
    