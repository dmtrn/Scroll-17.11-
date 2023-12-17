﻿
# ⚔️ Scroll Machine

Очень мощный инструмент в умелых руках. Практически полностью автоматизирован.
> Путь осилит идущий, а софт осилит любой деген🕵️

## Основные особенности 

* **Автоматическая работа большинства модулей*** 
    (не нужно настраивать каждый модуль отдельно)
* **Сохранение процесса выполнения аккаунта**
* **Автоматическая генерация маршрута** 
* **Ручная генерация маршрута**
* **Параллельный запуск** (для прогона дешевых аккаунтов)
* **Последовательный запуск** (с депом и выводом через OKX) 
* **Одиночный запуск** (1 модуль на все аккаунты)
* **Асинхронный ООП код** (все работает очень быстро)
* **Рандомизация сумм/задержек/количества транзакций**
* **Gas чекер, Повторитель** (при ошибках)
* **Плотнейшее логирование, даже ваш чих залогируется**

***❗Благодаря настройкам `AMOUNT_MIN` и `AMOUNT_MAX` софт сам решает, какое количество, какого токена, в какой токен нужно обменять или сделать депозит на лендинг, вывод на ОКХ.
% учитывается для нативного токена `ETH`, остальные токены(включая LP токены) обратно обмениваются на 100% от их баланса. Свапы реализованы во всех направлениях
(`ETH - Токен`, `Токен - Токен`, `Токен - ETH`).
Для оптимальной работы рекомендуется ставить от 60 до 80 %.** 


## 🧩Модули и их функционал

    1.  OKX             (Депозит / Вывод / Сбор средств с суб-аккаунтов)                                       
    2.  Rhino           (Bridge по любым направлениям)
    3.  LayerSwap       (Bridge по любым направлениям)    
    4.  Orbiter         (Bridge по любым направлениям)    
    5.  Official bridge (Bridge / Withdraw)                                          
    6.  Merkly          (Refuel все сети из zkSync)
    7.  SyncSwap        (Свапы между стейблами и ETH + ввод и вывод ликвидности)                         
    8.  OpenOcean       (Свапы между стейблами и ETH)                               
    9.  ScrollSwap      (Свапы между стейблами и ETH)                               
    10. iZumi           (Свапы между стейблами и ETH)   
    11. LayerBank       (Ввод и вывод ликвидности + вкл/выкл collateral)  
    12. Deployer        (Деплой собственного контракта)
    13. Safe (Gnosis)   (Создание сейфа)
    14. Zerius          (Минт NFT / Бридж NFT)
    15. Omnisea         (Создание коллекции)
    16. Dmail           (Отправка сообщений)
    17. Send ETH to random addresses (Отправка пыли в ETH на рандомные адресса)
    18. Send ETH to own addresses (Отправка пыли в ETH на свой адресс)
    19. Wrap/Unwrap ETH


## ♾️Основные функции

1.  **🚀Запуск прогона всех аккаунтов по подготовленным маршрутам.**

В настройках вы указываете режим работы софта (`SOFTWARE_MODE`), либо параллельный, либо последовательный. Запустив 
эту функцию софт будет брать каждый аккаунт поочереди и запускать его на маршрут. Чтобы 
понять всю мощность этого аппарата, попробуйте поставить задержку до 5с или вообще выключить (`SLEEP_MODE`).

2.  **🤖Генерация авто-роутов для каждого аккаунта**

Мощный генератор маршрутов. Смотрит на настройку `MAX_UNQ_CONTACTS` и `AUTO_ROUTES_MODULES_USING` и генерирует маршрут
по вашим предпочтениям. ВНИМАНИЕ: ПРИ ЗАПУСКЕ ЭТОЙ ФУНКЦИИ, ВСЕ ПРЕДЫДУЩИЕ МАРШРУТЫ БУДУТ УДАЛЕНЫ

3.  **📄Генерация классических роутов для каждого аккаунта**

Классический генератор, работает по дедовской методике. Вам нужно в каждом шаге в настройке `CLASSIC_ROUTES_MODULES_USING`
указать один или несколько модулей и при запуске этой функции софт соберет вам маршрут по этой настройке. Поддерживается 
`None` как один из модулей в списке, при его попадании в маршрут, софт пропустит этот шаг. ВНИМАНИЕ: ПРИ ЗАПУСКЕ ЭТОЙ 
ФУНКЦИИ, ВСЕ ПРЕДЫДУЩИЕ МАРШРУТЫ БУДУТ УДАЛЕНЫ

