
import unittest
import os.path
import csv


def build_file_path(filename):
    '''
    This is a helper function to make sure the file paths are correct.  
    This is necessary because the tests can be run from different root directories
    '''
    current_directory = os.path.dirname(
        os.path.realpath(__file__))
    return os.path.join(current_directory, 'test_data', filename)


class TestComplexCsv(unittest.TestCase):

    '''
    These tests are to demonstrate how to use the 
    csv module for a complex csv (ie with customization)
    '''

    def test_read_with_reader(self):
        '''
        This test demonstrates how to read from a csv using reader, 
        which pulls in each row of the csv as a list.
        Instead of the standard csv configuration, 
        the reader is configured to read in a tab delimited file 
        with strings values in double quotes.
        '''

        processed_rows = []

        def process_row_as_list(line_num, row):
            '''
            This is a simple function to demonstrate how to 
            'process' the row (which is a list)
            '''
            (name, age, occupation) = row

            processed_rows.append("[%d]%s works as a %s" %
                                  (line_num, name, occupation))

        filename = build_file_path('complex.csv')

        # open the file to read
        with open(filename, 'rb') as f:
            # create the csv reader based upon the open file
            reader = csv.reader(f, delimiter='\t',
                                quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            # reader acts as an iterator and can be looped over
            for i, row in enumerate(reader):
                # ignore header row
                if i > 0:
                    process_row_as_list(reader.line_num, row)

        expected_output = [
            '[2]John works as a Plumber',
            '[3]Cindy works as a CEO',
            '[4]Sara works as a Clerk',
            '[5]James works as a Stock Boy'
        ]
        self.assertEqual(processed_rows, expected_output)

    def test_write_single_rows_with_writer(self):
        '''
        This test demonstrates how to write to a csv using writer 
        by writing a single row at a time where the row is a list.
        Instead of the standard csv configuration, 
        the writer is configured to write a tab delimited file 
        with strings values in double quotes.
        '''

        filename = build_file_path('complex_single_rows_out_with_list.csv')

        # open the file to write
        with open(filename, 'wb') as f:
            # create the csv writer based upon the open file
            writer = csv.writer(f, delimiter='\t',
                                quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            # write column headers
            writer.writerow(['Name', 'Age', 'Occupation'])
            # write one row at a time
            writer.writerow(['Sam', 18, 'Baker'])
            writer.writerow(['Terry', 25, 'Stock Broker'])
            writer.writerow(['Don', 36, 'Post Person'])

        expected_output = (
            '"Name"\t"Age"\t"Occupation"\r\n'
            '"Sam"\t18\t"Baker"\r\n'
            '"Terry"\t25\t"Stock Broker"\r\n'
            '"Don"\t36\t"Post Person"\r\n'
        )
        with open(filename) as f:
            contents = f.read()
            self.assertEquals(contents, expected_output)

    def test_write_multiple_rows_with_writer(self):
        '''
        This test demonstrates how to write to a csv using writer 
        by writing a multiple rows at a time where each row is a list.
        Instead of the standard csv configuration, 
        the writer is configured to write a tab delimited file 
        with strings values in double quotes.
        '''

        filename = build_file_path('complex_all_rows_out_with_list.csv')

        data = [['Name', 'Age', 'Occupation'],
                ['Sam', 18, 'Baker'],
                ['Terry', 25, 'Stock Broker'],
                ['Don', 36, 'Post Person']]

        # open the file to write
        with open(filename, 'wb') as f:
            # create the csv writer based upon the open file
            writer = csv.writer(f, delimiter='\t',
                                quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            # write all data
            writer.writerows(data)

        expected_output = (
            '"Name"\t"Age"\t"Occupation"\r\n'
            '"Sam"\t18\t"Baker"\r\n'
            '"Terry"\t25\t"Stock Broker"\r\n'
            '"Don"\t36\t"Post Person"\r\n'
        )
        with open(filename) as f:
            contents = f.read()
            self.assertEquals(contents, expected_output)

    def process_row_as_dict(self, line_num, row):
        print "[%d]%s works as a %s" %\
            (line_num, row['Name'], row['Occupation'])

    def test_read_with_dictreader(self):
        '''
        This test demonstrates how to read from a csv using DictReader, 
        which pulls in each row of the csv as a dictionary 
        where the keys are the column names.
        Instead of the standard csv configuration, 
        the reader is configured to read in a tab delimited file 
        with strings values in double quotes.
        '''

        processed_rows = []

        def process_row_as_dict(line_num, row):
            '''
            This is a simple function to demonstrate how to 
            'process' the row (which is a dictionary 
            with column headers as keys)
            '''
            processed_rows.append("[%d]%s works as a %s" %
                                  (line_num, row['Name'], row['Occupation']))

        filename = build_file_path('complex.csv')

        # open the file to read
        with open(filename, 'rb') as f:
            # create the csv reader based upon the open file
            reader = csv.DictReader(
                f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            # reader acts as an iterator and can be looped over
            for i, row in enumerate(reader):
                process_row_as_dict(reader.line_num, row)

        expected_output = [
            '[2]John works as a Plumber',
            '[3]Cindy works as a CEO',
            '[4]Sara works as a Clerk',
            '[5]James works as a Stock Boy'
        ]
        self.assertEqual(processed_rows, expected_output)

    def test_write_single_rows_with_dictwriter(self):
        '''
        This test demonstrates how to write to a csv using DictWriter 
        by writing a single row at a time where the row is a dictionary
        with column headers as keys.
        (Notice that the ordering in which the data is created 
        is different from the output order.  
        The order of the columns is defined on the DictWriter)
        Instead of the standard csv configuration, 
        the writer is configured to write a tab delimited file 
        with strings values in double quotes.
        '''
        filename = build_file_path('complex_single_rows_out_with_dict.csv')

        # open the file to write
        with open(filename, 'wb') as f:
            # create the csv writer based upon the open file
            writer = csv.DictWriter(
                f, ['Name', 'Age', 'Occupation'],
                delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            # write column headers
            writer.writeheader()
            # write one row at a time
            writer.writerow(
                {'Name': 'Sam', 'Occupation': 'Baker', 'Age': 18})
            writer.writerow(
                {'Name': 'Terry', 'Occupation': 'Stock Broker', 'Age': 25})
            writer.writerow(
                {'Name': 'Don', 'Occupation': 'Post Person', 'Age': 36})

        expected_output = (
            '"Name"\t"Age"\t"Occupation"\r\n'
            '"Sam"\t18\t"Baker"\r\n'
            '"Terry"\t25\t"Stock Broker"\r\n'
            '"Don"\t36\t"Post Person"\r\n'
        )
        with open(filename) as f:
            contents = f.read()
            self.assertEquals(contents, expected_output)

    def test_write_multiple_rows_with_dictwriter(self):
        '''
        This test demonstrates how to write to a csv using DictWriter 
        by writing a multiple rows at a time where each row is a dictionary
        with column headers as keys.  
        (Notice that the ordering in which the data is created 
        is different from the output order.  
        The order of the columns is defined on the DictWriter)
        Instead of the standard csv configuration, 
        the writer is configured to write a tab delimited file 
        with strings values in double quotes.
        '''
        filename = build_file_path('complex_all_rows_out_with_dict.csv')

        data = [{'Name': 'Sam', 'Occupation': 'Baker', 'Age': 18},
                {'Name': 'Terry', 'Occupation': 'Stock Broker', 'Age': 25},
                {'Name': 'Don', 'Occupation': 'Post Person', 'Age': 36}]

        # open the file to write
        with open(filename, 'wb') as f:
            # create the csv writer based upon the open file
            writer = csv.DictWriter(
                f, ['Name', 'Age', 'Occupation'],
                delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            # write column headers
            writer.writeheader()
            # write all data
            writer.writerows(data)

        expected_output = (
            '"Name"\t"Age"\t"Occupation"\r\n'
            '"Sam"\t18\t"Baker"\r\n'
            '"Terry"\t25\t"Stock Broker"\r\n'
            '"Don"\t36\t"Post Person"\r\n'
        )
        with open(filename) as f:
            contents = f.read()
            self.assertEquals(contents, expected_output)


if __name__ == '__main__':
    unittest.main()
