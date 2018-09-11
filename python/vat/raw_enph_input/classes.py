class File:
  def __init__(self,name,filename,col_dict,corrections=[]):
    self.name = name
    self.filename = filename
    self.col_dict = col_dict
    self.corrections = corrections

class Correction:
  class Create_Constant_Column:
    def __init__(self,col_name,value):
      self.col_name = col_name
      self.value = value
    def correct(self,df):
      df[self.col_name] = self.value
  class Apply_Function_To_Column:
    def __init__(self,col_name,func):
      self.col_name = col_name
      self.func = func
    def correct(self,df):
      df[self.col_name] = df[self.col_name].apply(self.func)