4. **💾Создание файла зависимостей ваших и OKX кошельков**

Создает файл JSON, где привязываются ваши адреса к кошелькам OKX. Сделал для вашей безопасности. Софт выбирает
к каждой строке в `wallets.txt` эту же строку в `okx_wallets.txt` и если вы ошиблись, то всегда можно проверить это в 
файле `okx_withdraw_list.json`

5. **✅Проверка всех прокси на работоспособность**

Быстрая проверка прокси(реально быстрая, как с цепи срывается)

6. **👈Запуск одного модуля для всех аккаунтов**

Запуск одного модуля для всех аккаунтов. Дал себе слово, что будет 3 режима работы, поэтому третьим оказался этот.

7. **📊Получение статистики для каждого аккаунта**

Практически моментальное получение всей статистики по аккаунтам, даже если их больше 100 штук. Сделаны самые необходимые
поля

## 📄Ввод своих данных

### Все нужные файлы находятся в папке `/data`
    1. wallets.txt - ваши приватные ключи
    2. proxies.txt - ваши прокси в формате login:password@ip:port
    3. okx_wallets.txt - ваши адресса пополнения в OKX

Каждый ваш  `ключ` / `адресс` / `прокси` указывается на новой строке. Если проксей меньше, чем приватников, то
софт работает следующим образом:

    Кошелек 1 -> Прокси 1
    Кошелек 2 -> Прокси 2
    Кошелек 3 -> Прокси 3
    Кошелек 4 -> Прокси 1 (цикличное повторение)
    Кошелек 5 -> Прокси 2 (цикличное повторение)
    и так далее.


## ⚙️Настройка софта

Все настройки вынесены в файл `settings.py`. Заходим в него и видим подробное описание каждого раздела. 
Самые важные моменты продублирую здесь. 

1. Раздел `API KEYS`. Получите все API ключи. В разделе есть ссылки на сайты, где это нужно сделать
2. Раздел `GENERAL SETTINGS`. Внимательно прочитайте все описания и проставьте необходимые значения
3. Далее сверху вниз настройте все модули. К каждому модулю есть описание на русском английском
4. Когда вы подойдете к разделу `ROUTES`, нужно собрать всю силу в кулак и перекреститься. `AUTO-ROUTES` это список модулей, которые будут генерироваться самостоятельно для каждого аккаунта, то есть если у модуля значение `1`, то он будет участвовать в генерации маршрута. `CLASSIC-ROUTES` это славянский вариант установки маршрута для аккаунта, вы прописываете в список набор модулей и один из них будет добавлен во время генерации маршрута. 
Опять же, в файле есть примеры и подробное описание.

### 📚Основные параметры

