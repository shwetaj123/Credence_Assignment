from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine
app = Flask(__name__)


database_name = "Hollywood"
password = "Test123"
DB_URI = "mongodb+srv://Test:{}@pythoncluster.ymkyh.mongodb.net/{}?retryWrites=true&w=majority".format(password, database_name)
app.config['MONGODB_HOST'] = DB_URI

db = MongoEngine()
db.init_app(app)

class Series(db.Document):
    Name = db.StringField()
    Image = db.StringField()
    Summary = db.StringField()

    def to_json(self):
        return{
            "Name": self.Name,
            "Image" : self.Image,
            "Summary" : self.Summary
        }


@app.route('/Hollywood/Add_Entries', methods=['POST'])
def Add_Entries():
    series1 = Series(Name="Harry Potter and the Order of the Phoenix",
                 Image="https://bit.ly/2IcnSwz",
                 Summary="Harry Potter and Dumbledore's warning about the return of Lord Voldemort is not heeded by the wizard authorities who, in turn, look to undermine Dumbledore's authority at Hogwarts and discredit Harry"
                 )
    series2 = Series(Name="The Lord of the Rings: The Fellowship of the Ring",
                 Image="https://bit.ly/2tC1Lcg",
                 Summary="A young hobbit, Frodo, who has found the One Ring that belongs to the Dark Lord Sauron, begins his journey with eight companions to Mount Doom, the only place where it can be destroyed."
                 )
    series3 = Series(Name="Avengers: Endgame",
                 Image="https://bit.ly/2Pzczlb",
                 Summary="Adrift in space with no food or water, Tony Stark sends a message to Pepper Potts as his oxygen supply starts to dwindle. Meanwhile, the remaining Avengers -- Thor, Black Widow, Captain America, and Bruce Banner --"
                 )

    series1.save()
    series2.save()
    series3.save()
    return make_response('', 201)


@app.route('/Hollywood/get_Series', methods=['GET','POST'])
def get_series():
    if request.method == "GET":
        series_list =[]
        for series in Series.objects:
            series_list.append(series)
        return make_response(jsonify(series_list), 200)
    elif request.method == "POST":
        content = request.json
        series = Series(Name=content['Name'],
                        Image=content['Image'],
                        Summary=content['Summary'])
        series.save()
        return make_response("", 201)


@app.route('/Hollywood/get_Series/<Name>', methods=['GET', 'PUT', 'DELETE'])
def operation_perform(Name):
    if request.method == 'GET':
        series_obj = Series.objects(Name=Name).first()
        if series_obj:
            return make_response(jsonify(series_obj.to_json()), 200)
        else:
            return make_response("", 404)
    elif request.method == 'PUT':
        content = request.json
        series_obj = Series.objects(Name=Name).first()
        series_obj.update(Summary=content['Summary'])
        return make_response((""), 204)
    elif request.method == 'DELETE':
        series_obj = Series.objects(Name=Name).first()
        series_obj.delete()
        return make_response((""), 204)

if __name__== "__main__":
    app.run(debug=True)