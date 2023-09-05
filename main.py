import pymysql
from app import app
from config import mysql
from flask import request, json, jsonify, flash

#get data reservation
@app.route('/reservation')
def member():
    try:
        conn      = mysql.connect()
        cursor    = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery  = "SELECT * FROM reservation WHERE 1=1"
        cursor.execute(sqlQuery)
        empRows   = cursor.fetchall()
        respone   = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#get data member detail
@app.route('/reservation/<int:id>')
def memberDetails(id):
    try:
        conn    = mysql.connect()
        cursor  = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM reservation WHERE id =%s"
        cursor.execute(sqlQuery, id)
        empRow  = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 
        
#created data reservation
@app.route('/reservation/create', methods=['POST'])
def create_reservation():
    try:        
        _json   = request.json
        _name   = _json['name']
        _message  = _json['message']
        _confirm  = _json['confirm']
        if _name and _message and request.method == 'POST':
            conn      = mysql.connect()
            cursor    = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery  = "INSERT INTO reservation(name, message, confirm) VALUES(%s, %s, %s)"
            bindData  = (_name, _message, _confirm)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Reservation added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

#update data member
@app.route('/reservation/update', methods=['PUT'])
def memberUpdate():
    try:
        _json = request.json
        _id       = _json['id']
        _name   = _json['name']
        _message  = _json['message']
        _confirm  = _json['confirm']
        if _name and _message and _id and request.method == 'PUT':			
            sqlQuery  = "UPDATE reservation SET name=%s, message=%s, confirm=%s WHERE id=%s"
            bindData  = (_name, _message, _id, _confirm)
            conn      = mysql.connect()
            cursor    = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone   = jsonify('Reservation updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/reservation/delete/<int:id>', methods=['DELETE'])
def deleteMember(id):
	try:
		conn      = mysql.connect()
		cursor    = conn.cursor()
		cursor.execute("DELETE FROM reservation WHERE id =%s", (id,))
		conn.commit()
		respone   = jsonify('Reservation deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()