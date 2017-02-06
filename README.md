# Apikacja na platformę Raspberry Pi

**Aplikacja mobilna na platformę iOS do obsługi systemu inteligentnego domu zbudowanego na platformie Raspberry Pi**
**(ang. Smart home mobile application for iOS based devices, with support for Raspberry Pi devices)**

**Politechnika Krakowska im. Tadeusza Kościuszki**
**Wydział Inżynierii Elektrycznej i Komputerowej Politechniki Krakowskiej**

Wykonał: **Piotr Pawluś**

Promotor: **Dr Damian Grela**

Projekt wykonany przez w ramach pracy inżynieryjskiej.

* **Główne założenia**:
  - Podział użytkowników na administrację systemu oraz na użytkoników.
  - Możliwość samodzielnej rejestracji użytkownika w systemie.
  - Akceptacja rejestracji nowych użytkowników przez administratora systemu.
  - Autentykacja użytkownika w aplikacji.
  - Możliwość dodowania przez administratora systemu dwóch typów urządzeń (zasada działania przełącznika i zazada działania przycisku).
  - Możliwość usuwania urządzeń przez administratora.
  - Możliwość zmiany stanu urządzeń przez oba typy użytkowników.
  - Możliwość otrzymania listy wszystkich urządzeń dla obu typów użytkowników.
  - Możliwość otrzymania listy wszystkich użytkowników przez administratora systemu.
  - Możliwość nadawania praw do autentykacji w systemie oraz praw administracyjnych przez administratora systemu.

* **Wykorzystane narzędzia**:
  - Urządzenie fizyczne - Raspberry Pi wersja 3B
  - Język programowania - Python 2.7
  - System relacyjnej bazy danych - PostgreSQL
  - Biblioteka do tworzenia serwera REST - Flask
  - System - Raspbian GNU/Linux 8.0 (jessie)
  - Dodatkowe biblioteki - flask, flask_sqlalchemy, flask-restful, flask-httpauth, GPIO, time

Cześć [mobilna na platformę iOS](https://github.com/PiotrPawlus/PiHome_iOS)
