from subprocess import check_output
from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)



def getClients():
    try:
        clients = check_output(['jack_lsp', '-p']).decode('utf-8')
    except subprocess.CalledProcessError:
        return []
    if not clients:
        return []

    clientData = {}

    clients = clients.replace('\n\tproperties', '')
    for client in clients.split('\n'):
        data = client.split(':')
        if len(data) < 2:
            continue
        name = data[0]
        port = data[1]
        properties = data[2].strip().split(',')[0]
        if name not in clientData:
            clientData[name] = {}
        if properties not in clientData[name]:
            clientData[name][properties] = []
        clientData[name][properties].append(port)

    return clientData

class Clients(Resource):
    def get(self):
        return self.getClients()


@app.route('/ui', methods=['GET', 'POST'])
def getIndex():
    print(getClients())
    return render_template('index.html', clients=getClients())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="2323", debug=True)
