-- ============================================
-- 小遥配配 - 测试数据准备脚本
-- ============================================
-- 用途：为接口测试准备基础测试数据
-- 环境：开发环境/测试环境
-- 数据库：xiaoyao-peipei-dev / xiaoyao-peipei-test
-- 创建日期：2026-01-22
-- 更新日期：2026-01-23
-- 版本：v3.2（添加shop_id字段，share_link改为完整URL）
-- ============================================

-- 设置字符集
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 1. 清空现有测试数据
-- ============================================
TRUNCATE TABLE ai_logs;
TRUNCATE TABLE share_stats;
TRUNCATE TABLE leads;
TRUNCATE TABLE messages;
TRUNCATE TABLE conversations;
TRUNCATE TABLE skus;
TRUNCATE TABLE merchants;

-- ============================================
-- 2. 插入商家数据
-- ============================================
INSERT INTO merchants (
  id, username, password_hash, shop_name, phone, address,
  business_hours, shop_id, share_link, status, created_at, updated_at
) VALUES
-- 测试商家001：基础测试账号
(
  1000000000000000001,
  'test_merchant_001',
  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJWm5LHJ7e',
  '测试电脑城001',
  '13800138001',
  '北京市朝阳区测试路123号',
  '9:00-21:00',
  'shop_1000000000000000001',
  'https://peipei.xiaoyaos.com/?shop=shop_1000000000000000001',
  'active',
  '2025-01-01 10:00:00',
  '2025-01-01 10:00:00'
),
-- 测试商家002：完整信息账号
(
  1000000000000000002,
  'test_merchant_002',
  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJWm5LHJ7e',
  '上海数码广场',
  '13900139002',
  '上海市浦东新区测试大道456号',
  '10:00-22:00',
  'shop_1000000000000000002',
  'https://peipei.xiaoyaos.com/?shop=shop_1000000000000000002',
  'active',
  '2025-01-02 10:00:00',
  '2025-01-02 10:00:00'
),
-- 测试商家003：已禁用账号
(
  1000000000000000003,
  'test_merchant_003',
  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYJWm5LHJ7e',
  '广州电脑城（已关闭）',
  '13700137003',
  '广州市天河区测试路789号',
  '9:00-18:00',
  'shop_1000000000000000003',
  'https://peipei.xiaoyaos.com/?shop=shop_1000000000000000003',
  'inactive',
  '2025-01-03 10:00:00',
  '2025-01-03 10:00:00'
);

