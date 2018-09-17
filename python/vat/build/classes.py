class File:
  def __init__(self,name,filename,col_dict,corrections=[]):
    self.name = name
    self.filename = filename
    self.col_dict = col_dict
    self.corrections = corrections

class Correction:
  # PITFALL: Some of the return statements in the implementations of "correct" below are unnecessary,
    # because the operations before them are destructive. However, "drop" is not destructive.
    # For compatibility with Drop_Row_If_Column_Satisfies_Predicate, therefore, every "correct" function
    # must return the data frame it operates on.

  class Create_Constant_Column:
    def __init__(self,col_name,value):
      self.col_name = col_name
      self.value = value
    def correct(self,df):
      df[self.col_name] = self.value
      return df

  class Replace_Missing_Values:
    def __init__(self,col_name,value):
      self.col_name = col_name
      self.value = value
    def correct(self,df):
      df[self.col_name] = df[self.col_name].fillna( self.value )
      return df

  class Replace_Substring_In_Column:
    def __init__(self,col_name,before,after):
      self.col_name = col_name
      self.before = before
      self.after = after
    def correct(self,df):
      df[self.col_name] = ( df[self.col_name]
                            .astype(str)
                            .str.replace( self.before, self.after ) )
      return df

  class Apply_Function_To_Column:
    def __init__(self,col_name,func):
      self.col_name = col_name
      self.func = func
    def correct(self,df):
      df[self.col_name] = ( df[self.col_name]
                            .apply(self.func) )
      return df

  class Drop_Row_If_Column_Satisfies_Predicate:
    def __init__(self,col_name,pred):
      self.col_name = col_name
      self.pred = pred
    def correct(self,df):
      return df.drop(
        df[ self.pred( df[self.col_name] )
        ].index
      )

  class Replace_Entirely_If_Substring_Is_In_Column:
    def __init__(self,col_name,substring,replacement):
      self.col_name = col_name
      self.substring = substring
      self.replacement = replacement
    def correct(self,df):
      df.loc[ (~ df[self.col_name].isna() )
              & df[self.col_name].str.contains( self.substring )
            , self.col_name
      ] = self.replacement
      return df

  class Drop_Column:
    def __init__(self,col_name):
      self.col_name = col_name
    def correct(self,df):
      return df.drop( self.col_name, axis = 'columns' )
