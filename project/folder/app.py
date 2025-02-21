from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

@app.route('/')
def index():
    # RAW Query (Sebelum)
    # students = db.session.execute(text('SELECT * FROM student')).fetchall()
    # return render_template('index.html', students=students)

    # Menggunakan ORM untuk query data siswa (Sesudah)
    students = Student.query.all()
    return render_template('index.html', students=students)

# Sebelum
# @app.route('/add', methods=['POST'])
# def add_student():
#     name = request.form['name']
#     age = request.form['age']
#     grade = request.form['grade']
    

#     connection = sqlite3.connect('instance/students.db')
#     cursor = connection.cursor()

#     # RAW Query
#     # db.session.execute(
#     #     text("INSERT INTO student (name, age, grade) VALUES (:name, :age, :grade)"),
#     #     {'name': name, 'age': age, 'grade': grade}
#     # )
#     # db.session.commit()
#     query = f"INSERT INTO student (name, age, grade) VALUES ('{name}', {age}, '{grade}')"
#     cursor.execute(query)
#     connection.commit()
#     connection.close()
#     return redirect(url_for('index'))

# Sesudah 1
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']

    # Menggunakan parameter binding untuk mencegah SQL Injection
    query = "INSERT INTO student (name, age, grade) VALUES (?, ?, ?)"
    connection = sqlite3.connect('instance/students.db')
    cursor = connection.cursor()
    cursor.execute(query, (name, age, grade))
    connection.commit()
    connection.close()

    return redirect(url_for('index'))




# Sebelum
# @app.route('/delete/<string:id>') 
# def delete_student(id):
#     # RAW Query
#     db.session.execute(text(f"DELETE FROM student WHERE id={id}"))
#     db.session.commit()
#     return redirect(url_for('index'))

# Sesudah
@app.route('/delete/<int:id>') 
def delete_student(id):
    # Periksa apakah ID yang diberikan cocok dengan ID pengguna yang sedang login
    # Misalnya, gunakan session atau metode lain untuk mendapatkan ID pengguna
    user_id = get_logged_in_user_id()  # Fungsi ini perlu didefinisikan sesuai dengan aplikasi Anda
    
    if id != user_id:
        return "Unauthorized", 403  # Tanggapan jika pengguna tidak diizinkan

    db.session.execute(text(f"DELETE FROM student WHERE id={id}"))
    db.session.commit()
    return redirect(url_for('index'))


# Sebelum
# @app.route('/edit/<int:id>', methods=['GET', 'POST'])
# def edit_student(id):
#     if request.method == 'POST':
#         name = request.form['name']
#         age = request.form['age']
#         grade = request.form['grade']
        
#         # RAW Query
#         db.session.execute(text(f"UPDATE student SET name='{name}', age={age}, grade='{grade}' WHERE id={id}"))
#         db.session.commit()
#         return redirect(url_for('index'))
#     else:
#         # RAW Query
#         student = db.session.execute(text(f"SELECT * FROM student WHERE id={id}")).fetchone()
#         return render_template('edit.html', student=student)

# Sesudah
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    # Periksa apakah ID yang diberikan cocok dengan ID pengguna yang sedang login
    user_id = get_logged_in_user_id()  # Fungsi ini perlu didefinisikan sesuai dengan aplikasi Anda
    
    if id != user_id:
        return "Unauthorized", 403  # Tanggapan jika pengguna tidak diizinkan

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        db.session.execute(text(f"UPDATE student SET name='{name}', age={age}, grade='{grade}' WHERE id={id}"))
        db.session.commit()
        return redirect(url_for('index'))
    else:
        student = db.session.execute(text(f"SELECT * FROM student WHERE id={id}")).fetchone()
        return render_template('edit.html', student=student)


# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

