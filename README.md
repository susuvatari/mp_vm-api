📁 mp_vm-api/                             # Корень проекта
│
├── 📄 main.py                             # Глобальный оркестратор 
├── 📄 .env                                # Секреты окружения 
├── 📄 requirements.txt                    # Зависимости (pydantic>=2.0.0, requests, pandas, openpyxl)
├── 📄 README.md                           # Текущее описание
│
├── 📁 modules/                            # Бизнес-логика системы
│   └── 📁 jira/                           # Экосистема взаимодействия с Jira
│       ├── 📁 closure_manager/            # FEEDBACK LOOP: Пакет автоматической проверки
│       │   ├── 📄 discovery.py            # Jira Lookup: Поиск ключей через быстрые пакетные JQL-запросы
│       │   ├── 📄 validator.py            # MPVM Audit: Проверка уязвимостей на базе абсолютных путей Pathlib
│       │   ├── 📄 processor.py            # Actions: Атомарная смена статусов и изолированный Reject Flow
│       │   └── 📄 tags_isp.py             # Tags: Сессионное управление тегами Kanban (ИБ_X_дней)
│       │
│       ├── 📄 config_jira.py              # ЦЕНТР НАСТРОЕК
│       ├── 📄 issue_generator.py          # Рассылка
│       ├── 📄 main_task_creater.py        # Создание еженедельных задач
│       ├── 📄 jira_api.py                 # Поиск в Jira Assets 
│       ├── 📄 sd_utils.py                 # Работа с вложениями
│       └── 📄 csv_manager.py              # отчет
│
├── 📁 api_mp_vm/                          # API MP VM
│   ├── 📄 main_api_mp_vm.py               # PDQL
│   ├── 📄 client.py                       # ООП-клиент MaxPatrol VM
│   ├── 📄 models.py                       # очистка
│   └── 📄 mp_vm_variables.py              # env
│
├── 📁 integrations/                       # Входные PDQL-запросы
│   ├── 📁 jira-pdql/                      # выгрузки 
│   └── 📁 jira-check/                     # check_vuln_status.pdql 
│
├── 📁 files/                              # Результаты работы (генерируются автоматически, права gitlab-runner)
│   └── 📁 jira-pdql/
│       ├── 📁 JSONFiles/                  # Обогащенные данные (источник для рассылки)
│       ├── 📁 CSVFiles/                   # Промежуточные таблицы для парсинга
│       └── 📁 XLSXFiles/                  # Итоговые отчеты для вложения в ISP/SD
│
└── 📁 logs/                               # Логирование
```
