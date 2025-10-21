# zabbix_db_monitor — Инструкция запуска (ветка PostgreSQL)

Эта инструкция почти такая же, как в обычной ветке, но для корректной работы мониторинга PostgreSQL **необходимо** выполнить инициализацию пользователя/прав в базе перед входом в веб-интерфейс.

## Требования
- Docker & Docker Compose
- Python 3.8+ (для виртуального окружения)
- Git

## Быстрый старт

1. Клонируйте репозиторий и перейдите в папку:
```bash
git clone https://github.com/Substance-live/zabbix_db_monitor.git
cd zabbix_db_monitor
```

2. Создайте виртуальное окружение и установите Python-зависимости:
```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# Linux/macOS
# source venv/bin/activate

pip install -r requirements.txt
```

3. Поднимите контейнеры:
```bash
docker compose up -d
```

4. **ВАЖНО — инициализация базы (обязательный шаг для этой ветки)**  
   Выполните внутри контейнера Postgres инициализационный скрипт (он находится в `./sql-scripts/init_zbx_user.sql` в репозитории):
```bash
docker exec -i pg_local psql -U admin -d kurs_db -f /scripts/init_zbx_user.sql
```
   - Эта команда создаст/настроит пользователя, роль и нужные привилегии для шаблона мониторинга PostgreSQL.
   - Выполнять обязательно **перед** входом в веб-интерфейс Zabbix, иначе шаблон PostgreSQL не сможет подключиться и элементы станут unsupported.

5. Откройте веб-интерфейс:
```
http://localhost:8080
```

6. Войдите:
- Логин: `Admin`
- Пароль: `zabbix`

## Что дальше в UI
1. Перейдите в `Monitoring` → `Hosts`.  
2. Удалите дефолтный `Zabbix server`, если хотите (по шагам выше).  
3. Создайте свой Host и привяжите шаблон `Template DB PostgreSQL (by Zabbix agent 2)` (или тот, который используете).  
4. В настройках хоста заполните макросы шаблона (например `{$PG.CONNSTRING.AGENT2}`, `{$PG.USER}`, `{$PG.PASSWORD}`) — я добавлю скриншоты и пример макросов позже.

## Полезные команды
- Запустить/остановить стек:
```bash
docker compose up -d
docker compose down
```
- Проверить логи Postgres:
```bash
docker logs -f pg_local
```
- Проверить логи zabbix_agent2:
```bash
docker logs -f zabbix_agent2
```

## Траблшутинг для PostgreSQL ветки
- Если шаблон PostgreSQL показывает ошибки `Failed to create connection` — проверьте:
  1. Выполнен ли `init_zbx_user.sql` (см. шаг 4).  
  2. Правильно ли заданы макросы `{$PG.CONNSTRING.AGENT2}`, `{$PG.USER}`, `{$PG.PASSWORD}` для хоста в Zabbix.  
  3. Доступен ли Postgres по адресу, который видит агент (обычно `db`, `pg_local` или `127.0.0.1` в зависимости от сети).  
- Если web UI говорит `Database version does not match` — это конфликт версий Zabbix (server/web images должны быть одной серии). Проверяйте теги образов в `docker-compose.yml`.

---

Если нужно, я могу добавить готовые примеры значений макросов для шаблона PostgreSQL и пример SQL, который создаёт пользователя `zbx_monitor` с правильными правами (pg_monitor). Скажи — и я добавлю в README.
