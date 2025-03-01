flask db init || true
flask db migrate -m "Running migrations"
flask db upgrade
exec "$@"