from utils import JSONSaver, HeadHunterAPI, SuperJobAPI
from utils import filter_vacancies, sort_vacancies_by_salary


def interact_with_user():
    """Функция для взаимодействия с пользователем"""
    json_saver = JSONSaver("vacancies.json")
    vacancies = json_saver.load_from_file()

    while True:
        print()
        print("Выберите действие:")
        print("1. Получить вакансии с HeadHunter")
        print("2. Получить вакансии с SuperJob")
        print("3. Добавить вакансии в файл")
        print("4. Фильтровать вакансии по ключевому слову")
        print("5. Отсортировать вакансии по убыванию размера зарплаты")
        print("0. Выход")
        print()

        choice = input("Введите номер действия >>> ")

        if choice == "1":
            search_query = input("Введите ключевое слово для поиска >>> ")
            # Создание экземпляра класса для работы с HeadHunter API вакансиями
            hh_api = HeadHunterAPI()
            vacancies = hh_api.get_vacancies(search_query)
            for vacancy in vacancies:
                print(vacancy)
        elif choice == "2":
            search_query = input("Введите ключевое слово для поиска >>> ")
            # Создание экземпляра класса для работы с SuperJobAPI API с вакансиями
            superjob_api = SuperJobAPI("v3.r.12260473.e86d4e94c6265d8a7b5973fae265843f4a4f29fc"
                                       ".68b34e6a3bcc5a28606cd81082a6573fb7ed82ab")
            vacancies = superjob_api.get_vacancies(search_query)
            for vacancy in vacancies:
                print(vacancy)
        elif choice == "3":
            json_saver.save_to_file(vacancies)
        elif choice == "4":
            keywords = input("Введите ключевые слова через запятую >>> ").split(",")
            filtered_vacancies = filter_vacancies(vacancies, keywords)
            for vacancy in filtered_vacancies:
                print()
                print(f"Employer: {vacancy.employer}")
                print(f"Title: {vacancy.title}")
                print(f"Link: {vacancy.link}")
                print(f"Salary: {vacancy.salary}")
                print(f"Salary_from: {vacancy.salary_from}")
                print(f"Salary_to: {vacancy.salary_to}")
                print(f"Description: {vacancy.description}")
                print()
        elif choice == "5":
            sorted_vacancies = sort_vacancies_by_salary(vacancies)
            for vacancy in sorted_vacancies:
                print(vacancy)
        elif choice == "0":
            break
        else:
            print()
            print("Неверный номер действия. Попробуйте еще раз.")
            print()


if __name__ == "__main__":
    interact_with_user()
