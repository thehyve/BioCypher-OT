

# if the dump file already exists, delete it
mkdir -p /dump
chmod 777 /dump

DUMP_FILE=/dump/OTAR.dump
if [ -f "$DUMP_FILE" ]; then
    rm "$DUMP_FILE"
fi

bin/neo4j-admin dump --database=neo4j --to=$DUMP_FILE
