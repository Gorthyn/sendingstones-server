# sendingstones-server
Full-stack capstone server side

Sending Stones - Server Side README

This README describes the server-side API for Sending Stones, a comprehensive tool for tabletop gaming enthusiasts. This API uses JSON payloads to communicate data between the server and the client.

Fetch API Calls

This API exposes several endpoints for creating, retrieving, updating, and deleting game data. The endpoints include game, topic, post, comment, user, invitation, playergame, and tracker.

All requests to the API must include the Authorization header with the token obtained from the local storage. The header format is "Authorization": Token ${localStorage.getItem("ss_token")}`.

Comments

Get all comments of a post: /comment?post={postId}
Get a single comment: /comment/{commentId}
Create a comment: /comment (method: POST, body: JSON representation of the comment)
Delete a comment: /comment/{commentId} (method: DELETE)
Update a comment: /comment/{comment.id} (method: PUT, body: JSON representation of the comment)

Games

Get all games: /game
Get a single game: /game/{gameId}
Create a game: /game (method: POST, body: JSON representation of the game)
Delete a game: /game/{gameId} (method: DELETE)
Update a game: /game/{game.id} (method: PUT, body: JSON representation of the game)

Topics

Get all topics of a game: /topic?game={gameId}
Get a single topic: /topic/{topicId}
Create a topic: /topic (method: POST, body: JSON representation of the topic)
Delete a topic: /topic/{topicId} (method: DELETE)
Update a topic: /topic/{topicCopy.id} (method: PUT, body: JSON representation of the topic)

Posts

Get all posts of a topic: /post?topic={topicId}
Get a single post: /post/{postId}
Create a post: /post (method: POST, body: JSON representation of the post)
Delete a post: /post/{postId} (method: DELETE)
Update a post: /post/{post.id} (method: PUT, body: JSON representation of the post)

Users

Get all users: /users

Invitations

Get all invitations: /invitations
Create an invitation: /invitations (method: POST, body: JSON representation of the invitation)
Update an invitation: /invitations/{invitationId} (method: PUT, body: JSON representation of the invitation)
Delete an invitation: /invitations/{invitationId} (method: DELETE)

PlayerGames

Get all players of a game: /playergame?game={gameId}
Get all player games by gamer ID: /playergame?gamer={gamerId}
Remove a player: /playergame/{playerGameId} (method: DELETE)
Add a player game: /playergame (method: POST, body: JSON representation of the player game object)
Update a player game: /playergame/{playerGameObj.id} (method: PUT, body: JSON representation of the player game object)
Delete a player game: /playergame/{playerGameId} (method: DELETE)

Trackers

Get all trackers: /tracker
Get a single tracker: /tracker/{trackerId}
Create a tracker: /tracker (method: POST, body: JSON representation of the tracker)
Delete a tracker: /tracker/{trackerId} (method: DELETE)
Update a tracker: /tracker/{tracker.id} (method: PUT, body: JSON representation of the tracker)

Note
This API is subject to updates and changes. For the most current information, please refer to the latest documentation or API endpoint descriptions.
