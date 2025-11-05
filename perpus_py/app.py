from flask import Flask, request, jsonify, render_template
import pymysql
import pymysql.cursors

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
def index():
    # Ambil data dari MySQL untuk ditampilkan saat halaman pertama kali dibuka
    cur = mysql.cursor(pymysql.cursors.DictCursor) # dictionary=True agar mudah di-render
    cur.execute("SELECT * FROM buku ORDER BY nama")
    daftar_buku = cur.fetchall()
    cur.close()

    return render_template('index.html', daftar_buku=daftar_buku)

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
            'data' : buku
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

        cur = mysql.cursor()

        query = """
        UPDATE buku
        SET nama = %s,
            jenis = %s,
            kategori = %s,
            pengarang = %s,
            th_terbit = %s,
            penerbit = %s,
            rating = %s
        WHERE id = %s
        """
        params = nama, jenis, kategori, pengarang, th_terbit, penerbit, rating, buku_id

        cur.execute(query, params)

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
        cur.execute('DELETE FROM buku WHERE id = %s', (buku_id))
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