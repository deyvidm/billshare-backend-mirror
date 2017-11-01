# Bill Share API Route Documentation

   * [Bill Share API Route Documentation](#bill-share-api-route-documentation)
      * [Hosts](#hosts)
      * [Users](#users)
         * [GET User by Id](#get-user-by-id)
            * [Request](#request)
            * [Success](#success)
            * [Failure](#failure)
            * [Example 1](#example-1)
               * [Request](#request-1)
               * [Success](#success-1)
         * [GET Current User](#get-current-user)
            * [Request](#request-2)
            * [Success](#success-2)
            * [Failure](#failure-1)
            * [Example 1](#example-1-1)
               * [Request](#request-3)
               * [Success](#success-3)
            * [Example 2](#example-2)
               * [Request](#request-4)
               * [Failure](#failure-2)
      * [Auth](#auth)
         * [Create User](#create-user)
            * [Request](#request-5)
            * [Success](#success-4)
            * [Failure](#failure-3)
            * [Example 1](#example-1-2)
               * [Request](#request-6)
               * [Success](#success-5)
         * [Login](#login)
            * [Request](#request-7)
            * [Success](#success-6)
            * [Failure](#failure-4)
            * [Example 1](#example-1-3)
               * [Request](#request-8)
               * [Success](#success-7)
         * [Logout](#logout)
            * [Request](#request-9)
            * [Success](#success-8)
            * [Failure](#failure-5)
            * [Example 1](#example-1-4)
               * [Request](#request-10)
               * [Success](#success-9)
      * [Groups](#groups)
         * [GET Group by Id](#get-group-by-id)
            * [Request](#request-11)
            * [Success](#success-10)
            * [Failure](#failure-6)
            * [Example 1](#example-1-5)
               * [Request](#request-12)
               * [Success](#success-11)


## Hosts

```Bash
http://billshare.io:3000
127.0.0.1:3000
```

## Users

### GET User by Id

#### Request
```Bash
GET /user/<user_id>/
{}
```

#### Success
```Bash
200
{
  "id": <Integer, Required>,
  "last_login": <String, Required, DateTimeField or null>,
  "email": <String, Required, EmailField>,
  "first_name": <String, Required>,
  "last_name": <String, Required>
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
GET /user/4/
{}
```

##### Success

```Bash
200
{
  "id": 4,
  "last_login": "2017-10-26T13:47:40.346Z",
  "email": "person@example.com",
  "first_name": "bob",
  "last_name": "franks"
}
```

### GET Current User

* Return current logged in `user_id` or null

* Requires Session Cookie from Login

#### Request
```Bash
GET /user/
{}
```

#### Success
```Bash
200
{
  "user": <Integer, Required>
}
```

#### Failure
```Bash
200
{
  "user": <null, Required>
}
```

#### Example 1

##### Request

```Bash
GET /user/
{}
```

##### Success

```Bash
200
{
  "user": 1
}
```

#### Example 2

##### Request

```Bash
GET /user/
{}
```

##### Failure

```Bash
200
{
  "user": null
}
```

## Auth

### Create User

#### Request
```Bash
POST /auth/create/
{
  "email": <String, Required, EmailField>,
  "password": <String, Required>,
  "first_name": <String, Required>,
  "last_name": <String, Required>
}
```

#### Success
```Bash
200
{
  "id": <Integer, Required>,
  "last_login": <String, Required, DateTimeField or null>,
  "email": <String, Required, EmailField>,
  "first_name": <String, Required>,
  "last_name": <String, Required>
}
```

#### Failure
```Bash
404
{
  "error": "Email already exists" <String, Optional>
}
```

#### Example 1

##### Request

```Bash
POST /auth/create/
{
  "email": "person@example.com",
  "password": "hunter2",
  "first_name": "bob",
  "last_name": "franks"
}
```

##### Success

```Bash
200
{
  "id": 4,
  "last_login": "2017-10-26T13:47:40.346Z",
  "email": "person@example.com",
  "first_name": "bob",
  "last_name": "franks"
}
```

### Login

#### Request
```Bash
POST /auth/login/
{
  "email": <String, Required, EmailField>,
  "password": <String, Required>,
}
```

#### Success

> Returns a Session Cookie: `sessionid=<hash>; expires=<GMT Date>; HttpOnly; Max-Age=1209600; Path=/`

```Bash
200
{
  "id": <Integer, Required>,
  "last_login": <String, Required, DateTimeField or null>,
  "email": <String, Required, EmailField>,
  "first_name": <String, Required>,
  "last_name": <String, Required>
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
GET //
{
  "email": "person@example.com",
  "password": "hunter2"
}
```

##### Success

```Bash
200
{
  "id": 4,
  "last_login": "2017-10-26T13:47:40.346Z",
  "email": "person@example.com",
  "first_name": "bob",
  "last_name": "franks"
}
```

### Logout

> Clears the Session Cookie

#### Request
```Bash
POST /auth/logout/
{}
```

#### Success
```Bash
200
{}
```

#### Failure
```Bash
200
{}
```

#### Example 1

##### Request

```Bash
POST /auth/logout/
{}
```

##### Success

```Bash
200
{}
```

## Groups

### GET Group by Id

#### Request
```Bash
GET /group/<group_id>/
{}
```

#### Success
```Bash
200
{
  "id": <Integer, Required>,
  "label": <String, Required>,
  "group_users": [
    {
      "id": <Integer, Required>,
      "last_login": <String, Required, DateTimeField or null>,
      "email": <String, Required, EmailField>,
      "first_name": <String, Required>,
      "last_name": <String, Required>
    },
    ...
  ]
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
GET /group/3/
{}
```

##### Success

```Bash
200
{
  "id": 3,
  "label": "Restaurant Group",
  "group_users": [
    {
      "id": 4,
      "last_login": "2017-10-26T13:47:40.346Z",
      "email": "person@example.com",
      "first_name": "bob",
      "last_name": "franks"
    }
    {
      "id": 5,
      "last_login": "2017-10-26T13:47:40.346Z",
      "email": "daniel@jackson.com",
      "first_name": "Daniel",
      "last_name": "Jacckson"
    }
  ]
}
```

### Create Group

#### Request
```Bash
POST /group/
{
  "label": <String, Required>,
  "creator": <String, Required, EmailField>,
  "group_users": [
    "email": <String, Required, EmailField>,
    ...
  ]
}
```

#### Success
```Bash
200
{
  "id": <Integer, Required>,
  "label": <String, Required>,
  "group_users": [
    {
      "id": <Integer, Required>,
      "last_login": <String, Required, DateTimeField or null>,
      "email": <String, Required, EmailField>,
      "first_name": <String, Required>,
      "last_name": <String, Required>
    },
    ...
  ]
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
POST /group/
{
  "label": "Restaurant Group",
  "creator": "daniel@jackson.com",
  "group_users": [
     "daniel@jackson.com",
     "person@example.com"
  ]
}
```

##### Success

```Bash
200
{
  "id": 3,
  "label": "Restaurant Group",
  "group_users": [
    {
      "id": 4,
      "last_login": "2017-10-26T13:47:40.346Z",
      "email": "person@example.com",
      "first_name": "bob",
      "last_name": "franks"
    }
    {
      "id": 5,
      "last_login": "2017-10-26T13:47:40.346Z",
      "email": "daniel@jackson.com",
      "first_name": "Daniel",
      "last_name": "Jacckson"
    }
  ]
}
```

### DELETE Group

#### Request
```Bash
DELETE /group/<group_id>/
{}
```

#### Success
```Bash
200
{
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
DELETE /group/3/
{}
```

##### Success

```Bash
200
{}
```

### GET All Groups Related to a User

#### Request
```Bash
GET /user/<id>/groups/
{}
```

#### Success
```Bash
200
[
  {
    "id": <Integer, Required>,
    "label": <String, Required>,
    "group_users": [
      {
        "id": <Integer, Required>,
        "last_login": <String, Required, DateTimeField or null>,
        "email": <String, Required, EmailField>,
        "first_name": <String, Required>,
        "last_name": <String, Required>
      },
      ...
    ]
  },
  ...
]
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
GET /user/4/groups/
{}
```

##### Success

```Bash
200

[
  {
    "id": 3,
    "label": "Restaurant Group",
    "group_users": [
      {
        "id": 4,
        "last_login": "2017-10-26T13:47:40.346Z",
        "email": "person@example.com",
        "first_name": "bob",
        "last_name": "franks"
      }
      {
        "id": 5,
        "last_login": "2017-10-26T13:47:40.346Z",
        "email": "daniel@jackson.com",
        "first_name": "Daniel",
        "last_name": "Jacckson"
      }
    ] 
  },
  ...
]
...   
```   

## Transactions

### Create Transaction

#### Request
```Bash
POST /transaction/
{
  "total": <Decimal, Required>,
  "currency_code": <Character(3), Required>,
  "label": <String, Required>,
  "group": <Integer, Required>,
  "creator": <Integer, Required>,
  "user_shares":[
    {
      "user": <Integer, Required>,
      "owes": <Decimal, Required>,
      "paid": <Decimal, Required>,
      "label": <String, Optional>
    },
    ...
  ]
}
```

#### Success
```Bash
200
{
  "id": <Integer, Required>,
  "label": <String, Required>,
  "created_date": <String, Required, DateTimeField or null>,
  "updated_date": <String, Required, DateTimeField or null>,
  "group": <Integer, Required>,
  "creator": <Integer, Required>,
  "transaction_line_items": [
    {
      "id": <Integer, Required>,
      "label": <String, Optional>,
      "debt_currency": <Character(3), Required>,
      "debt": <Decimal, Required>,
      "resolved": <Boolean, Required>,
      "transaction": <Integer, Required>,
      "group": <Integer, Required>,
      "debtor": <Integer, Required>,
      "creditor": <Integer, Required>
    },
    ...
  ]
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
POST /transaction/
{}
```

##### Success

```Bash
200
{
}
```
### GET

#### Request
```Bash
GET //
{}
```

#### Success
```Bash
200
{
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
GET //
{}
```

##### Success

```Bash
200
{
}
```
### GET

#### Request
```Bash
GET //
{}
```

#### Success
```Bash
200
{
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
GET //
{}
```

##### Success

```Bash
200
{
}
```
### GET

#### Request
```Bash
GET //
{}
```

#### Success
```Bash
200
{
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
GET //
{}
```

##### Success

```Bash
200
{
}
```
### GET

#### Request
```Bash
GET //
{}
```

#### Success
```Bash
200
{
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
GET //
{}
```

##### Success

```Bash
200
{
}
```
### GET

#### Request
```Bash
GET //
{}
```

#### Success
```Bash
200
{
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
GET //
{}
```

##### Success

```Bash
200
{
}
```
### GET

#### Request
```Bash
GET //
{}
```

#### Success
```Bash
200
{
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
GET //
{}
```

##### Success

```Bash
200
{
}
```
### GET

#### Request
```Bash
GET //
{}
```

#### Success
```Bash
200
{
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
GET //
{}
```

##### Success

```Bash
200
{
}
```
### GET

#### Request
```Bash
GET //
{}
```

#### Success
```Bash
200
{
}
```

#### Failure
```Bash
404
{}
```

#### Example 1

##### Request

```Bash
GET //
{}
```

##### Success

```Bash
200
{
}
```