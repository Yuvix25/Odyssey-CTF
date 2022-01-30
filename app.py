import os
import json
import requests
from hashlib import sha256
from flask import Flask, Response, render_template, abort, jsonify, send_file, after_this_request, send_from_directory, request
from utils import *
from sqlite_intergration import *
from capture import capture_url

app = Flask(__name__)
db = Database()

DOWNLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/'), 'downloads/').replace('\\', '/')


def check_level_privileges(level, request):
    if 'X-Forwarded-For' not in request.headers and int(level[5:]) <= 7:
        # user is running locally
        return True

    cookies = request.cookies.get('passwords')
    if cookies:
        passwords = json.loads(cookies)
        if level in passwords and check_password(level, passwords[level]):
            return True
    return False


@app.route('/')
def index():
    # get the port heroku is running on:
    port = os.environ.get('PORT', 5000)
    return render_template('index.html', port=port)


@app.route('/check_level')
def check_level():
    query_params = request.args.to_dict()

    if 'password' in query_params and 'level' in query_params:
        password = query_params['password']
        level = query_params['level']

        if check_password(level, password):
            ret = jsonify({'success': True})
            passwords = request.cookies.get('passwords')
            if passwords:
                passwords = json.loads(passwords)
            else:
                passwords = {}
            passwords[level] = password
            ret.set_cookie('passwords', json.dumps(passwords))
            return ret
    
    return {'success': False, 'message': 'Invalid password! Come back later when you got some learning inside that primitive brain of yours.'}


@app.route('/levels/<level>')
def levels(level):
    level = level.split('.')[0]
    
    if not os.path.isfile(f'templates/levels/{level}.html'):
        abort(404)
    
    print(level)


    if level == 'level1':
        return render_template(f'levels/{level}.html', password=PASSWORDS['level2'])
    elif check_level_privileges(level, request):
        if level == 'level6':
            port = os.environ.get('PORT', 5000)
            return render_template(f'levels/{level}.html', port=port)
        elif level == 'level7':
            return render_template(f'levels/{level}.html', password=PASSWORDS['level7'])
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
def level5_streaming():
    if check_level_privileges('level5', request):
        if 'X-Forwarded-For' in request.headers and requests.get('http://ip-api.com/json/' + request.headers['X-Forwarded-For']).json()["country"] == "Italy":
            return {'success': True, 'url': 'https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1', 'message': f"Fine. Here you go: {PASSWORDS['level6']}"}
        else:
            return {'success': False, 'message': 'We are sorry, but our service currently only works in Italy.'}
    
    abort(403)

@app.route('/level6_capture')
def level6_capture():
    if check_level_privileges('level6', request):
        query_params = request.args.to_dict()
        if 'url' in query_params:
            url = query_params['url']
            if url.startswith('http') and '0.0.0.0' not in url:
                img_path = capture_url(url)
                if img_path:
                    return {'success': True, 'url': img_path}
                else:
                    return {'success': False, 'message': f"Couldn't capture <a href='{url}'>{url}</a>. Try again later or check if you typed it wrong (maybe 'http://' instead of 'https://'?)."}
            else:
                return {'success': False, 'message': "Invalid URL! (maybe you forgot 'http://' or 'https://'?)"}
        else:
            return {'success': False, 'message': 'URL is missing!'}

    abort(403)

# @app.route('/level7_password')
# def level7_password():
#     if 'X-Forwarded-For' not in request.headers:
#         return {'success': True, 'password': PASSWORDS['level7']}
#     abort(403)

# @app.route('/robots.txt')
# def robots():
#     if check_level_privileges('level7', request):
#         robots_data = open('robots.txt', 'r').read()
#         return Response(robots_data, mimetype='text/plain')
#     abort(403)
    


@app.route('/7_ZIP')
def level7_zip():
    if check_level_privileges('level7', request):
        return send_from_directory(DOWNLOADS_DIR, 'level7.zip', as_attachment=True)
    abort(403)

@app.route('/7_README')
def level7_readme():
    if check_level_privileges('level7', request):
        return send_from_directory(DOWNLOADS_DIR, '7_README.txt', as_attachment=True)
    abort(403)


@app.route('/captures/<file>')
def capture(file):
    file = './captures/' + file

    if check_level_privileges('level6', request):
        if os.path.isfile(file) and file.endswith('.png'):

            @after_this_request
            def delete_file(response):
                try:
                    os.remove(file)
                except:
                    pass
                return response

            return send_file(file, mimetype='image/png')
        else:
            abort(404)
    
    abort(403)


@app.route('/sources/<source>')
def sources(source):
    source = source.split('.')[0]
    
    if check_level_privileges(source, request):
        path = f'{app.template_folder}/sources/{source}.txt'
        if os.path.isfile(path):
            file_content = open(path).read()

            if source == 'level2':
                # password_hash=sha256(LEVEL3_SALT + PASSWORDS['level3'].encode('utf-8')).hexdigest(), salt=LEVEL3_SALT.__repr__()
                file_content = file_content.replace('"hash"', f'"{sha256(LEVEL3_SALT + PASSWORDS["level3"].encode()).hexdigest()}"')
                file_content = file_content.replace('"salt"', f'{LEVEL3_SALT.__repr__()}')

            return Response(file_content, mimetype='text/plain')
        else:
            abort(404)

    abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)