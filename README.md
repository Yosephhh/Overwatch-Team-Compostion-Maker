# Overwatch-Team-Compostion-Maker 
## A Character Assignment and Coaching Tool For The Modern Era

### This Is The ( Console Version ) Really Cool Web App Comming Soon :)

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


# How To Use This Program.


## Step 1: Install The Latest Version of The Anaconda(Conda) Enviroment Along With The Following Libraries
Download The Latest Version Of Anaconda Anaconda Here: [https://repo.anaconda.com/archive/](https://repo.anaconda.com/archive/) 
 
#### For Ubuntu/Bash:

```bash
$ wget https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86_64.sh
$ bash Anaconda3-5.3.1-Linux-x86_64.sh
$ source ~/.bashrc
$ conda list
$ python -v
```
### You can use the default enviroment 
```bash
conda activate base instead
```

### Or create your own conda enviroment (Optional) 
```bash
$ conda create --name AnacondaPrompt python=3
$ conda activate AnacondaPrompt
```

### Install The Libraries Needed

```bash
(AnacondaPrompt) $ pip install bs4
(AnacondaPrompt) $ pip install requests
(AnacondaPrompt) $ pip install fake_useragent
(AnacondaPrompt) $ pip install pprint
(AnacondaPrompt) $ pip install prettytable
(AnacondaPrompt) $ pip install numpy
(AnacondaPrompt) $ pip install lxml
```
### Modify Directory and File Permissions
```bash
(AnacondaPrompt) $ sudo chmod ugo+r .
(AnacondaPrompt) $ sudo chmod ugo+w .
(AnacondaPrompt) $ chmod 777 O_TCM.py
```
### Finaly Run The App 

```bash
(AnacondaPrompt) $ python -u O_TCM.py
```
### Run The App With Command Line Arguments (These Are Real Players)
```bash
python -u O_TCM.py Kanor#1507 lhcloudy#2273 KSAA#21785 Kitty#23844
```
## Go To [overbuff.com](overbuff.com/players/pc) For Players Stats And Battle Tags.

# :>> Enjoy.
