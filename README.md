# Overwatch-Team-Compostion-Maker
## A Character Assignment and Coaching Tool For The Modern Era

# About 
Overwatch is video game played under a fast paced environment that requires lots of quick decision making.

This Program will help the coach make QUICK and SMART decisions when choosing heroes against oposing teams.

# What Problem Is Being Solved Here ?

There are 31 characters in total
This makes for...     
<br> 31! / (31−6)!  <br>
      = 530,122,320 Possibilities if one wants to pick 6 heroes to play against an opposing team in a 6v6 match
      
### How can we get the optimal 6 heroes out of the possible 530,122,320 ?
### Using the Hungarian Algorithm of course !


# How This Program Works

### 1. Scrape Players Information From overbuff.com
### 2. Parse The Players Information and Get The Desired Values (Scores, Heroes, wins ... )
### 3. Prepare A Matrix Containing The Scores of the Heroes the player has played with.
### 4. Use the Hungarian algorithm to get the optimal results 
