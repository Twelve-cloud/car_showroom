#! /bin/bash
# master
kubectl exec -i statefulset-database-0 -n production -- bash << EOF
echo "host CarSalonProject all statefulset-database-1.service-database-headless.production.svc.cluster.local trust" >> /var/lib/postgresql/data/pg_hba.conf
echo "host CarSalonProject all statefulset-database-2.service-database-headless.production.svc.cluster.local trust" >> /var/lib/postgresql/data/pg_hba.conf
su - postgres
pg_ctl restart -D /var/lib/postgresql/data
EOF
sleep 10 && kubectl wait --for=condition=Ready pod/statefulset-database-0 -n production --timeout=-30s
kubectl exec -i statefulset-database-0 -n production -- bash << EOF
PGPASSWORD=Annieleo1 pg_dumpall --database=postgres --host=statefulset-database-0.service-database-headless.production.svc.cluster.local --username=Twelve --globals-only --no-privileges | psql -U Twelve CarSalonProject
exit
EOF

# replica1
kubectl exec -i statefulset-database-1 -n production -- bash << EOF
su - postgres
pg_ctl restart -D /var/lib/postgresql/data
EOF
sleep 10 && kubectl wait --for=condition=Ready pod/statefulset-database-1 -n production --timeout=-30s
kubectl exec -i statefulset-database-1 -n production -- bash << EOF
PGPASSWORD=Annieleo1 pg_dump --dbname=CarSalonProject --host=statefulset-database-0.service-database-headless.production.svc.cluster.local --username=Twelve --create --schema-only | psql -U Twelve CarSalonProject
exit
EOF


# replica2
kubectl exec -i statefulset-database-2 -n production -- bash << EOF
su - postgres
pg_ctl restart -D /var/lib/postgresql/data
EOF
sleep 10 && kubectl wait --for=condition=Ready pod/statefulset-database-2 -n production --timeout=-30s
kubectl exec -i statefulset-database-2 -n production -- bash << EOF
PGPASSWORD=Annieleo1 pg_dump --dbname=CarSalonProject --host=statefulset-database-0.service-database-headless.production.svc.cluster.local --username=Twelve --create --schema-only | psql -U Twelve CarSalonProject
exit
EOF

# master
kubectl exec -i statefulset-database-0 -n production -- bash << EOF
su - postgres << EOF
psql -U Twelve CarSalonProject << EOF
CREATE PUBLICATION db_pub FOR ALL TABLES;
\q
exit
exit
EOF

# replica1
kubectl exec -i statefulset-database-1 -n production -- bash << EOF
su - postgres
psql -U Twelve CarSalonProject << EOF
CREATE SUBSCRIPTION db_sub_replica1 CONNECTION 'host=statefulset-database-0.service-database-headless.production.svc.cluster.local dbname=CarSalonProject user=Twelve password=Annieleo1' PUBLICATION db_pub;
\q
exit
exit
EOF

# replica2
kubectl exec -i statefulset-database-2 -n production -- bash << EOF
su - postgres
psql -U Twelve CarSalonProject << EOF
CREATE SUBSCRIPTION db_sub_replica2 CONNECTION 'host=statefulset-database-0.service-database-headless.production.svc.cluster.local dbname=CarSalonProject user=Twelve password=Annieleo1' PUBLICATION db_pub;
\q
exit
exit
EOF