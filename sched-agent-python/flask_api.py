from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
from usage import main

app = Flask(__name__, template_folder='./templates',static_folder='./templates/static')
api = Api(app)

@app.route('/')
def hello_world():
    return render_template("index.html")

class Usage(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('image', type=str, required=True)
        parser.add_argument('cpus', type=int, required=True)  # add args
        parser.add_argument('gpus', type=int, required=True)
        parser.add_argument('memory', type=int, required=True)
        parser.add_argument('nodes', type=int, required=True)
        #parser.add_argument('cpusW', type=float, required=True)  # add args
        #parser.add_argument('gpusW', type=float, required=True)
        #parser.add_argument('memoryW', type=float, required=True)
        args = parser.parse_args()
        selected=main(args['name'], args['image'], args['cpus'], args['gpus'], args['memory'], args['nodes'])  #args['cpusW'], args['gpusW'], args['memoryW'])
        #args=request.args
        #args = args.to_dict()  # parse arguments to dictionary
        #print("\n Arguments = ",args)
        #data = {"node_name":"pakistan-node"}   # read local CSV
        #data = data.to_dict()
        return selected, 200  # return data and 200 OK

api.add_resource(Usage, '/usage', endpoint='usage')  # add endpoints

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # run our Flask app
