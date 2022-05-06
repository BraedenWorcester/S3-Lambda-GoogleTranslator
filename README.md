# Overview

This code is meant to be used as an Amazon Web Services Lambda function set to trigger from objects in one or more S3 buckets. It utilizes the 'google_trans_new' python library ( https://pypi.org/project/google-trans-new/ ) to translate the body content of the triggering object, provided that they are a .txt file, into english. This should successfully translate any .txt file if the language within is supported by Google Translate.

# Necessary Structure and Output

A Lambda function with this code should be triggered upon an object change, and I recommend setting a ".txt" suffix as well as possibly a prefix like "translate_this/" so that the Lambda doesn't run unnecessarily on every single object. The trigger should be associated with an S3 bucket that has been configured to allow your Lambda "GetObject" and "PutObject" access for the resources you want to be translated. Finally, your Lambda will need to have a layer containing the 'google_trans_new' library package. Assuming there are no issues accessing the bucket, a new folder named "translated/" should appear next to the triggering files, containing their english translations.

![image](https://user-images.githubusercontent.com/56178051/166860978-c3bd430d-5599-41a4-a91e-9b6130d70ed6.png)


# A Note on Lambdas
AWS Lambdas are wonderful in that they allow you run code online without having to pay for maintaining a server. This makes them perfect for scenarios where code only needs to be ran once under specific conditions, which is why I've elected to use Lambdas for this little foray into automatic translation. However, if misconfigured, they can cause problems. One such problem is never ending reccurrence if the Lambda is outputting to the bucket where it's getting input (Lambda sees new object added to bucket -> Lambda runs and adds result to bucket -> Lambda sees own added object to bucket -> Lambda runs and adds result to bucket -> Lambda sees own...). To avoid this problem, I've configured the code to place its output into "/translated/" and under no circumstances accept any input like "/translated/inputname.txt".

# Example Usage

Live demo at https://www.youtube.com/watch?v=AWVFFDU64fQ


This is the access policy configuration for a bucket which will accept GetObject and PutObject requests from the public:

![image](https://user-images.githubusercontent.com/56178051/166857204-a44180f4-0ca8-465d-93b8-e3c6b2928e33.png)

and this is a Lambda trigger set to go off whenever the bucket gets a new .txt file:

![image](https://user-images.githubusercontent.com/56178051/166857541-e869943b-8a01-4f98-83e2-23787f324b34.png)

Upon uploading this .txt file:

![image](https://user-images.githubusercontent.com/56178051/166857783-9ec0cf5d-f453-4cc2-9ea5-e4a0f5538aa8.png)

The Lambda will activate and create a new folder alongside the old file inside the bucket:

![image](https://user-images.githubusercontent.com/56178051/166857956-635883e8-ac76-4a81-af40-0dfc5d027f3e.png)

where you will find a copy of the old file:

![image](https://user-images.githubusercontent.com/56178051/166858084-08adad11-62ea-4d84-ad88-172a595561de.png)

now in English:

![image](https://user-images.githubusercontent.com/56178051/166858226-b03a8d4f-cb37-4a71-bd0a-2092dcdac8cb.png)

