###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- Metadata and profiling --
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#       
#       Licensed under GPLv3
#
##############################################################


class Profiler(object):
    """The profiler looks at the state of input files and parameters and generates metadata for the output files"""

    def checkprofiles(self, parameters):
        """Returns all matching profiles"""
        raise NotImplementedError #TODO: implement  

    def execute(self, parameters):
        raise NotImplementedError #TODO: implement

    

class Profile(object):
    def __init__(self, input, output, parameters, **kwargs):
        if isinstance(input, InputTemplate):
            input = [input]
        assert all([ isinstance(InputTemplate) for x in input])
        self.input = input

        if isinstance(output, OutputTemplate) or isinstance(output, ParameterCondition):
            output = [output]
        assert all([ isinstance(OutputTemplate) or isinstance(ParameterCondition)  for x in output])
        self.output = output

        self.multi = False

        for key, value in kwargs.items():
            if key == 'unique':
                self.multi = False
            elif key == 'multi':
                self.multi = True
            else:
                raise SyntaxError("Unknown parameter to profile: " + key)

            

class IncompleteError(Exception):
    pass


def getmetadata(xmldata):
    """Read metadata from XML"""
    raise NotImplementedError #TODO: implement

class CLAMMetaData(object):
    """A simple hash structure to hold arbitrary metadata"""
    attributes = None #if None, all attributes are allowed! Otherwise it should be a dictionary with keys corresponding to the various attributes and a list of values corresponding to the *maximally* possible settings (include False as element if not setting the attribute is valid), if no list of values are defined, set True if the attrbute is required or False if not

    mimetype = "" #No mimetype by default
    schema = ""

    def __init__(self, **kwargs):
        self.data = {}
        for key, value in kwargs.items():
            self[key] = value
        if attributes:
            for key, value in attributes.items():
                if value and (not isinstance(value,list) or not False in value):
                    if not key in self:
                        raise IncompleteError("Required attribute " + key +  " not specified")
            

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, key)
        return key in self.data

    def items(self):
        return self.data.items()

    def __iter__(self):
        return self.data

    def __setitem__(self, key, value):
        if attributes != None and not key in attributes:
            raise KeyError
        assert not isinstance(value, list)
        maxvalues = self.data[key]
        if isinstance(maxvalues, list):
            if not value in maxvalues:
                raise ValueError
        self.data[key] = value


    def xml(self):
        """Render an XML representation of the metadata"""
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += "<CLAMMetaData format=\"" + self.__class__.__name__ + "\"
        if self.mimetype:
             xml += " mimetype=\""+self.__class__.mimetype+"\""
        if self.schema:
             xml += " schema=\""+self.__class__.schema+"\""
        xml += ">\n"
        for key, value in self.data.items():
        xml += "\t<meta id=\""+key+"\">"+str(value)+"</meta>"
        xml += "</CLAMMetaData>"
        return xml


class CMDIMetaData(CLAMMetaData):
    #TODO: implement



def profilefromxml():
    """Produce profile from xml"""
    raise NotImplementedError #TODO: implement
    

class FormatTemplate(object):
    def __init__(self, formatclass, label, **kwargs)
        assert (formatclass is CLAMMetaData)
        self.formatclass = formatclass
        self.label = label

        self.inputtemplate = True
        self.outputtemplate = True #are the meta values non-ambiguous, and usable deterministically for output templates?

        self.metafields = []
        
        self.unique = True #may mark input/output as unique, even though profile may be in multi mode

        self.filename = None
        self.extension = None


        for key, value in kwargs.items():
            if key == 'unique':   
                self.unique = True
                self.unique = bool(value)
            elif key == 'filename':
                self.filename = value # use $N to insert a number in multi mode
            elif key == 'extension':
                self.extension = value
            else:
                if isinstance(value, list):
                    #value is list of values
                    if key[:-4] == '_not':
                           self.outputtemplate = False
                           self.metafields.append( (key[:-4],value,lambda x: not x in value, 'not') )
                    else:
                           self.outputtemplate = False
                           self.metafields.append( (key,value,lambda x: x in value,'') )
                else:
                    #value is single value
                    if key[:-4] == '_not':
                           self.metafields.append( (key[:-4],value,lambda x: x != value, 'not') )
                    elif key[:-5] == '_copy': #copy from input metadata
                           self.inputtemplate = False
                           self.metafields.append( (key[:-5],value,lambda x: True: 'copy') ) 
                    elif key[:-14] == '_fromparameter': #copy from parameter specificaton
                           self.inputtemplate = False
                           self.metafields.append( (key[:-14],value,lambda x: True: 'fromparameter') ) 
                    elif key[:-12] == '_greaterthan':
                           self.outputtemplate = False
                           self.metafields.append( (key[:-12],value,lambda x: x > value, 'greaterthan') )
                    elif key[:-17] == '_greaterequalthan':
                           self.outputtemplate = False
                           self.metafields.append( (key[:-17],value,lambda x: x >= value, 'greaterequalthan') )
                    elif key[:-10] == '_lessthan':
                           self.outputtemplate = False
                           self.metafields.append( (key[:-10],value,lambda x: x < value, 'lessthan') )
                    elif key[:-15] == '_lessequalthan':
                           self.outputtemplate = False
                           self.metafields.append( (key[:-15],value,lambda x: x <= value, 'lessequalthan') )
                    else:
                           self.metafields.append( (key,value,lambda x: x == value, '') )



    def match(self, metadata):
        """Does the specified metadata match this template?"""
        assert isinstance(metadata, self.formatclass)
        for key, value, evalf, operator in metafields:
            if key in metadata:
                if not evalf(metadata[key]):
                    return False
            else:
                if operator != 'not':
                    return False
        return True


    def generate(self, inputdata, parameters):
        """Convert the template into instantiated metadata (both input and output).

            inputdata is a dictionary-compatible structure, for outputtemplates it's the metadata of the primary (first) inputfile, for inputtemplate it is a dictionary with post data containing the user's choices for the multiple-choice meta fields.
        """

        #TODO


    def xml(self, maintag = "InputTemplate")
        """Produce Template XML"""
        xml = "<" + maintag + " format=\"" + self.formatclass.__name__ + "\""
        if self.formatclass.mimetype:
            xml +=" mimetype=\""+self.formatclass.mimetype+"\""
        if self.formatclass.schema:
            xml +=" schema=\""+self.formatclass.schema+"\""
        if self.unique:
            xml +=" unique=\"yes\""
        xml += ">\n"
        for key, value, evalf, operator in self.metafields:
            if isinstance(value, list):
                xml += "\t<metaselect id=\"" + key + "\""
                if operator:
                    xml += " operator=\"" + operator + "\"
                xml += ">"
                for option in value:
                    xml += "<option>" + value + "</option>"
                xml += "</metaselect>\n"
            else:
                xml += "\t<meta id=\"" + key + "\""
                if operator:
                    xml += " operator=\"" + operator + "\"
                xml += ">"
                xml += "</meta>\n"

        xml += "</" + maintag + ">\n"
        return xml

        

