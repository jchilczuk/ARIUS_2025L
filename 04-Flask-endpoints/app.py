from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import extract
from datetime import datetime
import os

print("Current working directory:", os.getcwd())

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'school.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

# Tabela pomocnicza, relacja wiele do wielu między nauczycielami a przedmiotami
teacher_subject = db.Table(
    'teacher_subject',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
)

# Tabela: Nauczyciele
class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    rating = db.Column(db.Float)
    phone_number = db.Column(db.String(20))
    rate = db.Column(db.Integer)
    currency = db.Column(db.String(20))
    email = db.Column(db.String(50))
    
    subjects = db.relationship('Subject', secondary=teacher_subject, backref='teachers')

    # ocena w skali 0-5
    @validates('rating')
    def validate_rating(self, key, value):
        if value < 0 or value > 5:
            raise ValueError("Ocena musi zawierać się w przedziale 0-5.")
        return value

# Tabela: Studenci
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))

# Tabela: Lekcje
class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    date = db.Column(db.Date)
    time = db.Column(db.Time)

    teacher = db.relationship('Teacher', backref=db.backref('lessons'))
    student = db.relationship('Student', backref=db.backref('lessons'))
    subject = db.relationship('Subject', backref=db.backref('lessons'))

# Tabela: Kalendarz nauczycieli
class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    available_from = db.Column(db.String(10))
    available_to = db.Column(db.String(10))

    teacher = db.relationship('Teacher', backref=db.backref('schedule'))

# Tabela: Przedmioty
class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    # Wybór przedmiotów z pośród dostępnych
    @validates('name')
    def validate_name(self, key, value):
        allowed_subjects = ["matematyka", "fizyka", "chemia", "historia", "biologia", "geografia", "WoS"]
        if value not in allowed_subjects:
            raise ValueError(f"Niepoprawna nazwa przedmiotu, dostępne są następujące przedmioty: {allowed_subjects}.")
        return value

# Tworzenie bazy danych
with app.app_context():
    db.create_all()


# Widok główny
@app.route('/')
def home():
    return "Witaj w aplikacji do zarządzania lekcjami!"

# Reset danych w bazie
@app.route('/reset_db')
def reset_db():
    db.drop_all()
    db.create_all()
    return "Baza danych rostała zresetowana!"

