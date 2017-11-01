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
               * [Request](#request-12)
               * [Success](#success-11)
      * [Groups](#groups)
         * [Create Group](#create-group)
            * [Request](#request-13)
            * [Success](#success-12)
            * [Failure](#failure-7)
            * [Example 1](#example-1-6)
               * [Request](#request-14)
               * [Success](#success-13)
         * [DELETE Group](#delete-group)
            * [Request](#request-15)
            * [Success](#success-14)
            * [Failure](#failure-8)
            * [Example 1](#example-1-7)
               * [Request](#request-16)
               * [Success](#success-15)
         * [GET All Groups Related to a User](#get-all-groups-related-to-a-user)
            * [Request](#request-17)
            * [Success](#success-16)
            * [Failure](#failure-9)
            * [Example 1](#example-1-8)
               * [Request](#request-18)
               * [Success](#success-17)
      * [Transactions](#transactions)
         * [Create Transaction](#create-transaction)
            * [Request](#request-19)
            * [Success](#success-18)
            * [Failure](#failure-10)
            * [Example 1](#example-1-9)
               * [Request](#request-20)
               * [Success](#success-19)
         * [GET Transaction by Id](#get-transaction-by-id)
            * [Request](#request-21)
            * [Success](#success-20)
            * [Failure](#failure-11)
            * [Example 1](#example-1-10)
               * [Request](#request-22)
               * [Success](#success-21)
         * [UPDATE Transaction, resolve debt](#update-transaction-resolve-debt)
            * [Request](#request-23)
            * [Success](#success-22)
            * [Failure](#failure-12)
            * [Example 1](#example-1-11)
               * [Request](#request-24)
               * [Success](#success-23)
         * [GET Transactions By User](#get-transactions-by-user)
            * [Request](#request-25)
            * [Success](#success-24)
            * [Failure](#failure-13)
            * [Example 1](#example-1-12)
               * [Request](#request-26)
               * [Success](#success-25)
         * [GET Transactions by Group](#get-transactions-by-group)
            * [Request](#request-27)
            * [Success](#success-26)
            * [Failure](#failure-14)
            * [Example 1](#example-1-13)
               * [Request](#request-28)
               * [Success](#success-27)


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
POST /auth/login/
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
{
  "total": 25.00,
  "currency_code": "CAD",
  "label": "Gryphs Last Night",
  "group": 3,
  "creator": 4,
  "user_shares":[
    {
      "user": 4,
      "owes": 10.00,
      "paid": 15
    },
    {
      "user": 5,
      "owes": 15,
      "paid": 10.00
    }
  ]
}

```

##### Success

```Bash
200
{
  "id": 10,
  "label": "Gryphs Last Night",
  "created_date": "2017-10-31T04:58:40.730834Z",
  "updated_date": "2017-10-31T04:58:40.730861Z",
  "group": 3,
  "creator": 4,
  "transaction_line_items": [
    {
      "id": 11,
      "label": "",
      "debt_currency": "CAD",
      "debt": "10.00",
      "resolved": true,
      "transaction": 10,
      "group": 3,
      "debtor": 4,
      "creditor": 4
    },
    {
      "id": 12,
      "label": "",
      "debt_currency": "CAD",
      "debt": "5.00",
      "resolved": false,
      "transaction": 10,
      "group": 3,
      "debtor": 5,
      "creditor": 4
    },
    {
      "id": 15,
      "label": "",
      "debt_currency": "CAD",
      "debt": "10.00",
      "resolved": true,
      "transaction": 10,
      "group": 3,
      "debtor": 5,
      "creditor": 5
    }
  ]
}
```

### GET Transaction by Id

#### Request
```Bash
GET /transaction/<transaction_id>/
{}
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
GET /transaction/10/
{}
```

##### Success

```Bash
200
{
  "id": 10,
  "label": "Gryphs Last Night",
  "created_date": "2017-10-31T04:58:40.730834Z",
  "updated_date": "2017-10-31T04:58:40.730861Z",
  "group": 3,
  "creator": 4,
  "transaction_line_items": [
    {
      "id": 11,
      "label": "",
      "debt_currency": "CAD",
      "debt": "10.00",
      "resolved": true,
      "transaction": 10,
      "group": 3,
      "debtor": 4,
      "creditor": 4
    },
    {
      "id": 12,
      "label": "",
      "debt_currency": "CAD",
      "debt": "5.00",
      "resolved": false,
      "transaction": 10,
      "group": 3,
      "debtor": 5,
      "creditor": 4
    },
    {
      "id": 15,
      "label": "",
      "debt_currency": "CAD",
      "debt": "10.00",
      "resolved": true,
      "transaction": 10,
      "group": 3,
      "debtor": 5,
      "creditor": 5
    }
  ]
}
```

### UPDATE Transaction, resolve debt

#### Request
```Bash
PUT /transaction/
{
  "id": <Integer, Required>,
  "transaction_line_items": [
    {
      "id": <Integer, Required>,
      "resolved": <Boolean, Required>
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
PUT /transaction/
{
  "transaction": 10,
  "transaction_line_items": [
    {
      "transaction_line_item": 12,
      "resolved": true
    }
  ]
}
```

##### Success

```Bash
200
{
  "id": 10,
  "label": "Gryphs Last Night",
  "created_date": "2017-10-31T04:58:40.730834Z",
  "updated_date": "2017-10-31T04:58:40.730861Z",
  "group": 3,
  "creator": 4,
  "transaction_line_items": [
    {
      "id": 11,
      "label": "",
      "debt_currency": "CAD",
      "debt": "10.00",
      "resolved": true,
      "transaction": 10,
      "group": 3,
      "debtor": 4,
      "creditor": 4
    },
    {
      "id": 12,
      "label": "",
      "debt_currency": "CAD",
      "debt": "5.00",
      "resolved": true,
      "transaction": 10,
      "group": 3,
      "debtor": 5,
      "creditor": 4
    },
    {
      "id": 15,
      "label": "",
      "debt_currency": "CAD",
      "debt": "10.00",
      "resolved": true,
      "transaction": 10,
      "group": 3,
      "debtor": 5,
      "creditor": 5
    }
  ]
}
```

### GET Transactions By User

#### Request
```Bash
GET /user/<user_id>/transactions/
{}
```

#### Success
```Bash
200
[
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
GET /user/4/transactions/
{}
```

##### Success

```Bash
200
[
  {
    "id": 10,
    "label": "Gryphs Last Night",
    "created_date": "2017-10-31T04:58:40.730834Z",
    "updated_date": "2017-10-31T04:58:40.730861Z",
    "group": 3,
    "creator": 4,
    "transaction_line_items": [
      {
        "id": 11,
        "label": "",
        "debt_currency": "CAD",
        "debt": "10.00",
        "resolved": true,
        "transaction": 10,
        "group": 3,
        "debtor": 4,
        "creditor": 4
      },
      {
        "id": 12,
        "label": "",
        "debt_currency": "CAD",
        "debt": "5.00",
        "resolved": true,
        "transaction": 10,
        "group": 3,
        "debtor": 5,
        "creditor": 4
      },
      {
        "id": 15,
        "label": "",
        "debt_currency": "CAD",
        "debt": "10.00",
        "resolved": true,
        "transaction": 10,
        "group": 3,
        "debtor": 5,
        "creditor": 5
      }
    ]
  }
]
```

### GET Transactions by Group

#### Request
```Bash
GET /group/<group_id>/transactions/
{}
```

#### Success
```Bash
200
[
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
GET /group/4/transactions/
{}
```

##### Success

```Bash
200
[
  {
    "id": 10,
    "label": "Gryphs Last Night",
    "created_date": "2017-10-31T04:58:40.730834Z",
    "updated_date": "2017-10-31T04:58:40.730861Z",
    "group": 3,
    "creator": 4,
    "transaction_line_items": [
      {
        "id": 11,
        "label": "",
        "debt_currency": "CAD",
        "debt": "10.00",
        "resolved": true,
        "transaction": 10,
        "group": 3,
        "debtor": 4,
        "creditor": 4
      },
      {
        "id": 12,
        "label": "",
        "debt_currency": "CAD",
        "debt": "5.00",
        "resolved": true,
        "transaction": 10,
        "group": 3,
        "debtor": 5,
        "creditor": 4
      },
      {
        "id": 15,
        "label": "",
        "debt_currency": "CAD",
        "debt": "10.00",
        "resolved": true,
        "transaction": 10,
        "group": 3,
        "debtor": 5,
        "creditor": 5
      }
    ]
  }
]
```