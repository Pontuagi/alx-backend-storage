-- Trigger that resets the attribute valied_email when email changes
DELIMITER //
CREATE TRIGGER update_valid_email AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email != OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;
//
DELIMITER ;