@app.route('/add_data')
def add_data():
    # Dodawanie przedmiotów
    math = Subject(name='matematyka')
    physics = Subject(name='fizyka')
    chemistry = Subject(name='chemia')
    history = Subject(name='historia')
    biology = Subject(name='biologia')
    db.session.add_all([math, physics, chemistry, history, biology])

    # Dodawanie nauczycieli
    teacher1 = Teacher(first_name='Jan', last_name='Kowalski', rating=4.5, phone_number='123456789', rate=50, currency='PLN', email='jan.kowalski@example.com', subjects=[math, physics])
    teacher2 = Teacher(first_name='Anna', last_name='Nowak', rating=4.2, phone_number='987654321', rate=55, currency='PLN', email='anna.nowak@example.com', subjects=[biology, chemistry])
    teacher3 = Teacher(first_name='Piotr', last_name='Wiśniewski', rating=4.8, phone_number='111222333', rate=60, currency='PLN', email='piotr.wisniewski@example.com', subjects=[history, math])
    teacher4 = Teacher(first_name='Katarzyna', last_name='Zielińska', rating=4.6, phone_number='444555666', rate=45, currency='PLN', email='katarzyna.zielinska@example.com', subjects=[biology, history])
    teacher5 = Teacher(first_name='Marek', last_name='Nowicki', rating=4.3, phone_number='777888999', rate=50, currency='PLN', email='marek.nowicki@example.com', subjects=[chemistry, physics])
    db.session.add_all([teacher1, teacher2, teacher3, teacher4, teacher5])

    # Dodawanie grafików
    schedule1 = Schedule(teacher=teacher1, available_from='09:00', available_to='17:00')
    schedule2 = Schedule(teacher=teacher2, available_from='08:00', available_to='16:00')
    schedule3 = Schedule(teacher=teacher3, available_from='14:00', available_to='20:00')
    schedule4 = Schedule(teacher=teacher4, available_from='08:00', available_to='13:00')
    schedule5 = Schedule(teacher=teacher5, available_from='08:00', available_to='13:00')
    db.session.add_all([schedule1, schedule2, schedule3, schedule4, schedule5])


    # Dodawanie studentów
    student1 = Student(first_name='Marek', last_name='Zieliński', email='marek.z@example.com')
    student2 = Student(first_name='Kasia', last_name='Wiśniewska', email='kasia.w@example.com')
    student3 = Student(first_name='Tomasz', last_name='Kowal', email='tomasz.k@example.com')
    db.session.add_all([student1, student2, student3])



    # Dodawanie lekcji
    lessons = [
        # Lekcje w dni powszednie (poniedziałek-piątek)
        Lesson(teacher=teacher1, student=student1, subject=math, date=datetime.strptime('2025-04-07', '%Y-%m-%d').date(), time=datetime.strptime('10:00', '%H:%M').time()),  # Poniedziałek
        Lesson(teacher=teacher1, student=student2, subject=physics, date=datetime.strptime('2025-04-07', '%Y-%m-%d').date(), time=datetime.strptime('12:00', '%H:%M').time()),  # Wtorek
        Lesson(teacher=teacher2, student=student2, subject=biology, date=datetime.strptime('2025-04-09', '%Y-%m-%d').date(), time=datetime.strptime('09:00', '%H:%M').time()),  # Środa
        Lesson(teacher=teacher2, student=student1, subject=chemistry, date=datetime.strptime('2025-04-10', '%Y-%m-%d').date(), time=datetime.strptime('11:00', '%H:%M').time()),  # Czwartek
        Lesson(teacher=teacher1, student=student2, subject=history, date=datetime.strptime('2025-04-07', '%Y-%m-%d').date(), time=datetime.strptime('14:00', '%H:%M').time()),  # Piątek
        Lesson(teacher=teacher4, student=student2, subject=math, date=datetime.strptime('2025-04-14', '%Y-%m-%d').date(), time=datetime.strptime('08:00', '%H:%M').time()),  # Poniedziałek
        Lesson(teacher=teacher5, student=student1, subject=chemistry, date=datetime.strptime('2025-04-16', '%Y-%m-%d').date(), time=datetime.strptime('13:00', '%H:%M').time()),  # Wtorek
        Lesson(teacher=teacher5, student=student1, subject=physics, date=datetime.strptime('2025-04-16', '%Y-%m-%d').date(), time=datetime.strptime('15:00', '%H:%M').time()),  # Środa
        Lesson(teacher=teacher2, student=student2, subject=math, date=datetime.strptime('2025-04-17', '%Y-%m-%d').date(), time=datetime.strptime('10:00', '%H:%M').time()),  # Czwartek
        Lesson(teacher=teacher2, student=student2, subject=math, date=datetime.strptime('2025-04-18', '%Y-%m-%d').date(), time=datetime.strptime('12:00', '%H:%M').time()),  # Piątek

        # Lekcje w weekendy (sobota-niedziela)
        Lesson(teacher=teacher3, student=student3, subject=math, date=datetime.strptime('2025-04-12', '%Y-%m-%d').date(), time=datetime.strptime('09:00', '%H:%M').time()),  # Sobota
        Lesson(teacher=teacher3, student=student1, subject=math, date=datetime.strptime('2025-04-13', '%Y-%m-%d').date(), time=datetime.strptime('11:00', '%H:%M').time()),  # Niedziela
        Lesson(teacher=teacher3, student=student1, subject=history, date=datetime.strptime('2025-04-19', '%Y-%m-%d').date(), time=datetime.strptime('14:00', '%H:%M').time()),  # Sobota
        Lesson(teacher=teacher3, student=student3, subject=biology, date=datetime.strptime('2025-04-20', '%Y-%m-%d').date(), time=datetime.strptime('16:00', '%H:%M').time()),  # Niedziela
        Lesson(teacher=teacher3, student=student2, subject=math, date=datetime.strptime('2025-04-21', '%Y-%m-%d').date(), time=datetime.strptime('10:00', '%H:%M').time()),  # Poniedziałek
    ]
    db.session.add_all(lessons)

    db.session.commit()

    return "Dane zostały dodane do bazy danych!"