-- ============================================
-- 3. 插入SKU配置数据
-- ============================================
INSERT INTO skus (
  id, merchant_id, device_type, name, brand, model, cpu, gpu, ram, storage,
  screen, weight, battery, price, stock, status, tags, images,
  view_count, select_count, created_at, updated_at
) VALUES
-- 笔记本配置
(
  1000000000000000001, 1000000000000000001, 'laptop',
  '联想拯救者Y7000P', '联想', 'Y7000P 2023',
  'i7-12700H', 'RTX 4060 8G', '16GB DDR5', '512GB SSD',
  '15.6英寸 2.5K 165Hz', '2.4kg', '5-6小时',
  7499.00, 5, 'active',
  '["gaming", "brand", "high-performance"]',
  '["https://file.xiaoyaosai.com/peipei/test/y7000p_1.jpg", "https://file.xiaoyaosai.com/peipei/test/y7000p_2.jpg"]',
  45, 12, '2025-01-01 10:00:00', '2025-01-01 10:00:00'
),
(
  1000000000000000002, 1000000000000000001, 'laptop',
  '华硕天选4', '华硕', '天选4 2023',
  'R7-7735HS', 'RTX 4060 8G', '16GB DDR5', '512GB SSD',
  '15.6英寸 2.5K 165Hz', '2.3kg', '4-5小时',
  6999.00, 8, 'active',
  '["gaming", "cost-effective"]',
  '["https://file.xiaoyaosai.com/peipei/test/tianxuan4_1.jpg"]',
  38, 10, '2025-01-01 10:00:00', '2025-01-01 10:00:00'
),
(
  1000000000000000003, 1000000000000000001, 'laptop',
  '联想ThinkPad X1 Carbon', '联想', 'X1 Carbon Gen11',
  'i7-1365U', '核显', '16GB LPDDR5', '1TB SSD',
  '14英寸 2.8K OLED', '1.12kg', '10-12小时',
  12999.00, 3, 'active',
  '["office", "business", "lightweight"]',
  '["https://file.xiaoyaosai.com/peipei/test/x1carbon_1.jpg"]',
  25, 5, '2025-01-01 10:00:00', '2025-01-01 10:00:00'
),
(
  1000000000000000004, 1000000000000000001, 'laptop',
  '荣耀MagicBook X14', '荣耀', 'MagicBook X14 Pro',
  'i5-13500H', '核显', '16GB DDR4', '512GB SSD',
  '14英寸 FHD IPS', '1.4kg', '8-10小时',
  4299.00, 15, 'active',
  '["budget", "office", "student"]',
  '["https://file.xiaoyaosai.com/peipei/test/magicbook_x14_1.jpg"]',
  62, 18, '2025-01-01 10:00:00', '2025-01-01 10:00:00'
),
-- 台式机配置
(
  1000000000000000005, 1000000000000000001, 'desktop',
  '华硕ROG玩家国度', '华硕', 'ROG GT501',
  'i9-13900K', 'RTX 4090 24G', '32GB DDR5', '1TB NVMe SSD',
  NULL, NULL, NULL,
  25999.00, 2, 'active',
  '["gaming", "high-end", "brand"]',
  '["https://file.xiaoyaosai.com/peipei/test/gt501_1.jpg"]',
  18, 3, '2025-01-01 10:00:00', '2025-01-01 10:00:00'
),
(
  1000000000000000006, 1000000000000000001, 'desktop',
  '联想GeekPro台式机', '联想', 'GeekPro 2023',
  'i5-13400F', 'GTX 1660S 6G', '16GB DDR4', '512GB SSD',
  NULL, NULL, NULL,
  4999.00, 10, 'active',
  '["gaming", "budget", "brand"]',
  '["https://file.xiaoyaosai.com/peipei/test/geekpro_1.jpg"]',
  35, 8, '2025-01-01 10:00:00', '2025-01-01 10:00:00'
),
-- 一体机配置
(
  1000000000000000007, 1000000000000000001, 'aio',
  '华为MateStation X', '华为', 'MateStation X 2023',
  'i7-12700H', '核显', '16GB', '512GB SSD',
  '28.2英寸 4K触控', NULL, NULL,
  12999.00, 3, 'active',
  '["office", "brand", "compact"]',
  '["https://file.xiaoyaosai.com/peipei/test/matestation_1.jpg"]',
  12, 2, '2025-01-01 10:00:00', '2025-01-01 10:00:00'
),
-- 已下架配置
(
  1000000000000000008, 1000000000000000001, 'laptop',
  '戴尔XPS 15（已停产）', '戴尔', 'XPS 15 9520',
  'i7-12700H', 'RTX 3050Ti 4G', '16GB DDR5', '512GB SSD',
  '15.6英寸 FHD+ OLED', '1.82kg', '6-8小时',
  15999.00, 0, 'inactive',
  '["office", "premium", "discontinued"]',
  '["https://file.xiaoyaosai.com/peipei/test/xps15_1.jpg"]',
  89, 15, '2025-01-01 10:00:00', '2025-01-01 10:00:00'
);

-- 商家2的配置
INSERT INTO skus (
  id, merchant_id, device_type, name, brand, model, cpu, gpu, ram, storage,
  screen, weight, battery, price, stock, status, tags, images,
  view_count, select_count, created_at, updated_at
) VALUES
(
  1000000000000000020, 1000000000000000002, 'laptop',
  'HP暗影精灵9', '惠普', 'Omen 16 2023',
  'i7-13700HX', 'RTX 4070 8G', '16GB DDR5', '1TB SSD',
  '16.1英寸 2.5K 165Hz', '2.4kg', '5-6小时',
  8999.00, 6, 'active',
  '["gaming", "brand", "high-performance"]',
  '["https://file.xiaoyaosai.com/peipei/test/omen16_1.jpg"]',
  28, 7, '2025-01-02 10:00:00', '2025-01-02 10:00:00'
),
(
  1000000000000000021, 1000000000000000002, 'desktop',
  '雷神911黑武士', '雷神', '911黑武士III',
  'i7-13700K', 'RTX 4070Ti 12G', '32GB DDR5', '1TB SSD',
  NULL, NULL, NULL,
  12999.00, 5, 'active',
  '["gaming", "brand"]',
  '["https://file.xiaoyaosai.com/peipei/test/911heishi_1.jpg"]',
  22, 6, '2025-01-02 10:00:00', '2025-01-02 10:00:00'
);

