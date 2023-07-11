-- CREATE AND REPLICATE TABLE FROM TRAIN.CSV
--  https://www.mysqltutorial.org/import-csv-file-mysql-table/
CREATE TABLE train (
    id INT NOT NULL AUTO_INCREMENT,
    date DATE NOT NULL,
    store_nbr INT NOT NULL,
    family VARCHAR(100) NOT NULL,
    sales DECIMAL(10 , 3 ) NOT NULL,
    onpromotion INT NOT NULL,
    PRIMARY KEY (id)
);

-- IMPORT DATA INTO TRAIN TABLE INSTEAD OF USING UI 
LOAD DATA LOCAL INFILE 'absolute_file_path_to_your_train.csv'
INTO TABLE train
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- IF YOU RUN INTO ERROR CODE 3948 ABOVE, DO THIS, AND REPEAT LOAD DATA COMMAND AGAIN
-- https://stackoverflow.com/questions/66848547/mysql-error-code-3948-loading-local-data-is-disabled-this-must-be-enabled-on-b#:~:text=Error%20Code%3A%203948.,the%20client%20and%20server%20side.
SHOW GLOBAL VARIABLES LIKE 'local_infile';

SET GLOBAL local_infile = ON;