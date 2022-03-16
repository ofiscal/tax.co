import python.email as e

def ioTest_email ( receiver : str ):
  e.send (
    receiver_address = receiver,
    subject = "This is a test.",
    body = "That's all.",
    attachment_paths = [] )

# theTest ( "jeffbrown.the@gmail.com" )
