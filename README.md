<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:020B12,20:061722,40:07303A,60:005C68,75:00A6A6,88:00D9C0,100:063B42&height=130&section=header&animation=fadeIn"/>

</div>

# ⚡ ORM Workbench

### A Dynamic Django ORM Playground

<p align="center">
  <strong>Learn • Experiment • Query • Understand Django ORM</strong>
</p>

<p align="center">
  A browser-based interactive playground for experimenting with Django ORM,
  models, relationships, database schemas, and queries — without repeatedly
  creating Django projects or manually managing migrations for every experiment.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

</p>

---

# 🌌 Project Preview

<p align="center">
  <img
    src="https://res.cloudinary.com/xpehvn66/image/upload/v1786135608/Screenshot_From_2026-08-08_02-13-53_zefyyg.png"
    alt="ORM Workbench Compiler Interface"
    width="100%"
  >
</p>

> **ORM Workbench** brings Django ORM experimentation into an interactive browser-based development environment.

Define models, compile them, inspect the generated database structure, write ORM queries, execute them, and immediately inspect the results.

---

# ✨ Features

### 🧩 Live Model Playground

Define Django models directly inside the browser.

```python
class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
```

The Workbench dynamically processes the model definition and creates the required database structure.

---

### 🔎 Interactive ORM Query Console

Execute Django ORM queries directly from the browser.

```python
Author.objects.all()
```

```python
Author.objects.filter(age__gte=25)
```

```python
Book.objects.select_related("author")
```

```python
Author.objects.annotate(
    book_count=Count("book")
)
```

---

### 🛡️ AST-Based Code Validation

Submitted Python code is inspected using Python's built-in `ast` module before execution.

```text
Submitted Code
      │
      ▼
 Python AST
      │
      ▼
 AST Validator
      │
 ├── Allowed
 │     │
 │     ▼
 │  Execution
 │
 └── Restricted
       │
       ▼
     Rejected
```

This provides a validation layer around dynamically executed Python code.

> ⚠️ The project is intended for learning and controlled experimentation. It should not be treated as a production-grade arbitrary-code execution sandbox.

---

### 🗄️ Dynamic Database Schema

Create database tables for dynamically defined models without manually creating migrations for every experiment.

```text
Define Model
     ↓
Validate
     ↓
Create Model
     ↓
Create Database Table
     ↓
Inspect Schema
```

---

### 🌱 Mock Database Seeding

ORM Workbench provides default models and sample records so you can start experimenting immediately.

Example relationships:

```text
Author
  │
  └── Book
        │
        └── Library
```

This allows users to experiment with filtering, relationships, joins, aggregation, and QuerySets without manually preparing test data.

---

### 🔗 Relationship Support

Experiment with Django relationships such as:

- `ForeignKey`
- `ManyToManyField`
- Reverse relationships
- Related lookups
- `select_related()`
- `prefetch_related()`

---

### 📊 Interactive Result Tables

Query results are displayed directly inside the Workbench.

Inspect:

- Model fields
- Field types
- Relationships
- Database records
- Query results
- Generated schema information

---

### 🖥️ Developer-Style Interface

The compiler interface is designed around a developer-tool workflow with:

- Model editor
- ORM query editor
- Result viewer
- Console output
- Database information
- Documentation
- Resizable panels
- Dark UI

---

### 🔄 Database Reset

Reset the playground and restore the default database state after experimentation.

This makes repeated ORM experiments much easier.

---

### 🧱 Service-Oriented Architecture

Business logic is separated from Django views through dedicated services.

```text
Views
  │
  ▼
Compiler Service
  │
  ├── Model Service
  ├── Database Service
  ├── Serializer
  └── Sandbox
        │
        └── AST Validator
```

---

# 🛠️ Technology Stack

## Backend

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Django | Web framework |
| Django ORM | Database abstraction and querying |
| Python AST | Code validation |

## Database