-- ============================================
-- 4. 插入对话数据
-- ============================================
INSERT INTO conversations (
  id, merchant_id, session_id, client_ip, user_agent, source, status, created_at, updated_at
) VALUES
-- 活跃对话
(
  1000000000000000001, 1000000000000000001, 'session_test_001',
  '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'qrcode', 'active',
  '2025-01-22 14:00:00', '2025-01-22 14:30:00'
),
(
  1000000000000000002, 1000000000000000001, 'session_test_002',
  '192.168.1.101', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0)', 'link', 'active',
  '2025-01-22 14:15:00', '2025-01-22 14:28:00'
),
-- 已完成对话
(
  1000000000000000003, 1000000000000000001, 'session_test_003',
  '192.168.1.102', 'Mozilla/5.0 (Android 13)', 'qrcode', 'completed',
  '2025-01-22 10:00:00', '2025-01-22 11:30:00'
),
-- 已放弃对话
(
  1000000000000000004, 1000000000000000001, 'session_test_004',
  '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0)', 'link', 'abandoned',
  '2025-01-21 20:00:00', '2025-01-21 20:15:00'
);

-- ============================================
-- 5. 插入消息数据
-- ============================================
INSERT INTO messages (
  id, conversation_id, role, content, extracted_info, confidence, created_at
) VALUES
-- 会话1的消息（活跃对话）
(
  1000000000000000001, 1000000000000000001, 'assistant',
  '您好！我是小遥，我来帮您选一台合适的电脑～请问您的预算大概是多少呢？',
  NULL, NULL, '2025-01-22 14:00:00'
),
(
  1000000000000000002, 1000000000000000001, 'user',
  '我想要一台6000左右的游戏笔记本能玩原神',
  '{"budget": "6000左右", "device_type": "笔记本", "usage": "游戏", "requirements": "玩原神"}',
  0.95, '2025-01-22 14:01:00'
),
(
  1000000000000000003, 1000000000000000001, 'assistant',
  '明白了！6000左右的游戏笔记本，玩原神完全够用～\n您需要经常携带吗？还是主要在家用？',
  NULL, NULL, '2025-01-22 14:01:05'
),
(
  1000000000000000004, 1000000000000000001, 'user',
  '主要在家用，偶尔出差会带',
  '{"portable": "主要在家用，偶尔出差会带"}',
  0.98, '2025-01-22 14:30:00'
),
-- 会话2的消息（活跃对话）
(
  1000000000000000005, 1000000000000000002, 'assistant',
  '您好！我是小遥，我来帮您选一台合适的电脑～请问您的预算大概是多少呢？',
  NULL, NULL, '2025-01-22 14:15:00'
),
(
  1000000000000000006, 1000000000000000002, 'user',
  '预算8000左右，想要台式机，主要用来剪辑视频，做后期',
  '{"budget": "8000左右", "device_type": "台式机", "usage": "剪辑视频", "requirements": "做后期"}',
  0.92, '2025-01-22 14:28:00'
),
-- 会话3的消息（已完成对话）
(
  1000000000000000007, 1000000000000000003, 'assistant',
  '您好！我是小遥，我来帮您选一台合适的电脑～请问您的预算大概是多少呢？',
  NULL, NULL, '2025-01-22 10:00:00'
),
(
  1000000000000000008, 1000000000000000003, 'user',
  '5000左右，办公用，笔记本，要轻便',
  '{"budget": "5000左右", "device_type": "笔记本", "usage": "办公", "requirements": "要轻便"}',
  0.96, '2025-01-22 10:05:00'
),
(
  1000000000000000009, 1000000000000000003, 'assistant',
  '好的！为您推荐以下配置：\n1. 荣耀MagicBook X14 - 4299元，重量1.4kg，续航8-10小时\n\n您可以选择一个方案查看详情，或者提交联系方式我们会为您详细介绍。',
  NULL, NULL, '2025-01-22 10:05:10'
),
(
  1000000000000000010, 1000000000000000003, 'user',
  '我选第一个，麻烦联系我，电话138****1234',
  NULL, NULL, '2025-01-22 11:30:00'
);

