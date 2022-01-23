import os
import json
from flask import Flask, render_template, request, abort, Response
from utils import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_level')
def check_level():
    query_params = request.args.to_dict()

    if 'password' in query_params and 'level' in query_params:
        password = query_params['password']
        level = query_params['level']

        if check_password(level, password):
            return {'success': True}
    
    return {'success': False, 'message': 'Invalid password! Come back later when you got some learning inside that primitive brain of yours.'}


@app.route('/levels/<level>')
def levels(level):
    if '.html' in level:
        level = level.split('.html')[0]
    
    if not os.path.isfile(f'templates/levels/{level}.html'):
        abort(404)
    
    print(level)


    if level == 'level1':
        return render_template(f'levels/{level}.html', password=PASSWORDS['level2'])
    else:
        cookies = request.cookies.get('passwords')
        if cookies:
            passwords = json.loads(cookies)
            if level in passwords and check_password(level, passwords[level]):
                return render_template(f'levels/{level}.html')

    return render_template('wrong_password.html')

@app.route('/game')
def game():
    user = request.headers.get('privileges')
    message = "How cool is that?!? When you click the square it literally changes colors 😱😱😱"
    radius = "0%"
    if user.lower() == 'admin':
        message = "Here's your password you smart-aleck: " +  PASSWORDS['level4'] + ", and now since you're an admin you get a circllle!!! 😱😱😱"
        radius = "100%"

    return render_template('/other/game.html', message=message, radius=radius)




@app.route('/sources/<source>')
def sources(source):
    if '.txt' in source:
        source = source.split('.txt')[0]
    
    cookies = request.cookies.get('passwords')
    if cookies:
        passwords = json.loads(cookies)
        if source in passwords and check_password(source, passwords[source]):
            file_content = open(f'{app.template_folder}/sources/{source}.txt').read()
            if source == 'level2':
                file_content = file_content.replace('""', f'"{do_sha256(PASSWORDS["level3"])}"')
            return Response(file_content, mimetype='text/plain')

    abort(403)


if __name__ == '__main__':
    app.run()