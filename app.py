from flask import Flask, jsonify
from flask_cors import CORS

# initialize a flask application (app)
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

# ... your existing Flask

# add an api endpoint to flask app
@app.route('/api/vincent')
def get_vincent():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Vincent",
        "LastName": "Herranen",
        "DOB": "Novemeber 29",
        "Residence": "San Diego",
        "Email": "vincent.herranen@gmail.com",
        "Owns_Cars": ["2015-Fusion", "2011-Ranger", "2003-Excursion", "1997-F350", "1969-Cadillac"]
    })    
    return jsonify(InfoDb)

@app.route('/api/manahil')
def get_manahil():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Manahil",
        "LastName": "Khan",
        "DOB": "May 27",
        "Residence": "San Diego",
        "Email": "manahilkhan2708@gmail.com",
        "Owns_Cars": ["2015-Fusion", "2011-Ranger", "2003-Excursion", "1997-F350", "1969-Cadillac"]
    })    
    return jsonify(InfoDb)

@app.route('/api/shriya')
def get_shriya():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Shriya",
        "LastName": "Shah",
        "DOB": "July 10",
        "Residence": "San Diego",
        "Email": "shriya.s.shah@gmail.com",
        "Owns_Cars": ["2015-Fusion", "2011-Ranger", "2003-Excursion", "1997-F350", "1969-Cadillac"]
    })    
    return jsonify(InfoDb)

@app.route('/api/justin')
def get_justin():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Justin",
        "LastName": "Quach",
        "DOB": "January 1",
        "Residence": "San Diego",
        "Email": "justinquach@gmail.com",
        "Owns_Cars": ["2015-Fusion", "2011-Ranger", "2003-Excursion", "1997-F350", "1969-Cadillac"]
    })    
    return jsonify(InfoDb)

@app.route('/api/lars')
def get_lars():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Lars",
        "LastName": "Lindain",
        "DOB": "July 4",
        "Residence": "San Diego",
        "Email": "andre.lindain@gmail.com",
        "Owns_Cars": ["2015-Fusion", "2011-Ranger", "2003-Excursion", "1997-F350", "1969-Cadillac"]
    })    
    return jsonify(InfoDb)

@app.route('/api/shaurya')
def get_shaurya():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Shaurya",
        "LastName": "Singh",
        "DOB": "November 18",
        "Residence": "San Diego",
        "Email": "akanchasingh08gmail.com",
        "Owns_Cars": ["2015-Fusion", "2011-Ranger", "2003-Excursion", "1997-F350", "1969-Cadillac"]
    })    
    return jsonify(InfoDb) 

@app.route('/api/rutvik')
def get_rutvik():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Rutvik",
        "LastName": "Chavda",
        "DOB": "June 30",
        "Residence": "San Diego",
        "Email": "rchavda2009@gmail.com",
        "Owns_Cars": ["2015-Fusion", "2011-Ranger", "2003-Excursion", "1997-F350", "1969-Cadillac"]
    })    
    return jsonify(InfoDb) 

@app.route('/api/weston')
def get_weston():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Weston",
        "LastName": "Gardner",
        "DOB": "October 2",
        "Residence": "San Diego",
        "Email": "westonrgardner@gmail.com",
        "Owns_Cars": ["2008 Jeep Wrangler"]
    })    
    return jsonify(InfoDb)

# add an HTML endpoint to flask app
@app.route('/')
def say_hello():
    html_content = """
    <html>
    <head>
        <title>Hellox</title>
    </head>
    <body>
        <h2>Hello, World!</h2>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    # starts flask server on default port, http://127.0.0.1:5001
    app.run(port=5001)