#Wyświetlanie danych w bazie danych
@app.route('/print_db')
def print_db():
    output = "<h1>Zawartość bazy danych:</h1>"

    # Nauczyciele
    output += "<h2>Nauczyciele:</h2><ul>"
    for teacher in Teacher.query.all():
        subjects = ", ".join([subject.name for subject in teacher.subjects])  # Pobranie nazw przedmiotów
        output += f"<li>{teacher.id}. {teacher.first_name} {teacher.last_name}, email: {teacher.email}, ocena: {teacher.rating}, przedmioty: {subjects}</li>"
    output += "</ul>"

    # Studenci
    output += "<h2>Studenci:</h2><ul>"
    for student in Student.query.all():
        output += f"<li>{student.id}. {student.first_name} {student.last_name}, email: {student.email}</li>"
    output += "</ul>"

    # Przedmioty
    output += "<h2>Przedmioty:</h2><ul>"
    for subject in Subject.query.all():
        output += f"<li>{subject.id}. {subject.name}</li>"
    output += "</ul>"

    # Lekcje
    output += "<h2>Lekcje:</h2><ul>"
    for lesson in Lesson.query.all():
        output += f"<li>{lesson.id}. Data: {lesson.date}, Godzina: {lesson.time}, Nauczyciel: {lesson.teacher.first_name} {lesson.teacher.last_name}, Uczeń: {lesson.student.first_name} {lesson.student.last_name}, Przedmiot: {lesson.subject.name}</li>"
    output += "</ul>"

    # Grafiki nauczycieli
    output += "<h2>Grafiki nauczycieli:</h2><ul>"
    for schedule in Schedule.query.all():
        output += f"<li>{schedule.id}. Nauczyciel: {schedule.teacher.first_name} {schedule.teacher.last_name}, dostępność: {schedule.available_from} - {schedule.available_to}</li>"
    output += "</ul>"

    return output

# F1: Sprawdzanie liczby studentów z lekcjami w dni powszednie
@app.route('/f1')
def f1():
    weekday_lessons = db.session.query(Lesson.student_id).filter(
        extract('dow', Lesson.date).in_([1, 2, 3, 4, 5])  # Poniedziałek - Piątek
    ).distinct().count()
    return f'Liczba studentów, którzy mają umówione lekcje w dni powszednie: {weekday_lessons}'

# F2: Sprawdzanie liczby nauczycieli z lekcjami w weekendy
@app.route('/f2')
def f2():
    weekend_lessons = db.session.query(Lesson.teacher_id).filter(
        extract('dow', Lesson.date).in_([0, 6])  # Sobota - Niedziela
    ).distinct().count()
    return f'Liczba nauczycieli, którzy mają umówione lekcje w weekend: {weekend_lessons}'

# F3: Student z największą liczbą lekcji
@app.route('/f3')
def f3():
    most_lessons_student = db.session.query(Student, db.func.count(Lesson.id)).join(Lesson).group_by(Student.id).order_by(
        db.func.count(Lesson.id).desc()
    ).first()
    student = most_lessons_student[0]
    lesson_count = most_lessons_student[1]
    return f'Student z największą liczbą umówionych lekcji ({lesson_count}): {student.first_name} {student.last_name}, email: {student.email}'

# F4: Przedmiot z najczęściej umawianymi lekcjami
@app.route('/f4')
def f4():
    most_booked_subject = db.session.query(Subject, db.func.count(Lesson.id)).join(Lesson).group_by(Subject.id).order_by(
        db.func.count(Lesson.id).desc()
    ).first()
    subject = most_booked_subject[0]
    lesson_count = most_booked_subject[1]
    return f'Najczęściej umawiany przedmiot: {subject.name} - {lesson_count} lekcji'

