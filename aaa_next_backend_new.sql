CREATE TABLE `api_version` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app_id` bigint NOT NULL DEFAULT '0',
  `api_id` bigint NOT NULL DEFAULT '0',
  `channel_id` bigint NOT NULL DEFAULT '0',
  `channel_type` tinyint NOT NULL DEFAULT '0',
  `content_id` bigint NOT NULL DEFAULT '0',
  `version` bigint NOT NULL,
  `method` varchar(10) DEFAULT NULL,
  `path` varchar(200) DEFAULT NULL,
  `other` varchar(50) DEFAULT NULL,
  `is_delete` tinyint NOT NULL DEFAULT '0',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_appId_apiId_channel` (`app_id`,`api_id`,`channel_id`,`content_id`,`version`),
  KEY `idx_delete_lastUpdateTime` (`is_delete`,`last_update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `api_tag` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `app_id` bigint NOT NULL DEFAULT '0',
  `api_id` bigint NOT NULL DEFAULT '0',
  `grpc_path` varchar(255) DEFAULT NULL,
  `tag_key` varchar(50) NOT NULL DEFAULT '',
  `tag_value` varchar(1024) DEFAULT '',
  `is_delete` tinyint NOT NULL DEFAULT '0',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_appId_tagKey` (`app_id`,`tag_key`),
  KEY `idx_appId_apiId_tagKey` (`app_id`,`api_id`,`tag_key`),
  KEY `idx_appId_path_tagKey` (`app_id`,`grpc_path`,`tag_key`),
  KEY `idx_delete_lastUpdateTime` (`is_delete`,`last_update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `api` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app_id` bigint NOT NULL DEFAULT '0',
  `r_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `title` varchar(200) NOT NULL DEFAULT '',
  `method` varchar(10) NOT NULL DEFAULT '',
  `path` varchar(200) NOT NULL DEFAULT '',
  `status` int NOT NULL DEFAULT '-1',
  `maintainer` varchar(300) DEFAULT '',
  `other` bigint DEFAULT NULL,
  `collection_ids` varchar(200) NOT NULL DEFAULT '',
  `type` tinyint NOT NULL DEFAULT '0',
  `is_delete` tinyint NOT NULL DEFAULT '0',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `create_user` varchar(50) NOT NULL,
  `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_update_user` varchar(50) DEFAULT NULL,
  `uid` varchar(220) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_appId_uid` (`app_id`,`uid`),
  KEY `idx_appId_collectionIds` (`app_id`,`collection_ids`),
  KEY `idx_delete_lastUpdateTime` (`is_delete`,`last_update_time`),
  KEY `idx_appId_rname` (`app_id`,`r_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;