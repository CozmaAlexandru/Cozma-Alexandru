CREATE OR REPLACE PROCEDURE bronze.load_bronze()
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE NOTICE '------------------------------------------------';
    RAISE NOTICE 'Loading CRM Tables';
    RAISE NOTICE '------------------------------------------------';
    
    
    RAISE NOTICE '>> Truncating Table: bronze.crm_cust_info';
    TRUNCATE TABLE bronze.crm_cust_info;

    RAISE NOTICE '>> Inserting Data Into: bronze.crm_cust_info';
    COPY bronze.crm_cust_info
    FROM 'C:/temp/cust_info.csv'
    WITH (
        FORMAT CSV,
        HEADER,
        DELIMITER ','
    );

    
    RAISE NOTICE '>> Truncating Table: bronze.crm_prd_info';
    TRUNCATE TABLE bronze.crm_prd_info;

    RAISE NOTICE '>> Inserting Data Into: bronze.crm_prd_info';
    COPY bronze.crm_prd_info
    FROM 'C:/temp/prd_info.csv'
    WITH (
        FORMAT CSV,
        HEADER,
        DELIMITER ','
    );


    RAISE NOTICE '>> Truncating Table: bronze.crm_sales_details';
    TRUNCATE TABLE bronze.crm_sales_details;

    RAISE NOTICE '>> Inserting Data Into: bronze.crm_sales_details';
    COPY bronze.crm_sales_details
    FROM 'C:/temp/sales_details.csv'
    WITH (
        FORMAT CSV,
        HEADER,
        DELIMITER ','
    );

    RAISE NOTICE '------------------------------------------------';
    RAISE NOTICE 'Loading ERP Tables';
    RAISE NOTICE '------------------------------------------------';


	RAISE NOTICE '>> Truncating Table: bronze.erp_cust_az12';
    TRUNCATE TABLE bronze.erp_cust_az12;

    RAISE NOTICE '>> Inserting Data Into: bronze.erp_cust_az12';
    COPY bronze.erp_cust_az12
    FROM 'C:/temp/cust_az12.csv'
    WITH (
        FORMAT CSV,
        HEADER,
        DELIMITER ','
    );


	RAISE NOTICE '>> Truncating Table: bronze.erp_px_cat_g1v2';
    TRUNCATE TABLE bronze.erp_px_cat_g1v2;

    RAISE NOTICE '>> Inserting Data Into: bronze.erp_px_cat_g1v22';
    COPY bronze.erp_px_cat_g1v2
    FROM 'C:/temp/px_cat_g1v2.csv'
    WITH (
        FORMAT CSV,
        HEADER,
        DELIMITER ','
    );


	RAISE NOTICE '>> Truncating Table: bronze.erp_loc_a101';
    TRUNCATE TABLE bronze.erp_loc_a10;

    RAISE NOTICE '>> Inserting Data Into: bronze.erp_loc_a101';
    COPY bronze.erp_loc_a101
    FROM 'C:/temp/loc_a101.csv'
    WITH (
        FORMAT CSV,
        HEADER,
        DELIMITER ','
    );

	

END;
$$;
