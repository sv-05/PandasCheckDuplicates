import pandas as pd
import pandasql as ps
import sys
import logging
import argparse

logging.basicConfig(format='%(asctime)s %(message)s')                       # Logging Code For Better Traceability.
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

df_1 = pd.DataFrame(
data=[
['A','a', 'x', 1],
['A','b', 'x', 1],
['A','c', 'x', 1],
['B','a', 'x', 1],
['B','b', 'x', 1],
['B','c', 'x', 1],
['A','a', 'y', 1],
],
columns=['col_1', 'col_2', 'col_3', 'col_4']
)

def check_duplicates(df, columns):                                          # Function for the main output

    output_dict = {'count': 0}
    cols = ",".join(columns)                                                # Making Columns for SQL Query
    logger.info(" : Columns you passed - {}".format(cols))

    logger.info(" : Running Query on Dataframe ")
    try:                                                                    # Converting Pandas DataFrame To SQL
        query1 = "SELECT {}, COUNT(*) AS cnt " \
                "FROM df " \
                "GROUP BY {} " \
                "HAVING COUNT(*) > 1"
        result = ps.sqldf(query1.format(cols, cols))

    except Exception as error1:
        print('Caught this error in Query1 : Lines[23 - 27]: ' + repr(error1))
        sys.exit(1)
    logger.info(" : Checking If Query Result Is Not Empty")

    if result.empty != True:
        try:
            query3 = "SELECT COUNT(*) AS count " \
                     "FROM result"
            result3 = ps.sqldf(query3)

            logger.info(" : Preparing The Output In A Dictionary")
            output_dict['count'] = (result3.to_dict('list')['count'][0])
            output_dict['sample'] = result.to_dict('list')
            return output_dict                                             # Adding Output To Dictionary As Required

        except Exception as error2:
            print('Caught this error in Query : Lines[34 - 43]: ' + repr(error2))
            sys.exit(1)
    else:
        print("No duplicates found")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('column', nargs='+', help = 'This is where the user passes the column names with space speration in Command Line Arguments')
    params = parser.parse_args()
    print(check_duplicates(df_1, params.column))