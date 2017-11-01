# Bill Share API Route Documentation

## Hosts

```Bash
http://billshare.io:3000
127.0.0.1:3000
```

## User

### GET - Specific User

#### Request
```Bash
/user/<user_id>/

GET
{}
```

#### Success
```Bash
200
{
  "id": <Integer, Required>,
  "last_login": <String, Required, DateTimeField or Null>,
  "email": <String, Required, EmailField>,
  "first_name": <String, Required>,
  "last_name": <String, Required>
}
```

##### Example

###### Request
```Bash
/user/1/

GET
{}
```

###### Success
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

#### Failure
```Bash
404
{}
```