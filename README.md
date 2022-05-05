# Overview

This code is meant to be implemented as an Amazon Web Services Lambda function set to trigger from objects in one or more S3 buckets. It utilizes the 'google_trans_new' library to translate the contents of the triggering object, provided that they are a .txt file, into english. This should successfully translate any .txt file provided that the original language is supported by Google Translate.
