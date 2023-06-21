from abc import ABC, abstractmethod
import requests
import json
from typing import List


class JobAPI(ABC):

    @abstractmethod
    def get_vacancies(self, search_query):
        pass


class HeadHunterAPI(JobAPI):
    def __init__(self):
        self.base_url = "https://api.hh.ru"

    def get_vacancies(self, keyword):
        """Функция для парсинга вакансия с api.hh.ru"""
        url = f"{self.base_url}/vacancies"
        params = {
            "page": None,
            "text": keyword,
            "area": 1,  # Moscow
            "per_page": 100,
            "archived": False,
        }
        response = requests.get(url, params=params)
        data = response.json()
        vacancies = []
        for item in data["items"]:
            salary = item.get("salary")
            salary_from = salary.get("from") if salary else None
            salary_to = salary.get("to") if salary else None
            vacancy = Vacancy(
                id=item["id"],
                employer=item["employer"]["name"],
                title=item["name"],
                link=item["alternate_url"],
                salary=item["salary"],
                salary_from=salary_from,
                salary_to=salary_to,
                description=item["snippet"],
                snippet=item["snippet"]
            )
            vacancies.append(vacancy)
        return vacancies


class SuperJobAPI:
    def __init__(self, api_key: str):
        self.base_url = "https://api.superjob.ru/2.0"
        self.api_key = api_key

    def get_vacancies(self, search_query: str) -> List['Vacancy']:
        """Функция для парсинга вакансия с api.superjob.ru"""
        headers = {"X-Api-App-Id": self.api_key}
        params = {
            "keyword": search_query,
            "town": 4,  # Moscow
            "count": 100,
            "catalogues": 33,  # IT, Internet
            "show_agreement_period": 1
        }
        response = requests.get(f"{self.base_url}/vacancies", headers=headers, params=params)
        print(response.status_code)
        response.raise_for_status()

        data = response.json()

        vacancies = []
        for item in data["objects"]:

            vacancy = Vacancy(
                id=item["id"],
                employer=item.get("firm_name", {}),
                title=item.get("profession", ""),
                link=item.get("link", ""),
                salary_from=item.get("payment_from", None),
                salary_to=item.get("payment_to", None),
                salary=item["payment_from"] or item["payment_to"],
                description=item.get("description", ""),
                snippet=item.get("snippet", "")
            )
            vacancies.append(vacancy)
        return vacancies


class Vacancy:
    def __init__(self, id, employer, title, link, salary_from, salary_to, salary, description, snippet):
        self.id = id
        self.employer = employer
        self.title = title
        self.link = link
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary = salary
        self.description = description
        self.snippet = snippet

    def get_salary(self):
        if isinstance(self.salary, dict):
            return self.salary.get('from')
        return None

    def __str__(self):
        return f"Employer: {self.employer}\nTitle: {self.title}\nLink: {self.link}\nSalary: {self.salary}" \
               f"\nSalary_from: {self.salary_from}\nSalary_to: {self.salary_to}\nDescription: {self.description}\n"


class JSONSaver:
    """Класс для работы с файлом JSON"""

    def __init__(self, file_name):
        self.file_name = file_name

    def save_to_file(self, vacancies):
        """Сохраняет вакансии в JSON-файл"""
        data = []
        for vacancy in vacancies:
            item = {
                'id': vacancy.id,
                'employer': vacancy.employer,
                'title': vacancy.title,
                'link': vacancy.link,
                'salary': vacancy.salary,
                'salary_from': vacancy.salary_from,
                'salary_to': vacancy.salary_to,
                'description': vacancy.description,
                'snippet': vacancy.snippet,
            }
            data.append(item)
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Вакансии сохранены в файл: {self.file_name}")

    def load_from_file(self):
        """Выгружает вакансии из JSON-файла"""
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                data = json.load(file)
                vacancies = []

                for item in data:
                    vacancy = Vacancy(
                        id=item.get('id', ''),
                        employer=item.get('employer', ''),
                        title=item.get('title', ''),
                        link=item.get('link', ''),
                        salary=item.get('salary', {}),
                        salary_from=item.get('payment_from', {}),
                        salary_to=item.get('payment_to', {}),
                        description=item.get('description', ''),
                        snippet=item.get('snippet', ''),
                    )
                    vacancies.append(vacancy)

                return vacancies
        except FileNotFoundError:
            return []


def filter_vacancies(vacancies, keywords):
    """Фильтрует вакансии по ключевым словам"""
    filtered_vacancies = []
    for vacancy in vacancies:
        for keyword in keywords:
            if keyword.lower() in vacancy.title.lower():
                filtered_vacancies.append(vacancy)
                break
    return filtered_vacancies


def sort_vacancies_by_salary(vacancies):
    return sorted(vacancies, key=lambda x: x.salary_from or 0, reverse=True)


