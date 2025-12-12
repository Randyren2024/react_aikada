-- 打卡位置字段扩展（可选）
-- 当前后端已支持将位置信息写入 checkins.location(JSONB) 字段。
-- 如需结构化查询或索引，可执行以下迁移：

-- 1) 结构化列（可选）
ALTER TABLE checkins
    ADD COLUMN IF NOT EXISTS latitude NUMERIC(9,6),
    ADD COLUMN IF NOT EXISTS longitude NUMERIC(9,6),
    ADD COLUMN IF NOT EXISTS accuracy NUMERIC(6,2),
    ADD COLUMN IF NOT EXISTS address TEXT;

-- 2) 复合索引（可选）
CREATE INDEX IF NOT EXISTS idx_checkins_lat_lng ON checkins(latitude, longitude);

-- 3) 从 JSON 迁移到结构化列（可选）
-- 注意：根据实际 JSON 结构调整路径
UPDATE checkins
SET
  latitude = (location->>'latitude')::NUMERIC,
  longitude = (location->>'longitude')::NUMERIC,
  accuracy = (location->>'accuracy')::NUMERIC,
  address = (location->>'address');

-- 4) 可选 PostGIS 支持（需要已安装扩展）
-- CREATE EXTENSION IF NOT EXISTS postgis;
-- ALTER TABLE checkins ADD COLUMN IF NOT EXISTS geog GEOGRAPHY(POINT, 4326);
-- UPDATE checkins SET geog = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);