-- ============================================
-- 6. 插入线索数据
-- ============================================
-- 注意：phone字段需要AES加密，这里使用明文，实际插入时需要加密
INSERT INTO leads (
  id, merchant_id, conversation_id, phone, wechat, remark,
  budget, device_type, `usage`, requirements, selected_sku_id,
  status, notes, created_at, updated_at
) VALUES
-- 待处理线索
(
  1000000000000000001, 1000000000000000001, 1000000000000000001,
  '13800138001', 'test_wechat_001', '希望尽快联系，周末有空',
  '6000左右', 'laptop', '游戏', '玩原神',
  1000000000000000002, -- 华硕天选4
  'pending',
  '[{"content": "线索刚创建，待联系", "created_at": "2025-01-22T14:30:00Z", "created_by": "system"}]',
  '2025-01-22 14:30:00', '2025-01-22 14:30:00'
),
(
  1000000000000000002, 1000000000000000001, 1000000000000000003,
  '13800138002', NULL, '需要轻便的办公本',
  '5000左右', 'laptop', '办公', '要轻便',
  1000000000000000004, -- 荣耀MagicBook X14
  'contacted',
  '[{"content": "已电话联系，客户表示满意", "created_at": "2025-01-22T15:00:00Z", "created_by": "test_merchant_001"}]',
  '2025-01-22 11:30:00', '2025-01-22 15:00:00'
),
-- 已成交线索
(
  1000000000000000003, 1000000000000000001, 1000000000000000005,
  '13800138003', 'customer_003', '预算充足，要高端配置',
  '20000左右', 'desktop', '游戏', '玩3A大作',
  1000000000000000005, -- 华硕ROG
  'closed',
  '[{"content": "已到店体验，支付定金", "created_at": "2025-01-20T16:00:00Z", "created_by": "test_merchant_001"}, {"content": "已全款提货", "created_at": "2025-01-21T14:00:00Z", "created_by": "test_merchant_001"}]',
  '2025-01-20 10:00:00', '2025-01-21 14:00:00'
),
-- 已放弃线索
(
  1000000000000000004, 1000000000000000001, 1000000000000000006,
  '13800138004', NULL, '觉得价格偏高',
  '3000左右', 'laptop', '办公', '基础办公',
  NULL,
  'abandoned',
  '[{"content": "电话无法接通", "created_at": "2025-01-19T10:00:00Z", "created_by": "test_merchant_001"}, {"content": "客户表示预算不够，暂不考虑", "created_at": "2025-01-19T15:00:00Z", "created_by": "test_merchant_001"}]',
  '2025-01-19 09:00:00', '2025-01-19 15:00:00'
);

-- ============================================
-- 7. 插入分享统计数据
-- ============================================
INSERT INTO share_stats (
  id, merchant_id, date, scan_count, consult_count, lead_count,
  device_type_stats, budget_stats, created_at
) VALUES
-- 今天
(1000000000000000001, 1000000000000000001, CURDATE(), 45, 23, 15,
 '{"laptop": 14, "desktop": 7, "aio": 2}',
 '{"3000-5000": 5, "5000-8000": 10, "8000-12000": 6, "12000+": 2}',
 NOW()),
-- 昨天
(1000000000000000002, 1000000000000000001, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 55, 30, 16,
 '{"laptop": 10, "desktop": 8, "aio": 3}',
 '{"3000-5000": 4, "5000-8000": 12, "8000-12000": 7, "12000+": 1}',
 DATE_SUB(NOW(), INTERVAL 1 DAY)),
-- 2天前
(1000000000000000003, 1000000000000000001, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 48, 25, 14,
 '{"laptop": 11, "desktop": 9, "aio": 1}',
 '{"3000-5000": 6, "5000-8000": 9, "8000-12000": 5, "12000+": 2}',
 DATE_SUB(NOW(), INTERVAL 2 DAY)),
-- 3天前
(1000000000000000004, 1000000000000000001, DATE_SUB(CURDATE(), INTERVAL 3 DAY), 52, 28, 18,
 '{"laptop": 12, "desktop": 10, "aio": 2}',
 '{"3000-5000": 7, "5000-8000": 11, "8000-12000": 6, "12000+": 2}',
 DATE_SUB(NOW(), INTERVAL 3 DAY)),
