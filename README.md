# Kino jako system mikroserwisów

**Autorzy:** Michał Kobiera, Szymon Ożóg, Aleksandra Poskróbek, Wiktor Satora  
**Rok:** 2025  
**Grupa:** gr.4


## 1. Wprowadzenie

Celem naszego projektu jest stworzenie mikroserwisowej aplikacji dla kina, umożliwiającej użytkownikom:

- przegląd repertuaru,
- rezerwację biletów,
- zarządzanie salami i pokazami przez pracowników kina.

Aplikacja zostanie zrealizowana w architekturze mikroserwisowej w celu zapewnienia:

- skalowalności,
- rozdzielenia odpowiedzialności,
- możliwości łatwego rozszerzania systemu.

Kluczowym aspektem projektu jest implementacja efektywnego systemu monitoringu i logowania opartego na technologii **Fluent Bit**, która będzie zbierać, przetwarzać i przesyłać logi z poszczególnych mikroserwisów. Fluent Bit to lekki i wydajny agent przetwarzający logi, który będzie pełnił kluczową rolę w naszym systemie monitoringu. Jego zadaniem będzie:

1. **Kolekcja logów** - zbieranie danych logowych z wszystkich mikroserwisów (UserService, MovieService, BookingService itd.)
2. **Filtrowanie i przetwarzanie** - parsowanie i wzbogacanie danych logowych
3. **Agregacja** - grupowanie i buforowanie logów przed wysłaniem
4. **Przekierowanie** - wysyłka przetworzonych logów do systemu Loki

Dane będą przepływać przez następujący pipeline monitoringu:
`Fluent Bit → Loki → Grafana`

Gdzie:
- **Loki** będzie służyć jako skalowalne repozytorium logów
- **Grafana** zapewni wizualizację danych i tworzenie dashboardów monitorujących działanie systemu

Taka architektura monitoringu pozwoli nam na:
- Centralne zarządzanie logami z wszystkich mikroserwisów
- Szybkie wykrywanie i diagnozowanie problemów
- Monitorowanie wydajności poszczególnych komponentów systemu
- Tworzenie niestandardowych wizualizacji i alertów


## 2. Teoretyczne tło / Stos technologiczny

Nasza architektura mikroserwisowa będzie oparta o następujące komponenty i technologie:

- **Język programowania:** Python + Flask (REST API)
- **Baza danych:** Mockowane dane / JSON
- **Komunikacja między serwisami:** REST (HTTP)
- **Monitoring i logowanie:** Fluent Bit + Loki + Grafana
- **Zarządzanie kontenerami:** Docker + Docker Compose

### Przykładowe mikroserwisy:

- **UserService** – zarządza kontami użytkowników
- **MovieService** – zarządza repertuarem filmowym
- **BookingService** – obsługuje rezerwacje biletów
- **ScreeningService** – planuje seanse w salach kinowych
- **NotificationService** – wysyła powiadomienia e-mail/SMS


## 3. Opis koncepcji studium przypadku

### Założenia systemu:

- Pracownik kina dodaje film i planuje seanse (dzień, godzina, sala).
- Użytkownik rejestruje się, loguje, przegląda dostępne seanse.
- Rezerwacja biletu blokuje miejsce na określony czas.
- Po potwierdzeniu rezerwacji zostaje wygenerowany bilet.
- Powiadomienia e-mail potwierdzają zakup biletu.


## 4. Architektura rozwiązania

![Opis obrazka](./cinema_microservices.png)


![Opis obrazka](./diagram_fluent-bit.png)


## 5. Opis konfiguracji środowiska

### Struktura katalogów
<pre> 
├── docker-compose.yml
├── fluentbit/
│   └── conf/
│       ├── fluent-bit.conf
│       └── parsers.conf
├── user_service/
│   └── user_service.py
├── movie_service/
│   └── ...
...
</pre>

### Dostępne porty
| Usługa                | Adres URL              |
|------------------------|------------------------|
| `user_service`         | http://localhost:5001 |
| `movie_service`        | http://localhost:5002 |
| `booking_service`      | http://localhost:5003 |
| `screening_service`    | http://localhost:5004 |
| `notification_service` | http://localhost:5005 |
| `Grafana`              | http://localhost:3000 |
| `Loki`                 | http://localhost:3100 |

