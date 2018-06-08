echo "Creating $DATABASE_NAME"
mysql --host db <<EOF
CREATE DATABASE $DATABASE_NAME;
EOF
echo "Done. Loading into $DATABASE_NAME"
mysql --host db $DATABASE_NAME < /data/up.sql
echo "Done loading into $DATABASE_NAME"
