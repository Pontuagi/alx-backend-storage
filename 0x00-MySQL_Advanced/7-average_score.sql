-- SQL script to create the stored procedure ComputeAverageScoreForUser

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_count INT;
    DECLARE average_score FLOAT;

    SELECT SUM(score), COUNT(*)
    INTO total_score, total_count
    FROM corrections
    WHERE user_id = user_id;

    IF total_count > 0 THEN
        SET average_score = total_score / total_count;

        UPDATE users
        SET average_score = average_score
        WHERE id = user_id;
    END IF;
END
//

DELIMITER ;
