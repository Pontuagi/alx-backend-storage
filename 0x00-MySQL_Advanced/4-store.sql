--  script that creates a trigger that decreases the quantity of an item after
DELIMITER //

CREATE TRIGGER decrease_quantity AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE item_name VARCHAR(255); -- Use the appropriate data type

    -- Get the item name from the new order
    SET item_name = NEW.item_name;

    -- If the item exists, update its quantity
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = item_name;

END;
//
DELIMITER ;
