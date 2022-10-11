# api_back_end
 
# ENDPOINTS
## CONNECTION

POST: /SIGNUP

POST: /LOGIN

__________________________

## USERS

GET: /USERS/ME

PATCH: /USERQ/ME

GET: /USERS/:ID

__________________________

## POSTS

PATCH: /POST/:ID

POST: /POSTS/

DELETE: /POST/:ID

GET: /POSTS

GET: /POST/ME

__________________________

## FOLLOWERS

GET: /POSTS/FOLLOWERS/ME

POST: /FOLLOWERS

GET: /FOLLOWERS/ME

DELETE: /FOLLOWERS/:ID

__________________________

## LIKES

POST: /LIKES

GET: /LIKES/ME

GET: /LIKES

DELETE: /LIKES/:ID

__________________________

## POSTS 

POST: /MESSAGES/

GET: /MESSAGES/:ID/:

__________________________

## COMMENTS 

POST: /COMMENTS

GET: /COMMENTS/:ID

GET: /COMMENTS/ME

DELETE: /COMMENTS/:ID




# RESPONSE FROM DB

## USER

{
    "id": ObjectId(),
    "username": String,
    "password": String,
    "createdAt": Date,
}

__________________________

## POSTS 

{
    "id": ObjectId(),
    "userId": ObjectId(),
    "content": String,
    "createdAt": Date,
}

__________________________

## LIKES

{
    "id": ObjectId(),
    "postId": ObjectId(),
    "userId": ObjectId(),
    "createdAt": Date,
}

__________________________

## COMMENTS 

{
    "id": ObjectId(),
    "postId": ObjectId(),
    "userId": ObjectId(),
    "content": String
    "createdAt": Date,
}

__________________________

## FOLLOWERS

{
    "id": ObjectId(),
    "userId": ObjectId(),
    "followingId": ObjectId(),
    "createdAt": Date,
}
__________________________

## MESSAGES

{
    "id": ObjectId(),
    "talkId": ObjectId(),
    "senderId": ObjectId(),
    "receiverId": ObjectId(),
    "content": String,
    "createdAt": Date,
}


# -------------------------------------

# SEND TO BACK

## USER

{
    "username": String,
    "password": String,
}

## POSTS 

{
    "userId": ObjectId(),
    "content": String,
}


## LIKES

{
    "postId": ObjectId(),
    "userId": ObjectId(),
}

## COMMENTS 

{
    "postId": ObjectId(),
    "userId": ObjectId(),
    "content": String
}

## FOLLOWERS

{
    "userId": ObjectId(),
    "followingId": ObjectId(),
}

## MESSAGES

{
    "talkId": ObjectId(),
    "senderId": ObjectId(),
    "receiverId": ObjectId(),
    "content": String,
}

# ------------------------------- 