import os
from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.debug = True

app.config["MONGODB_SETTINGS"] = {'DB': "csps", "host":'mongodb://csps:iddqd1@kahana.mongohq.com:10006/app28781290'}
db = MongoEngine(app)

@app.route('/')
def hello():
    return 'hellllo'

if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)