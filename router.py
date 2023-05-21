from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import CORS
import query
import llm
import threading

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/login')
def login():
    return render_template('login.html')    


@app.route('/process_words', methods=['POST'])
def process_words():
    words = request.form.get('words', '')
    uid = request.cookies.get('uid')
    
    result = query.createStory(uid, words);
    
    # 开始生产故事 
    task_thread = threading.Thread(target=llm.outputHtml, args=(words, "Breaking new", uid))
    
    # 启动协程，后台自运行
    task_thread.start()
   
    print(result)
    
    
    # 在这里添加处理words参数的代码

    return jsonify({'status': 'success', 'words': words})
    
    
@app.route('/user', methods=['POST'])
def user():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    result = query.login(email, password)
    print(result)
    if len(result) > 0:
        # 创建一个响应对象
        response = make_response(jsonify({"status": "success", "message": "登录成功"}))
        
        # 设置cookie，名称为`user`, 值为`email`
        response.set_cookie("uid", result[0][3])

        # 返回带有cookie的响应对象
        return response
    else:
        return jsonify({"status": "error", "message": "登录失败：用户名或密码错误"})

if __name__ == '__main__':
    app.run(debug=True, port=8008)
