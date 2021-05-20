import email.encoders as Encoders
from   email.mime.base import MIMEBase
from   email.mime.multipart import MIMEMultipart
from   email.mime.text import MIMEText
from   os import path
import smtplib
from   typing import List

import python.common.common as c


secrets_path = "/mnt/apache2/secret"

def getSecret ( filename : str ):
  # The file should contain the secret and nothing else --
  # no surrounding whitespace, no newline, no comments, etc.
  return ( open( path.join ( secrets_path,
                             filename ) )
           . read ()
           . strip () )

def send ( receiver_address : str,
           subject          : str,
           body             : str,
           attachment_paths : List [ str ] ):
  sender   = getSecret ( "email address.txt" )
  password = getSecret ( "email password.txt" )
  server = smtplib . SMTP ( 'smtp.gmail.com',  587 )
  server . ehlo ()
  server . starttls ()
  server . login ( sender, password )
  #
  msg = MIMEMultipart ()
  msg [ 'Subject' ] = subject
  msg [ 'To' ] = " " . join( [
    # This might seem unneessarily verbose,
    # but it makes clear what to do for multiple recipients.
    receiver_address ] )
  msg [ 'From' ] = sender
  msg . attach ( MIMEText ( body,
                            "plain" ) )
  #
  for file in attachment_paths:
    part = MIMEBase ( 'application', 'octet-stream' )
    part . set_payload ( open ( file, 'rb' )
                         . read () )
    Encoders . encode_base64 ( part )
    part . add_header(
        'Content-Disposition',
        'attachment; filename="%s"' % file)
    msg . attach ( part )
  #
  server . send_message ( msg )
  server . quit ()
