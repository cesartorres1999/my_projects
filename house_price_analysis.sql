-- House Price Data Exploration Project in SQL

-- Step 1: Create a new database to work with
CREATE DATABASE IF NOT EXISTS HousePriceDB;

-- Step 2: Switch to the newly created database
USE HousePriceDB;

-- Step 3: Drop the existing table (if it exists) to avoid conflicts
DROP TABLE IF EXISTS HousePrices;

-- Step 4: Create the HousePrices table to match the CSV structure
CREATE TABLE HousePrices (
    Square_Footage INT,
    Num_Bedrooms INT,
    Num_Bathrooms INT,
    Year_Built INT,
    Lot_Size FLOAT,
    Garage_Size INT,
    Neighborhood_Quality INT,
    House_Price FLOAT
);

-- Step 5: Load the CSV data into the table
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/house_price_regression_dataset.csv'
INTO TABLE HousePrices
FIELDS TERMINATED BY ',' -- Assumes a comma-separated CSV
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS -- Ignore the header row
(Square_Footage, Num_Bedrooms, Num_Bathrooms, Year_Built, Lot_Size, Garage_Size, Neighborhood_Quality, House_Price);

-- Data Analysis Phase: Perform data exploration and analysis using SQL queries

-- Analysis 1: Average house price by year built
-- Step 1: Drop the temporary table if it already exists
DROP TEMPORARY TABLE IF EXISTS AvgPriceByYear;

-- Step 2: Create the temporary table to save the result
CREATE TEMPORARY TABLE AvgPriceByYear AS
SELECT Year_Built, AVG(House_Price) AS Avg_Price
FROM HousePrices
GROUP BY Year_Built;

-- Step 3: Display the temp table
SELECT * FROM AvgPriceByYear;

-- Analysis 2: Price by neighborhood quality
-- Step 1: Drop the temporary table if it already exists
DROP TEMPORARY TABLE IF EXISTS AvgPriceByNeighborhood;

-- Step 2: Create the temporary table for neighborhood prices
CREATE TEMPORARY TABLE AvgPriceByNeighborhood AS
SELECT Neighborhood_Quality, AVG(House_Price) AS Avg_Price
FROM HousePrices
GROUP BY Neighborhood_Quality;

-- Step 3: Display the temp table
SELECT * FROM AvgPriceByNeighborhood;

-- Analysis 3: Price distribution by number of bedrooms
-- Step 1: Drop the temporary table if it already exists
DROP TEMPORARY TABLE IF EXISTS PriceByBedrooms;

-- Step 2: Create the temporary table for bedroom-based prices
CREATE TEMPORARY TABLE PriceByBedrooms AS
SELECT Num_Bedrooms, COUNT(*) AS House_Count, AVG(House_Price) AS Avg_Price
FROM HousePrices
GROUP BY Num_Bedrooms;

-- Step 3: Display the temp table
SELECT * FROM PriceByBedrooms;

-- Analysis 4: Lot size effect on house price (Updated Query)
-- Step 1: Drop the temporary table if it already exists
DROP TEMPORARY TABLE IF EXISTS PriceByLotSize;

-- Step 2: Calculate the average price by lot size category and save in a temp table
CREATE TEMPORARY TABLE PriceByLotSize AS
WITH LotSizeCategory AS (
    SELECT Lot_Size, House_Price,
           CASE
               WHEN Lot_Size < 1 THEN 'Small'
               WHEN Lot_Size BETWEEN 1 AND 3 THEN 'Medium'
               ELSE 'Large'
           END AS LotCategory
    FROM HousePrices
)
SELECT LotCategory, COUNT(*) AS House_Count, AVG(House_Price) AS Avg_Price
FROM LotSizeCategory
GROUP BY LotCategory;

-- Step 3: Display the temp table
SELECT * FROM PriceByLotSize;

-- Analysis 5: Correlation between square footage and price
-- Step 1: Drop the temporary table if it already exists
DROP TEMPORARY TABLE IF EXISTS PriceVsSquareFootage;

-- Step 2: Create the temporary table for price vs square footage
CREATE TEMPORARY TABLE PriceVsSquareFootage AS
SELECT Square_Footage, AVG(House_Price) AS Avg_Price
FROM HousePrices
GROUP BY Square_Footage;

-- Step 3: Display the temp table
SELECT * FROM PriceVsSquareFootage;

-- Analysis 6: Filter houses built after 2000 with garages
-- Step 1: Drop the temporary table if it already exists
DROP TEMPORARY TABLE IF EXISTS HighValueHouses;

-- Step 2: Save the filtered results in a temp table
CREATE TEMPORARY TABLE HighValueHouses AS
SELECT Square_Footage, Year_Built, Garage_Size, House_Price
FROM HousePrices
WHERE Year_Built > 2000 AND Garage_Size > 0
ORDER BY House_Price DESC;

-- Step 3: Display the temp table
SELECT * FROM HighValueHouses;

-- Analysis 7: Outlier detection for high house prices
-- Step 1: Drop the temporary table if it already exists
DROP TEMPORARY TABLE IF EXISTS PriceOutliers;

-- Step 2: Detect high-price outliers and save in a temp table
CREATE TEMPORARY TABLE PriceOutliers AS
SELECT House_Price
FROM HousePrices
WHERE House_Price > (SELECT AVG(House_Price) + 2 * STDDEV(House_Price) FROM HousePrices);

-- Step 3: Display the temp table
SELECT * FROM PriceOutliers;

-- Analysis 8: Price distribution for houses with more than 3 bedrooms
-- Step 1: Drop the temporary table if it already exists
DROP TEMPORARY TABLE IF EXISTS HousesWithMoreThan3Bedrooms;

-- Step 2: Create the temp table for houses with more than 3 bedrooms
CREATE TEMPORARY TABLE HousesWithMoreThan3Bedrooms AS
SELECT Square_Footage, Num_Bedrooms, House_Price
FROM HousePrices
WHERE Num_Bedrooms > 3
ORDER BY House_Price DESC;

-- Step 3: Display the temp table
SELECT * FROM HousesWithMoreThan3Bedrooms;

-- Final Summary: Global statistics by year
-- Step 1: Calculate global statistics by year
SELECT Year_Built, COUNT(*) AS House_Count, AVG(House_Price) AS Avg_Price, MAX(House_Price) AS Max_Price
FROM HousePrices
GROUP BY Year_Built
ORDER BY Year_Built;

-- End of project
