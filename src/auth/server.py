import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)

#conifg
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_PORT"] = os.environ.get("MYSQL_HOST")


app.route('/login', method=["POST"])
def login():
    auth = request.authorization()
    if not auth:
        return "Missing credentials", 401
    
    #check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        f"SELECT email, password FROM user WHERE email={auth.username}"
    )
    if res > 0 :
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.passord != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid creadentials", 401

def createJWT(username, secret, authz):
    return jwt.encode(
        {
        'username':username,
        'exp': datetime.datetime.now(tz =datetime.timezone.utc) + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        "admin": authz
        },
        secret,
        algoritmz = "HS256"
    )

app.route('/validate', method=["POST"])
def validateJWT():
    encoded_jwt = request.headers['Authorization']

    if not encoded_jwt:
        return "missing creadentials", 401 

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt,
            os.environ.get("JWT_SECRET"), algorithm=["HS256"]
        )
        return decoded, 200
    except:
        return "not authorized", 403
    


if __name__ == "__main__":
    """
    since the docker container changes its ip when rebooting, so that
    we should use a global ip on my flask so that my flask port can access all ports
    so that port id is 0.0.0.0
    """
    app.run(host="0.0.0.0", port=5000) 