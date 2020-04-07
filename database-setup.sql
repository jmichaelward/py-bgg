/**
Database schema to pull data from BoardGameGeek into a localized structure.
*/

CREATE DATABASE IF NOT EXISTS `py-bgg`;

USE `py-bgg`;

/*
Users should have the following properties:
- id
- username

At least for now. There may be a case for more properties, but that's the bare minimum.
 */
CREATE TABLE IF NOT EXISTS `users` (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    bgg_id INT UNSIGNED UNIQUE NOT NULL,
    username VARCHAR(256) NOT NULL
);


/*
Games should inherit the primary values we care about from BGG.
- id
- bgg_id
- title

 */
CREATE TABLE IF NOT EXISTS `games` (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    bgg_id INT UNSIGNED UNIQUE NOT NULL,
    title VARCHAR(256) NOT NULL
) ENGINE = InnoDB;

/*
A user_collection contains records of games owned by users. It should have the following fields:
- id
- user_id (foreign key)
- game_id (foreign key)
- game_status - a game can have multiple statuses, so it may be necessary to split this up. Think about its structure.

Look into whether it's necessary to create an index on the user_id (so that you can quickly search for a user ID), or
if MariaDB automatically creates indexes for foreign keys, because hey, it's been awhile since that database management
fundamentals course.
 */

CREATE TABLE IF NOT EXISTS `user_collection` (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNSIGNED NOT NULL,
    game_id INT UNSIGNED NOT NULL,
    CONSTRAINT `collection_user_id`
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE
        ON UPDATE RESTRICT,
    CONSTRAINT `collection_game_id`
        FOREIGN KEY (game_id) REFERENCES games (id)
        ON DELETE CASCADE
        ON UPDATE RESTRICT
) ENGINE = InnoDB;

CREATE UNIQUE INDEX `user_owned_game`
    ON user_collection (user_id, game_id)

 /*
 A table to track user plays. This should contain the following fields:
 - id
 - user_id
 - game_id
 - date_played

 Look into the BGG API and find out whether there are other details to track.
  */
# CREATE TABLE IF NOT EXISTS `user_plays` (
#     id INT PRIMARY KEY AUTO_INCREMENT
# );
