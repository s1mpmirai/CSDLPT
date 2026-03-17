-- Master initialization script for Docker
-- Combines DB1 and DB2 creation

-- Note: We run DB2 creation first because some views in DB1 might reference DB2 tables
SOURCE /docker-entrypoint-initdb.d/DB2_Luong.sql;
SOURCE /docker-entrypoint-initdb.d/DB1_NhanSu.sql;
