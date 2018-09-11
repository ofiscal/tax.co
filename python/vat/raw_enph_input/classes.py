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
      return df
