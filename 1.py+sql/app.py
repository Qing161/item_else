from flask import Flask, render_template, request, redirect, url_for, flash
import MySQLdb #pip install mysql-connector-python
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 确保设置了密钥

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    database = request.form['database']

    if not database.isalnum() and '_' not in database:
        flash('数据库名只能包括字母、数字和下划线。')
        return redirect(url_for('index'))
    try:
        # 尝试连接数据库
        conn = MySQLdb.connect(host=name, user=username, passwd=password, db=database)
        conn.close()  # 关闭连接，因为我们只需要验证连接是否成功
        # 如果连接成功，则重定向到 /data
        return redirect(url_for('data', name=name, username=username, password=password, database=database))
    except Exception as e:
        flash(f'数据库连接失败：{str(e)}')
        return redirect(url_for('index'))

@app.route('/data')
def data():
    name = request.args.get('name')
    username = request.args.get('username')
    password = request.args.get('password')
    database = request.args.get('database')

    try:
        conn = MySQLdb.connect(host=name, user=username, passwd=password, db=database)
        with conn.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            table_list = [t[f'Tables_in_{database}'] for t in tables]

        return render_template('data.html', tables=table_list, name=name, username=username, password=password, database=database)

    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/table_image')
def table_image():
    name = request.args.get('name')
    username = request.args.get('username')
    password = request.args.get('password')
    database = request.args.get('database')
    table = request.args.get('table')

    try:
        conn = MySQLdb.connect(host=name, user=username, passwd=password, db=database)
        with conn.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute(f"SELECT * FROM `{table}`;")
            results = cursor.fetchall()
            # 将数据转换为DataFrame
            df = pd.DataFrame(results)
            # 生成HTML表格
            html_table = df.to_html(classes='data', index=False, border=0)
            # 返回渲染后的模板
            return render_template('table_image.html',
                                   html_table=html_table,
                                   table=table,
                                   name=name,
                                   username=username,
                                   password=password,
                                   database=database)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)