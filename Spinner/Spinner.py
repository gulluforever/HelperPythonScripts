import random
 
def spin(content):
    """takes a string like
 
    {Hi|Hello|Good morning}, my name is Matt and I have {something {important|special} to say|a favorite book}.
 
    and randomly selects from the options in curly braces
    to produce unique strings.
    """
    start = content.find('{')
    end = content.find('}')
 
    if start == -1 and end == -1:
        #none left
        return content
    elif start == -1:
        return content
    elif end == -1:
        raise "unbalanced brace"
    elif end < start:
        return content
    elif start < end:
        rest = spin(content[start+1:])
        end = rest.find('}')
        if end == -1:
            raise "unbalanced brace"
        return content[:start] + random.choice(rest[:end].split('|')) + spin(rest[end+1:])
       
 
if __name__=='__main__':
    inputtext = raw_input("Enter the Spin Text: ")
    noofarticles = input("Enter No. Of OutPut Articles : ")
    for i in range(0,noofarticles):
        output = spin(inputtext)
        slist = open('OP/output'+str(i)+'.txt', 'w')
        slist.write(output)
        slist.close()
        if i == noofarticles-1:
            print "Program Completed Its Execution"


    

