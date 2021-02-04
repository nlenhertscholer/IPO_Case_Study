# IPO Case Study for Ensemble VC
by Nesta Lenhert-Scholer

## File Descriptions
- (store_data.py)[./store_data.py]: This file downloads stock data from Quandl using their API and 
stores the information into a sqlite database.
- (analyze_data.py)[./analyse_data.py]: This file retrieves the data from the database, and performs
a monthly net percent change in the stocks and compares that to Russell 3000. The plots are then saved
into the (plots directory)[./directory/]
- (test.py)[./test.py]: This file performs a simple unit test on the Quandl API access function.