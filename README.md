[![Баннер](https://i.ibb.co/Pj5033T/slide.png)](presentation.pptx)  

[![SvelteIcon](https://img.shields.io/static/v1?label=&message=Svelte&color=white&style=flat&logo=svelte)](https://svelte.dev/)  [![FastAPIIcon](https://img.shields.io/static/v1?label=&message=FastAPI&color=white&style=flat&logo=fastapi)](https://fastapi.tiangolo.com/) [![SwaggerIcon](https://img.shields.io/static/v1?label=&message=Swagger&color=white&style=flat&logo=swagger)](https://swagger.io/) [![DockerIcon](https://img.shields.io/static/v1?label=&message=Docker&color=white&style=flat&logo=docker)](https://www.docker.com/)
## 📖 О проекте

**[Платформа парсинга документов](http://159.65.63.72)** предназначена для автоматизации рутинной работы по распределению документов от частной комании.
Позволяет определять типы в системе документооборота, регистрировать их в карточках и распределять до конечных точек.

## ⚙️ Текущий функционал платформы 

* Поддержка нескольких форматов документов 
* Адаптивный конвеер данных, под разные типы 
* Исправление ошибок и опечаток
* Удаление шума и артефактов при помощи *BERT*
* Вычисление расстояний до целевых классов 
* Регистрация документов в банковской системе
* Поиск и просмотр статистики по компаниям
* Автоматическое формирование отчетов

## 🚀 Запуск вручную
Установите библиотеку *ocrmypdf*. [Инструкция](https://ocrmypdf.readthedocs.io/en/latest/installation.html) по установке.
Выполните следующие команды в терминале. Необходимы *Python 3.8* и *NodeJS 14*
```bash
$: cd frontend
$: npm install
$: npm run build
$: cd ..
$: pip install -r requirements.txt
$: python app.py
```
## 🐳 Запуск с помощью Docker

Соберите образ и запустите контейнер
```bash
$: docker build -t service .
$: docker run -p 8000:8000 service
```

