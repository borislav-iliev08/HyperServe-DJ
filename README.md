# HyperServe  — Global Culinary Discovery Platform

![HyperServe Banner](https://private-user-images.githubusercontent.com/215028638/683974813-777d6488-108c-415d-9eef-29682b2b6b62.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3OTI5MjAzOTUsIm5iZiI6MTc5MjkyMDA5NSwicGF0aCI6Ii8yMTUwMjg2MzgvNjgzOTc0ODEzLTc3N2Q2NDg4LTEwOGMtNDE1ZC05ZWVmLTI5NjgyYjJiNmI2Mi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYxMDI1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MTAyNVQwOTIxMzVaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0yM2ZhZDNhN2MxNDRmMjI0ZjlmM2EwMTRiMzBhYWVkZWM3OGE0MmE5MTEwYmU4MGEyNmFkMjEzMTNlYjliMTNkJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.THVVvt7aI_3LeObhFO2CFkDu5wHozLZQnBLLlVABQBI)

[![Django](https://img.shields.io/badge/Django-5.2+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](#license)

**HyperServe** is a premier global digital platform uniting restaurants, culinary teams, and diners worldwide. Built using Python and Django, HyperServe provides a centralized ecosystem where food enthusiasts discover top-rated dining spots, explore authentic reviews, and connect with the hospitality professionals (chefs, managers, waiters, bartenders) behind every exceptional meal.

---

##  Interface Preview

Here is a visual overview of the HyperServe platform interface:

###  Landing & Discovery Dashboard
> *Discover top-rated restaurants, top-rated chefs, and recent dining experiences in real time.*

| Home Page Showcase |
| ![Home Page](https://private-user-images.githubusercontent.com/215028638/683975834-e88f8f85-8e94-4b4c-8de7-676d65507f83.PNG?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3OTI5MjA2MTcsIm5iZiI6MTc5MjkyMDMxNywicGF0aCI6Ii8yMTUwMjg2MzgvNjgzOTc1ODM0LWU4OGY4Zjg1LThlOTQtNGI0Yy04ZGU3LTY3NmQ2NTUwN2Y4My5QTkc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYxMDI1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MTAyNVQwOTI1MTdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mNTU2NzI5ZTZkYmZkOGRmNDIyNmVmYjhkMjgzZmI5MTE4ZWMwNWE0NWE5ZWJmMDExMTFkMWJjMTY4YjM4NDEzJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.qw9zTpBgN5aTwz8W-yhKl1MKEnFeIau5YrT8SfvRgss)

---

###  Restaurant & Staff Management
> *Manage restaurant profiles, dynamic perks, cuisine tags, and dedicated staff records.*

| Restaurants Catalog | Restaurant Details|
| :---: | :---: |
| ![Restaurant Directory](https://private-user-images.githubusercontent.com/215028638/683978427-45151c9a-84ac-4a56-95d3-9226d8faa90c.PNG?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3OTI5MjExNzQsIm5iZiI6MTc5MjkyMDg3NCwicGF0aCI6Ii8yMTUwMjg2MzgvNjgzOTc4NDI3LTQ1MTUxYzlhLTg0YWMtNGE1Ni05NWQzLTkyMjZkOGZhYTkwYy5QTkc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYxMDI1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MTAyNVQwOTM0MzRaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1hZGU1MTZhNzc5MDMxOTZjNWY0NmQ4MWQyODIxYmU4MjU0YWIwOTMxYTk4ZWRlYjJlZmNlZTdmNjU4ZGNmMTNmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.Ag9XuLZgmgBx4o3HuAYYuLL-aZTbOfL1sC08ZPghs3w) | ![Restaurant Detail View](https://private-user-images.githubusercontent.com/215028638/683978754-38340193-ca8f-4469-8e1c-57916d7a6ed0.PNG?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3OTI5MjEyNzgsIm5iZiI6MTc5MjkyMDk3OCwicGF0aCI6Ii8yMTUwMjg2MzgvNjgzOTc4NzU0LTM4MzQwMTkzLWNhOGYtNDQ2OS04ZTFjLTU3OTE2ZDdhNmVkMC5QTkc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYxMDI1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MTAyNVQwOTM2MThaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT02ZDQzMDlmMmY5NTI2ZTA4MjE0MTY4MTFmOTg0ZTZkM2Y5Mzg0ZWI0NzhjMjc1ZDczZWZkMGM0Njc0NDU2YzBmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.nrPT-ZL_2yj3J6n4QLjqEumKumC7EDYCIijcaERL-KA) |

| Staff Directory | Employee Profile & Reviews |
| :---: | :---: |
| ![Staff Directory](docs/images/employees_list.png) | ![Employee Detail View](docs/images/employee_detail.png) |

---

###  Moderated Review System
> *Community-driven review platform featuring automated keyword moderation and star rating aggregation.*

| Community Reviews Catalog | Flagged Content Moderation |
| :---: | :---: |
| ![Review Catalog](docs/images/reviews_list.png) | ![Moderation & Filtering](docs/images/reviews_moderation.png) |

---

##  Key Features

- ** Global Restaurant Directory:** Detailed profiles with custom slugs (`/restaurants/restaurant-name-cuisine/`), cuisine types, operating addresses, owner credentials, and dynamic perks.
- ** Professional Hospitality Staffing:** Employee management categorized by roles (Chef, Sous Chef, Bartender, Waiter, Manager, Host, Cleaner) linked directly to their respective venues.
- ** Dual Review Engine:** Separate evaluation engines for **Venue Experience** and **Staff Performance**, calculating average ratings dynamically via Django `Avg` annotations.
- ** Automated Content Moderation:** Built-in bad word filtering automatically marks abusive or inappropriate reviews with an `is_flagged` flag without blocking submission.
- ** Domain Verification:** Strict email validation enforcing real/supported email providers (`@gmail.com`, `@yahoo.com`, `@outlook.com`, `@hypserve.com`, etc.).
- ** Read-Only Form Safety:** Custom `DisabledFormMixin` for confirmation workflows (delete/disable views) preserving UI consistency without code duplication.
- ** Comprehensive Search & Filtering:** Filter by cuisine types, employee positions, active perks, and flagged review statuses with optimized pagination.

---

##  Tech Stack & Architecture

- **Backend:** Python 3.10+, Django 5.2 (Class-Based Views, Mixins, ORM Aggregation)
- **Database:** PostgreSQL
- **Frontend:** HTML5, CSS3, Bootstrap 5 / Custom Styling
- **Architecture Pattern:** MVT (Model-View-Template) with modular app structure (`restaurants`, `employees`, `reviews`)

---


##  Installation & Setup Guide

### 1. Prerequisites
Ensure you have the following installed:
- Python 3.10 or higher
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/borislav-iliev08/hyperservedj.git
cd hyperservedj
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup & Migrations
Create your PostgreSQL database named `hyperserve_db`, then run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin Access)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit the platform in your browser at `http://127.0.0.1:8000/`.

---

##  Author & Connect

**Borislav Iliev** — Software Developer & Creator of HyperServe

- **Instagram:** [@b_.iliew._](https://www.instagram.com/b_.iliew._?xtok=MWszZHR0OGxkOTMwNQ==)
- **Facebook:** [Borislav Iliev Profile](https://www.facebook.com/share/1FChyJ1qt9/)
- **GitHub:** [@borislav-iliev08](https://github.com/borislav-iliev08)
- **Email:** borislav718@gmail.com
---

##  License

This project is open-source and available under the [MIT License](LICENSE).
