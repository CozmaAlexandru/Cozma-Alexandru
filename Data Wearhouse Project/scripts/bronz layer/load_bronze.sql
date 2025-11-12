/*
===============================================================================
Stored Procedure: Load Bronze Layer (Source -> Bronze)
===============================================================================
Script Purpose:
    This stored procedure loads data into the 'bronze' schema from external CSV files. 
    It performs the following actions:
    - Truncates the bronze tables before loading data.
    - Uses the `COPY` command to load all the data from csv Files to bronze tables, in a batch.

Parameters:
    None. 
	  This stored procedure does not accept any parameters or return any values.

Usage Example:
    CALL bronze.load_bronze();
===============================================================================
*\

CREATE OR REPLACE PROCEDURE bronze.load_bronze()
LANGUAGE plpgsql
AS $$
DECLARE start_time TIMESTAMP;
			end_time TIMESTAMP;
BEGIN
	
    RAISE NOTICE '------------------------------------------------';
    RAISE NOTICE 'Loading CRM Tables';
    RAISE NOTICE '------------------------------------------------';
    
    start_time = now();
    RAISE NOTICE '>> Truncating: bronze.crm_cust_info';
    TRUNCATE TABLE bronze.crm_cust_info;

    RAISE NOTICE '>> Loading: bronze.crm_cust_info';
    COPY bronze.crm_cust_info
    FROM 'C:/temp/cust_info.csv'
    WITH (
        FORMAT CSV,
        HEADER,
        DELIMITER ','
    );
	end_time = now();
	RAISE NOTICE 'Duration: % seconds', EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '------';

	 start_time = now();
    RAISE NOTICE '>> Truncating: bronze.crm_prd_info';
    TRUNCATE TABLE bronze.crm_prd_info;

    RAISE NOTICE '>> Loading: bronze.crm_prd_info';
    COPY bronze.crm_prd_info
    FROM 'C:/temp/prd_info.csv'
    WITH (
        FORMAT CSV,
        HEADER,
        DELIMITER ','
    );
	 end_time = now();
	RAISE NOTICE 'Duration: % seconds', EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '------';

	 start_time = now();
    RAISE NOTICE '>> Truncating: bronze.crm_sales_details';
    TRUNCATE TABLE bronze.crm_sales_details;

    RAISE NOTICE '>> Loading: bronze.crm_sales_details';
    COPY bronze.crm_sales_details
    FROM 'C:/temp/sales_details.csv'
    WITH (
        FORMAT CSV,
        HEADER,
        DELIMITER ','
    );
	 end_time = now();
	RAISE NOTICE 'Duration: % seconds', EXTRACT(EPOCH FROM (end_time - start_time));
	
    RAISE NOTICE '------------------------------------------------';
    RAISE NOTICE 'Loading ERP Tables';
    RAISE NOTICE '------------------------------------------------';
	
	 start_time = now();
	RAISE NOTICE '>> Truncating: bronze.erp_cust_az12';
    TRUNCATE TABLE bronze.erp_cust_az12;

    RAISE NOTICE '>> Loading: bronze.erp_cust_az12';
    COPY bronze.erp_cust_az12
    FROM 'C:/temp/cust_az12.csv'
    WITH (
        FORMAT CSV,
        HEADER,
        DELIMITER ','
    );
	 end_time = now();
	RAISE NOTICE 'Duration: % seconds', EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '------';

	 start_time = now();
	RAISE NOTICE '>> Truncating: bronze.erp_px_cat_g1v2';
    TRUNCATE TABLE bronze.erp_px_cat_g1v2;

    RAISE NOTICE '>> Loading: bronze.erp_px_cat_g1v22';
    COPY bronze.erp_px_cat_g1v2
    FROM 'C:/temp/px_cat_g1v2.csv'
    WITH (
        FORMAT CSV,
        HEADER,
        DELIMITER ','
    );
	 end_time = now();
	RAISE NOTICE 'Duration: % seconds', EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '------';

	 start_time = now();
	RAISE NOTICE '>> Truncating: bronze.erp_loc_a101';
    TRUNCATE TABLE bronze.erp_loc_a101;

    RAISE NOTICE '>> Loading: bronze.erp_loc_a101';
    COPY bronze.erp_loc_a101
    FROM 'C:/temp/loc_a101.csv'
    WITH (
        FORMAT CSV,
        HEADER,
        DELIMITER ','
    );
	 end_time = now();
	RAISE NOTICE 'Duration: % seconds', EXTRACT(EPOCH FROM (end_time - start_time));
END;
$$;
