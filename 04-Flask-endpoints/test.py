import requests
import json

# Nagłówek Authorization
headers = {
    "Authorization": "Julia Chilczuk"
}
# Dodanie danych do bazy
def add_data():
    url = 'http://localhost:5000/add_data'
    response = requests.get(url, headers=headers)
    print("\nDodawanie danych do bazy...")
    print(response.text)
    print("Status code:", response.status_code)

# 1. Testowanie endpointu /teacher-list
def test_teacher_list():
    url = 'http://localhost:5000/teacher-list'
    response = requests.get(url, headers=headers)
    print("\nTest /teacher-list:")
    print(response.text)
    print("Status code:", response.status_code)

# 2. Testowanie endpointu /teacher-details
def test_teacher_details():
    url = 'http://localhost:5000/teacher-details'

    # Przypadek pozytywny
    params = {"id_nauczyciela": 1}  # Nauczyciel o ID 1 istnieje
    response = requests.get(url, headers=headers, params=params)
    print("\nTest /teacher-details (pozytywny):")
    print(response.text)
    print("Status code:", response.status_code)

    # Przypadek negatywny
    params = {"id_nauczyciela": 999}  # Nauczyciel o ID 999 nie istnieje
    response = requests.get(url, headers=headers, params=params)
    print("\nTest /teacher-details (negatywny):")
    print(response.text)
    print("Status code:", response.status_code)

# 3. Testowanie endpointu /book-lesson
def test_book_lesson():
    url = 'http://localhost:5000/book-lesson'

    # Przypadek pozytywny
    data = {
        "id_studenta": 1,
        "id_nauczyciela": 1,
        "data": "2025-04-22",
        "czas": "10:00",
        "nazwa_przedmiotu": "matematyka"
    }
    response = requests.post(url, headers=headers, json=data)
    print("\nTest /book-lesson (pozytywny):")
    print(response.text)
    print("Status code:", response.status_code)

    # Przypadek negatywny: Termin poza godzinami pracy nauczyciela
    data = {
        "id_studenta": 3,
        "id_nauczyciela": 2,
        "data": "2025-04-22",
        "czas": "04:00",
        "nazwa_przedmiotu": "matematyka"
    }
    response = requests.post(url, headers=headers, json=data)
    print("\nTest /book-lesson (Termin poza godzinami pracy nauczyciela):")
    print(response.text)
    print("Status code:", response.status_code)

    # Przypadek negatywny: Termin już zajęty
    data = {
        "id_studenta": 1,
        "id_nauczyciela": 1,
        "data": "2025-04-07",
        "czas": "10:00",
        "nazwa_przedmiotu": "matematyka"
    }
    response = requests.post(url, headers=headers, json=data)
    print("\nTest /book-lesson (Termin już zajęty):")
    print(response.text)
    print("Status code:", response.status_code)

    # Przypadek negatywny: Niepoprawny przedmiot
    data = {
        "id_studenta": 1,
        "id_nauczyciela": 1,
        "data": "2025-04-22",
        "czas": "10:00",
        "nazwa_przedmiotu": "religia"
    }
    response = requests.post(url, headers=headers, json=data)
    print("\nTest /book-lesson (Niepoprawny przedmiot):")
    print(response.text)
    print("Status code:", response.status_code)

# 4. Testowanie endpointu /add-teacher
def test_add_teacher():
    url = 'http://localhost:5000/add-teacher'

    # Przypadek pozytywny
    data = {
        "imie": "Adam",
        "nazwisko": "Nowak",
        "opis": "Doświadczony nauczyciel",
        "ocena": 4.5,
        "numer_telefonu": "123456789",
        "stawka": 50,
        "waluta": "PLN",
        "email": "adam.nowak@example.com",
        "przedmioty": ["matematyka", "fizyka"],
        "grafik": {"od": "08:00", "do": "16:00"}
    }
    response = requests.post(url, headers=headers, json=data)
    print("\nTest /add-teacher (pozytywny):")
    print(response.text)
    print("Status code:", response.status_code)

    # Przypadek negatywny
    data = {
        "imie": "Adam",
        "nazwisko": "Nowak",
        # Brak wymaganych pól
    }
    response = requests.post(url, headers=headers, json=data)
    print("\nTest /add-teacher (negatywny):")
    print(response.text)
    print("Status code:", response.status_code)

     # Przypadek negatywny
    data = {
        "imie": "Adam",
        "nazwisko": "Nowak",
        "opis": "Doświadczony nauczyciel",
        "ocena": 4.5,
        "numer_telefonu": "123456789",
        "stawka": 50,
        "waluta": "PLN",
        "email": "adam.nowak@example.com",
        "przedmioty": ["matematyka", "religia"],  # Niepoprawny przedmiot
        "grafik": {"od": "08:00", "do": "16:00"}
    }
    response = requests.post(url, headers=headers, json=data)
    print("\nTest /add-teacher (negatywny):")
    print(response.text)
    print("Status code:", response.status_code)

# 5. Testowanie endpointu /get-lessons
def test_get_lessons():
    url = 'http://localhost:5000/get-lessons'

    # Przypadek pozytywny
    params = {
        "id_studenta": 3,
        "data_początkowa": "2025-04-01",
        "data_końcowa": "2025-04-30"
    }
    response = requests.get(url, headers=headers, params=params)
    print("\nTest /get-lessons (pozytywny):")
    print(response.text)
    print("Status code:", response.status_code)

    # Przypadek negatywny
    params = {
        "id_studenta": 999,  # Nieistniejący student
        "data_początkowa": "2025-04-01",
        "data_końcowa": "2025-04-30"
    }
    response = requests.get(url, headers=headers, params=params)
    print("\nTest /get-lessons (negatywny):")
    print(response.text)
    print("Status code:", response.status_code)



# Uruchomienie testów
if __name__ == "__main__":
    add_data()
    test_teacher_list()
    test_teacher_details()
    test_book_lesson()
    test_add_teacher()
    test_get_lessons()
    