# F5: Liczba lekcji z matematyki
@app.route('/f5')
def f5():
    math_lessons = db.session.query(Lesson).join(Subject).filter(Subject.name == 'matematyka').count()
    return f'Liczba lekcji matematyki: {math_lessons}'

# F6: Liczba lekcji w środy
@app.route('/f6')
def f6():
    wednesday_lessons = db.session.query(Lesson).filter(
        extract('dow', Lesson.date) == 3  # Środa
    ).count()
    return f'Liczba lekcji w środy: {wednesday_lessons}'

# F7: Lista lekcji dla nauczyciela w określonym dniu
@app.route('/f7')
def f7():
    teacher_id = 1  # Przykładowy nauczyciel
    day = datetime.strptime('2025-04-07', '%Y-%m-%d').date()  # Przykładowy dzień

    # Pobranie nauczyciela
    teacher = Teacher.query.get(teacher_id)

    # Pobranie lekcji
    lessons = db.session.query(Lesson).filter(
        Lesson.teacher_id == teacher_id,
        Lesson.date == day
    ).all()

    if not lessons:
        return f"Nauczyciel {teacher.first_name} {teacher.last_name} nie ma lekcji w dniu {day}."
    
    lesson_details = [
        f"{lesson.student.id}. {lesson.student.first_name} {lesson.student.last_name}, przedmiot: {lesson.subject.name}"
        for lesson in lessons
    ]
    return f'<h3>Lekcje prowadzone w dniu {day} przez nauczyciela: {teacher.first_name} {teacher.last_name}</h3><ul>' + ''.join(f'<li>{detail}</li>' for detail in lesson_details) + '</ul>'

# Lista nauczycieli
@app.route('/teacher-list', methods=['GET'])
def teacher_list():
    teachers = Teacher.query.all()
    teacher_data = [
        {
            "id_nauczyciela": teacher.id,
            "imie": teacher.first_name,
            "nazwisko": teacher.last_name,
            "przedmioty": [subject.name for subject in teacher.subjects]
        }
        for teacher in teachers
    ]
    return jsonify({"nauczyciele": teacher_data}), 200

@app.route('/teacher-details', methods=['GET'])
def teacher_details():
    teacher_id = request.args.get('id_nauczyciela', type=int)
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return jsonify({"error": f"Nauczyciel o ID {teacher_id} nie istnieje."}), 404

    teacher_data = {
        "id_nauczyciela": teacher.id,
        "imie": teacher.first_name,
        "nazwisko": teacher.last_name,
        "opis": teacher.description,
        "ocena": teacher.rating,
        "numer_telefonu": teacher.phone_number,
        "stawka": teacher.rate,
        "waluta": teacher.currency,
        "email": teacher.email,
        "przedmioty": [subject.name for subject in teacher.subjects],
        "grafik": [
            {"od": schedule.available_from, "do": schedule.available_to}
            for schedule in teacher.schedule
        ]
    }
    return jsonify(teacher_data), 200

@app.route('/book-lesson', methods=['POST'])
def book_lesson():
    data = request.json
    student_id = data.get('id_studenta')
    teacher_id = data.get('id_nauczyciela')
    date = datetime.strptime(data.get('data'), '%Y-%m-%d').date()
    time = datetime.strptime(data.get('czas'), '%H:%M').time()  # Pobranie godziny lekcji
    subject_name = data.get('nazwa_przedmiotu')

    # Pobranie danych z bazy
    teacher = Teacher.query.get(teacher_id)
    student = Student.query.get(student_id)
    subject = Subject.query.filter_by(name=subject_name).first()

    # Walidacja danych wejściowych
    if not teacher:
        return jsonify({"error": f"Nauczyciel o ID '{teacher_id}' nie istnieje."}), 404
    if not student:
        return jsonify({"error": "Student o podanym ID nie istnieje."}), 404
    if not subject:
        return jsonify({"error": f"Przedmiot '{subject_name}' nie istnieje."}), 400

    # Sprawdzenie grafiku nauczyciela
    schedule = Schedule.query.filter_by(teacher_id=teacher_id).first()
    if not schedule:
        return jsonify({"error": "Grafik nauczyciela nie zostal zdefiniowany."}), 400

    if not (schedule.available_from <= time.strftime('%H:%M') <= schedule.available_to):
        return jsonify({"error": "Termin poza godzinami pracy nauczyciela."}), 400

    # Sprawdzenie, czy termin jest już zajęty
    existing_lesson = Lesson.query.filter_by(
        teacher_id=teacher_id,
        date=date,
        time=time
    ).first()
    if existing_lesson:
        return jsonify({"error": "Termin jest juz zarezerwowany."}), 400

    # Rezerwacja lekcji
    new_lesson = Lesson(
        teacher_id=teacher_id,
        student_id=student_id,
        subject_id=subject.id,
        date=date,
        time=time
    )
    db.session.add(new_lesson)
    db.session.commit()
    return jsonify({"message": "Lekcja zostala pomyslnie zarezerwowana."}), 201

