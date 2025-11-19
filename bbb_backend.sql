CREATE TABLE `t_scheduled_scan` (
    `id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `record_id` bigint NOT NULL DEFAULT '0',
    `start_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `end_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `app_orig_log_id` bigint NOT NULL DEFAULT '0',
    `scan_id` bigint NOT NULL DEFAULT '0',
    `error_message` varchar(255) CHARACTER
    SET
        utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
        `vuln_ids` json DEFAULT NULL,
        PRIMARY KEY (`id`),
        KEY `idx_last_update_time` (`last_update_time`),
        KEY `idx_record_id` (`record_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

CREATE TABLE `t_app_origin_log` (
    `id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `app_id` bigint NOT NULL DEFAULT '0',
    `domain` varchar(256) NOT NULL DEFAULT '',
    `scheme` varchar(32) NOT NULL DEFAULT '',
    `api_path` varchar(256) NOT NULL DEFAULT '',
    `method` varchar(32) NOT NULL DEFAULT '',
    `param` varchar(2048) NOT NULL DEFAULT '',
    `req_body` varchar(1024) NOT NULL DEFAULT '',
    `resp_length` int NOT NULL DEFAULT '0',
    `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_last_update_time` (`last_update_time`),
    KEY `idx_domain` (`domain`),
    KEY `idx_app_path_method` (`app_id`, `api_path`, `method`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE `t_vuln_forensic` (
    `id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `vuln_id` bigint NOT NULL DEFAULT '0',
    `scan_host` varchar(256) NOT NULL DEFAULT '',
    `scan_url` varchar(128) NOT NULL DEFAULT '',
    `method` varchar(32) NOT NULL DEFAULT '',
    `status_code` int NOT NULL DEFAULT '0',
    `response_length` bigint NOT NULL DEFAULT '0',
    `response_duration` float NOT NULL DEFAULT '0',
    `request_path` varchar(256) NOT NULL DEFAULT '',
    `response_path` varchar(256) NOT NULL DEFAULT '',
    `request_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_last_update_time` (`last_update_time`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE `t_vuln` (
    `id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `task_id` varchar(128) NOT NULL DEFAULT '',
    `scan_id` bigint NOT NULL DEFAULT '0',
    `rule_id` bigint NOT NULL DEFAULT '0',
    `scan_mode` tinyint NOT NULL DEFAULT '0',
    `scan_host` varchar(256) NOT NULL DEFAULT '',
    `severity` varchar(32) NOT NULL DEFAULT '',
    `department` varchar(128) NOT NULL DEFAULT '',
    `business_name` varchar(128) NOT NULL DEFAULT '',
    `system_name` varchar(128) NOT NULL DEFAULT '',
    `leak_type` varchar(64) NOT NULL DEFAULT '',
    `state` tinyint NOT NULL DEFAULT '0',
    `reason` varchar(256) NOT NULL DEFAULT '',
    `raw_request_path` varchar(256) NOT NULL DEFAULT '',
    `raw_response_path` varchar(256) NOT NULL DEFAULT '',
    `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `app_name` varchar(128) NOT NULL DEFAULT '',
    `scan_env` varchar(32) NOT NULL DEFAULT '',
    `api_path` varchar(256) NOT NULL DEFAULT '',
    `advanced_rule_id` bigint DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_last_update_time` (`last_update_time`),
    KEY `idx_scanId_scanMode` (`scan_id`, `scan_mode`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