| Technology | Purpose |
|---|---|
| PostgreSQL | Relational database |
| psycopg | PostgreSQL database driver |
| Neon PostgreSQL | Cloud PostgreSQL |

## Frontend

| Technology | Purpose |
|---|---|
| HTML5 | Page structure |
| CSS3 | UI and styling |
| Vanilla JavaScript | Frontend interaction |

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │       Browser       │
                         │                     │
                         │  Model Editor       │
                         │  ORM Query Console  │
                         │  Result Viewer      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │        Views        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │     Compiler Service       │
                     └──────────────┬─────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
       │ Model Service│     │   Database   │     │  Serializer  │
       │              │     │   Service    │     │              │
       └──────────────┘     └──────────────┘     └──────────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │     Sandbox     │
                           │                 │
                           │ AST Validator   │
                           │ Controlled Exec │
                           └────────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │   Django ORM    │
                           └────────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │   PostgreSQL    │
                           └─────────────────┘
```

---

# 🔄 How It Works

```text
┌──────────────────┐
│  Define Django   │
│      Model       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  AST Validation  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Dynamic Model     │
│    Creation      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Database Schema   │
│     Creation      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Inspect Tables    │
│ & Relationships   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Write ORM Query   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Execute Query     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ View Results      │
└──────────────────┘
```

---

# 📁 Project Structure

```text
ORM_WORKBENCH/
└── orm_workbench/
    │
    ├── manage.py
    ├── requirements.txt
    │
    ├── config/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    │
    ├── templates/
    │   ├── compiler.html
    │   └── documentation.html
    │
    ├── static/
    │   ├── css/
    │   ├── js/
    │   └── images/
    │
    └── applications/
        │
        ├── compiler/
        │   │
        │   ├── sandbox/
        │   │   ├── executor.py
        │   │   └── validator.py
        │   │
        │   ├── serializers/
        │   │   └── serializer.py
        │   │
        │   ├── services/
        │   │   ├── compiler_service.py
        │   │   ├── database.py
        │   │   └── model_service.py
        │   │
        │   ├── models.py
        │   ├── views.py
        │   └── urls.py
        │
        └── documentation/
            ├── views.py
            └── urls.py
```

---

# 🚀 Getting Started

## Prerequisites

Make sure you have:

- Python 3.x
- PostgreSQL
- Git
- `pip`
- Virtual environment support

---

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/orm-workbench.git
```

Enter the project:

```bash
cd orm-workbench
```

---

## 2. Create a Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

ORM Workbench uses a `.env` file for environment-specific configuration and sensitive values such as database credentials.

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@host:5432/database_name
```

You can also add other environment-specific configuration values to this file as required by your setup.

> ⚠️ Never commit your `.env` file or expose your credentials publicly.

Add `.env` to `.gitignore`:

```gitignore
.env
```

---

# 🗄️ Database Setup

ORM Workbench uses PostgreSQL by default.

## Option 1 — PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE orm_workbench;
```

Then configure the database in:

```text
config/settings.py
```

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "orm_workbench",
        "USER": "postgres",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

---

## OR — Use a Database URL

You can also configure PostgreSQL using a database URL. This is useful when using cloud database providers such as **Neon PostgreSQL**.

Install `dj-database-url`:

```bash
pip install dj-database-url
```

Add it to `requirements.txt`:

```text
dj-database-url
```

Create or update your `.env` file:

```env
DATABASE_URL=postgresql://username:password@host:5432/database_name
```

For example, a Neon PostgreSQL connection string may look like:

```env
DATABASE_URL=postgresql://user:password@your-neon-host/database_name?sslmode=require
```

Then configure Django:

```python
import os
import dj_database_url

DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL")
    )
}
```

> ⚠️ Keep your `.env` file private and never commit database credentials to GitHub.

---

## OR — Use SQLite

If you don't want to configure PostgreSQL, you can use SQLite for local experimentation.

