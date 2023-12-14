-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE avg_weighted_score FLOAT;

    SELECT SUM(c.score * p.weight) INTO total_score
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    SELECT SUM(p.weight) INTO total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    IF total_score IS NOT NULL AND total_weight IS NOT NULL THEN
        SET avg_weighted_score = total_score / total_weight;
        UPDATE users SET average_score = avg_weighted_score WHERE id = user_id;
    END IF;
END //

DELIMITER ;