### Logowanie i monitoring
- **Fluent Bit** monitoruje pliki logów kontenerów i przekazuje je dalej w czasie rzeczywistym z `/var/lib/docker/containers` i przesyła je do Loki
- **Loki** zbiera logi i udostępnia je Grafanie
- **Grafana** pozwala filtrować logi na podstawie etykiet (`container_name`, `job=fluentbit`, itp.)

## 6. Instalacja

Do poprawnego uruchomienia środowiska wymagane są:

### Wymagania systemowe:
- Docker (https://www.docker.com/)

- Docker Compose (https://docs.docker.com/compose/)

### Kroki instalacyjne:
1. Klonowanie repozytorium:

```bash
git clone https://github.com/SzymixOz/suu.git
cd suu
```

2. Przygotowanie dodatkowych dashboardów:
Umieść pliki .json dashboardów w folderze:

```bash
./grafana/dashboards/
```

## 7. Reprodukcja – krok po kroku

1. Budowa i uruchomienie kontenerów:
W katalogu głównym projektu uruchom:

```bash
docker-compose up --build
```

2. Dostęp do usług zgodnie z portami podanymi w punkcie 5.

## 8. Demo

### Konfiguracja, przygotowanie danych i uruchomienie
Tak jak w punkcie 6 i 7. Dashboardy do Grafany ładowane są z pliku, a ruch generowany jest automatycznie przez jeden z mikroserwisów. Do grafany można się zalogować wpisując login i hasło `admin`, a następnie klikając w przycisk 'skip'.

### Prezentacja wyników

![Opis obrazka](./pictures/1.png)
![Opis obrazka](./pictures/2.png)
![Opis obrazka](./pictures/3.png)
![Opis obrazka](./pictures/4.png)
![Opis obrazka](./pictures/5.png)
![Opis obrazka](./pictures/6.png)

## 9. Zastosowanie AI w projekcie

W projekcie wykorzystywaliśmy modele językowe do szybszego wyszukiwania informacji oraz wyszukiwania ewentualnych błędów w plikach konfiguracyjnych.

## 10. Podsumowanie - wnioski

Kluczowym celem naszego projektu było zaprojektowanie i wdrożenie wydajnego systemu monitoringu i logowania przy pomocy Fluent Bit.

Na podstawie doświadczeń z implementacją wyciągnęliśmy następujące wnioski:

1. Fluent Bit jest lekki, szybki i niezwykle efektywny jako narzędzie do zbierania i przetwarzania logów w środowisku opartym na kontenerach Docker. Jego niskie zużycie zasobów sprawdziło się szczególnie dobrze w naszym wieloserwisowym środowisku.

2. Konfiguracja Fluent Bit okazała się elastyczna, ale wymagała dokładnego zrozumienia plików konfiguracyjnych

3. Integracja z Loki przebiegła sprawnie, dzięki natywnemu wsparciu Fluent Bit dla tego backendu. Wysyłane logi były wzbogacane o dodatkowe metadane (etykiety), co umożliwiło ich dokładną analizę i filtrowanie w Grafanie.

4. Dzięki zastosowaniu centralnego systemu logowania z Fluent Bitem:
    - Udało się uniknąć ręcznego przeglądania logów w poszczególnych kontenerach.
    - Możliwe było tworzenie dashboardów i alertów w Grafanie bez potrzeby modyfikowania każdego mikroserwisu osobno.

5. Największym wyzwaniem okazało się skonfiguraowanie przesyłania logów między mikroserwisami a Loki/FluentBit.

Podsumowując, Fluent Bit spełnił swoją rolę jako lekki i potężny agent logujący, a jego zastosowanie znacznie zwiększyło możliwości kontrolne i diagnostyczne naszego systemu.

## 11. Źródła/Referencje
- https://docs.docker.com/
- https://docs.fluentbit.io/manual
- https://pomoc.small.pl/Flask/
- https://medium.com/@svss1995/centralized-logging-in-microservices-using-grafana-stack-and-fluent-bit-a77a650a3ad6
- https://grafana.com/docs/grafana/latest/