class InputTemplate(FormatTemplate):
    def __init__(self, formatclass, label, **kwargs)
        super(InputTemplate,self).__init__(formatclass, label, **kwargs)

    def xml(self):
        return super(InputTemplate,self).xml('InputTemplate')


class OutputTemplate(object):
    def __init__(self, formatclass, label, **kwargs)
        super(OutputTemplate,self).__init__(formatclass, label, **kwargs)
        assert self.suitableforoutput == True

    def xml(self):
        return super(InputTemplate,self).xml('OutputTemplate')



def ParameterCondition(object):
    def __init__(self, **kwargs):
        if not 'then' in kwargs:
            assert Exception("No 'then=' specified!")

        self.then = None
        self.otherwise = None

        self.conditions = []
        self.disjunction = False

        for key, value in kwargs.items():
            if key == 'then'
                if not isinstance(value, OutputTemplate) and not isinstance(value, InputTemplate) and not isinstance(value, ParameterCondition):
                    assert Exception("Value of 'then=' must be InputTemplate, OutputTemplate or ParameterCondition!")
                else:
                    self.then = value
            elif key == 'else' or key == 'otherwise':
                if not isinstance(value, OutputTemplate) and not isinstance(value, InputTemplate) and not isinstance(value, ParameterCondition):
                    assert Exception("Value of 'else=' must be InputTemplate, OutputTemplate or ParameterCondition!")
                else:
                    self.otherwise = value
            elif key == 'disjunction' or key == 'or':
                self.disjunction = value
            else:
                if key[-10:] == '_notequals':
                    self.conditions.append( (key[:-10], value,lambda x: x != value, 'notequals') )
                elif key[-12:] == '_greaterthan':
                    self.conditions.append( (key[:-12], value,lambda x: x > value, 'greaterthan') )
                elif key[-17:] == '_greaterequalthan':
                    self.conditions.append( (key[:-17],value, lambda x: x > value, 'greaterequalthan') )
                elif key[-9:] == '_lessthan':
                    self.conditions.append( (key[:-9],value, lambda x: x >= value , 'lessthan' ) )
                elif key[-14:] == '_lessequalthan':
                    self.conditions.append( (key[:-14], value,lambda x: x <= value, 'lessequalthan') )
                elif key[-9:] == '_contains':
                    self.conditions.append( (key[:-9], value,lambda x: x in value, 'contains') )
                elif key[-7:] == '_equals':
                    self.conditions.append( (key[:-7], value,lambda x: x == value, 'equals') )
                else: #default is _is
                    self.conditions.append( (key,value, lambda x: x == value,'equals') )
                    

    def match(self, parameters):
        for key,_,evalf,_ in self.conditions:
            if key in parameters:
                value = parameters[key]
            else:
                value = None
            if evalf(value):
                if self.disjunction:
                    return True
            else:
                if not self.disjunction: #conjunction
                    return False
         if self.disjunction:
             return False
         else:
             return True

    def evaluate(self, parameters):
        #Returns an False or whatever
        if self.match(parameters):
            if isinstance(self.then, ParameterCondition):
                #recursive parametercondition
                return self.then.evaluate()
            else:
                return self.then
        elif self.otherwise:
            if isinstance(self.otherwise, ParameterCondition):
                #recursive else
                return self.otherwise.evaluate()
            else:
                return self.otherwise
        return False

    def xml(self):
        #TODO
        pass
