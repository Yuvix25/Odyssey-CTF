import os
import json
import requests
from flask import Flask, render_template, request, abort, Response
from flask_cors import CORS, cross_origin
from utils import *
from sqlite_intergration import *

app = Flask(__name__)
CORS(app)
db = Database()



def check_level_privileges(level, request):
    cookies = request.cookies.get('passwords')
    if cookies:
        passwords = json.loads(cookies)
        if level in passwords and check_password(level, passwords[level]):
            return True
    return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_level')
@cross_origin()
def check_level():
    query_params = request.args.to_dict()

    if 'password' in query_params and 'level' in query_params:
        password = query_params['password']
        level = query_params['level']

        if check_password(level, password):
            return {'success': True}
    
    return {'success': False, 'message': 'Invalid password! Come back later when you got some learning inside that primitive brain of yours.'}


@app.route('/levels/<level>')
@cross_origin()
def levels(level):
    level = level.split('.')[0]
    
    if not os.path.isfile(f'templates/levels/{level}.html'):
        abort(404)
    
    print(level)


    if level == 'level1':
        return render_template(f'levels/{level}.html', password=PASSWORDS['level2'])
    elif check_level_privileges(level, request):
        return render_template(f'levels/{level}.html')

    return render_template('wrong_password.html', level=f'Level {level[5:]}')




@app.route('/level3_game')
def game():
    user = request.headers.get('privileges')
    message = "How cool is that?!? When you click the square it literally changes colors 😱😱😱"
    radius = "0%"
    if user and user.lower() == 'admin':
        message = "Here's your password you smart-aleck: " +  PASSWORDS['level4'] + ", and now since you're an admin you get a circllle!!! 😱😱😱"
        radius = "100%"

    return render_template('/other/game.html', message=message, radius=radius)


@app.route('/level4_validate_login')
def validate_password():
    query_params = request.args.to_dict()
    if 'password' in query_params and 'username' in query_params:
        password = query_params['password']
        username = query_params['username']
        result = db.validate_login(username, password)
        if result and result != 'Error':
            return {'success': True, 'message': f"Correct! Indeed the password for '{username}' is '{result}'"}
        elif result == 'Error':
            return {'success': False, 'message': 'Hmmm... Something broke. Try again later.'}
    
    return {'success': False, 'message': 'Password is incorrect or username does not exist!'}


@app.route('/level5_streaming')
@cross_origin()
def level5_streaming():
    if check_level_privileges('level5', request):
        print(request.headers['X-Forwarded-For'])
        if requests.get('http://ip-api.com/json/' + request.headers['X-Forwarded-For']).json()["country"] != "Israel":
            return {'success': True}
        else:
            return {'success': False, 'message': 'We are sorry, but our service is currently not supported in Israel.'}
    
    abort(403)



@app.route('/sources/<source>')
def sources(source):
    source = source.split('.')[0]
    
    if check_level_privileges(source, request):
        path = f'{app.template_folder}/sources/{source}.txt'
        if os.path.isfile(path):
            file_content = open(path).read()

            if source == 'level2':
                file_content = file_content.replace('""', f'"{do_sha256(PASSWORDS["level3"])}"')

            return Response(file_content, mimetype='text/plain')
        else:
            abort(404)

    abort(403)


if __name__ == '__main__':
    app.run()