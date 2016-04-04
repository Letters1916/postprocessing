#-*- coding: utf-8 -*-
from lxml import etree
import os, shutil, re

NSMAP = {"tei": "http://www.tei-c.org/ns/1.0", 
          "xml": "http://www.w3.org/XML/1998/namespace",
          "office" :"urn:oasis:names:tc:opendocument:xmlns:office:1.0",
          "text" : "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
          }
    


error_log = {}
error_log['not_valid'] = []
error_log['schema_issue'] = []
error_log['unicode_issue'] = []

parser = etree.XMLParser(dtd_validation=True)

def open_file(xml_file):
    #do not encode in unicode when opening, e.g. with codecs module
    
    with open(xml_file, "r+b") as f:
        
        tree = etree.XML(f.read())
        #return tree
        return tree
    
def validate_with_schema(schema, xml_tree):
    return schema.validate(xml_tree)

def replaceStrg(strg, pat, replaceStrg):
    m = re.split(pat, strg)
    return replaceStrg.join(m)

def transformTEI(fileName, fileTree, xsltTree):
    try:
        if fileTree is not None:
            transform = etree.XSLT(xsltTree)
            result_tree = transform(fileTree)
            return result_tree
        else:
            error_log['not_valid'].append(fileName)
    except UnicodeDecodeError:
        print("Unicode error!")
        """
            with open(xml_file_path+os.sep+f_name, "r") as f:
                error_line = 0
                try:
                    for line in f.readline():
                        error_line+=1
                except UnicodeDecodeError:
                    print(error_line)
        """
        error_log['unicode_issue'].append(fileName)
    except etree.XMLSyntaxError:
        print("XMLSyntaxError error!")
        error_log['not_valid'].append(fileName)
        
def validateRNG(fileName, fileTree, schemaTree):
    try:
            #print("Now processing file {}".format(f_name))
        if fileTree is not None:
            #valid = validate_with_schema(relaxng, result_tree)
            if fileTree.relaxng(schemaTree) is False:
                error_log['schema_issue'].append(fileName)
                return False
            return True
           
        else:
            error_log['not_valid'].append(fileName)
            print("Schema Error: {}".format(fName))
            return False
    except UnicodeDecodeError:
        error_log['unicode_issue'].append(fileName)
    except etree.XMLSyntaxError:
        print("XMLSyntaxError error!")
        error_log['not_valid'].append(fileName)
            

      
def write_files_to_disk(lst_files, error_log):
    cwd = os.getcwd()
    new_dir = cwd+os.sep+"testFolder"+os.sep+"resultFiles"
    if os.path.isdir(new_dir):
        shutil.rmtree(new_dir)
    valid_dir = new_dir + os.sep+"valid_files"
    problem_dir = new_dir + os.sep+ "problem_files"
    os.mkdir(new_dir)
    os.mkdir(problem_dir)
    os.mkdir(valid_dir)
    
    
    for f_name, xslt_result in lst_files:
        if f_name in error_log['schema_issue']:
            xslt_result.write(problem_dir+os.sep+f_name)
        else:
            xslt_result.write(valid_dir+os.sep+f_name)

    error_log_strg = "{} files have unicode issues:\n".format(len(error_log['unicode_issue']))
    error_log_strg += "\n".join(error_log['unicode_issue'])
    error_log_strg += "\n"
    error_log_strg += "-"*20
    error_log_strg += "\n{} files invalid before transformation:\n".format(len(error_log['not_valid']))
    error_log_strg += "\n".join(error_log['not_valid'])
    error_log_strg += "\n"
    error_log_strg += "-"*20
    error_log_strg += "\n{} files have schema issues:\n".format(len(error_log['schema_issue']))
    error_log_strg += "\n".join(error_log['schema_issue'])
    error_log_strg += "\n"""
    """error_log_strg += "-"*20
    error_log_strg += "\n{} files have TEI_all schema issues:\n".format(len(error_log['tei_schema_issue']))
    error_log_strg += "\n".join(error_log['tei_schema_issue'])"""
    
                                                              
    with open(new_dir+os.sep+"error.log", "w") as f:
        f.write(error_log_strg)

if __name__=='__main__':
    """File and folder path"""
    cwd = os.getcwd()
    
    #get TEI schema
    """tei_schema_file = cwd + os.sep + 'tei_all.rng'
    with open(tei_schema_file, "r") as f:
        tei_schema_tree = f.read()"""
     
    containerFolder = cwd + os.sep + 'LETTERS 2016-02-22 14-12-45'
    xmlFilePath = containerFolder + os.sep + 'letters'
    #xml_file_path = cwd + os.sep + 'testFolder'
    
    files = os.listdir(xmlFilePath)
    
    transformed_files = []
    
    xsltFile = cwd + os.sep + 'copyAndChange.xsl'
    xsltTree = open_file(xsltFile)
    
    schemaFile = 'C:' + os.sep + 'Users' + os.sep + 'Rombli' + os.sep + 'Documents' + os.sep + 'GitHub' + os.sep + 'TEI-sample-files' + os.sep + 'plain corresp templates' + os.sep + 'template.rng'
    schemaTree = open_file(schemaFile)
    
    patAndReplStrg = [(b"\s*-\s*<lb/>\s*-?",b"<lb rend='hyphen'/>"),
                      (b"\s*-<lb/>\s*-?\s*",b"<lb rend='hyphen'/>"),
                      (b"\s*—\s*<lb/>\s*",b"<lb rend='hyphen'/>"),
                      #(b"\s*&#x2014;\s*<lb/>\s*",b"<lb rend='hyphen'/>"),
                      #(b"\s*&#8212;\s*<lb/>\s*",b"<lb rend='hyphen'/>"),
                      (b"<!-<lb rend='hyphen'/>",b"<!-- <lb/>"),
                      (b"<lb rend='hyphen'/>->",b"<lb/> -->"),
                   ]
    
    new_dir = containerFolder+os.sep+"resultFiles"
    #new_dir = cwd+os.sep+"testFolder"+os.sep+"resultFiles"
    if os.path.isdir(new_dir):
        shutil.rmtree(new_dir)
    valid_dir = new_dir + os.sep+"valid_files"
    problem_dir = new_dir + os.sep+ "problem_files"
    os.mkdir(new_dir)
    os.mkdir(problem_dir)
    os.mkdir(valid_dir)
    
    for fName in files:
        
        with open(xmlFilePath+os.sep+fName, "r+b") as f:
            bStrg = f.read()
            bTEI = re.split(b"<text>", bStrg)
            bHeader = bTEI[0]
            bText = bTEI[1]
            for pat, replStrg in patAndReplStrg:
                #print(fName)
                bText = replaceStrg(bText, pat , replStrg)
                
                
            bStrg =  bHeader + b"<text>" + bText
                
                
           
            tree = etree.XML(bStrg)
        
        teiResult = transformTEI(fName, tree, xsltTree)
        
        if validateRNG(fName, teiResult, schemaTree):
            teiResult.write(valid_dir+os.sep+fName)
        else:
            print("File {} is not valid.".format(fName))
            with open(problem_dir+os.sep+fName, "w+b") as f:
                f.write(teiResult)
    
    
    print('All ok!')



