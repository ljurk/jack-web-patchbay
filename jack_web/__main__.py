from subprocess import check_output, CalledProcessError
from flask import Flask, render_template, render_template_string, request, redirect
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# add arguments to parser
parser = reqparse.RequestParser()
parser.add_argument('input',
                    type=str)
parser.add_argument('output',
                    type=str)
parser.add_argument('state',
                    type=str)

def getClients():
    try:
        clients = check_output(['jack_lsp', '-c', '-p']).decode('utf-8')
    except CalledProcessError:
        return []
    if not clients:
        return []


    # split output into sections
    data = clients.strip().split(',\n')

    # parse sections
    clientData = {}
    for section in data:
        name = ""
        port = ""
        connections = []
        for client in section.split('\n'):
            if client.startswith('\tproperties'):
                #properties
                prop = client.strip().replace("properties: ","").split(',')[0]
                if prop not in clientData[name]:
                    clientData[name][prop] = {}
                continue
            if client.startswith('   '):
                #connections
                connections.append(client.strip())
                continue
            name = client.split(':')[0]
            port = client.split(':')[1]
            if name not in clientData:
                clientData[name] = {}
        clientData[name][prop][port] = {}
        clientData[name][prop][port]['connections'] = connections

    return clientData


class Server(Resource):
    def get(self):
        return self.status()

    @staticmethod
    def status():
        status = ''
        try:
            status = check_output(["jack_control", "status"]).decode('utf-8')
        except CalledProcessError as err:
            status = str(err.output.decode('utf-8'))
        status = status.replace('--- status\n','').replace('\n','')
        return {'status': status}

class Clients(Resource):
    def get(self):
        return getClients()

    def post(self):
        print("POST")
        print(request.referrer)
        args = parser.parse_args()

        if args['state'] == 'connect':
            cmd = ['jack_connect']

        elif args['state'] == 'disconnect':
            cmd = ['jack_disconnect']

        cmd.append(args['input'])
        cmd.append(args['output'])
        print(cmd)
        check_output(cmd)
        return redirect(request.referrer)

api.add_resource(Clients, '/clients')
api.add_resource(Server, '/server')

@app.route('/', methods=['GET', 'POST'])
def getIndex():
    if Server.status()['status'] != 'started':
        return render_template_string("""Jack Server Status: {{ status }}
                                        </br>
                                        start Server to access patchbay""",
                                      status=Server.status()['status'])
    return render_template('index.html', clients=getClients())

def main():
    app.run(host='0.0.0.0', port="2323", debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="2323", debug=True)
