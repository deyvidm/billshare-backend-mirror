# Bill Share API Route Documentation

Table of Contents
=================

Table of Contents
=================

Table of Contents
=================

   * [Bill Share API Route Documentation](#bill-share-api-route-documentation)
   * [Table of Contents](#table-of-contents)
   * [Table of Contents](#table-of-contents-1)
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
            * [Example 2](#example-2-1)
               * [Request](#request-21)
               * [Success](#success-20)
         * [GET Transaction by Id](#get-transaction-by-id)
            * [Request](#request-22)
            * [Success](#success-21)
            * [Failure](#failure-11)
            * [Example 1](#example-1-10)
               * [Request](#request-23)
               * [Success](#success-22)
         * [UPDATE Transaction, resolve debt](#update-transaction-resolve-debt)
            * [Request](#request-24)
            * [Success](#success-23)
            * [Failure](#failure-12)
            * [Example 1](#example-1-11)
               * [Request](#request-25)
               * [Success](#success-24)
         * [GET Transactions By User](#get-transactions-by-user)
            * [Request](#request-26)
            * [Success](#success-25)
            * [Failure](#failure-13)
            * [Example 1](#example-1-12)
               * [Request](#request-27)
               * [Success](#success-26)
         * [GET Transactions by Group](#get-transactions-by-group)
            * [Request](#request-28)
            * [Success](#success-27)
            * [Failure](#failure-14)
            * [Example 1](#example-1-13)
               * [Request](#request-29)
               * [Success](#success-28)
      * [Currency](#currency)
         * [GET List of Available Currency Codes](#get-list-of-available-currency-codes)
            * [Request](#request-30)
            * [Success](#success-29)
            * [Failure](#failure-15)
            * [Example 1](#example-1-14)
               * [Request](#request-31)
               * [Success](#success-30)
         * [GET Dictionary of Available Currency Codes and their Foreign Exchange Rates](#get-dictionary-of-available-currency-codes-and-their-foreign-exchange-rates)
            * [Request](#request-32)
            * [Success](#success-31)
            * [Failure](#failure-16)
            * [Example 1](#example-1-15)
               * [Request](#request-33)
               * [Success](#success-32)
      * [Data Visualization](#data-visualization)
         * [GET User Transaction Summary per date range](#get-user-transaction-summary-per-date-range)
            * [Request](#request-34)
            * [Success](#success-33)
            * [Failure](#failure-17)
            * [Example 1](#example-1-16)
               * [Request](#request-35)
               * [Success](#success-34)
         * [GET User Transaction balance within a group](#get-user-transaction-balance-within-a-group)
            * [Request](#request-36)
            * [Success](#success-35)
            * [Example 1](#example-1-17)
               * [Request](#request-37)
               * [Success](#success-36)
      * [Dashboard](#dashboard)
         * [GET Activity updates since last login](#get-activity-updates-since-last-login)
            * [Request](#request-38)
            * [Success](#success-37)
            * [Example 1](#example-1-18)
               * [Request](#request-39)
               * [Success](#success-38)


## Hosts

```Bash
https://api.billshare.io
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

> `group_users` list is ordered by most recent `updated_date`, which is updated when transactions are created or updated, and when groups are updated

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
  "split_type" <String, Required>,
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
split_type can be one of `percent` or `money`
```

#### Success
```Bash
200
{
  "id": <Integer, Required>,
  "label": <String, Required>,
  "created_date": <String, Required, DateTimeField or null>,
  "updated_date": <String, Required, DateTimeField or null>,
  "total_currency": <Character(3), Required>,
  "total": <String, Required>,
  "group": <Integer, Required>,
  "creator": <Integer, Required>,
  "transaction_line_items": [
    {
      "id": <Integer, Required>,
      "label": <String, Optional>,
      "percentage": <String, Required>,
      "debt_currency": <Character(3), Required>,
      "debt": <String, Required>,
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
  "split_type": "money",
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
      "percentage": "40.00",
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
      "percentage": "20.00",
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
      "percentage": "40.00",
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


#### Example 2

##### Request

```Bash
POST /transaction/
{
	"total": 6.77,
	"currency_code": "CAD",
	"label": "testLabel",
	"group": 1,
	"creator": 1,
	"split_type": "percent",
	"user_shares":[
		{
			"user": 1,
			"owes": 33.33,
			"paid": 6.00
		},
		{
			"user": 2,
			"owes": 33.33,
			"paid": 0.71
		},
		{
			"user": 3,
			"owes": 33.34,
			"paid": 0.06
		}
	]
}

```

##### Success

```Bash
200
{
    "id": 81,
    "transaction_line_items": [
        {
            "id": 113,
            "label": "",
            "percentage": "0.89",
            "debt_currency": "CAD",
            "debt": "0.05",
            "resolved": true,
            "transaction": 81,
            "group": 1,
            "debtor": 3,
            "creditor": 3
        },
        {
            "id": 114,
            "label": "",
            "percentage": "10.49",
            "debt_currency": "CAD",
            "debt": "0.71",
            "resolved": true,
            "transaction": 81,
            "group": 1,
            "debtor": 2,
            "creditor": 2
        },
        {
            "id": 115,
            "label": "",
            "percentage": "33.33",
            "debt_currency": "CAD",
            "debt": "2.26",
            "resolved": true,
            "transaction": 81,
            "group": 1,
            "debtor": 1,
            "creditor": 1
        },
        {
            "id": 116,
            "label": "",
            "percentage": "22.84",
            "debt_currency": "CAD",
            "debt": "1.55",
            "resolved": false,
            "transaction": 81,
            "group": 1,
            "debtor": 2,
            "creditor": 1
        },
        {
            "id": 117,
            "label": "",
            "percentage": "32.45",
            "debt_currency": "CAD",
            "debt": "2.20",
            "resolved": false,
            "transaction": 81,
            "group": 1,
            "debtor": 3,
            "creditor": 1
        }
    ],
    "label": "testLabel",
    "created_date": "2017-11-10T02:44:55.108601Z",
    "updated_date": "2017-11-10T02:44:55.108660Z",
    "total_currency": "CAD",
    "total": "6.77",
    "group": 1,
    "creator": 1
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
  "total_currency": <Character(3), Required>,
  "total": <String, Required>,
  "group": <Integer, Required>,
  "creator": <Integer, Required>,
  "split_type" <String, Required>,
  "transaction_line_items": [
    {
      "id": <Integer, Required>,
      "label": <String, Optional>,
      "percentage" <String, Required>,
      "debt_currency": <Character(3), Required>,
      "debt": <String, Required>,
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
  "total_currency": "CAD"",
  "total": "25.00",
  "group": 3,
  "creator": 4,
  "split_type": "money",
  "transaction_line_items": [
    {
      "id": 11,
      "label": "",
      "percentage": "40.00",
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
      "percentage": "20.00",
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
      "percentage": "40.00",
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
  "transaction": <Integer, Required>,
  "transaction_line_items": [
    {
      "transaction_line_item": <Integer, Required>,
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
  "total_currency": <Character(3), Required>,
  "total": <String, Required>,
  "group": <Integer, Required>,
  "creator": <Integer, Required>,
  "transaction_line_items": [
    {
      "id": <Integer, Required>,
      "label": <String, Optional>,
      "debt_currency": <Character(3), Required>,
      "debt": <String, Required>,
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
  "total_currency": "CAD",
  "total": "25.00",
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
    "total_currency": <Character(3), Required>,
    "total": <String, Required>,
    "group": <Integer, Required>,
    "creator": <Integer, Required>,
    "transaction_line_items": [
      {
        "id": <Integer, Required>,
        "label": <String, Optional>,
        "debt_currency": <Character(3), Required>,
        "debt": <String, Required>,
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
    "total_currency": "CAD",
    "total": "25.00",
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
    "total_currency": <Character(3), Required>,
    "total": <String, Required>,
    "group": <Integer, Required>,
    "creator": <Integer, Required>,
    "transaction_line_items": [
      {
        "id": <Integer, Required>,
        "label": <String, Optional>,
        "debt_currency": <Character(3), Required>,
        "debt": <String, Required>,
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
    "total_currency": "CAD"
    "total": "25.00"
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

## Currency

### GET List of Available Currency Codes

#### Request

```Bash
GET /currency/codes/
{}
```

#### Success

```Bash
200
[
  <Character(3), Required>,
  ...
]
```

#### Failure

```Bash
404
{
  'error': 'Could not provide currency codes'
}
```

#### Example 1

##### Request

```Bash
GET /currency/codes/
{}
```

##### Success

```Bash
200
[
  "AUD",
  "BGN",
  "BRL",
  "CAD",
  "CHF",
  "CNY",
  "CZK",
  "DKK",
  "EUR",
  "GBP",
  "HKD",
  "HRK",
  "HUF",
  "IDR",
  "ILS",
  "INR",
  "JPY",
  "KRW",
  "MXN",
  "MYR",
  "NOK",
  "NZD",
  "PHP",
  "PLN",
  "RON",
  "RUB",
  "SEK",
  "SGD",
  "THB",
  "TRY",
  "USD",
  "ZAR"
]
```

### GET Dictionary of Available Currency Codes and their Foreign Exchange Rates

#### Request

```Bash
GET /currency/
{}
```

#### Success

```Bash
200
{
  <Character(3), Required>: <Decimal, Required>,
  ...
}
```

#### Failure

```Bash
404
{
  'error': 'Could not provide currency codes'
}
```

#### Example 1

##### Request

```Bash
GET /currency/
{}
```

##### Success

> The "base" currency is always 1, default being CAD

> The default date is always "today" in UTC Time

```Bash
200
{
  "AUD": 1.0239,
  "BGN": 1.3188,
  "BRL": 2.5632,
  "CAD": 1,
  "CHF": 0.78456,
  "CNY": 5.2057,
  "CZK": 17.297,
  "DKK": 5.0183,
  "EUR": 0.67431,
  "GBP": 0.59962,
  "HKD": 6.133,
  "HRK": 5.0799,
  "HUF": 209.23,
  "IDR": 10606,
  "ILS": 2.7538,
  "INR": 50.717,
  "JPY": 89.562,
  "KRW": 875.72,
  "MXN": 14.931,
  "MYR": 3.3265,
  "NOK": 6.3953,
  "NZD": 1.1326,
  "PHP": 40.205,
  "PLN": 2.8579,
  "RON": 3.1003,
  "RUB": 46.052,
  "SEK": 6.6023,
  "SGD": 1.069,
  "THB": 26.034,
  "TRY": 3.0295,
  "USD": 0.78604,
  "ZAR": 11.105
}
```

## Data Visualization

### GET User Transaction Summary per date range

#### Request

```bash
GET /user/<user_id>/transactions/summary/

date_start <String, Required>
date_end <String, Required>
{}
``` 

#### Success

```Bash
200
{
    "date_end": <String, Required>,
    "date_start": <String, Required>,
    "total transactions": <Int, Required>,
    "debt": <Float, Required>,
    "credit": <Float, Required>
}
```

#### Failure
```bash
404
{
    "error": "['date_start cannot be more recent than date_end']"
}
```

#### Example 1

##### Request
```bash
GET /user/1/transactions/summary?date_start=2017-08-01&date_end=2017-09-01/
```

##### Success
>let the time range be 2017-08-01 and 2018-09-01 

>within the time range there were 5 transactions involving the user

>user is owed 20 across all transactions (within range)

>user owes 90 across all transactions (within range)
```bash
200
{
    "date_end": "2017-09-01",
    "date_start": "2017-08-01",
    "total transactions": 5,
    "debt": 20,
    "credit": 90
}
```

### GET User Transaction balance within a group 

#### Request

```bash
GET /user/<user_id>/group/<group_id>/balance/
{}
``` 

#### Success

```Bash
200
<Float, Required>
```

#### Example 1

##### Request
```bash
GET /user/3/group/1/balance
```

##### Success
>positive number means the user is owed by others

>negative number means the user owes others

```bash
200
60.08
```

## Dashboard

### GET Activity updates since last login

#### Request

```bash
GET /user/<user_id>/dashboard/
```

#### Success
- 'groups' is a list of Group objects as outlined by `GET /group/<group_id>/`
- 'transactions' is a list of Transaction objects as outline by `GET /transactions/<transaction_id>` 
- an item in theses lists means that the item was updated while the user was offline
- it's possible for both lists to be empty (i.e. no new activity since last login)

```Bash
200
{
    "groups": [
        <Group, Optional>
    ],
    "transactions": [
        <Transaction, Optional>,
        ...
    ]
}
```

#### Example 1

##### Request
```bash
GET /user/2/dashboard/
```

##### Success
```bash
200
{
    "transactions": [
        {
            "id": 2,
            "transaction_line_items": [
                {
                    "id": 6,
                    "label": "",
                    "percentage": "60.00",
                    "debt_currency": "CAD",
                    "debt": "60.00",
                    "resolved": false,
                    "transaction": 2,
                    "group": 1,
                    "debtor": 2,
                    "creditor": 3
                },
                {
                    "id": 5,
                    "label": "",
                    "percentage": "30.00",
                    "debt_currency": "CAD",
                    "debt": "30.00",
                    "resolved": true,
                    "transaction": 2,
                    "group": 1,
                    "debtor": 2,
                    "creditor": 2
                },
                {
                    "id": 4,
                    "label": "",
                    "percentage": "10.00",
                    "debt_currency": "CAD",
                    "debt": "10.00",
                    "resolved": true,
                    "transaction": 2,
                    "group": 1,
                    "debtor": 3,
                    "creditor": 3
                }
            ],
            "label": "User 2 owes User 3",
            "created_date": "2017-11-22T19:35:00.295984Z",
            "updated_date": "2017-11-22T19:35:00.296025Z",
            "total_currency": "CAD",
            "total": "100.00",
            "split_type": "money",
            "group": 1,
            "creator": 2
        }
    ],
    "groups": [
        {
            "id": 1,
            "label": "frozen bois",
            "group_users": [
                {
                    "id": 3,
                    "email": "jon@test.ca",
                    "first_name": "jon",
                    "last_login": "2017-11-22T19:35:00.054840Z",
                    "last_name": "snow"
                },
                {
                    "id": 2,
                    "email": "sandor@test.ca",
                    "first_name": "sandor",
                    "last_login": "2017-11-22T19:34:59.811355Z",
                    "last_name": "clegane"
                },
                {
                    "id": 1,
                    "email": "tormund@test.ca",
                    "first_name": "tormund",
                    "last_login": "2017-11-26T19:17:14.048552Z",
                    "last_name": "giantsbane"
                }
            ]
        }
    ]
}
```