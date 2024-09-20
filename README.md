
# Thoughts Backend

## Auth Endpoints:

- `auth/login`
Body input:  
```
{
  "username": username, 
  "password": password
}
```
  
- `auth/register`
Body input: 
```
{
  "email": email, 
  "password": password, 
  "username": username
}
```

- `auth/whoami`
Bearer Token Required.

- `auth/logout`

## Thought Endpoints

- `thought/create`
Bearer Token Required.
Body Input: 
```
{
  "content": content,
  "anonymous": "true"
}
```
- `thought/get`

- `thought/get/<username>`

## Social

- `social/follow`
Bearer Token Required.
Body Input:
```
{
  "username": username being followed
}
```
- `social/unfollow`
Bearer Token Required.
Body Input:
```
{
  "username": username being unfollowed
}
```

