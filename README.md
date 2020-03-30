# NineHorses

### Tworzenie Issues
Jeśli chcesz dodać zadanie lub buga, utwórz nowy Issue z nastęnym numerem:  
- dla interfejsu graficznego `G-1` (G-2 itd.)  
- dla logiki `L-1` (L-2 itd.)  

Następnie utwórz nowy branch dla tego problemu (jako branch wyjściowy przyjmij branch **gui** albo **logic**, nazwa powiązana z Issue np. `G-1` mile widziana).
Po zakończeniu prac zmień Issue na PR.  

### Pomoc w używaniu Issues i Pull Request
[github/hub](https://github.com/github/hub) - oficjalne rozszerzenie do konsoli wspierające wiele funkcji GitHuba.

Po instalacji można używać w konsoli polecenia `hub` zamiast `git`

Jeśli **ukończyliście** pracę nad problemem i chcecie zrobić merge request, zróbcie z poziomu konsoli:

        hub pull-request -i <GitHubowy numer Issue> -b gui

gdzie ten GitHubowy numer Issue, to numer z kratką znajdujący się za nazwą issue np #1

W ten sposób Issue zostanie zamieniony na Pull Request, z całą historią dyskusji itp.
