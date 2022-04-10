# gosuslugi-find-free-timeslot
Поиск свободного слота для записи через госуслуги 

По мотивам хабрапоста
https://habr.com/ru/post/554406/

Последнее время часто случается, что записаться на прием на подачу документов на нужную тебе услугу
(новый загранпаспорт например) невозможно, т.к. в нужном отделении просто нет ни одного таймслота на следующий месяц.

Знающие люди в очереди говорят, что слоты выкладывают или по будням в 8-00 или ночью с пятницы на субботу в 00-00,
или ночью с субботы на воскресенье в 00-00.

Данный скриптец автоматизирует проверку доступности слота на госуслугах и шлет email нотификацию, если слоты доступны.
Обычно они появляются сразу большим обьемом, так что после получения нотификации можно успеть забрать один из слотов вручную.

Для запуска скрипта вам потребуются:
Айдишники организации из POST запроса при нажатии на ваше отделение на карте
POST с этим урлом надо искать в девелопер консоли браузера и в нем payload 
https://www.gosuslugi.ru/api/lk/v1/equeue/agg/slots
- eserviceId
- serviceId
- organizationId

Так же логин и пароль от госуслуг (стоит отключить двухфакторку в настройках).
А так же логин и пароль от почты для отправки емейла через SMTP.
По дефолту запускается каждые 2 минуты. Периодичность можно подкрутить в bash скрипте.

