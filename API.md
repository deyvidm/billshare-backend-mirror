# Bill Share API Route Documentation

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
GET /user/1/
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
    }
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