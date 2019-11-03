# football-score-checker
A code where you can enter a list of team names that you wish to follow and it will print out the live score of those teams if they are playing and what minute the match is in.

This code requires an install of BeautifulSoup, for those unfamiliar this can be accomplished by (if you're using the anaconda distribution) opening Anaconda Prompt and typing the following command:

```
pip install bs4
```

Then press enter and then the code should be able to be run. This code works by webscraping BBC sport scores and fixtures page for match data, for all teams playing today then displaying the data for the relevant teams that you have passed the main function. If you want to display all premier league matches for the day call it like this:

```
matches,matchtimes = main('Prem')
for i in range(0,len(matches)):
    print(matches[i])
    print(matchtimes[i])
```

Also note that the premier league teams list inside the main function will need manually updating yearly with the relegated and newly promoted teams. Otherwise just pass a list of team names (still use list notation even if it's one team) that you want to get the match data of exactly as they are listed on the BBC Sports and Fixtures webpage, that would be called like this:

```
matches,matchtimes = main(['Leicester City','Manchester United'])
for i in range(0,len(matches)):
    print(matches[i])
    print(matchtimes[i])
```

The matches and matchtimes data is returned so you can display it as you like, an example output would be the following:

Charlton Athletic 0 - 0 Preston North End

43 mins

If a game has not kicked off yet the score and matchtimes are currently presented as N/A, this means that theya re playing today (unless game has been postponed) but the game has not started yet, this could potentially be modified to find kick off times if you desire. If you want to continuously live update the score just loop calling the main function but add a delay using a time.sleep() for example as calling an update request too frequently might cause BBC sport to reject the request. If the passed teans are not playing today the code will return two empty lists.
