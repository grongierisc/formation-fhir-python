# formation-fhir-python

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

## Objectives

This training aims to provide the participants with the following skills:

- Configure and use the FHIR server
- Create an OAuth2 Authorization Server
- Bind the FHIR server to the OAuth2 Authorization Server for support of SMART on FHIR
- Use the interoperability capabilities of IRIS for Health to filter FHIR resources
- Create a custom operation on the FHIR server

## Installation

To install the training environment, you need to have Docker and Docker Compose installed on your machine.

You can install Docker and Docker Compose by following the instructions on the [Docker website](https://www.docker.com/).

Once you have Docker and Docker Compose installed, you can clone this repository and run the following command:

```bash
docker-compose up -d
```

This command will start the IRIS for Health container and the Web Gateway container to expose the FHIR server over HTTPS.

### Access to the FHIR server

Once the containers are started, you can access the FHIR server at the following URL:

```url
https://localhost:4443/fhir/r5/
```

### Access the InterSystems IRIS Management Portal

You can access the InterSystems IRIS Management Portal at the following URL:

```url
http://localhost:8089/csp/sys/UtilHome.csp
```

The default username and password are `SuperUser` and `SYS`.

## Configuration of the OAuth2 Authorization Server

To configure the OAuth2 Authorization Server, you need to connect to the InterSystems IRIS Management Portal and navigate to the System Administration > Security > OAuth 2.0 > Servers.

![OAuth2 Servers](./misc/img/Oauth2_Server_Menu.png)

Next, we will fulfill the form to create a new OAuth2 Authorization Server.

### General Tab

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

### Scope Tab

Next we move to the Scope tab.

![Scope Tab](./misc/img/Oauth2_Server_Scope.png)

We will create 3 scopes:

- **user/Patient.read**: The scope to read patient resources
- **VIP**: The scope to read VIP patient resources
- **user/*.***: The scope to read all resources, for administrative purposes

### JWT Tab

Next we move to the JWT tab.

![JWT Tab](./misc/img/Oauth2_Server_JWT.png)

Here we simply select the algorithm to use for the JWT.

We will use the RS256 algorithm.

If needed, we can select encryption for the JWT. We will not use encryption for this training.

### Customization Tab

Next we move to the Customization tab.

![Customization Tab](./misc/img/Oauth2_Server_Customization.png)

Here is all the customization classes for the OAuth2 Authorization Server.

We change the following classes:

- **Generate token class**: The class to use to generate the token
  - *FROM* : %OAuth2.Server.Generate
  - *TO* : %OAuth2.Server.JWT

We can now save the OAuth2 Authorization Server.

Great, we have now configured the OAuth2 Authorization Server. 🥳

## Configuration of the Client

To configure the client, you need to connect to the InterSystems IRIS Management Portal and navigate to the System Administration > Security > OAuth 2.0 > Client.

![OAuth2 Clients](./misc/img/Oauth2_Client_Menu.png)

To create a new client, we need first to register the OAuth2 Authorization Server.

### Register the OAuth2 Authorization Server

On the client page, click on the `Create Server Description` button.

![Create Server Description](./misc/img/Oauth2_Client_Create_Server_Description.png)

### Server Description

In the Server Description form, we need to fulfill the following parameters:

![Server Description](./misc/img/Oauth2_Client_Server_Form_Description.png)

- **Server URL**: The URL of the OAuth2 Authorization Server
  - https://webgateway/oauth2
- **SSL/TLS Configuration**: The SSL/TLS configuration to use for the OAuth2 Authorization Server
  - Default : BFC_SSL

Click on the `Discover and Save` button.

Neat, we have now registered the OAuth2 Authorization Server.

![Server Description](./misc/img/Oauth2_Client_Server_Form_Description_Discovered.png)

### Create a new client

Next, we can create a new client.

On the client page, we have a new button `Client Configuration`.

![Client Configuration](./misc/img/Oauth2_Client_Create_Client.png)

Click on the `Client Configuration` button link to the Server Description.

We can now Create a new client.

![Create Client](./misc/img/Oauth2_Client_Create_Client_Form.png)

#### General Tab

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

# debug

## FHIR Server Log

```objectscript
set ^HS.FHIRServer("dev") = 1
```

## Csp log

Dans %SYS

```objectscript
set ^%ISCLOG = 5
zw ^ISCLOG
```