Replace the database configuration with:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

SQLite requires no separate database server and is useful for quickly running the project locally.

---

### Database Options

| Database | Recommended For |
|---|---|
| PostgreSQL | Default / Full project usage |
| Neon PostgreSQL | Cloud / Deployment |
| SQLite | Quick local experimentation |

After configuring your database, run:

```bash
python manage.py migrate
```

Then start the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 🧪 Using the Workbench

## Step 1 — Define a Model

Inside the model editor:

```python
class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
```

---

## Step 2 — Compile

The submitted model is:

```text
Python Code
     ↓
AST Validation
     ↓
Dynamic Model Creation
     ↓
Database Schema Creation
```

---

## Step 3 — Inspect the Database

Explore:

```text
Table
├── Columns
├── Data Types
├── Primary Key
├── Foreign Keys
└── Relationships
```

---

## Step 4 — Write an ORM Query

Try:

```python
Author.objects.all()
```

Then:

```python
Author.objects.filter(age__gt=20)
```

---

## Step 5 — Experiment

Progress from simple queries to advanced ORM concepts:

```text
Filtering
   ↓
Lookups
   ↓
Ordering
   ↓
Relationships
   ↓
select_related()
   ↓
prefetch_related()
   ↓
Aggregation
   ↓
Annotation
   ↓
Complex Queries
```

---

# 📚 ORM Learning Guide

ORM Workbench is particularly useful for learning Django ORM incrementally.

## Basic Queries

```python
Author.objects.all()

Author.objects.get(id=1)

Author.objects.filter(age__gte=18)

Author.objects.exclude(age=20)

Author.objects.create(
    name="John",
    age=25
)
```

---

## Query Lookups

Experiment with:

- `exact`
- `contains`
- `icontains`
- `startswith`
- `endswith`
- `gt`
- `gte`
- `lt`
- `lte`
- `in`
- `isnull`

Example:

```python
Author.objects.filter(
    name__icontains="john"
)
```

---

## QuerySet Operations

Explore:

```python
order_by()
values()
values_list()
distinct()
exists()
count()
first()
last()
```

---

## Relationships

Practice:

- `ForeignKey`
- `ManyToManyField`
- Reverse relationships
- Related lookups

Example:

```python
Book.objects.filter(
    author__name="John"
)
```

---

## Query Optimization

Experiment with:

```python
Book.objects.select_related("author")
```

and:

```python
Author.objects.prefetch_related("books")
```

This makes ORM Workbench useful for understanding the **N+1 query problem** and Django relationship optimization.

---

## Aggregation & Annotation

Practice:

```python
Author.objects.annotate(
    book_count=Count("book")
)
```

And:

```python
Book.objects.aggregate(
    total=Count("id")
)
```

---

## Advanced ORM

Explore:

- `Q`
- `F`
- `Count`
- `Sum`
- `Avg`
- `Min`
- `Max`
- `annotate()`
- `aggregate()`
- Subqueries
- Conditional expressions

Example:

```python
Author.objects.filter(
    Q(age__gt=30) |
    Q(name__icontains="john")
)
```

---

# 💡 Example Experiments

### Filtering

```python
Book.objects.filter(
    title__icontains="django"
)
```

### Ordering

```python
Book.objects.order_by("-published_date")
```

### Related Lookup

```python
Book.objects.filter(
    author__name="John"
)
```

### select_related

```python
Book.objects.select_related("author")
```

### Annotation

```python
Author.objects.annotate(
    book_count=Count("book")
)
```

### Q Objects

```python
Author.objects.filter(
    Q(age__gt=30) |
    Q(name__icontains="john")
)
```

---

# 🔐 Security Notes

ORM Workbench dynamically executes Python code supplied through the playground.

The project therefore includes:

