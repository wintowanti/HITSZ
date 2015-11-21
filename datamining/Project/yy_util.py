def read_lines(filename):
    '''
        return a list include each line value
    '''
    fs = open(filename,"r");
    ans = fs.read();
    fs.close();
    ans = ans.split("\n")[0::]
    return ans[0:len(ans)-1:]
    
if __name__ == "__main__":
    pass        
    