* `SOFTWARE_MODE` - определяет режим работы софта (параллельный или последовательный). Параллельный способен одновременно
крутить очень больше количество аккаунтов (необходимы прокси для каждого аккаунта, так как RPC блокчейнов заблокируют вас в 
противном случае). Последовательный режим работает как ручной прогон. Условно: депозит на аккаунт -> прохождение маршрута ->
вывод на OKX и так по кругу, для всех аккаунтов
* `WALLETS_TO_WORK` - определяет какие кошельки будут работать. Варианты работы: Одиночный, Выборка, От Х до У, Все сразу. Подробнее в настройках. 
* `TX_COUNT` - определяет необходимое количество транзакций(модулей) в маршруте. Это не финальное значение, так как генератор
добавляет к этому числу еще немного, так как существуют зависимости (вывод из EraLend нельзя сделать, если вы еще не депнули туда)
* `MAX_UNQ_CONTRACTS` - при установке в `True`, генератор авто-роутов добавит все включенные модули из списка `AUTO_ROUTES_MODULES_USING`
хотя бы 1 раз, а дальше доделает маршрут случайными модулями
* `RHINO_CHAIN_ID_FROM(TO)`, `LAYERSWAP_CHAIN_ID_FROM(TO)` и `ORBITER_CHAIN_ID_FROM(TO)` - устанавливают исходящие и входящие сети, также возможно 
выбрать несколько сетей и софт случайным образом выберет одну из них
* `DESTINATION_MERKLY_DATA` и `DESTINATION_ZERIUS` - определяет входящий блокчейн(куда делаем refuel) и минимальную/максимальную
сумму для refuel. Также можно выбрать несколько сетей, софт выберет одну случайную.
* `AMOUNT_MIN` и `AMOUNT_MAX` - благодаря этим параметрам, софт понимает, сколько % от вашего баланса ему необходимо использовать
в свапах, депозитах на лендинги и выводе на OKX. Более подробно описал [**здесь**](https://github.com/realaskaer/zkSync#%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D1%8B%D0%B5-%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8)
* `MIN_BALANCE` - устанавливает минимальный баланс для аккаунта, опустившись за который, софт будет выдаться ошибку о
недостаточном балансе на аккаунте `Insufficient balance on account!`
* `GAS_CONTROL` - включает/выключает контроль газа для каждого шага в маршруте
* `GAS_MULTIPLIER` - множитель газа, рекомендуемые значения от 1.3 до 1.5. Этот параметр умножается на газ лимит, чтобы 
увеличить шанс успешного завершения транзакции
* `MAXIMUM_RETRY` - количество повторных попыток при ошибках в модулях
* `UNLIMITED_APPROVE` - выбор между бесконечными и точными апрувами
* `SLEEP_MODE` - включает/выключает режим сна после каждого модуля и между аккаунтами. Включив параллельный режим софта и
выключив эту настройку, вы сможете лицезреть скорость данного аппарата

## 💻Как софт работает изнутри?

### Маршруты и сохранение прогресса его выполнения

С помощью сгенерированных маршрутов, каждый аккаунт знает по какому пути ему необходимо пройти. Также реализовано сохранение текущего шага при выполнении маршрута движения аккаунтом, то есть если вы выключите софт на 3 модуле, то включив его заново, аккаунт продолжит свою работу ровно с `третьего` модуля.  

### Контроль газа и выполнения

Внутри софта есть два работника. Первый будет `проверять газ` перед каждым запуском модуля, и если газ будет выше установленного, аккаунт уйдет в ожидание нормального газа. Второй работник во время выполнения модуля следит, чтобы этот модуль был выполнен, если все же произойдет ошибка, он `повторит выполнение` указанное количество раз. Но если после нескольких повторений (кол-во устанавливаете вы сами) будет выскакивать ошибка, работник пропустит этот модуль и приступит к выполнению следующего.  

## 🤛🏻Реферальная программа

Внутри файла `сonfig.py` есть настройка `HELP_SOFTWARE`, если она включена (по умолчанию - включена), то от суммы вашей транзакции на любом агрегаторе (пока что только `OpenOcean`) мне будет идти `1%`. Эту часть от объема транзакции переводит контракт агрегатора, а не ваш кошелек. Поэтому вы не будете иметь дел с моим кошельком.
Чтобы выключить эту функции, укажите значение `False` 


## 🛠️Установка проекта
> Устанавливая проект, вы принимаете риски использования софта для добывания денег(потерять жопу, деньги, девственность).

Как только вы скачаете проект, убедитесь, что у вас Python 3.10.11 и последняя версия PyCharm (2023.2)

Для установки необходимых библиотек, пропишите в консоль PyCharm

```bash
  pip install -r requirements.txt
```
## 🔗 Ссылки на программы

 - [Установка PyCharm](https://www.jetbrains.com/pycharm/download/?section=windows)
 - [Установка Python](https://www.python.org/downloads/windows/) (Вам нужна версия 3.10.11)

## 🧾FAQ

#### Есть ли дрейнер в софте?

> Нет, но перед запуском любого софта, необходимо его проверять 

#### Как запустить софт?

> Сначала, прочитать README, если не получилось с первого раза, попытаться еще раз.

## ❔Куда писать свой вопрос?

- [@foundation](https://t.me/askaer) - мой канал в телеграм  
- [@foundation.chat](https://t.me/askaerchat) - ответы на любой вопрос
- [@askaer](https://t.me/realaskaer) - **при обнаружении бомбы в коде**  

## ❤️‍🔥Donate (Any EVM)
### `0x000000a679C2FB345dDEfbaE3c42beE92c0Fb7A5`
> Спасибо за поддержку❤️