```text
Submitted Python
       │
       ▼
   AST Parser
       │
       ▼
 AST Validator
       │
       ├── Restricted Nodes
       ├── Restricted Imports
       ├── Restricted Operations
       └── Allowed Operations
       │
       ▼
 Controlled Execution
```

The validator is designed to prevent known restricted operations before execution.

However:

> ⚠️ **AST validation alone is not a complete security boundary for arbitrary Python execution.**

Python's `exec()` and `eval()` can be dangerous when exposed to untrusted users.

Therefore, ORM Workbench should primarily be used for:

- Local development
- Learning
- ORM experimentation
- Controlled environments
- Demonstrations

If deploying an arbitrary-code playground publicly, stronger isolation such as containers, restricted processes, resource limits, and network isolation should be considered.

---

# 🎯 Why ORM Workbench?

Traditional ORM experimentation often looks like:

```text
Create Project
      ↓
Create App
      ↓
Create Models
      ↓
Create Migrations
      ↓
Run Migrations
      ↓
Create Test Data
      ↓
Open Django Shell
      ↓
Write Query
      ↓
Inspect Result
```

ORM Workbench simplifies this into:

```text
Open Browser
     ↓
Define Model
     ↓
Compile
     ↓
Write Query
     ↓
Run
     ↓
Inspect
```

The goal is to make Django ORM experimentation **faster, visual, interactive, and easier to understand**.

---

# 🎓 What You Can Learn

Using this project, you can explore:

```text
Django Models
      │
      ├── Fields
      ├── Relationships
      └── Metadata
            │
            ▼
        Django ORM
            │
            ├── QuerySets
            ├── Lookups
            ├── Filtering
            ├── Relationships
            ├── Aggregation
            ├── Annotation
            └── Optimization
                    │
                    ▼
                SQL Database
```

---

# 📸 Screenshots

## Compiler

<p align="center">
  <img
    src="https://res.cloudinary.com/xpehvn66/image/upload/v1786135608/Screenshot_From_2026-08-08_02-13-53_zefyyg.png"
    alt="ORM Workbench Compiler"
    width="100%"
  >
</p>

---

<p align="center">
  <img
    src="https://res.cloudinary.com/xpehvn66/image/upload/v1786135800/Screenshot_From_2026-08-08_02-19-07_jxdwhr.png"
    alt="ORM Workbench Compiler"
    width="100%"
  >
</p>

---

# 🎬 Demo

A short looping GIF can make the README more interactive.

The ideal recording:

```text
┌────────────────────┐
│ Define Model       │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Click Compile      │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Table Created      │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Write ORM Query    │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Execute Query      │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Results Displayed  │
└────────────────────┘
```

A **5–10 second seamless loop** is enough to demonstrate the project's main workflow.

---

# 🤝 Contributing

Contributions are welcome.

### 1. Fork the repository

```bash
git clone https://github.com/YOUR_USERNAME/orm-workbench.git
```

### 2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

### 3. Make your changes

### 4. Commit your changes

```bash
git add .
git commit -m "feat: add new ORM feature"
```

### 5. Push the branch

```bash
git push origin feature/new-feature
```

### 6. Open a Pull Request

---

# 🧹 Development Guidelines

When contributing:

- Keep views thin.
- Keep business logic inside services.
- Keep serialization responsibilities separate.
- Validate dynamic code before execution.
- Keep security restrictions explicit.
- Use clear commit messages.
- Document new ORM functionality.
- Avoid unnecessary logic inside templates.

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

## Ambadi Kannan M

**Python Developer • Django Developer • Backend Enthusiast**

<p align="center">

⭐ If you found ORM Workbench useful, consider giving the repository a star!

</p>

---

<p align="center">

### ⚡ ORM Workbench

**Experiment with Django ORM. Understand what happens underneath.**

</p>

<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:063B42,12:00D9C0,25:00A6A6,40:005C68,60:07303A,80:061722,100:020B12&height=130&section=footer&animation=fadeIn"/>

</div>