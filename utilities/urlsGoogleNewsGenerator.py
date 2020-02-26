def urlsGenerator(stock,window):
    
    '''
    Parameters:
    string: stock
    list: window
    
    Return:
    list: urls
    
    Documentation: This method receives the name of a stock as a string and a list with two values (strings with the following format: yyyy-mm-dd) indicating a period of time (window). 
                   The first value indicates the begining and the second one the end of the period.
                   This method returns a list with the urls of the news obtained by google which mention the name of the stock. In addition, this method create a text file with with one url per line.
                   
    How to use it?
    
    Here you are an example:
    
    lista = urlsGenerator('alphabet inc', ['2019-01-01','2020-02-13'])
    
    '''
    
    import datetime
    
    urls = []
    
    stk = stock.split(' ')
    stk_str = ""
    f_name = ""
    for p in stk:
        stk_str += p + "+"
        f_name += p + "_"
    stk_str = stk_str[:-1]
    
    #file_urls = open('urls_'+f_name+'.txt', 'w')
    
    #inicio = date.fromisoformat(window[0])
    #final = date.fromisoformat(window[1])
    inicio = datetime.datetime.strptime(window[0], '%Y-%m-%d').date()
    final = datetime.datetime.strptime(window[1], '%Y-%m-%d').date()
    siguiente = inicio
    
    dy = window[0].split("-")[0]
    dm = window[0].split("-")[1]
    dd = window[0].split("-")[2]
    
    while(siguiente != final):
        
        url = "https://www.google.com/search?q=%22" + stk_str +"%22&tbs=cdr%3A1%2Ccd_min%3A"+ dm + "%2F" + dd + "%2F" + dy + "%2Ccd_max%3A" + dm+ "%2F" + dd + "%2F" + dy + "&tbm=nws"
        urls.append(url)
        """file_urls.write(url+'\n')"""
        
        siguiente = siguiente + datetime.timedelta(days=1)
        
        dy = str(siguiente).split("-")[0]
        dm = str(siguiente).split("-")[1]
        dd = str(siguiente).split("-")[2]
                 
    """file_urls.close()"""
    
    return urls