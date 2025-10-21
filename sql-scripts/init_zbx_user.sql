CREATE USER zbx_monitor WITH PASSWORD 'zabbix_pass' INHERIT;
GRANT pg_monitor TO zbx_monitor;
