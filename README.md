
# Thoughts Backend

## Auth Endpoints:

- POST `auth/login`
  
Body input:  
```
{
  "username": username, 
  "password": password
}
```
  
- POST `auth/register`
  
Body input: 
```
{
  "email": email, 
  "password": password, 
  "username": username
}
```

- GET `auth/whoami`
  
Bearer Token Required.

- GET `auth/refresh`

Bearer Token Required.

- GET `auth/logout`

## Thought Endpoints

- POST `thought/create`
  
Bearer Token Required.

Body Input: 
```
{
  "content": content,
  "anonymous": "true"
}
```
- GET `thought/get`

- GET `thought/get/<username>`

## Social Endpoints

- POST `social/follow`
  
Bearer Token Required.

Body Input:
```
{
  "username": username being followed
}
```
- POST `social/unfollow`
  
Bearer Token Required.

Body Input:
```
{
  "username": username being unfollowed
}
```

