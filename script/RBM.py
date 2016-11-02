from Data import *
import numpy as np


class RBM(object):
    '''
    implement RBM for Recommend System. This code now can just handle the case that the score system is binary. Further work include handling cases that are more complex.
    '''
    def __init__(self,min=0,max=1):
        '''
        Set the up and down bound of score.
        
        Parameter:
            min : down bound of score.
            max : up bound of score.
        '''
        self._data = Data()
        self.min = min
        self.max = max
        #self.randomness_source = np.random.rand(1, 7000000)

    def _init_W(self, force=False):
        '''
        initialization Weight that connect visible layer and hidden layer
        
        Parameter:
            force : if you want to specify the shape of M or not       
        '''
        if not force:
            if (not self._m_num) or (not self._k_num) or (not self._s_num):
                raise ValueError('You should run train if you set parameter force False.')
            else:
                if self._s_num>2:
                    self.W = 0.02*np.random.random((self._m_num,self._k_num,self._s_num))/np.sqrt(self._k_num * self._s_num)
                else:
                    self.W = 0.02*np.random.random((self._m_num,self._k_num))/np.sqrt(self._k_num)
        else:
            raise ValueError('Warning: you should have specified items number and features number.')
        
    def _init_Bk(self, force=False):
        '''
        initialization biaos of hidden layer.
        
        Parameter:
            force : if you want to specify the shape of M or not
            
        '''     
        if not force:
            if (not self._k_num):
                raise ValueError('You should run train if you set parameter force False.')
            else:
                self.Bk = 0.02*np.random.random((self._k_num))
        else:
            raise ValueError('Warning: you should have specified items number and features number.')
            
    def _init_Bms(self,force=False):
        '''
        initialization biaos of visible layer.
        
        Parameter:
            force : if you want to specify the shape of M or not
            
        '''      
        if not force:
            if (not self._m_num) or (not self._s_num):
                raise ValueError('You should run train if you set parameter force False.')
            else:
                if self._s_num>2:
                    self.Bms = np.zeros((self._m_num,self._s_num))
                    try:
                        self.Bms[:,1] = np.log( ( 1+self.data.sum(axis=0) ) / ( 2+self.mask.sum(axis=0 )) )
                        self.Bms[:,0] = np.log( ( 1+self.mask.sum(axis=0)-self.data.sum(axis=0) ) / ( 2+self.mask.sum(axis=0) ) )
                    except:
                        raise ValueError('Missing data and mask, you should run train first.')
                else:
                    self.Bms = 0.02*np.random.random((self._m_num))
                
        else:
            raise ValueError('Warning: you should have specified items number and features number.')
    
    def sigmoid(self, x):
        # sigmoid function.
        return 1.0/(1.0+np.exp(-x))
        
    def load_data(self, path, force=True, sep='\t', format=None, pickle=False, split=False,percent=0.8):
        '''
        Loads data from a file. user is for row and item is for col.
        
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
        '''
        self._data.load(path, force, sep, format, pickle)
        if split == True:
            self._data.SplitData(percent)
            
    def randomize(self, size, seed):
        '''
        Generate random variable given seed and size.
        
        Parameter:
            size : the of desired random output.
            seed : seed of the random process.
        '''
        ret = np.random.random( size )
        return ret        
    
    # TODO : This function fit just when s ==2 ;     
    def discretization(self,probabilities):
        '''
        Gibbs sampliing.
        
        Parameter:
            probabilities : the probability that need to be sampled.
        '''
        try:
            seed = np.int64( probabilities.sum() )
        except:
            raise ValueError('parameter <probabilities> was given in wrong form. We recommend using a numpy type.')
        binary = 0 + (probabilities > self.randomize(probabilities.shape, seed))
        return binary
        
    def getHiddenProbUnderVisibleState(self,Visible):
        '''
        get hidden probability given visible layer state.
        
        Parameter:
            Visible: visible layer state.
        '''
        return self.sigmoid(np.dot(Visible,self.W) + self.Bk)
    
    def getVisibleProbUnderHiddenState(self,Hidden):
        '''
        get visible layer probability given hidden layer state.
        
        Parameter:
            Hidden : hidden layer state.
        '''
        return self.sigmoid(np.dot(Hidden,self.W.T) + self.Bms) 
        
    def update(self,lr=0.001,lambda1=0.001,lambda2=0,mu=0,T=20):
        '''
        update for every iteration.
        '''
        if self._s_num>2:
            raise ValueError('This code cannot handle it when s>2.')
        else:
            W = self.W
            Bk = self.Bk
            Bms = self.Bms
            visibleState = self.data
            hiddenProb = self.getHiddenProbUnderVisibleState(visibleState)
            gradientW1 = np.dot(visibleState.T,hiddenProb)/ ( np.float32(hiddenProb.shape[0]) )
            gradientBm1 = visibleState.sum(axis=0) / hiddenProb.shape[0]
            gradientBk1 = hiddenProb.sum(axis=0) / hiddenProb.shape[0]
            hiddenState = self.discretization(hiddenProb)
            for i in range(T):
                visibleProb = self.getVisibleProbUnderHiddenState(hiddenState)
                visibleState = self.discretization(visibleProb)
                hiddenProb = self.getHiddenProbUnderVisibleState(visibleState)
                hiddenState = self.discretization(hiddenProb)
            gradientW2 = np.dot(visibleState.T,hiddenProb) / ( np.float32(hiddenProb.shape[0]) )
            gradientBm2 = visibleStatesum.sum(axis=0) / hiddenProb.shape[0]
            gradientBk2 = hiddenProb.sum(axis=0) / hiddenProb.shape[0]
            gradientW = gradientW1 - gradientW2 
            gradientBm = gradientBm1 - gradientBm2
            gradientBk = gradientBk1 - gradientBk2
            
            self.W = self.W + lr * gradientW
            self.Bk = self.Bk + lr * gradientBk
            self.Bms = self.Bms + lr * gradientBm
            
            
    def valid(self):
        '''
        valid the train task during training.
        '''
        if self._s_num>2:
            raise ValueError('This code cannot handle it when s>2.')
        else:
            hiddenProb = self.getHiddenProbUnderVisibleState(self.valid_data)
            visibleProb = self.getVisibleProbUnderHiddenState(hiddenProb)
            
            return ( ( self.valid_mask * ( visibleProb - self.valid_data ) )**2 ).sum()

    def train(self,k=100,s=2,iter=100,lr=0.001,lambda1=0.001,lambda2=0,mu=0):
        '''
        training the RBM model.
        '''
        try:
            self._u_num = self._data.row_max + 1
            self._m_num = self._data.col_max + 1
            self._k_num = k
            self._s_num = s
        except:
            raise ValueError('you sould run MF.load_data first.')
        #TODO : what if users specify U and M's shape?
        self.data = self._data.get_in_numpy_format()
        self.mask = self._data.get_mask()
        self.valid_data = self._data.get_in_numpy_format_valid()
        self.valid_mask = self._data.get_mask_valid()
        if not hasattr(self,'W'):
            self._init_W()
        if not hasattr(self,'Bk'):
            self._init_Bk()
        if not hasattr(self,'Bms'):
            self._init_Bms()
        #test if initialization is right
        try:
            assert self.W.shape == self.Bms.shape[:1] + self.Bk.shape + self.Bms.shape[1:]
        except:
            raise ValueError('Initialization is wrong.')
        prvs_score = 1.0e12
        for i in range(iter):
            self.update(lr,lambda1,lambda2,mu)
            cost = self.valid()
            if cost>prvs_score:
                break
            prvs_score =cost
            print 'Iteration:' + str(i+1) +': cost is ' + str(cost)
            


        
    def predict(self,user=None,item=None):
        '''
        Predict score given a user and a item.
        
        Parameter:
            user : user's id
            item : item's id
        '''
        #TODO : here assuming that user and item are given in integer form.
        try:
            assert hasattr(self,'W')
            assert hasattr(self,'Bk')
            assert hasattr(self,'Bms')
        except:
            raise ValueError('You should run MF.factorize first to train the model.')
            
        try:
            if not hasattr(self,'Matrix'):
                hiddenProb = self.getHiddenProbUnderVisibleState(self.data)
                visibleProb = self.getVisibleProbUnderHiddenState(hiddenProb)
                self.Matrix = visibleProb
            score = self.Matrix[user,item]
        except:
            raise ValueError('user and item should be specified as integer.')
            
        score = max(score,self.min)
        score = min(score,self.max)
        
        return float(score)
        
        

    def save_weight(self,path):
        pickle.dump([self.W, self.Bk, self.Bms],open(path,'w'))
    
    def load_weight(self,path):
        self.W, self.Bk, self.Bms = pickle.load(open(path,'r'))
