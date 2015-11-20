def read_lines(filename):
    '''
        return a list include each line value
    '''
    fs = open(filename,"r");
    ans = fs.read();
    fs.close();
    return ans.split("\r\n");
    
if __name__ == "__main__":
    pass        
    
