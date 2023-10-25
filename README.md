# Serverless-Intelligent-Document-Processing

![image](https://github.com/paulkannan/Serverless-Intelligent-Document-Processing/assets/46925641/9ef6dd28-4d1e-4b6e-bff5-57c08c53a7ad)

**Overview**

This architecture aims to identify valid Indian ID cards from uploaded documents. The system supports only .jpg, .jpeg, and .png file formats. If any other document types are uploaded, they will not be processed. The workflow comprises three main phases: Image Validation, Data Extraction, and PII Entity Identification, followed by document categorization into valid and invalid ID cards. A notification is sent to end users through Amazon SNS, and the data is forwarded to Amazon SQS for consumption by end user applications.

**Workflow**
**Image Validation (Rekognition):**
Uploaded documents are first checked for the presence of specific elements, such as faces, QR codes, images, and documents.
If any of these elements are detected, the document is passed to the next phase, Data Extraction (Textract).
Documents lacking these elements are categorized as invalid and sent to the "Invalid ID Bucket."

**Data Extraction (Textract):**
In this phase, Textract is used to perform text extraction from the documents.
Extracted text is then processed by Amazon Comprehend to identify known Personally Identifiable Information (PII) entity types.
Comprehend calculates a confidence score for each identified entity, with a threshold set at 50%.

**Categorization (Valid/Invalid):**
Documents with a high confidence score for known PII entities are categorized as valid ID cards and sent to the "Valid ID Bucket."
Documents with a low confidence score or no PII entities are categorized as invalid ID cards and sent to the "Invalid ID Bucket."

**Notification (Amazon SNS):**
A notification is sent to end users via Amazon SNS to inform them about the processing results.

**Data Forwarding (Amazon SQS):**
The processed data, along with categorization details, is forwarded to Amazon SQS for consumption by end user applications.

**Supported Document Types**
Input: .jpg, .jpeg, .png
Output (Valid ID Cards): Any document with high-confidence PII entity types.
Output (Invalid ID Cards): Documents lacking high-confidence PII entities or failing the Image Validation phase.

**Usage**

This architecture is designed to provide a serverless, efficient, and automated solution for identifying valid Indian ID cards from uploaded documents. It leverages AWS services (Amazon Rekognition) to perform image validation, text extraction (Amazon Textract), PII entity identification (Amazon Comprehend), categorization, and notifications (Amazon SNS & SQS). It is highly adaptable and can be integrated into various applications and workflows.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```
You can now deploy the CDK Stack

```
$ cdk deploy
```
To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
   
To clean up the resources created

```
$ cdk destroy
```

