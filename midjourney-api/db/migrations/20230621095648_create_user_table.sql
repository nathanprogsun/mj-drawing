-- migrate:up


CREATE TABLE `user`
(
    `id`                  int          NOT NULL AUTO_INCREMENT,
    `created_at`          datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP (6),
    `updated_at`          datetime(6) NOT NULL DEFAULT (now(6)) ON UPDATE CURRENT_TIMESTAMP (6),
    `deleted_at`          datetime(6) DEFAULT NULL,
    `nickname`            varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `email`               varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `phone`               varchar(20)  NOT NULL,
    `avatar`              varchar(255)                                                 DEFAULT NULL,
    `hashed_password`     varchar(100) NOT NULL,
    `last_login_datetime` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP (6),
    `gender`              int                                                          DEFAULT '0',
    `hobbies`             varchar(255)                                                 DEFAULT NULL,
    `motto`               varchar(255)                                                 DEFAULT NULL,
    `birthdate`           date                                                         DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- migrate:down
DROP TABLE IF EXISTS User;
