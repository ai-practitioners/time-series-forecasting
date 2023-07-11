-- CREATE AND REPLICATE TABLE FROM TRAIN.CSV
--  https://www.mysqltutorial.org/import-csv-file-mysql-table/
-- CREATE SCHEMA time_series;

-- IF YOU RUN INTO ERROR CODE 3948 ABOVE, DO THIS, AND REPEAT LOAD DATA COMMAND AGAIN
-- https://stackoverflow.com/questions/66848547/mysql-error-code-3948-loading-local-data-is-disabled-this-must-be-enabled-on-b#:~:text=Error%20Code%3A%203948.,the%20client%20and%20server%20side.

USE time_series;

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
LOAD DATA INFILE '/home/ubuntu/repos/time-series-forecasting/data/raw/train.csv'
INTO TABLE train
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SHOW VARIABLES LIKE "secure_file_priv";

SHOW GLOBAL VARIABLES LIKE 'local_infile';

SET GLOBAL local_infile = ON;
