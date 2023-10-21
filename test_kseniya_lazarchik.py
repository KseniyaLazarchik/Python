import pyodbc
import pandas
import variables

class TestDataBase:
    conn = pyodbc.connect(DRIVER=variables.driver,
                          SERVER=variables.server,
                          DATABASE=variables.database,
                          UID=variables.username,
                          PWD=variables.password,
                          Trusted_Connection='yes')

    def get_dataframe(self, query):
        print(query)
        df = pandas.read_sql_query(query, self.conn)
        return df

    def test_check_count_rows_in_countries(self):
        """Check the count of rows in the table hr.countries"""
        expected_res = 25  #count of rows in the table
        df = self.get_dataframe("""
                                SELECT *
                                FROM [hr].[countries]
                                """)
        actual_df = df.shape[0]
        assert actual_df == expected_res, "The count of rows is different"

    def test_check_zero_value_in_region_id(self):
        """Check rows with zero value in the table hr.regions"""
        expected_res = 0  # count of expected rows in the table
        df = self.get_dataframe("""
                                    SELECT * 
                                    FROM [hr].[regions]
                                    WHERE region_id = 0; 
                                """)
        actual_df = df.shape[0]
        assert actual_df == expected_res, "rows with zero in region_id"

    def test_check_unexpected_values_in_country_id(self):
        """Check rows with unexpected value in the table hr.regions"""
        expected_res = 0  # count of expected rows in the table
        df = self.get_dataframe("""
                                    SELECT country_id
                                    FROM [hr].[locations]
                                    WHERE country_id NOT LIKE '[A-Z][A-Z]';
                                    """)
        actual_df = df.shape[0]
        assert actual_df == expected_res, "some unexpected values in country_id"

    def test_verify_columns_count_in_table_employees(self):
        """Check the count of columns in the hr.employees table"""
        expected_res = 10  # count of columns in the table
        df = self.get_dataframe("""
                                    SELECT *
                                    FROM INFORMATION_SCHEMA.COLUMNS;
                                """)
        actual_df = df[(df['TABLE_CATALOG'] == 'TRN')
                       & (df['TABLE_NAME'] == 'employees')]
        actual_df = actual_df.shape[0]
        assert actual_df == expected_res, "The count of columns doesn't match"

    def test_check_duplicates_in_jobs_table(self):
        """Check the job_id field for duplicates
            in the hr.jobs table"""
        expected_res = 0  # there should be no duplicates
        df = self.get_dataframe("""
                                   SELECT *
                                   FROM [hr].[jobs];
                                """)
        actual_df = df[['job_id', 'job_title']]. \
            groupby(['job_id']). \
            size().reset_index(name='counts')
        actual_df = actual_df[actual_df['counts'] > 1]
        actual_df = len(actual_df.index)
        assert actual_df == expected_res, "There are duplicates in the table"

    def test_check_min_max_values_for_max_salary(self):
        """ Check min and max values of the max_salary field
            in the hr.jobs table"""
        expected_res = {'max_salary': {'min': 5000.0, 'max': 40000.0}}
        df = self.get_dataframe("""
                                    Select *
                                    From [hr].[jobs];
                                """)
        actual_df = df[['max_salary']].agg(['min', 'max']).to_dict()
        assert actual_df == expected_res, \
            "Min and max values of the max_salary field are incorrect"

    def test_verify_column_name_data_type_in_locations(self):
        """Check the column name and data type
            in the hr.locations table"""
        expected_res = [['location_id', 'int'],
                        ['street_address', 'varchar 40'],
                        ['postal_code', 'varchar 12'],
                        ['city', 'varchar 30'],
                        ['state_province', 'varchar 25'],
                        ['country_id', 'char 2']]
        df = self.get_dataframe("""
            SELECT COLUMN_NAME
                  ,TABLE_CATALOG
                  ,TABLE_NAME
                  ,CASE
                        WHEN CHARACTER_MAXIMUM_LENGTH is NULL
                        THEN Data_type
                        ELSE CONCAT (DATA_TYPE,' ',CHARACTER_MAXIMUM_LENGTH)
                        END [Data_type]
            FROM INFORMATION_SCHEMA.COLUMNS;
                                """)
        actual_df = df[['COLUMN_NAME', 'Data_type']]
        actual_df = actual_df[(df['TABLE_CATALOG'] == 'TRN')
                              & (df['TABLE_NAME'] == 'locations')]
        actual_df = actual_df.values.tolist()
        assert actual_df == expected_res, \
            "The data type or column names are incorrect"

    def close(self):
        pass
