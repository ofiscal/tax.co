We have a model of the Colombian tax code. We want Colombian citizens to be able to experiment with it -- for instance, changing the VAT rate and seeing the effect on working couples with children. For that, we would like you to build a website that wraps a GUI around the model, and set it up on a web hosting platform.

The model takes in a collection of numbers and words, and produces a collection of numbers and images. The webpage should be a function of that Python code, and of some documents that specify the model's inputs and outputs.

By "the webpage should be a function of", I mean that if we change the Python code or the input and output descriptions, the webpage should change automatically. This is because we will be changing those three things a lot, and we don't want to have to contact you every time we do.

The document "input.md" will be structured like this:

  integer: Number of children
  dropdown: Rent or own
    rent
    own
  dropdown: Marital status
    single
    married
    divorced
  integer: Years of education
  table: Marginal tax rates by income
    columns: Income threshold, millions of pesos per month | Marginal tax rate
    rows: not every | row or column needs a name | |
    types:
      float float
      float float
      float float
      float float

The only three kinds of things "input.md" describes are numbers, dropdown menus and tables. Each begins with its type, followed by a colon, followed by its title. If it is a number, it includes no more information. If it is a dropdown, the title is followed by an indented list of the possible values.

If it is a table, the title is followed by three tab-indented items. The first is a list of column names, separated with "|" characters. The second is a list of row names, separated with "|" characters. Row or column names may be empty (in the example above, the last two rows have no name). Following that is a rectangular array of numeric types with the same dimensions as the table.

Your code should read input.md and generate a page with a collection of widgets as input.md describes, in the same order. After all those input widgets, there should appear a button labeled "Run the model".

When the user hits that button, their input should be turned into files. Each integer and dropdown word or phrase should be turned into a file with a name equal to the title of the widget that generated it. For instance, in the example above, if the user input "2" under "Number of children", the GUI should generate a text file called "Number of children" containing nothing but the number "2", followed by a newline. Similarly, if the user chose "rent", the GUI would generate a file called "Rent or own" containing the single word "rent", followed by a newline.

For tabular input, the GUI should generate a standard CSV file. For instance, in the above example, the file "Marginal tax rates by income" would contain something like this:

  ,"Income threshold, millions of pesos per month",Marginal tax rate
  not every,1,2
  row or column needs a name,3,4
  ,5,6
  ,7,8

Those files should be written to the folder "model-inputs/". Once they are there, the webpage should the model. It will generate output, written to the folder "model-outputs/".

There will be three kinds of files in model-outputs/: Numbers, tables and images. Each filename will begin with a number; these indicate the order in which the files should be rendered. The next part of the filename is its title, and the last part is its type. Tables will end in .csv, images in .png, and numbers in .num

For example, suppose the model generated the following output filenames:

  001.Number of people in extreme poverty.num
  002.Effective tax rates per income decile.csv
  003.After tax income by income percentile.png

The output webpage should then begin with a number titled "number of people in extreme poverty". After that should be a table titled "Effective tax rates per income decile", with column title, row title and cell values corresponding to the csv content. The page should end with the .png image, titled "After tax income by income percentile".