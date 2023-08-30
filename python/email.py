if True:
  import email.encoders as Encoders
  from   email.mime.base import MIMEBase
  from   email.mime.multipart import MIMEMultipart
  from   email.mime.text import MIMEText
  from   os import path
  import smtplib
  from   typing import List
  #
  import python.common.common as c


secrets_path = "/mnt/apache2/secret"

def getSecret ( filename : str ):
  # The file should contain the secret and nothing else -- no comments, etc.
  # (Whitespace before or after the secret is harmless.)
  return ( open( path.join ( secrets_path,
                             filename ) )
           . read ()
           . strip () )

# PITFALL: This *only* works with Gmail.
# It probably can be easily modified to work with other
# SMTP-compatible email servers -- by, I imagine,
# changing the definitions of "sender" and "server" below --
# but I haven't tried that.
def send ( receiver_address : str, # To send to multiple addresses, this should be a space-separated list of email addresses. (It's still a string, not a list of strings.)
           subject          : str,
           body             : str,
           attachment_paths : List [ str ]
): # TODO: Update type signature to incorporate the new return type.
   # (It used to return nothing.)
  sender   = getSecret ( "email address.txt" )
  password = getSecret ( "email password, app.txt" ) # This might be the same as your ordinary Gmail password. But if Google complains "Application-specific password required," you'll have to use that instead. To do so, enable "Less secure apps" for Gmail, enable 2-step verification, and then generate an "app key" for controlling your Gmail account.
  server = smtplib . SMTP ( 'smtp.gmail.com',  587 )
  server . ehlo ()
  server . starttls ()
  server . login ( sender, password )
  #
  msg = MIMEMultipart ()
  msg [ 'Subject' ] = subject
  msg [ 'To' ] = receiver_address
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
  send_dict = server . send_message ( msg ) # If this is empty,
    # someone should have received the message.
  server . quit ()
  return send_dict

def test( recipient : str ):
  return send (
    recipient,
    "Testing Ofiscal automated emails",
    "Hi! Jeff here. Did you receive this message?",
    [] )
