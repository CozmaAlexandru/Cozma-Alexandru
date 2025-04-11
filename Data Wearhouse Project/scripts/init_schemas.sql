/*
==========================================================
Create Schemas 
==========================================================
Script purpose:
	This script sets up three schemas: 'bronze', 'silve' and 'gold' which are
	going to be developed later into the data processing layers of the warehouse
*/

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
