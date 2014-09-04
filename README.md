# ESWC Publicity Tools (v. 1.0)

The *ESWC Publicity Tools* are a set of Python scripts that allow you to send emails containing (TXT versions of) ESWC call for papers to a list of emails stored in a CSV file.

To run the service you have to call the *run.py* script as follows:

```python run.py
    <audience> <call-type> <emails-file> <call-file>
    <conf-file> <n-emails-per-turn> <sleeping-time>
```

The parameters are:
* *audience* - It is a sort of macro category defining the intended audience of the call. In past editions, the values that were used in this parameter were "conference", "workshops", "tutorials", "demo", "poster", "phd-symposium", "challenge-recsys", "challenge-sempub", "challenge-semsa", "eu-project", "student-grants", "participation".
* *call-type* - It allows you to specify the particular kind of call - e.g., "first-call", "second-call" and "final-call" - associated to the target audience defined in the previous parameter.
* *emails-file* - It is the path of the CSV file containing al the emails to which sending the call. The format used to indicate emails will be explained below with more details. A exemplary file is defined in "test-mails.csv".
* *call-file* - It is the path of the TXT file containing the text of tha call. The format used to indicate calls will be explained below with more details. A exemplary file is defined in "test-message.csv".
* *conf-file* - It is the path of the JSON file containing some configuration data of the email account to use to send the calls. The format used to indicate configuration data will be explained below with more details. A exemplary file is defined in "conf.csv".
* *n-emails-per-turn* - It indicates the number of mails to send before sleeping (see next parameter). Specifying "0" means to send all the mails without sleeping. This and the following parameter are very useful for addressing possible constraints that the email server defines in terms of max number of emails per minute.
* *sleeping-time* - It indicates the number seconds to sleep before sending the remaining emails (see previous parameter). Specifying "0" means not to sleep at all. This and the preceding parameter are very useful for addressing possible constraints that the email server defines in terms of max number of emails per minute.


## How _run.py_ works

A file "data.json" will be created once you will run the script "run.py" for the first time. All the other executions simply modify such file. For instance, if you call the script as follows:

```python run.py
    conference first-call test-emails.csv test-message.txt
    test-conf.json 10 60
```

what happens is to send the text of the call to all the emails specified (10 emails each minute). The resulting "data.json" will have the following form:

```{
    "conference": {
        "first-call": [
            {
                "object": {
                    "failure": [],
                    "success": [
                        "john.doe@example.com"
                    ]
                },
                "onTime": "2013-12-10T10:15:00"
            }
        ]
    }
}
```

Note that all the emails that are not accompanied by a "true" value in the emails file or to which the call (characterised by the pair audience/call-type) has been already sent successfully won't be considered in future execution of the script. This means, for instance, that if you run again the script as above, no mail will be sent.


## JSON format of _data.json_

The JSON format used to store data related with the sending of calls is summarised as follows:

```{
	"conference" : {
		"first-call" : [
			{
				"onTime": "2013-05-13T14:45:15" ,
				"object" : {
					"success" : [ "john@mail.com" , "doe@mail.com" ] ,
					"failure" : [ "jane@mail.com" ]
				}
			} ,
			{
				"onTime": "2013-05-17T16:15:17" ,
				"object" : {
					"success" : [ "jane@mail.com" ] ,
					"failure" : [ ]
				}
			}
		] ,
		"second-call" : [
			{
				"onDate": "2013-06-19T14:45:15" ,
				"object" : {
					"success" : [ "john@mail.com" , "doe@mail.com" , "jane@mail.com" ] ,
					"failure" : [ ]
				}
			}
		]
	} ,
	"workshops" : { ... } ,
	"tutorials" : { ... } ,
	"challenge-sempub" : { ... } ,
	"demo" : { ... } ,
	...
}
```

The *audience* and the *call-type* are used to define first- and second-level JSON objects respectively. Each *call-type* then contains a list of JSON object composed by the lists of the emails to which the call have (key "success") or have not ("failure") been delivered properly, and the date tracking when such data have been added to the JSON file.


## Converting into CSV

In order to import such data in a Excel-like stylesheet (such as in Google Docs), we have developed another script called *tocsv.py*. You can call the service as follows:

```python tocsv.py <input-json> <output-csv>
```

The *input-json* parameter allows you to specify the JSON file (stored according to the format introduced above) to be converted, while *output-csv* refers to the path where the converted CSV file must be stored.

Running this script on the small example in the introductory part of this documentation will result in the creation of the following CSV records:

```mail,conference#first-call
john.doe@example.com,2013-12-10T10:15:00
```


## The emails file

This file describe a list of email to use to send the call. It is a CSV file and it has the following format:

```Mailing list,Use it
john.doe@example.com,true
jane.doe@example.net,she_considered_our_calls_as_spam
```

In the first cell you have to specify the email address, while in the second cell you need to define whether the "run.py" script will use (i.e., "true") or not (i.e., any other value) the email specified in the first cell.


## The call file

This TXT file contains the the subject and the body of the email containing the call. A small example of such file can be defined as follows:

```ESWC 2014 First call for research and in-use papers
Here starts the body of the message.
Split in two paragraphs.
```

In this file, the first line will be always used as email subject, while all the other lines form the body of the email.


## The configuration file

This JSON file allows you to specify data for enabling the sending of emails, such as username, password, SMTP server and the sender emails. It has the following format:

```{
	"user": "john.smith",
    "password": "bestpasswordever",
    "smtp": "your.smtp.server.com",
    "sender": "john.smith@yourprovider.com"
}
```


## List of all ESWC mailing list

In the file *all-mailing-lists.csv* there are listed all the mailing list that were used in the previous editions of ESWC. The main part of them are marked with "true" values, while few of them where marked with other values according to the reason we didn't use them (e.g., because the subscription was rejected, or because the messages from the Publicity Chair generated too much traffic).


## Log files

Every time the script "run.py" is executed, a ".report" file will be stored in order to summarised (in natural language) all the activities done by the script. A typical content of such file is:

```Mail sent to john.doe@example.com
Mail sent to jane.doe@example.net
```


## License

Copyright (c) 2013-2014, Silvio Peroni <essepuntato@gmail.com>

Permission to use, copy, modify, and/or distribute the ESWC Publicity Tools for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
SOFTWARE.