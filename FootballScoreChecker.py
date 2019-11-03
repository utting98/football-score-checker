import requests
from bs4 import BeautifulSoup
from datetime import date

def main():
    datetoday = date.today() #get current date to add to url
    url = 'https://www.bbc.co.uk/sport/football/scores-fixtures/'+str(datetoday) #specify url of page for today
    result = requests.get(url) #get access to the page via python
    soup = BeautifulSoup(result.content, "lxml") #store the page html as a variable that we are going to look at the tags of with BeautifulSoup
    #look for all of the spans with the attribute class defined by the long tag the home team name is stored under
    teams = soup.find_all("span",attrs={'class':"gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc"}) 
    finishedhomescores = soup.find_all("span",attrs={'class':"sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft"})
    livehomescores = soup.find_all("span",attrs={'class':"sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--live"})
    finishedawayscores = soup.find_all("span",attrs={'class':"sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--ft"})
    liveawayscores = soup.find_all("span",attrs={'class':"sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--live"})
    matchstatus = soup.find_all("span",attrs={'class':"sp-c-fixture__status-wrapper"})
    homenames = [] #define empty list to fill with the actual names, before we just had tag info
    awaynames = []
    homescores = []
    awayscores = []
    #this will need updating yearly, can replace this list with any teams you are interested in following and will only get scores for those teams
    premteamslist = ['Arsenal','AFC Bournemouth','Aston Villa','Brighton & Hove Albion','Burnley','Chelsea','Crystal Palace','Everton','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle United','Norwich City','Sheffield United','Southampton','Tottenham Hotspur','Watford','West Ham United','Wolverhampton Wanderers']
    premhomescores = []
    premawayscores = []
    matchtimes = []
    premmatchtimes = []
    finishediterator = 0
    liveiterator=0
    
    for j in range(0,len(matchstatus)):
        if(matchstatus[j].text=='FT'): #if full time append full time score
            homescores.append(finishedhomescores[finishediterator].text)    
            awayscores.append(finishedawayscores[finishediterator].text)
            matchtimes.append(matchstatus[j].text)
            finishediterator+=1 #increase finished iterator so it only goes up when a finished score is appended
        elif(('mins' in matchstatus[j].text) or (matchstatus[j].text=='HT') or ('+' in matchstatus[j].text)): #if it says a minute count game is live so append live score
            homescores.append(livehomescores[liveiterator].text)    
            awayscores.append(liveawayscores[liveiterator].text)
            matchtimes.append(matchstatus[j].text)
            liveiterator+=1 #as with the finished iterator
        else: #if it is blank a game today hasn't kicked off yet so flag for deletion (can remove this to still display something else but score may have issues)
            homescores.append('N/A') #An easy to spot flag, means game postponed or not kicked off yet
            awayscores.append('N/A')
            matchtimes.append('N/A') #Flag game time not running yet as not kicked off
    
    premflag = [0]*len(matchstatus) #list of flags to note if prem game
    
    for i in range(0,len(teams),2): #loop over to do all of the found teams in incremenets of two to stop duplicates
        
        if(i>0): #also loop an iterator increasing by 1
            j=int(i/2)
        else:
            j=0
        
        for k in range(0,len(premteamslist)): #loop over premteamsllist
            if(teams[i].text==premteamslist[k]): #if teams is in premteamslist
                if((teams[i].text in homenames) or (teams[i].text in awaynames)): #and name not already listed (this is to stop duplicates e.g. getting women's teams when you wanted mens etc. or vice versa)
                    pass
                else:
                    homenames.append(teams[i].text) #append the text inside the tag for home teams, e.g. AFC Bournemouth 
                    awaynames.append(teams[i+1].text)
                    premmatchtimes.append(matchtimes[j])
                    premflag[j]=1 #flag as prem team
            else:
                pass
        l = i+1 #also check odd indexes for away teams
        for k in range(0,len(premteamslist)): #loop over the same way
            if(teams[l].text==premteamslist[k]): #if the away team is in premteamslist
                if((teams[l].text in homenames) or (teams[l].text in awaynames)): #and game isn't already found from home teams list
                    pass
                else:
                    #not the indexes are swapped because here we've gone past the home to find the away so previous index is the home team
                    homenames.append(teams[l-1].text) #append the text inside the tag for home teams, e.g. AFC Bournemouth 
                    awaynames.append(teams[l].text)
                    premmatchtimes.append(matchtimes[j])
                    premflag[j]=1 #flag as prem team
            else:
                pass
    
    for i in range(0,len(homescores)): #loop over all appended homescores (now a full list with just 'Del' if postponed or cancelled)
        if(premflag[i]==1): #if game was prem
            premhomescores.append(homescores[i]) #append the scores
            premawayscores.append(awayscores[i])
    
    gamestrings = [] #empty gamestring list
    for i in range(0,len(homenames)): #loop over and define score string for game then display them
        gamestrings.append(homenames[i]+' '+premhomescores[i] + ' - ' + premawayscores[i] + ' ' + awaynames[i])
        print(gamestrings[i])
        print(premmatchtimes[i])
    
    return

if __name__=='__main__':
    main()


