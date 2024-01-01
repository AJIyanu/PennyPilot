DELIMITER //

CREATE TRIGGER update_stock_after_sale
AFTER INSERT ON sales
FOR EACH ROW
BEGIN
    IF NEW.stock_id IS NOT NULL THEN
        UPDATE stock
        SET stock_qty = stock_qty - NEW.quantity
        WHERE id = NEW.stock_id;
    END IF;
END //

DELIMITER ;
