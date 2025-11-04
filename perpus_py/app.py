from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'perpus'

mysql = pymysql.connect(
    host = app.config['MYSQL_HOST'],
    user = app.config['MYSQL_USER'],
    password = app.config['MYSQL_PASSWORD'],
    db = app.config['MYSQL_DB'],
)

@app.route('/')
def test():
    return 'Success'

@app.route('/tambah_buku', methods = ['POST'])
def tambah_buku():
    try:
        data = request.get_json()

        nama = data['nama']
        jenis = data['jenis']
        kategori = data['kategori']
        pengarang = data['pengarang']
        th_terbit = data['th_terbit']
        penerbit = data['penerbit']
        rating = data['rating']
        id = data['id']

        cur = mysql.cursor()
        cur.execute('INSERT INTO buku (nama, jenis, kategori, pengarang, th_terbit, penerbit, rating, id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (nama, jenis, kategori, pengarang, th_terbit, penerbit, rating, id))
        mysql.commit()
        cur.close

        response = {
            'error' : False,
            'message': 'Berhasil di Tambah',
            'data' : data
        }

        return jsonify(response), 201
    except Exception as e:
        response = {
            'error' : False,
            'message': f'Error Ocurred: {e}',
            'data' : None
        }
        return jsonify(response), 500

@app.route('/get_buku', methods = ['GET'])
def get_buku():
    try:
        cur = mysql.cursor()
        cur.execute('SELECT * FROM buku')
        data = cur.fetchall()
        cur.close()

        buku = [{'nama': buku[0], 'jenis': buku[1], 'kategori': buku[2], 'pengarang': buku[3], 'th_terbit': buku[4], 'penerbit': buku[5], 'rating': buku[6], 'id': buku[7]} for buku in data]

        response = {
            'error' : False,
            'message': 'Berhasil di Ambil',
            'data' : data
        }

        return jsonify(response), 200
    except Exception as e:
        response = {
            'error' : False,
            'message': f'Error Ocurred: {e}',
            'data' : None
        }
        return jsonify(response), 500
    
@app.route('/update_buku/<int:buku_id>', methods = ['PUT'])
def update_buku(buku_id):
    try:  
        data = request.get_json()

        nama = data['nama']
        jenis = data['jenis']
        kategori = data['kategori']
        pengarang = data['pengarang']
        th_terbit = data['th_terbit']
        penerbit = data['penerbit']
        rating = data['rating']
        id = data['id']

        cur = mysql.cursor()
        cur.execute('UPDATE buku SET (nama, jenis, kategori, pengarang, th_terbit, penerbit, rating, id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) WHERE id = $s', (nama, jenis, kategori, pengarang, th_terbit, penerbit, rating, id, buku_id))

        mysql.commit()
        cur.close()

        response = {
            'error' : False,
            'message': 'Berhasil di Ubah',
            'data' : {'buku_id' : buku_id}
        }

        return jsonify(response), 201
    except Exception as e:
        response = {
            'error' : False,
            'message': f'Error Ocurred: {e}',
            'data' : None
        }
    return jsonify(response), 500

@app.route('/hapus_buku/<int:buku_id>', methods = ['DELETE'])
def hapus_buku(buku_id):
    try:
        cur = mysql.cursor()
        cur.execute('DELETE * FROM buku WHERE id = $s')
        mysql.commit()
        cur.close()
 
        response = {
            'error' : False,
            'message': 'Berhasil di Hapus',
            'data' : {'buku_id' : buku_id}
        }

        return jsonify(response), 201
    except Exception as e:
        response = {
            'error' : False,
            'message': f'Error Ocurred: {e}',
            'data' : None
        }
    return jsonify(response), 500  
     
if __name__ == '__main__':
    app.run(debug=True)