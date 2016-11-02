import numpy as np
import pickle
import sys
import codecs
import scipy
from scipy import sparse


class Data(object):

    '''
    This data class can load recommend data from file and transform them to numpy format and other format(TODO).
    
    '''

    def __init__(self):
        '''
        Parameter:
            None
        '''
        self._data = []
        self.vals = []
        self.rows = []
        self.cols = []
        self.is_int = False 
        self.split = False
    def set(self,data,extend=False):
        '''
        Set data(a list) to this data class.
        
        Parameter:
           data: a list of tuples
           extend:  covering old data or not
        '''
        
        if extend:
            self._data.append(data)
        else:
            self._data = data
        
        return None
        
    def get(self):
        '''
        get origin data (a list of tuples)
        '''
        
        return self._data
        
    def get_in_scipy_csr_sparse(self,not_map = True,row_dict=None,col_dict=None):
        '''
        get data in scipy.sparse.csr_matrix formate
        
        Parameter:
            row_dict: a dictory Mapping names in row to integer
            col_dict: a dictory Mapping names in col to integer
        '''
        # TODO:: it is not necessary to pass on dictory
        if not not_map:
            if not row_dict or not row_dict:
                raise ValueError('You must pass on map function.')
            else:
                '''
                TODO : Deal with dictory
                '''
                
                return scipy.sparse.csr_matrix( scipy.sparse.coo_matrix( (self.vals,(self.rows,self.cols)) ) )
        else:
            if not self.is_int:
                raise ValueError('Since you pass row and col on as no integer,you should set not_map False and pass dictory on.')
            else:
                '''
                for line in self._data:
                    try:
                        value,row,col = line
                    except:
                        raise ValueError
                    vals.append(value)
                    rows.append(row)
                    cols.append(col)
                '''
                return scipy.sparse.csr_matrix( scipy.sparse.coo_matrix( (self.vals,(self.rows,self.cols)) ) )
        
    def get_in_numpy_format(self,not_map = True,row_dict=None,col_dict=None):
        '''
        get data in numpy formate
        
        Parameter:
            row_dict: a dictory Mapping names in row to integer
            col_dict: a dictory Mapping names in col to integer
        '''
        return self.get_in_scipy_csr_sparse(not_map,row_dict,col_dict).toarray() 
    
    def get_mask(self):
        '''
        score matrix's indicator
        '''
        return scipy.sparse.csr_matrix( scipy.sparse.coo_matrix( (np.ones(len(self.rows)) ,( np.array(self.rows),np.array(self.cols) ) ) ) ).toarray()
        
    def get_in_scipy_csr_sparse_valid(self,not_map = True,row_dict=None,col_dict=None):
        '''
        get data in scipy.sparse.csr_matrix formate
        
        Parameter:
            row_dict: a dictory Mapping names in row to integer
            col_dict: a dictory Mapping names in col to integer
        '''
        try:
            assert self.split==True
        except:
            raise ValueError('you should run Splitdata first.')
        # TODO:: it is not necessary to pass on dictory
        if not not_map:
            if not row_dict or not row_dict:
                raise ValueError('You must pass on map function.')
            else:
                '''
                TODO : Deal with dictory
                '''
                
                return scipy.sparse.csr_matrix( scipy.sparse.coo_matrix( (self.vals,(self.rows,self.cols)) ) )
        else:
            if not self.is_int:
                raise ValueError('Since you pass row and col on as no integer,you should set not_map False and pass dictory on.')
            else:
                '''
                for line in self._data:
                    try:
                        value,row,col = line
                    except:
                        raise ValueError
                    vals.append(value)
                    rows.append(row)
                    cols.append(col)
                '''
                return scipy.sparse.csr_matrix( scipy.sparse.coo_matrix( (self.valid_vals,(self.valid_rows,self.valid_cols)) ) )
        
    def get_in_numpy_format_valid(self,not_map = True,row_dict=None,col_dict=None):
        '''
        get data in numpy formate
        
        Parameter:
            row_dict: a dictory Mapping names in row to integer
            col_dict: a dictory Mapping names in col to integer
        '''
        return self.get_in_scipy_csr_sparse_valid(not_map,row_dict,col_dict).toarray() 
    
    def get_mask_valid(self):
        '''
        score matrix's indicator
        '''
        try:
            assert self.split==True
        except:
            raise ValueError('you should run Splitdata first.')
        return scipy.sparse.csr_matrix( scipy.sparse.coo_matrix( (np.ones(len(self.valid_rows)) ,( np.array(self.valid_rows),np.array(self.valid_cols) ) ) ) ).toarray()
    
    def add_tuple(self, tuple):
        '''
        add data to this data class.
        '''
        
        #E.g: tuple = (25, "ocelma", "u2") -> "ocelma has played u2 25 times"
        if not len(tuple) == 3:
            raise ValueError('Tuple format not correct (should be: <value, row_id, col_id>)')
        value, row_id, col_id = tuple
        if not value and value != 0:
            raise ValueError('Value is empty %s' % (tuple,))
        if isinstance(value, basestring):
            raise ValueError('Value %s is a string (must be an int or float) %s' % (value, tuple,))
        if row_id is None or row_id == '':
            raise ValueError('Row id is empty %s' % (tuple,))
        if col_id is None or col_id == '':
            raise ValueError('Col id is empty %s' % (tuple,))
        self._data.append(tuple)
        self.vals.append(value)
        self.rows.append(row_id)
        self.cols.append(col_id)
    
    def SplitData(self, percent = 0.8):
        '''
        Split the dataset into two parts
        
        Parameter:
            percent : how much percent training set hold
        '''
        try:
            assert self.split == False
        except:
            raise ValueError("Data set has been splited")
        dividePoint = np.int64(len(self.vals) * percent)
        self.valid_vals = self.vals[dividePoint:]
        self.valid_rows = self.rows[dividePoint:]
        self.valid_cols = self.cols[dividePoint:]
        self.vals = self.vals[:dividePoint]
        self.rows = self.rows[:dividePoint]
        self.cols = self.cols[:dividePoint]
        self.split = True
        #Matrix size was determined by training data. Spliting data may diminish matrix size, which case index-out-of-range error.
        try:
            self.add_tuple((0,self.row_max, self.col_max))
        except:
            raise ValueError('Missing row_max and row_col, you should run load first.')
        try:
            self.valid_vals.append(0.0)
            self.valid_rows.append(self.row_max)
            self.valid_cols.append(self.col_max)
        except:
            raise ValueError('Missing row_max and row_col, you should run load first.')
        
    def load(self, path, force=True, sep='\t', format=None, pickle=False):
        """
        Loads data from a file
        
        Pamameter:
            path: file path
            force: Clearn already added data or not
            sep: Seperator among file
            format:Format of the file content. 
                Default format is 'value': 0 (first field), then 'row': 1, and 'col': 2.
                E.g: format={'row':0, 'col':1, 'value':2}. The row is in position 0, 
                then there is the column value, and finally the rating. 
                So, it resembles to a matrix in plain format
            pickle: if input file is a pickle file
        """
        if force:
            self._data = list([])
        if pickle:
            self._load_pickle(path)
        else:
            i = 0 
            self.row_max = 0
            self.col_max = 0
            for line in codecs.open(path, 'r', 'utf8'):
                data = line.strip('\r\n').split(sep)
                value = None
                if not data:
                    raise TypeError('Data is empty or None!')
                if not format:
                    # Default value is 1
                    try:
                        value, row_id, col_id = data
                    except:
                        value = 1
                        row_id, col_id = data
                else:
                    try:
                        # Default value is 1
                        try:
                            value = data[format['value']]
                        except KeyError, ValueError:
                            value = 1
                        try: 
                            row_id = data[format['row']]
                        except KeyError:
                            row_id = data[1]
                        try:
                            col_id = data[format['col']]
                        except KeyError:
                            col_id = data[2]
                        row_id = row_id.strip()
                        col_id = col_id.strip()
                        if format.has_key('ids') and (format['ids'] == int or format['ids'] == 'int'):
                            self.is_int = True
                            try:
                                row_id = int(row_id)
                                if row_id > self.row_max:
                                    self.row_max = row_id
                            except:
                                print 'Error (ID is not int) while reading: %s' % data #Just ignore that line
                                continue
                            try:
                                col_id = int(col_id)
                                if col_id > self.col_max:
                                    self.col_max = col_id
                            except:
                                print 'Error (ID is not int) while reading: %s' % data #Just ignore that line
                                continue
                    except IndexError:
                        #raise IndexError('while reading %s' % data)
                        print 'Error while reading: %s' % data #Just ignore that line
                        continue
                # Add tuple
                try:
                    self.add_tuple((float(value), row_id, col_id))
                except:
                    if 1:
                        sys.stdout.write('\nError while reading (%s, %s, %s). Skipping this tuple\n' % (value, row_id, col_id))
                    #raise ValueError('%s is not a float, while reading %s' % (value, data))
                i += 1
                if 1:
                    if i % 100000 == 0:
                        sys.stdout.write('.')
                    if i % 1000000 == 0:
                        sys.stdout.write('|')
                    if i % 10000000 == 0:
                        sys.stdout.write(' (%d M)\n' % int(i/1000000))


    def load_pickle(self,path):
    
        self._data = pickle.load(codecs.open(path))
    
    def save_pickle(self,path):
    
        pickle.dump(self._data,open(path,'w'))
        
        
        
        
        
        