-- 4天前
(1000000000000000005, 1000000000000000001, DATE_SUB(CURDATE(), INTERVAL 4 DAY), 38, 20, 12,
 '{"laptop": 8, "desktop": 7, "aio": 3}',
 '{"3000-5000": 4, "5000-8000": 8, "8000-12000": 4, "12000+": 1}',
 DATE_SUB(NOW(), INTERVAL 4 DAY)),
-- 5天前
(1000000000000000006, 1000000000000000001, DATE_SUB(CURDATE(), INTERVAL 5 DAY), 45, 23, 10,
 '{"laptop": 9, "desktop": 8, "aio": 1}',
 '{"3000-5000": 3, "5000-8000": 10, "8000-12000": 5, "12000+": 1}',
 DATE_SUB(NOW(), INTERVAL 5 DAY)),
-- 6天前
(1000000000000000007, 1000000000000000001, DATE_SUB(CURDATE(), INTERVAL 6 DAY), 32, 18, 10,
 '{"laptop": 7, "desktop": 6, "aio": 2}',
 '{"3000-5000": 5, "5000-8000": 8, "8000-12000": 4, "12000+": 0}',
 DATE_SUB(NOW(), INTERVAL 6 DAY));

-- ============================================
-- 8. 插入AI调用日志
-- ============================================
INSERT INTO ai_logs (
  id, conversation_id, api_type, prompt, response, tokens, cost, response_time, error_message, created_at
) VALUES
(
  1000000000000000001, 1000000000000000001, 'extraction',
  '从用户消息中提取需求：我想要一台6000左右的游戏笔记本能玩原神',
  '{"budget": "6000左右", "device_type": "笔记本", "usage": "游戏", "requirements": "玩原神"}',
  256, 0.01, 850, NULL, '2025-01-22 14:01:00'
),
(
  1000000000000000002, 1000000000000000001, 'recommendation',
  '根据用户需求推荐配置：预算6000左右，笔记本，游戏，玩原神',
  '推荐了2个配置：华硕天选4、联想拯救者Y7000P',
  512, 0.02, 1200, NULL, '2025-01-22 14:01:10'
),
(
  1000000000000000003, 1000000000000000002, 'extraction',
  '从用户消息中提取需求：预算8000左右，想要台式机，主要用来剪辑视频',
  '{"budget": "8000左右", "device_type": "台式机", "usage": "剪辑视频", "requirements": "做后期"}',
  280, 0.011, 920, NULL, '2025-01-22 14:28:00'
),
(
  1000000000000000004, 1000000000000000003, 'extraction',
  '从用户消息中提取需求：5000左右，办公用，笔记本，要轻便',
  '{"budget": "5000左右", "device_type": "笔记本", "usage": "办公", "requirements": "要轻便"}',
  240, 0.009, 780, NULL, '2025-01-22 10:05:00'
),
(
  1000000000000000005, 1000000000000000003, 'recommendation',
  '根据用户需求推荐配置：预算5000左右，笔记本，办公，轻便',
  '推荐了3个配置：荣耀MagicBook X14、联想IdeaPad、HP星14',
  480, 0.019, 1100, NULL, '2025-01-22 10:05:10'
);

-- ============================================
-- 9. 数据验证
-- ============================================
-- 验证插入结果
SELECT 'merchants' AS table_name, COUNT(*) AS count FROM merchants
UNION ALL
SELECT 'skus' AS table_name, COUNT(*) AS count FROM skus
UNION ALL
SELECT 'conversations' AS table_name, COUNT(*) AS count FROM conversations
UNION ALL
SELECT 'messages' AS table_name, COUNT(*) AS count FROM messages
UNION ALL
SELECT 'leads' AS table_name, COUNT(*) AS count FROM leads
UNION ALL
SELECT 'share_stats' AS table_name, COUNT(*) AS count FROM share_stats
UNION ALL
SELECT 'ai_logs' AS table_name, COUNT(*) AS count FROM ai_logs;

-- ============================================
-- 10. 完成
-- ============================================
SET FOREIGN_KEY_CHECKS = 1;

SELECT '✅ 测试数据准备完成！' AS result;
