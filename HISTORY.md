# HISTORY

__

# SET UP PROJECT 

1. Create a new repository on GitHub.

2. Endpoints of API.

>3. DATA JSON format. 

>4. BDD ONLINE. 

>5. Create a new project on Trello.
__
# Merge # 1
# Add implementation of structure of the project

- Write redme.md
- Add routes packages.
- Add models packages.
- Add middleware packages.
- Add core packages.
- Add requirements.txt.
- init mongodb connection WORKS With insert.
- Add route exemple get -> not finished.

# Merge # 2
# Add add example for crud with route + model

- Add contenu for user and Auth model.
- Add route for user and Auth in route package.
- Add auth router for main.py.
- Add Motor async for mongodb.

# Merge # 3
# Add model with datetime for user

- Add datetime for crud_auth user model and auth model.

# Merge # 4
# Implement handling of posts

- Get all posts.
- Create post.
- Patch post.
- Get all posts.
- Complet model, route and crud for posts.

# Merge # 5
# Feat/auth/jwt/login signup

- Add security.py for hashed password, generate token, verify token and get current user.
- Add crud_auth.py for craete user, login user and verify password.
- Modify the route for create user and add login method.

# Merge # 6
# Feat/docstring/security 

- Add HTTPException method for security.
- Complete followers model and route.
- Import typing for use Optional method.

# Merge # 7
# Implement delete and get_me_posts

- Add Function crud_get_all_posts for get all posts from all users.
- Add Function crud_create_post for create a post and adding created_at field.
- Add Function crud_patch_post for edit the content of a precise post by its ID.
- Add Function crud_get_me_posts for get all posts by the current user.
- Add Function crud_delete_post for delete a precise post by its ID.
- Add route for crud_get_all_posts, crud_create_post, crud_patch_post, crud_get_me_posts and crud_delete_post.

# Merge # 8
# Feat/followings/logic

- Modify Readme
- Implement logic for creating followers.
- Add router.get articles for users I follow.
- Add router.get /followers/me to get all my followers.
- Add router.get /followers/following for getting all users I follow
- Implement router.delete for unfollowing user I follow
- Implement get followers and following and retreive username instead o…
- Add docstring for followers crud
- Implement following logic

# Merge # 9
# Feat/comments/implementation

- Complete a route for comments.
- Implement getting comments from a postId.
- Implement patch commentary on post.
- Implement get/comments/me for getting all commentary of the user.
- Implement delete comments with id.
- Add docstring for comments logic.

# Merge # 10
# Feat/modify/users

- Add tags for documentation.
- Add method for change username.

# Merge # 11`
# Feat/docstrings missings

- Add method for get all users.
- Add Comment for method in Crud_users.
- Add response methods in users.py

# Merge # 12
# Add all likes methods + dependencies added on posts + likes

- Add all likes methods 
- Add dependencies added on posts 
- Add likes

# Merge # 13
# Change/reviews/routes

- Add a review and change some logic for likes routes.
- add logic for posts routes
- Implement reviewing route logic posts and likes.

# Merge # 14
# Added messages functions + doc on likes and messages
- Add messages functions 
- Add doc on likes and messages

# Merge # 15
# Feat/raises/exceptions

- raises exceptions for comments.
- Add raises exceptions for followers.
- Add raises exceptions for likes.
- Implement raises exceptions for crud posts.
- Implement raises exceptions for the users.
- Implement raises exceptions done.