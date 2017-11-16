
    
def print_(text, print_it=False):
    prefix = "netshort >>> "
    if not isinstance(text, str): text = text.decode('ascii')
    if print_it:
        
        print("%s%s"%(prefix, text.replace("\n", "\n"+prefix)))
    
    
def print_v(text):
    print_(text, True)
