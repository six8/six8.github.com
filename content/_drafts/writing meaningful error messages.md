
Error messages should be concise and describe the problem as well as steps to correct the error. 'AWS credential not provided in init' is a good start as it describes the problem and indicates where to fix it. However, it only describes the root cause of the problem, not the problem that the user of `_get_connection` is experiencing. 

"Unable to connect to AWS, credentials not configured. Configure the AWS credentials by passing an account when initializing AwsScraper."

Positive assertions: If you're asserting something to be true, the error message should be positive. 'AWS credential not provided in init' is a good start as it describes the problem and indicates where to fix it. However, it's a negative assertion. Flipping it to positive would be 'Provide AWS credentials in init'.

http://www.nngroup.com/articles/error-message-guidelines/
http://cbio.ufs.ac.za/live_docs/nbn_tut/writing_errors.html