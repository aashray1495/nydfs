from flask import Flask, request, redirect, render_template
import sys
import pandas as pd
sys.path.insert(1, "PATH TO LOCAL PYTHON PACKAGES")  #OPTIONAL: Only if need to access Python packages installed on a local (non-global) directory
sys.path.insert(2, "PATH TO FLASK DIRECTORY")      #OPTIONAL: Only if you need to add the directory of your flask app

app = Flask(__name__)

@app.route('/') 
def sql_database():
    from functions.sqlquery import sql_query
    results = sql_query(''' SELECT * FROM data_table''')
    msg = 'SELECT * FROM data_table'
    return render_template('sqldatabase.html', results=results, msg=msg)   
@app.route('/insert',methods = ['POST', 'GET']) #this is when user submits an insert
def sql_datainsert():
    from functions.sqlquery import sql_edit_insert, sql_query
    if request.method == 'POST':
        txn_id = request.form['txn_id']
        sender = request.form['sender']
        receiver = request.form['receiver']
        token = request.form['token']
        value = request.form['value']
        created = request.form['created']
        sql_edit_insert(''' INSERT INTO data_table (txn_id,sender,receiver,token,value,created) VALUES (?,?,?,?,?,?) ''', (txn_id,sender,receiver,token,value,created) )
    results = sql_query(''' SELECT * FROM data_table''')
    msg = 'INSERT INTO data_table (txn_id,sender,receiver,token,value,created) VALUES ('+txn_id+','+sender+','+receiver+','+token+','+value+','+created+')'
    return render_template('sqldatabase.html', results=results, msg=msg) 
@app.route('/delete',methods = ['POST', 'GET']) #this is when user clicks delete link
def sql_datadelete():
    from functions.sqlquery import sql_delete, sql_query
    if request.method == 'GET':
        t_id = request.args.get('t_id')
        create = request.args.get('create')
        sql_delete(''' DELETE FROM data_table where txn_id = ? and created = ?''', (t_id,create) )
    results = sql_query(''' SELECT * FROM data_table''')
    msg = 'DELETE FROM data_table WHERE txn_id = ' + t_id + ' and created = ' + create
    return render_template('sqldatabase.html', results=results, msg=msg)
@app.route('/query_edit',methods = ['POST', 'GET']) #this is when user clicks edit link
def sql_editlink():
    from functions.sqlquery import sql_query, sql_query2
    if request.method == 'GET':
        etxn_id = request.args.get('etxn_id')
        ecreated = request.args.get('ecreated')
        eresults = sql_query2(''' SELECT * FROM data_table where txn_id = ? and created = ?''', (etxn_id,ecreated))
    results = sql_query(''' SELECT * FROM data_table''')
    return render_template('sqldatabase.html', eresults=eresults, results=results)
@app.route('/edit',methods = ['POST', 'GET']) #this is when user submits an edit
def sql_dataedit():
    from functions.sqlquery import sql_edit_insert, sql_query
    if request.method == 'POST':
        old_txn_id = request.form['old_txn_id']
        old_created = request.form['old_created']
        txn_id = request.form['txn_id']
        sender = request.form['sender']
        receiver = request.form['receiver']
        token = request.form['token']
        value = request.form['value']
        created = request.form['created']
        sql_edit_insert(''' UPDATE data_table set txn_id=?,sender=?,receiver=?,token=?,value=?,created=? WHERE txn_id=? and created=? ''', (txn_id,sender,receiver,token,value,created,old_txn_id,old_created) )
    results = sql_query(''' SELECT * FROM data_table''')
    msg = 'UPDATE data_table set txn_id = ' + txn_id + ', sender = ' + sender + ', receiver = ' + receiver + ', token = ' + token + ', value = ' + value + ', created = ' + created + ' WHERE txn_id = ' + old_txn_id + ' and created = ' + old_created
    return render_template('sqldatabase.html', results=results, msg=msg)
@app.route("/tables")
def show_tables():
    data = pd.read_csv('templates/dummy.csv')
    data.set_index(['Id'], inplace=True)
    # data.index.name=None
    # females = data.loc[data.Address=='w1']
    # males = data.loc[data.Address=='w8']
    # return render_template('view.html',tables=[females.to_html(classes='female'), males.to_html(classes='male')],
    return render_template('view.html',tables=[data.to_html()],
    titles = ['Transaction Id', 'Address'])
if __name__ == "__main__":
    app.run(debug=True)

