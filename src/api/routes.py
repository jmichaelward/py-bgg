from flask import jsonify
import main

app = main.get_app()
db = main.get_db()


@app.route('/api/v1/users', methods=['GET'])
def users():
    """
    Return a collection of users as a JSON object. This displays their username and BoardGameGeek user ID.
    """
    return jsonify(db.get_users())
