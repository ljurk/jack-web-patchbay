from subprocess import check_output, CalledProcessError, Popen
from flask import Flask, render_template, request, redirect
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# add arguments to parser
parser = reqparse.RequestParser()
parser.add_argument('input',
                    type=str,
                    help='number that will be displayed')
parser.add_argument('output',
                    type=str,
                    help='number that will be displayed')
parser.add_argument('state',
                    type=str,
                    help='number that will be displayed')





def parseSections(data):
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

def getClients():
    try:
        clients = check_output(['jack_lsp', '-c', '-p']).decode('utf-8')
    except CalledProcessError:
        return []
    if not clients:
        return []


    # split output into sections
    sections = clients.strip().split(',\n')

    return parseSections(sections)


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
        Popen(cmd)
        return redirect(request.referrer)

api.add_resource(Clients, '/')

@app.route('/ui', methods=['GET', 'POST'])
def getIndex():
    return render_template('index.html', clients=getClients())

if __name__ == '__main__':    app.run(host='0.0.0.0', port="2323", debug=True)