@app.route('/add-teacher', methods=['POST'])
def add_teacher():
    data = request.json
    try:
        first_name = data['imie']
        last_name = data['nazwisko']
        description = data.get('opis', '')
        rating = float(data['ocena'])
        phone_number = data['numer_telefonu']
        rate = data['stawka']
        currency = data['waluta']
        email = data['email']
        subjects = data['przedmioty']
        schedule = data['grafik']

        # Walidacja stawki
        if not isinstance(rate, int):
            return jsonify({"error": "Stawka musi być liczba całkowita."}), 400

        # Walidacja przedmiotów
        subject_objects = Subject.query.filter(Subject.name.in_(subjects)).all()
        if len(subject_objects) != len(subjects):
            return jsonify({"error": "Niektore przedmioty sa niepoprawne."}), 400

        # Tworzenie nauczyciela
        new_teacher = Teacher(
            first_name=first_name,
            last_name=last_name,
            description=description,
            rating=rating,
            phone_number=phone_number,
            rate=rate,
            currency=currency,
            email=email,
            subjects=subject_objects
        )
        db.session.add(new_teacher)
        db.session.flush()  # Pobranie ID nauczyciela przed zatwierdzeniem

        # Dodanie grafiku
        new_schedule = Schedule(
            teacher_id=new_teacher.id,
            available_from=schedule['od'],
            available_to=schedule['do']
        )
        db.session.add(new_schedule)
        db.session.commit()

        return jsonify({"id_nauczyciela": new_teacher.id}), 201
    except KeyError as e:
        return jsonify({"error": f"Brak wymaganego pola: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get-lessons', methods=['GET'])
def get_lessons():
    try:
        # Pobranie i walidacja parametrów wejściowych
        student_id = request.args.get('id_studenta', type=int)
        if not student_id:
            return jsonify({"error": "Brak wymaganego parametru 'id_studenta'."}), 400

        start_date_str = request.args.get('data_początkowa')
        end_date_str = request.args.get('data_końcowa')
        if not start_date_str or not end_date_str:
            return jsonify({"error": "Brak wymaganych parametrów 'data_poczatkowa' lub 'data_koncowa'."}), 400

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Niepoprawny format daty. Użyj formatu 'YYYY-MM-DD'."}), 400

        # Sprawdzenie, czy student istnieje
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"error": f"Student o Id {student_id} nie istnieje."}), 404

        # Pobranie lekcji w podanym zakresie dat
        lessons = Lesson.query.filter(
            Lesson.student_id == student_id,
            Lesson.date.between(start_date, end_date)
        ).all()

        # Przygotowanie danych do odpowiedzi
        lesson_data = [
            {
                "data": lesson.date.strftime('%Y-%m-%d'),
                "godzina": lesson.time.strftime('%H:%M'),
                "id_nauczyciela": lesson.teacher.id,
                "imie_nauczyciela": lesson.teacher.first_name,
                "nazwisko_nauczyciela": lesson.teacher.last_name,
                "przedmiot": lesson.subject.name
            }
            for lesson in lessons
        ]

        return jsonify({"lekcje": lesson_data}), 200

    except Exception as e:
        return jsonify({"error": f"Wystąpił nieoczekiwany błąd: {str(e)}"}), 500

# Uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True)
