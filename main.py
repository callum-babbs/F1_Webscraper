# Callum Babbs
# F1 Website Scraper

import requests
import pandas as pd
import openpyxl
from bs4 import BeautifulSoup

# ------------ BLOCK FOR 2022 RACE RESULTS (team standings) ------------

raceResults = pd.DataFrame(columns=['Grand Prix', 'Date', 'Winner FName', 'Winner LName', 'Winner Abbrev.',
                                    'Car', 'Laps', 'Time'])

results = requests.get('https://www.formula1.com/en/results.html/2022/races.html')

# print(results.url)
# debugging

# print(results.status_code)
# debugging - this should print "200" (OK success status) if request was successful

soup1 = BeautifulSoup(results.content, 'html.parser')
# BeautifulSoup object and specified parser to use

# print(soup.prettify())
# debugging, should print out the html code of the webpage (prettify indents it correctly for html)

results1 = soup1.find('tbody')

results2 = results1.find_all('tr')

for resultsOut in results2:
    print(resultsOut.text)
    temp = resultsOut.text
    temp = temp.split('\n')
    temp = [x.strip(' ') for x in temp]
    temp = list(filter(None, temp))
    raceResults.loc[len(raceResults)] = temp

raceResults.to_excel("RaceResults.xlsx", index=False)


# ------------ BLOCK FOR DRIVER INFORMATION ------------

driverInformation = pd.DataFrame(columns=['Name', 'Team', 'Country', 'Podiums', 'Points',
                                   'Grand Prix Entered', 'World Championships', 'Highest Race Finish',
                                   'Highest Grid Position', 'Date of Birth', 'Place of Birth'])

preDrivers = requests.get('https://www.formula1.com/en/drivers.html')

soup2 = BeautifulSoup(preDrivers.content, 'html.parser')

driversLinks = []

for element in soup2.find_all(attrs={'class': 'listing-item--link'}):
    link = element.get('href')
    driversLinks.append(link)

rootURL = "https://www.formula1.com"

driverIndex = 0

for x in driversLinks:
    drivers = requests.get(rootURL + driversLinks[driverIndex])
    soupX = BeautifulSoup(drivers.content, 'html.parser')
    driverName = soupX.find(attrs={'class': 'driver-name'})
    print(driverName.text)
    driverInfo = soupX.find(attrs={'class': 'stat-list'})
    print(driverInfo.text)
    driverIndex += 1

    temp = (driverName.text + driverInfo.text)

    temp = temp.split('\n')
    temp = [x.strip(' ') for x in temp]
    temp = list(filter(None, temp))
    temp.remove('Team')
    temp.remove('Country')
    temp.remove('Podiums')
    temp.remove('Points')
    temp.remove('Grands Prix entered')
    temp.remove('World Championships')
    temp.remove('Highest race finish')
    temp.remove('Highest grid position')
    temp.remove('Date of birth')
    temp.remove('Place of birth')
    driverInformation.loc[len(driverInformation)] = temp

    driverInformation.to_excel('DriverInformation.xlsx', index=False)


# ------------ BLOCK FOR TEAM INFORMATION ------------

teamInformation = pd.DataFrame(columns=['Full Team Name', 'Base', 'Team Chief', 'Technical Chief', 'Chassis',
                                        'Power Unit', 'First Team Entry', 'World Championships', 'Highest Race Finish',
                                        'Pole Positions', 'Fastest Laps'])

preTeams = requests.get('https://www.formula1.com/en/teams.html')

soup3 = BeautifulSoup(preTeams.content, 'html.parser')

teamLinks = []

for element1 in soup3.find_all(attrs={'class': 'listing-link'}):
    link1 = element1.get('href')
    teamLinks.append(link1)

teamIndex = 0

for y in teamLinks:
    teams = requests.get(rootURL + teamLinks[teamIndex])
    soupY = BeautifulSoup(teams.content, 'html.parser')
    teamStats = soupY.find(attrs={'class': 'stat-list'})
    print(teamStats.text)
    teamIndex += 1

    temp = teamStats.text
    temp = temp.split('\n')
    temp = [x.strip(' ') for x in temp]
    temp = list(filter(None, temp))
    temp.remove('Full Team Name')
    temp.remove('Base')
    temp.remove('Team Chief')
    temp.remove('Chassis')
    temp.remove('Power Unit')
    temp.remove('First Team Entry')
    temp.remove('World Championships')
    temp.remove('Highest Race Finish')
    temp.remove('Pole Positions')
    temp.remove('Fastest Laps')
    temp.remove('Technical Chief')
    teamInformation.loc[len(teamInformation)] = temp

    teamInformation.to_excel('TeamInformation.xlsx', index=False)


# ------------ BLOCK FOR PRACTICE, QUALIFIER, RACE INFORMATION ------------

raceLinks = []
raceNames = []

for raceLink in soup1.find_all(attrs={'class': 'dark bold ArchiveLink'}):
    link2 = raceLink.get('href')
    name = raceLink.text
    name = name.strip(' \n')
    link2 = rootURL + link2
    raceLinks.append(link2)
    raceNames.append(name)

raceIndex = 0
separator = '\n'

for x in raceLinks:
    raceResultInformation = pd.DataFrame(columns=['Position', 'No.', 'Driver FName', 'Driver LName', 'Driver Abbrev.',
                                                  'Car', 'Laps', 'Time/retired', 'Points'])

    raceResultInfo = requests.get(raceLinks[raceIndex])
    soupA = BeautifulSoup(raceResultInfo.content, 'html.parser')
    raceTitle = soupA.find(attrs={'class': 'ResultsArchiveTitle'}).text
    raceTitle = raceTitle.strip()
    raceTitle = raceTitle.split(separator, 1)[0]
    print(raceTitle)

    raceDate = soupA.find(attrs={'class': 'full-date'}).text
    print(raceDate)

    circuit = soupA.find(attrs={'class': 'circuit-info'}).text
    print(circuit)

    raceFinal = soupA.find(attrs={'class': 'resultsarchive-table'}).text

    temp1 = ['', '', '', '', '', '', '', '', '']
    temp2 = ['Race Title', 'Race Date', 'Circuit', '', '', '', '', '', '']
    temp3 = [raceTitle, raceDate, circuit, '', '', '', '', '', '']

    raceFinal = raceFinal.split(separator)
    raceFinal = [x.strip(' ') for x in raceFinal]
    raceFinal = list(filter(None, raceFinal))
    raceFinal.remove('Pos')
    raceFinal.remove('No')
    raceFinal.remove('Driver')
    raceFinal.remove('Car')
    raceFinal.remove('Laps')
    raceFinal.remove('Time/Retired')
    raceFinal.remove('PTS')

    iterator = 0
    for i in raceFinal:
        temp = raceFinal[iterator:iterator+9]
        if len(temp) == 0:
            break
        raceResultInformation.loc[len(raceResultInformation)] = temp
        iterator += 9

    raceResultInformation.loc[len(raceResultInformation)] = temp1
    raceResultInformation.loc[len(raceResultInformation)] = temp2
    raceResultInformation.loc[len(raceResultInformation)] = temp3
    raceResultInformation.to_excel(raceNames[raceIndex] + '.xlsx', index=False)

    raceIndex += 1
