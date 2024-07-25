В репозитории представлен код сайта, посвящённого тренировкам. Сайт можно посмотреть по ссылке https://myworkout.beagun.ru/.

На сайте реализованы:
- каталог упражнений
- деление упражнений по категориям, уровень вложенности категорий по мышечной группе можно увеличивать, добавляя подкатегории в админ-панели; отображение информации об упражнении; пагинация
  
  ![image](https://github.com/beAgun/django_workout_/assets/140337252/6199d3e5-6c52-4981-9229-68c43d1e8bcd)

- авторизация и регистрация, редактирование профиля, смена и восстановление пароля
  
  ![image](https://github.com/beAgun/django_workout_/assets/140337252/6851aec2-ce96-4bba-9704-3b9916ff4227)

- возможность вести дневник тренировок, отображение тренировок по неделям, детальное отображение тренировки, добавление упражнений и подходов, а также возможности редактирования и удаления записей
  
  ![image](https://github.com/beAgun/django_workout_/assets/140337252/744a20d6-5dd5-4fd7-b342-ace0075b0b8a)
  
  ![image](https://github.com/beAgun/django_workout_/assets/140337252/0840748d-f30f-4e7c-9735-302cf73359c9)

- оптимизированы запросы к базе данных с помощью debug toolbar
  - Например, по адресу http://127.0.0.1:8000/catalogue/ к БД было сделано 19 запросов:
    
    ![image](https://github.com/beAgun/django_workout_/assets/140337252/a9c7dd41-a5d4-4dbd-801f-bb5ccf2b6aad)
    
    ![image](https://github.com/beAgun/django_workout_/assets/140337252/b5fdb0ad-9516-467b-8d84-be2e0e603e55)
    
    После оптимизации (при том же содержании страницы) 10 запросов:
    
    ![image](https://github.com/beAgun/django_workout_/assets/140337252/d1082f7f-de5f-48e3-a7ad-92046ed8ce2c)
    
  - По адресу http://127.0.0.1:8000/equipment/shtanga/ к БД было сделано 14 запросов:
    
    ![image](https://github.com/beAgun/django_workout_/assets/140337252/d6e0c48d-7ccc-4dd0-abdd-bd7c03c38a5c)
    
    ![image](https://github.com/beAgun/django_workout_/assets/140337252/e7ee68c2-ce97-4deb-a46c-84588c9cd147)
    
    После оптимизации 11 запросов:
    
    ![image](https://github.com/beAgun/django_workout_/assets/140337252/91be22db-56fc-4423-9e2a-fb4d6e14c27b)
    
  - По адресу http://127.0.0.1:8000/tracker/workout/2/ к БД был сделан 21 запрос:
    
    ![image](https://github.com/beAgun/django_workout_/assets/140337252/f586b10a-95d4-42db-b504-2c891368525c)
    
    ![image](https://github.com/beAgun/django_workout_/assets/140337252/0956d5b8-1621-4a6f-b347-48b030f7c865)
    
    После оптимизации 7 запросов:
    
    ![image](https://github.com/beAgun/django_workout_/assets/140337252/9b7c258d-6cc5-4b40-85de-f2182f144e75)

- Адаптивная вёрстка
  
  Например, мобильная версия:
  
  ![image](https://github.com/beAgun/django_workout_/assets/140337252/d7e33ac5-0dcb-4a85-b90f-eeb706492acf)
  
- В БД данные подгружены из json файла, который был сформирован автоматически с помощью распознования текста отсканированной книги и библиотеки regex.


