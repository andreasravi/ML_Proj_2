#coding: utf-8
import os
import re
#import yaml

def check_def(list, new_cf_def):
    for i in list:
        if "#" in i:
            pass
        elif "def " in i:
            new_cf_def.append(i[0:-1])
        else:
            pass

def check_mod(list, new_cf_mod):
    for i in list:
        if "#" in i:
            pass
        elif "module " in i:
            new_cf_mod.append(i[0:-1])
        else:
            pass

def hardcheck(string):
    wrong_list = ["", " "]
    if string in wrong_list:
        return False
    else:
        for i in ["when", "VERSION"]:
            if i in string:
                return False
        return True

def gen_ori_fc(list, new_cf_float, cf_ori_list):
    buffering = ""
    wrong_list = ["", " ", "VERSION", "VERSION="]
    for i in list:
        #print i
        if re.findall(r"\d+\.?\d*",i):
            #print re.findall(r"\d+\.?\d*\.?\d*",i)[0]

            temp_value = re.findall(r"\d+\.?\d*",i)[0]
            temp_key = re.sub('\s','',re.split(temp_value, i)[0])
            if "#" in temp_key:
                pass
            else:
                if len(temp_key) <= 1:
                    temp_key = buffering + temp_key
                if (temp_key not in cf_ori_list) and (hardcheck(temp_key) == True):
                    cf_ori_list.append(temp_key)

        else:
            pass

        if i[-1] == "\n":
            buffering = re.sub('\s','',i)[:-1]
        else:
            buffering = re.sub('\s','',i)
        #buffering = i

def boundary(value):
    if value > 10000000000:
        return 10000000000
    else:
        return value

def check_float(list, new_cf_float, cf_ori_list):
    buffering = ""
    for i in list:
        #print i
        if re.findall(r"\d+\.?\d*",i):
            #print re.findall(r"\d+\.?\d*\.?\d*",i)[0]

            temp_value = re.findall(r"\d+\.?\d*",i)[0]
            temp_key = re.sub('\s','',re.split(temp_value, i)[0])
            temp_value = boundary(float(temp_value))
            temp_value = str(float(temp_value))
            if len(temp_key) <= 1:
                temp_key = buffering + temp_key
            new_cf_float.append((temp_key, temp_value))
            
        else:
            pass

        if i[-1] == "\n":
            buffering = re.sub('\s','',i)[:-1]
        else:
            buffering = re.sub('\s','',i)

    '''
    for i in list:
        if re.findall(r"\d+\.?\d*",i):
            #print re.findall(r"\d+\.?\d*\.?\d*",i)[0]

            temp = re.findall(r"\d+\.?\d*",i)[0]
            new_cf_float.append((re.sub('\s','',re.split(temp, i)[0]),re.findall(r"\d+\.?\d*",i)[0]))
            
        else:
            pass
    #print "kakaka", len(cf_ori_list)
    '''


def ymlparser(obj, indent=' '):
    str_list = []
    def _pretty(obj, indent):
        for i, tup in enumerate(obj.items()):
            k, v = tup
            if isinstance(k, basestring): k = '"%s"'% k
            if isinstance(v, basestring): v = '"%s"'% v
            if isinstance(v, dict):
                v = ''.join(_pretty(v, indent + k))
            if i == 0:
                if len(obj) == 1:
                    yield '%s%s'% (k, v)
                else:
                    yield '%s%s\n'% (k, v)
            elif i == len(obj) - 1:
                yield '%s%s%s'% (indent, k, v)
            else:
                yield '%s%s%s\n'% (indent, k, v)
    temp = ""
    for i in (''.join(_pretty(obj, indent)) + '\n'):
        if i == "\n":
            str_list.append(temp)
            temp = ""
        else:
            temp += i
    return str_list


def codefeature_src(rootDir, depth, cf_ori_list):
    if depth == 1:
        new_cf_float = []
        list_dirs = os.walk(rootDir)
        for root, dirs, files in list_dirs:
            
            for f in files:
                if f == ".DS_Store":
                    pass
                else:
                                      
                    if ("travis.yml" in os.path.join(root,f)) or (".gemspec" in os.path.join(root,f)) or ("Gemfile" in os.path.join(root,f)) or (".rb" in os.path.join(root,f)): #now we only consider source code, in order not to hard coding, kind of exclude travis.yml and gemfile
                        
                        onputting = open(os.path.join(root,f)).readlines()
                        
                        gen_ori_fc(onputting, new_cf_float, cf_ori_list)
                    else:
                        pass


                    '''
                    #start coding 7.20
                    if ("travis.yml" in os.path.join(root,f)):
                        with open(os.path.join(root,f)) as tempfile:
                            dataMap = yaml.safe_load(tempfile)
                        temp_list = ymlparser(dataMap)
                        for i in temp_list:
                            if i not in cf_ori_list:
                                cf_ori_list.append(i)
                            else:
                                pass

                    else:
                        pass
                    '''

        

        return "\n"


    elif depth == 2:

        new_cf_def = []
        new_cf_mod = []
        new_cf_float = []
        list_dirs = os.walk(rootDir)
        #depth = 0
        cnt_file = 0

        for root, dirs, files in list_dirs:

            for f in files:
                cnt_file += 1
                if f == ".DS_Store":
                    pass
                else:
                    #print os.path.join(root,f)
                    #print type(os.path.join(root,f))
                    if ("travis.yml" in os.path.join(root,f)) or (".gemspec" in os.path.join(root,f)) or ("Gemfile" in os.path.join(root,f)) or (".rb" in os.path.join(root,f)):
                        onputting = open(os.path.join(root,f)).readlines()
                        #check_def(onputting,new_cf_def)
                        #check_mod(onputting,new_cf_mod)
                        check_float(onputting, new_cf_float, cf_ori_list)
                    else:
                        pass


                    '''
                    #start coding 7.20
                    if ("travis.yml" in os.path.join(root,f)):
                        with open(os.path.join(root,f)) as tempfile:
                            dataMap = yaml.safe_load(tempfile)
                        temp_list = ymlparser(dataMap)
                        for i in temp_list:
                            new_cf_float.append((i, "1.000001"))

                    else:
                        pass
                    '''


        #for i in new_cf_float:
        #    print "nwe", i

        newstring = ""

        for i in cf_ori_list:
            flag_have = 0
            for j in new_cf_float:
                if j[0] == i:
                    flag_have = 1
                    buffering = j[1]
            if flag_have == 0:
                newstring = newstring + "0" + ","
            elif flag_have == 1:
                newstring = newstring + buffering + ","
            else:
                pass

        
        newstring = newstring[0:-1]
        re.sub('\s','',newstring)


        #print "all length", len(re.split(',', newstring))
        return newstring + "\n"
        
    


