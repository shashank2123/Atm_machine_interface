DELIMITER $$
CREATE PROCEDURE SelectTransaction
(IN id INT)
BEGIN
  SELECT * FROM atm_db.atm_app_transcations
  WHERE  account_id_id = id;
END$$ 
DELIMITER ;

DELIMITER $$
CREATE TRIGGER change_lastAccess AFTER INSERT ON atm_db.atm_app_transcations
FOR EACH ROW
BEGIN 
	UPDATE atm_db.atm_app_accounts SET last_access=CURRENT_TIMESTAMP
    WHERE idAccount=NEW.account_id_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER last_passChange AFTER UPDATE ON atm_db.atm_app_pin
FOR EACH ROW
BEGIN 
	UPDATE atm_db.atm_app_carddetails SET last_pinChange=CURRENT_TIMESTAMP
    WHERE pin_id_id=NEW.id;
END$$
DELIMITER ;