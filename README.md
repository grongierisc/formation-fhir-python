# 1. formation-fhir-python

Training on FHIR and Python based on IRIS for Health.

This repository contains the material for the training.

During the training, we will use the following tools:

- [IRIS for Health](https://www.intersystems.com/products/iris-for-health/)
- [Python](https://www.python.org/)
- [VSCode](https://code.visualstudio.com/)
- [Postman](https://www.postman.com/)
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [IoP](https://github.com/grongierisc/interoperability-embedded-python)

# 2. Table of Contents

- [1. formation-fhir-python](#1-formation-fhir-python)
- [2. Table of Contents](#2-table-of-contents)
- [3. Objectives](#3-objectives)
- [4. Installation](#4-installation)
  - [4.1. Access to the FHIR server](#41-access-to-the-fhir-server)
  - [4.2. Access the InterSystems IRIS Management Portal](#42-access-the-intersystems-iris-management-portal)
- [5. Configuration of the OAuth2 Authorization Server](#5-configuration-of-the-oauth2-authorization-server)
  - [5.1. General Tab](#51-general-tab)
  - [5.2. Scope Tab](#52-scope-tab)
  - [5.3. JWT Tab](#53-jwt-tab)
  - [5.4. Customization Tab](#54-customization-tab)
- [6. Configuration of the Client](#6-configuration-of-the-client)
  - [6.1. Register the OAuth2 Authorization Server](#61-register-the-oauth2-authorization-server)
  - [6.2. Server Description](#62-server-description)
  - [6.3. Create a new client](#63-create-a-new-client)
    - [6.3.1. General Tab](#631-general-tab)
- [7. Configuration of the FHIR server](#7-configuration-of-the-fhir-server)
  - [7.1. Create a new FHIR server](#71-create-a-new-fhir-server)
  - [7.2. Bind the FHIR server to the OAuth2 Authorization Server](#72-bind-the-fhir-server-to-the-oauth2-authorization-server)
  - [7.3. Test the FHIR server](#73-test-the-fhir-server)
- [Filter FHIR Resources with InterSystems IRIS for Health](#filter-fhir-resources-with-intersystems-iris-for-health)
  - [Interoperability Framework](#interoperability-framework)
  - [Install the Interoperability Production](#install-the-interoperability-production)
  - [Create the Interoperability Production](#create-the-interoperability-production)
    - [Test the Interoperability Production](#test-the-interoperability-production)
  - [Modify the Business Process](#modify-the-business-process)
    - [Prepare your development environment](#prepare-your-development-environment)
    - [Run the tests](#run-the-tests)
    - [Implement the code](#implement-the-code)
      - [check\_token](#check_token)
      - [filter\_patient\_resource](#filter_patient_resource)
      - [filter\_resources](#filter_resources)
      - [on\_fhir\_request](#on_fhir_request)
    - [Run the tests](#run-the-tests-1)
- [Tips \& Tricks](#tips--tricks)
  - [7.4. Csp log](#74-csp-log)
  - [BP Solution](#bp-solution)


# 3. Objectives

This training aims to provide the participants with the following skills:

- Configure and use the FHIR server
- Create an OAuth2 Authorization Server
- Bind the FHIR server to the OAuth2 Authorization Server for support of SMART on FHIR
- Use the interoperability capabilities of IRIS for Health to filter FHIR resources
- Create a custom operation on the FHIR server

# 4. Installation

To install the training environment, you need to have Docker and Docker Compose installed on your machine.

You can install Docker and Docker Compose by following the instructions on the [Docker website](https://www.docker.com/).

Once you have Docker and Docker Compose installed, you can clone this repository and run the following command:

```bash
docker-compose up -d
```

This command will start the IRIS for Health container and the Web Gateway container to expose the FHIR server over HTTPS.

## 4.1. Access to the FHIR server

Once the containers are started, you can access the FHIR server at the following URL:

```url
https://localhost:4443/fhir/r5/
```

## 4.2. Access the InterSystems IRIS Management Portal

You can access the InterSystems IRIS Management Portal at the following URL:

```url
http://localhost:8089/csp/sys/UtilHome.csp
```

The default username and password are `SuperUser` and `SYS`.

# 5. Configuration of the OAuth2 Authorization Server

To configure the OAuth2 Authorization Server, you need to connect to the InterSystems IRIS Management Portal and navigate to the System Administration > Security > OAuth 2.0 > Servers.

![OAuth2 Servers](./misc/img/Oauth2_Server_Menu.png)

Next, we will fulfill the form to create a new OAuth2 Authorization Server.

## 5.1. General Tab

First we start with the General tab.

![General Tab](./misc/img/Oauth2_Server_General.png)

The parameters are as follows:

- **Description**: The description of the OAuth2 Authorization Server
  - Oauth2 Auth Server
- **Issuer**: The URL of the OAuth2 Authorization Server
  - https://webgateway/oauth2
  - *NOTE* : Here we use the URL of the Web Gateway to expose the FHIR server over HTTPS this is the internal dns name of the Web Gateway container.
- **Supported grant types**: The grant types supported by the OAuth2 Authorization Server
  - Authorization Code
  - Client Credentials
  - JWT Authorization 
  - *NOTE* : We will use the Client Credentials grant type to authenticate the FHIR server to the OAuth2 Authorization Server.
- **SSL/TLS Configuration**: The SSL/TLS configuration to use for the OAuth2 Authorization Server
  - Default : BFC_SSL

## 5.2. Scope Tab

Next we move to the Scope tab.

![Scope Tab](./misc/img/Oauth2_Server_Scope.png)

We will create 3 scopes:

- **user/Patient.read**: The scope to read patient resources
- **VIP**: The scope to read VIP patient resources
- **user/*.***: The scope to read all resources, for administrative purposes

## 5.3. JWT Tab

Next we move to the JWT tab.

![JWT Tab](./misc/img/Oauth2_Server_JWT.png)

Here we simply select the algorithm to use for the JWT.

We will use the RS256 algorithm.

If needed, we can select encryption for the JWT. We will not use encryption for this training.

## 5.4. Customization Tab

Next we move to the Customization tab.

![Customization Tab](./misc/img/Oauth2_Server_Customization.png)

Here is all the customization classes for the OAuth2 Authorization Server.

We change the following classes:

- **Generate token class**: The class to use to generate the token
  - *FROM* : %OAuth2.Server.Generate
  - *TO* : %OAuth2.Server.JWT

We can now save the OAuth2 Authorization Server.

Great, we have now configured the OAuth2 Authorization Server. 🥳

# 6. Configuration of the Client

To configure the client, you need to connect to the InterSystems IRIS Management Portal and navigate to the System Administration > Security > OAuth 2.0 > Client.

![OAuth2 Clients](./misc/img/Oauth2_Client_Menu.png)

To create a new client, we need first to register the OAuth2 Authorization Server.

## 6.1. Register the OAuth2 Authorization Server

On the client page, click on the `Create Server Description` button.

![Create Server Description](./misc/img/Oauth2_Client_Create_Server_Description.png)

## 6.2. Server Description

In the Server Description form, we need to fulfill the following parameters:

![Server Description](./misc/img/Oauth2_Client_Server_Form_Description.png)

- **Server URL**: The URL of the OAuth2 Authorization Server
  - https://webgateway/oauth2
- **SSL/TLS Configuration**: The SSL/TLS configuration to use for the OAuth2 Authorization Server
  - Default : BFC_SSL

Click on the `Discover and Save` button.

Neat, we have now registered the OAuth2 Authorization Server.

![Server Description](./misc/img/Oauth2_Client_Server_Form_Description_Discovered.png)

## 6.3. Create a new client

Next, we can create a new client.

On the client page, we have a new button `Client Configuration`.

![Client Configuration](./misc/img/Oauth2_Client_Create_Client.png)

Click on the `Client Configuration` button link to the Server Description.

We can now Create a new client.

![Create Client](./misc/img/Oauth2_Client_Create_Client_Form.png)

### 6.3.1. General Tab

First we start with the General tab.

![General Tab](./misc/img/Oauth2_Client_Create_Client_Form_General.png)

The parameters are as follows:

- **Application Name**: The name of the client
  - App
  - *NOTE* : This is the name of the client.
- **Client Name**: The name of the client
  - App
- **Client Type**: The type of the client
  - Confidential
  - *NOTE* : We will use the confidential client type to authenticate the FHIR server to the OAuth2 Authorization Server.
- **Redirect URI**: The redirect URI of the client
  - https://webgateway/oauth2
  - *NOTE* : Here we use the URL of the Web Gateway to expose the FHIR server over HTTPS this is the internal dns name of the Web Gateway container.
  - *NOTE* : This will not be used in this training.
- **Grant Types**: The grant types supported by the client
  - Client Credentials
  - *NOTE* : We will use the Client Credentials grant type to authenticate the Client Application to the OAuth2 Authorization Server.
- **Authentication Type**: The authentication type of the client
  - Basic
  - *NOTE* : We will use the Basic authentication type to authenticate the Client Application to the OAuth2 Authorization Server.

Now we can click the `Dynamic Registration` button.

Congratulations, we have now created the client. 🥳

If we go to the `Client Credentials` tab, we can see the client credentials.

Notice that the client credentials are the `Client ID` and the `Client Secret`.

# 7. Configuration of the FHIR server

⚠️ **WARNING** ⚠️ : Make sure to be on the `FHIRSERVER` namespace.

![Namespace](./misc/img/FHIR_Server_Namespace.png)

To configure the FHIR server, you need to connect to the InterSystems IRIS Management Portal and navigate to the Health > FHIR Configuration > Servers.

![FHIR Servers](./misc/img/FHIR_Server_Menu.png)

Next, we will create a new FHIR server.

Click on the `Server Configuration` button.

![Server Configuration](./misc/img/FHIR_Server_Create_Server.png)

## 7.1. Create a new FHIR server

In the Server Configuration form, we need to fulfill the following parameters:

![Server Configuration](./misc/img/FHIR_Server_Create_Server_Form.png)

- **Core FHIR Package**: The core FHIR package to use for the FHIR server
  - r5
- **URL**: The URL of the FHIR server
  - /fhir/r5
- **Interactions strategy**: The interactions strategy to use for the FHIR server
  - HS.FHIRServer.Storage./son.InteractionsStrategy
  - *NOTE* : This is the default interactions strategy for the FHIR server.

Click on the `Add` button.

This can take a few minutes. 🕒 Let's go grabe a coffee. ☕️

Great, we have now created the FHIR server. 🥳

## 7.2. Bind the FHIR server to the OAuth2 Authorization Server

Select the FHIR server and scroll down to the `Edit` button.

![FHIR Server](./misc/img/FHIR_Server_Edit.png)

In the FHIR Server form, we need to fulfill the following parameters:

![FHIR Server](./misc/img/FHIR_Server_Edit_Form.png)

- **OAuth2 Client Name**: The name of the client
  - App

Click on the `Save` button.

Great, we have now bind the FHIR server to the OAuth2 Authorization Server. 🥳

## 7.3. Test the FHIR server

To test the FHIR server, you can use the following command:

```http
GET https://localhost:4443/fhir/r5/Patient
```

Without the `Authorization` header, you will get a `401 Unauthorized` response.

To authenticate the request, you need to add the `Authorization` header with the `Bearer` token.

For that let's claim a token from the OAuth2 Authorization Server.

```http
POST https://localhost:4443/oauth2/token
Content-Type: application/x-www-form-urlencoded
Authorization: Basic 05GwihcDYkLBrB2LQI2a1jidips6o6I1X0DCIaij3rk:EyJAiDODy76vfE10RGVqza94jwfFrZ7IrdpBU7pLTdVXTSvQo5TiNZJTbGHLSxt6q1rDmeAbTdll9mtGhEniaw

grant_type=client_credentials&scope=user/Patient.read&aud=https://localhost:4443/fhir/r5
```

You will get a `200 OK` response with the `access_token` and the `token_type`.

Now you can use the `access_token` to authenticate the request to the FHIR server.

```http
GET https://localhost:4443/fhir/r5/Patient
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6MX0.eyJqdGkiOiJodHRwczovL3dlYmdhdGV3YXkvb2F1dGgyLmhzX2VjU2N5SnIyMTVKZi1iRHdHUVNBOGM2QSIsImlzcyI6Imh0dHBzOi8vd2ViZ2F0ZXdheS9vYXV0aDIiLCJzdWIiOiIwNUd3aWhjRFlrTEJyQjJMUUkyYTFqaWRpcHM2bzZJMVgwRENJYWlqM3JrIiwiZXhwIjoxNzA4OTU2MDQ3LCJhdWQiOiJodHRwczovL2xvY2FsaG9zdDo0NDQzL2ZoaXIvcjUiLCJzY29wZSI6InVzZXIvUGF0aWVudC5yZWFkIiwiaWF0IjoxNzA4OTUyNDQ3fQ.EJ0FyDyZfG3lRr9UfMfFNtD-SL54yb-YOcc2zrAMM0UkEpHTxGaxMCuZoabToxnCqBTD-tDx6BxC4ww8cA-PjI2MaAJKeosvlFaWxarvm_KRTQhJgUTRTq0ympvInl2n4aeG9ZlWnqeUpgB-p_zQCyJKLR8yIGq7z37Vys_Ycue7EdIOJkMQX3AfK6Mby96WkWsg33_ayuSdl1MMh3JG3pmu1LKzuao9PL8D-s14GoOwZVnIT70hyvwnztwof61jpOOX9WYo43X9PCN1OfxyFiHCFlI25nX90tCisfluboGiSuRQhU0hTQekmLnlDHPhZ-GL7bFAKrLdOCOh0ytp1Q
Accept: application/fhir+json
```

Great, you have now authenticated the request to the FHIR server. 🥳

# Filter FHIR Resources with InterSystems IRIS for Health

Ok, we now start a big topic.

The whole point of this topic will be to put in between the FHIR server and the client application the interoperability capabilities of IRIS for Health.

Here is a macro view of the architecture:

![Interoperability](./misc/img/Schema.png)

And here is the workflow:

![Workflow](./misc/img/Workflow.png)

What we notice here is that the `EAI` (Interoperability capabilities of IRIS for Health) will act as a path through for incoming requests to the FHIR server.
Will filter the response from the FHIR server based on scopes and send the filtered response to the client application.

Before going further, let me make a quick introduction to the Interoperability capabilities of IRIS for Health.

## Interoperability Framework

This is the IRIS Framework.

![FrameworkFull](https://raw.githubusercontent.com/thewophile-beep/formation-template/master/misc/img/FrameworkFull.png)

The whole point of this framework is to provide a way to connect different systems together.

We have 4 main components:

- **Business Services**: The entry point of the framework. It receives the incoming request and sends it to the production.
- **Business Processes**: The workflow of the framework. It processes the incoming request and sends it to the business operation.
- **Business Operations**: The exit point of the framework. It processes the incoming request and sends it to the business service.
- **Messages**: The data of the framework. It contains the incoming request and the outgoing response.

For this training, we will use the following components:

- One `Business Service` to receive the incoming request from the client application.
- One `Business Process` to filter the response from the FHIR server based on scopes.
- One `Business Operation` to send messages to the FHIR server.

For this training, we will be using a pre-built interoperability production.

And we will only focus on the `Business Process` to filter the response from the FHIR server based on scopes.

## Install the Interoperability Production

For this part, we will use the `IoP` tool. `IoP` stands for Interoperability on Python.

You can install the `IoP` tool by following the instructions on the [IoP repository](https://github.com/grongierisc/interoperability-embedded-python)

`IoP` is pre-installed in the training environment.

Connect to the running container:

```bash
docker exec -it formation-fhir-python-iris-1 bash
```

And run the following command:

```bash
iop --init
```

This will install `iop` on the IRIS for Health container.

## Create the Interoperability Production

Still in the container, run the following command:

```bash
iop --migrate /irisdev/app/src/python/EAI/settings.py
```

This will create the interoperability production.

Now you can access the interoperability production at the following URL:

```url
http://localhost:8089/csp/healthshare/eai/EnsPortal.ProductionConfig.zen?$NAMESPACE=EAI&$NAMESPACE=EAI&
```

You can now start the production.

Great, you have now created the interoperability production. 🥳

### Test the Interoperability Production

Get a token from the OAuth2 Authorization Server.

```http
POST https://localhost:4443/oauth2/token
Content-Type: application/x-www-form-urlencoded
Authorization : Basic 05GwihcDYkLBrB2LQI2a1jidips6o6I1X0DCIaij3rk:EyJAiDODy76vfE10RGVqza94jwfFrZ7IrdpBU7pLTdVXTSvQo5TiNZJTbGHLSxt6q1rDmeAbTdll9mtGhEniaw

grant_type=client_credentials&scope=user/Patient.read&aud=https://webgateway/fhir/r5
```

⚠️ **WARNING** ⚠️ : we change the `aud` parameter to the URL of the Web Gateway to expose the FHIR server over HTTPS.

Get a patient through the interoperability production.

```http
GET https://localhost:4443/fhir/Patient
Authorization : Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6MX0.eyJqdGkiOiJodHRwczovL3dlYmdhdGV3YXkvb2F1dGgyLmI3UjBEbUl1NmhBeTdkem94Zk1JUGJrdWN2QSIsImlzcyI6Imh0dHBzOi8vd2ViZ2F0ZXdheS9vYXV0aDIiLCJzdWIiOiIwNUd3aWhjRFlrTEJyQjJMUUkyYTFqaWRpcHM2bzZJMVgwRENJYWlqM3JrIiwiZXhwIjoxNzA4OTYwMDA3LCJhdWQiOiJodHRwczovL3dlYmdhdGV3YXkvZmhpci9yNSIsInNjb3BlIjoidXNlci9QYXRpZW50LnJlYWQiLCJpYXQiOjE3MDg5NTY0MDd9.MfZ2UWjQaKN0hzEs0VaCtVPSS00aNgOl0mN_1IRD0QbbJtb3lRsXk0za_vK4-FQ78AC8rPl5d_gbQ9OGMJK7mDlMIeUa_zyshu79S-0VXihvDneUTMpKglWRdkxpwW2gXEuwumuQGSKH13A6capgbLIMcoIqeLSvPna_ufPulyVgcr4SOi2vtHvojaogysW349-VsAUkEWUZPvqLskq6UY-uuLzHBu7ZE-QqPhqGA5qwlyEcgshbmgzFydb2CgReeck1WXAjesm5EcllQLphYaTfWU3zNbgtb8jDUrjfg6ZNlpAB7l1_TM3GEJ79D4jDTKOeWW-Ple5bretSA3LuTg
Accept: application/fhir+json
```

You can see the trace of the request in the interoperability production.

```url
http://localhost:8089/csp/healthshare/eai/EnsPortal.MessageViewer.zen?SOURCEORTARGET=Python.EAI.bp.MyBusinessProcess
```

## Modify the Business Process

All the code for the `Business Process` is in this file : `./src/python/EAI/bp.py`

For this training, we will be as a `TTD` (Test Driven Development) approach.

All the tests for the `Business Process` are in this file : `./src/python/tests/EAI/test_bp.py`

### Prepare your development environment

To prepare your development environment, we need to create a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the tests

To run the tests, you can use the following command:

```bash
pytest
```

Tests are failing.

### Implement the code

We have 4 functions to implement:

- `check_token`
- `on_fhir_request`
- `filter_patient_resource`
- `filter_resources`

You can implement the code in the `./src/python/EAI/bp.py` file.

#### check_token

This function will check if the token is valid and if the scope contains the `VIP` scope.
If the token is valid and the scope contains the `VIP` scope, the function will return `True`, otherwise it will return `False`.
We will use the `jwt` library to decode the token.

<details>
<summary>Click to see the code</summary>

```python
def check_token(self, token:str) -> bool:

    # decode the token
    decoded_token= jwt.decode(token, options={"verify_signature": False})

    # check if the token is valid
    if 'VIP' in decoded_token['scope']:
        return True
    else:
        return False
```

</details>

#### filter_patient_resource

This function will filter the patient resource.

It will remove the `name`, `address`, `telecom` and `birthdate` fields from the patient resource.

The function will return the filtered patient resource as a string.

We will use the `fhir.resources` library to parse the patient resource.

Notice the signature of the function.

The function takes a string as input and returns a string as output.

So we need to parse the input string to a `fhir.resources.patient.Patient` object and then parse the `fhir.resources.patient.Patient` object to a string.

<details>
<summary>Click to see the code</summary>

```python
def filter_patient_resource(self, patient_str:str) -> str:
    # filter the patient
    p = patient.Patient(**json.loads(patient_str))
    # remove the name
    p.name = []
    # remove the address
    p.address = []
    # remove the telecom
    p.telecom = []
    # remove the birthdate
    p.birthDate = None

    return p.json()
```

</details>

#### filter_resources

This function will filter the resources.

We need to check the resource type and filter the resource based on the resource type.

If the resource type is `Bundle`, we need to filter all the entries of the bundle that are of type `Patient`.

If the resource type is `Patient`, we need to filter the patient resource.

The function will return the filtered resource as a string.

We will use the `fhir.resources` library to parse the resource.

<details>
<summary>Click to see the code</summary>

```python
def filter_resources(self, resource_str:str) -> str:
    # parse the payload
    payload_dict = json.loads(resource_str)

    # what is the resource type?
    resource_type = payload_dict['resourceType'] if 'resourceType' in payload_dict else 'None'
    self.log_info('Resource type: ' + resource_type)

    # is it a bundle?
    if resource_type == 'Bundle':
        obj = bundle.Bundle(**payload_dict)
        # filter the bundle
        for entry in obj.entry:
            if entry.resource.resource_type == 'Patient':
                self.log_info('Filtering a patient')
                entry.resource = patient.Patient(**json.loads(self.filter_patient_resource(entry.resource.json())))

    elif resource_type == 'Patient':
        # filter the patient
        obj = patient.Patient(**json.loads(self.filter_patient_resource(resource_str)))

    return obj.json()
```

</details>

#### on_fhir_request

This function will be the entry point of the `Business Process`.

It will receive the request from the `Business Service`, check the token, filter the response from the FHIR server based on scopes and send the filtered response to the `Business Service`.

The function will return the response from the FHIR server.

We will use the `iris` library to send the request to the FHIR server.

The message will be a `iris.HS.FHIRServer.Interop.Request` object.

This object contains the request to the FHIR server.

This includes the `Method`, the `URL`, the `Headers` and the `Payload`.

To check the token, we will use the `check_token` function and use the header `USER:OAuthToken` to get the token.

To filter the response, we will use the `filter_resources` function and use the `QuickStream` to read the response from the FHIR server.

<details>
<summary>Click to see the code</summary>

```python
def on_fhir_request(self, request:'iris.HS.FHIRServer.Interop.Request'):
    # Do something with the request
    self.log_info('Received a FHIR request')

    # pass it to the target
    rsp = self.send_request_sync(self.target, request)

    # Try to get the token from the request
    token = request.Request.AdditionalInfo.GetAt("USER:OAuthToken") or ""

    # Do something with the response
    if self.check_token(token):
        self.log_info('Filtering the response')
        # Filter the response
        payload_str = self.quick_stream_to_string(rsp.QuickStreamId)

        # if the payload is empty, return the response
        if payload_str == '':
            return rsp

        filtered_payload_string = self.filter_resources(payload_str)

        # write the json string to a quick stream
        quick_stream = self.string_to_quick_stream(filtered_payload_string)

        # return the response
        rsp.QuickStreamId = quick_stream._Id()

    return rsp
```

</details>

### Run the tests

To run the tests, you can use the following command:

```bash
pytest
```

Tests are passing. 🥳

# Tips & Tricks

## 7.4. Csp log

In %SYS

```objectscript
set ^%ISCLOG = 5
zw ^ISCLOG
```

## BP Solution


<details>
<summary>Click to see the code</summary>

```python
from grongier.pex import BusinessProcess
import iris
import jwt
import json
from fhir.resources import patient, bundle

class MyBusinessProcess(BusinessProcess):

    def on_init(self):
        if not hasattr(self, 'target'):
            self.target = 'HS.FHIRServer.Interop.HTTPOperation'
            return

    def on_fhir_request(self, request:'iris.HS.FHIRServer.Interop.Request'):
        # Do something with the request
        self.log_info('Received a FHIR request')

        # pass it to the target
        rsp = self.send_request_sync(self.target, request)

        # Try to get the token from the request
        token = request.Request.AdditionalInfo.GetAt("USER:OAuthToken") or ""

        # Do something with the response
        if self.check_token(token):
            self.log_info('Filtering the response')
            # Filter the response
            payload_str = self.quick_stream_to_string(rsp.QuickStreamId)

            # if the payload is empty, return the response
            if payload_str == '':
                return rsp

            filtered_payload_string = self.filter_resources(payload_str)

            # write the json string to a quick stream
            quick_stream = self.string_to_quick_stream(filtered_payload_string)

            # return the response
            rsp.QuickStreamId = quick_stream._Id()

        return rsp
    
    def check_token(self, token:str) -> bool:

        # decode the token
        decoded_token= jwt.decode(token, options={"verify_signature": False})

        # check if the token is valid
        if 'VIP' in decoded_token['scope']:
            return True
        else:
            return False

    def quick_stream_to_string(self, quick_stream_id) -> str:
        quick_stream = iris.cls('HS.SDA3.QuickStream')._OpenId(quick_stream_id)
        json_payload = ''
        while quick_stream.AtEnd == 0:
            json_payload += quick_stream.Read()

        return json_payload
    
    def string_to_quick_stream(self, json_string:str):
        quick_stream = iris.cls('HS.SDA3.QuickStream')._New()

        # write the json string to the payload
        n = 3000
        chunks = [json_string[i:i+n] for i in range(0, len(json_string), n)]
        for chunk in chunks:
            quick_stream.Write(chunk)

        return quick_stream

    def filter_patient_resource(self, patient_str:str) -> str:
        # filter the patient
        p = patient.Patient(**json.loads(patient_str))
        # remove the name
        p.name = []
        # remove the address
        p.address = []
        # remove the telecom
        p.telecom = []
        # remove the birthdate
        p.birthDate = None

        return p.json()

    def filter_resources(self, resource_str:str) -> str:
        # parse the payload
        payload_dict = json.loads(resource_str)

        # what is the resource type?
        resource_type = payload_dict['resourceType'] if 'resourceType' in payload_dict else 'None'
        self.log_info('Resource type: ' + resource_type)

        # is it a bundle?
        if resource_type == 'Bundle':
            obj = bundle.Bundle(**payload_dict)
            # filter the bundle
            for entry in obj.entry:
                if entry.resource.resource_type == 'Patient':
                    self.log_info('Filtering a patient')
                    entry.resource = patient.Patient(**json.loads(self.filter_patient_resource(entry.resource.json())))

        elif resource_type == 'Patient':
            # filter the patient
            obj = patient.Patient(**json.loads(self.filter_patient_resource(resource_str)))

        return obj.json()
```

</details>

