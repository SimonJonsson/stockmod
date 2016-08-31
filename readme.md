Git instruktioner

-----
Första gången
-----
0) Öppna terminal i mapp du vill ha projektet i
1) git config --global user.name "SimonJonsson"
2) git config --global user.email "simonjonsson3@hotmail.com"
3) git clone https://gralo184@github.com/SimonJonsson/stockmod
4) cd stockmod

----
Varje gång man ändrar saker 
-----
5) Ändra saker
6) git status - se vilka filer som ändrats
7) git diff - se kod som ändrats
8) (låt säga man ändrat readme.md och main.cpp)
git add readme.md main.cpp (var försiktig med git add ., lägger till allt)
9) git status (visar grönt på filer man lagt till)
10) git commit -m "vad har jag gjort"
11) git pull (updatera innan du pushar ändringar)
12) git push (mata in lösenord till github konto)


git rm fil.namn (tar bort fil)
git mv fil.namn mappnamn (flyttar fil)
dessa ändringar måste även committas


q för att komma ut
