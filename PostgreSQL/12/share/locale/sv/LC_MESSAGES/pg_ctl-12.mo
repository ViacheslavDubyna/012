��    �        �   �	      H      I     j  &   |     �     �  3   �          ,  /   ?     o  "   �  1   �  �   �  "   �  j   �  o        ~  D   �  !   �  3     ?   7  H   w  D   �  C     E   I  ?   �  ?   �  >     9   N  L   �  B   �  E     �   ^  0   �  F     >   [  B   �  I   �  %   '  <   M  O   �  7   �               "  M   4  -   �  !   �  >   �  E     C   W  y   �  9     D   O  C   �  D   �  E     >   c  A   �  '   �  (     ,   5  7   b  2   �  6   �  >     *   C  /   n  7   �  4   �  %     1   1  0   c  #   �     �  4   �  7     2   C  6   v  1   �  0   �  ,     .   =  3   l  7   �     �  +   �  1   $   6   V   6   �   1   �   *   �   "   !!  7   D!  "   |!  $   �!  J   �!     "     +"  3   B"  0   v"     �"  #   �"  !   �"      #  !   #  $   A#      f#  -   �#     �#  4   �#  %   
$  $   0$  "   U$  !   x$  u   �$  F   %     W%  7   k%  )   �%  k   �%  `   9&  %   �&  &   �&     �&  d   �&     T'  /   s'  &   �'  0   �'  .   �'  -   *(     X(     o(  &   �(      �(  ,   �(  (   �(     )  %   :)     `)     t)     �)     �)     �)     �)     �)     �)  #   �)     *     !*     2*     B*     Z*      y*  "   �*     �*  ?  �*  ,   ,     I,  /   _,  #   �,  #   �,  8   �,     -     *-  /   >-     n-  "   �-  0   �-  �   �-  "   �.  l   �.  p   /     �/  F   �/  !   �/  ?   0  <   K0  F   �0  O   �0  M   1  R   m1  A   �1  C   2  ?   F2  :   �2  T   �2  K   3  J   b3  �   �3  J   J4  I   �4  L   �4  I   ,5  D   v5  (   �5  N   �5  S   36  5   �6     �6     �6     �6  Z   �6  0   B7     s7  <   �7  B   �7  D   8  ~   W8  C   �8  C   9  C   ^9  E   �9  A   �9  S   *:  E   ~:  %   �:  ,   �:  (   ;  5   @;  3   v;  @   �;  ?   �;  7   +<  '   c<  <   �<  4   �<  '   �<  0   %=  1   V=  )   �=      �=  5   �=  7   	>  5   A>  @   w>  7   �>  7   �>  /   (?  2   X?  9   �?  <   �?  "   @  *   %@  1   P@  7   �@  6   �@  4   �@  ,   &A  "   SA  ;   vA      �A  *   �A  N   �A     MB     jB  7   �B  :   �B     �B  #   C      ,C     MC     lC  )   �C  (   �C  )   �C     D  8   "D      [D  "   |D     �D     �D  p   �D  I   NE     �E  E   �E  .   �E  h   F  e   �F  ,   �F  /   G     HG  �   VG     �G  -   �G      #H  -   DH  )   rH  )   �H     �H     �H  %   �H  "    I  3   CI  *   wI     �I  '   �I     �I     �I     
J     J     2J     EJ     XJ     nJ  *   �J     �J     �J     �J     �J  !    K  *   "K  ,   MK  '   zK             3           M   �   >           N          !   �   :   i   9          �       l       E       =   *       C      g      s   {      &      �   �   [       �      B             7   �   �   ?   y           �       -           
      J   4   D       h       o   6   w   �   _   b          8       ~                  @   O   I   |   �   Y      <   c   "       �   �   �   ^   �   X   p   z           f   )   x   A   V   P       .       ;   $          S      �                    �   �       a   0       r         	   d   �   �       #           �       1   \   �   n               q      G      �   +   (   k   ,   m   e   �       K   �   5   F       t       U   2   �   Q   �          %   H         W   }      j   ]                  T   �   �   /   Z       `       �   �       L   '      R   u      v        
Allowed signal names for kill:
 
Common options:
 
Options for register and unregister:
 
Options for start or restart:
 
Options for stop or restart:
 
Report bugs to <pgsql-bugs@lists.postgresql.org>.
 
Shutdown modes are:
 
Start types are:
   %s init[db]   [-D DATADIR] [-s] [-o OPTIONS]
   %s kill       SIGNALNAME PID
   %s logrotate  [-D DATADIR] [-s]
   %s promote    [-D DATADIR] [-W] [-t SECS] [-s]
   %s register   [-D DATADIR] [-N SERVICENAME] [-U USERNAME] [-P PASSWORD]
                    [-S START-TYPE] [-e SOURCE] [-W] [-t SECS] [-s] [-o OPTIONS]
   %s reload     [-D DATADIR] [-s]
   %s restart    [-D DATADIR] [-m SHUTDOWN-MODE] [-W] [-t SECS] [-s]
                    [-o OPTIONS] [-c]
   %s start      [-D DATADIR] [-l FILENAME] [-W] [-t SECS] [-s]
                    [-o OPTIONS] [-p PATH] [-c]
   %s status     [-D DATADIR]
   %s stop       [-D DATADIR] [-m SHUTDOWN-MODE] [-W] [-t SECS] [-s]
   %s unregister [-N SERVICENAME]
   -?, --help             show this help, then exit
   -D, --pgdata=DATADIR   location of the database storage area
   -N SERVICENAME  service name with which to register PostgreSQL server
   -P PASSWORD     password of account to register PostgreSQL server
   -S START-TYPE   service start type to register PostgreSQL server
   -U USERNAME     user name of account to register PostgreSQL server
   -V, --version          output version information, then exit
   -W, --no-wait          do not wait until operation completes
   -c, --core-files       allow postgres to produce core files
   -c, --core-files       not applicable on this platform
   -e SOURCE              event source for logging when running as a service
   -l, --log=FILENAME     write (or append) server log to FILENAME
   -m, --mode=MODE        MODE can be "smart", "fast", or "immediate"
   -o, --options=OPTIONS  command line options to pass to postgres
                         (PostgreSQL server executable) or initdb
   -p PATH-TO-POSTGRES    normally not necessary
   -s, --silent           only print errors, no informational messages
   -t, --timeout=SECS     seconds to wait when using -w option
   -w, --wait             wait until operation completes (default)
   auto       start service automatically during system startup (default)
   demand     start service on demand
   fast        quit directly, with proper shutdown (default)
   immediate   quit without complete shutdown; will lead to recovery on restart
   smart       quit after all clients have disconnected
  done
  failed
  stopped waiting
 %s is a utility to initialize, start, stop, or control a PostgreSQL server.

 %s: -S option not supported on this platform
 %s: PID file "%s" does not exist
 %s: WARNING: cannot create restricted tokens on this platform
 %s: WARNING: could not locate all job object functions in system API
 %s: another server might be running; trying to start server anyway
 %s: cannot be run as root
Please log in (using, e.g., "su") as the (unprivileged) user that will
own the server process.
 %s: cannot promote server; server is not in standby mode
 %s: cannot promote server; single-user server is running (PID: %ld)
 %s: cannot reload server; single-user server is running (PID: %ld)
 %s: cannot restart server; single-user server is running (PID: %ld)
 %s: cannot rotate log file; single-user server is running (PID: %ld)
 %s: cannot set core file size limit; disallowed by hard limit
 %s: cannot stop server; single-user server is running (PID: %ld)
 %s: control file appears to be corrupt
 %s: could not access directory "%s": %s
 %s: could not allocate SIDs: error code %lu
 %s: could not create log rotation signal file "%s": %s
 %s: could not create promote signal file "%s": %s
 %s: could not create restricted token: error code %lu
 %s: could not determine the data directory using command "%s"
 %s: could not find own program executable
 %s: could not find postgres program executable
 %s: could not get LUIDs for privileges: error code %lu
 %s: could not get token information: error code %lu
 %s: could not open PID file "%s": %s
 %s: could not open process token: error code %lu
 %s: could not open service "%s": error code %lu
 %s: could not open service manager
 %s: could not read file "%s"
 %s: could not register service "%s": error code %lu
 %s: could not remove log rotation signal file "%s": %s
 %s: could not remove promote signal file "%s": %s
 %s: could not send log rotation signal (PID: %ld): %s
 %s: could not send promote signal (PID: %ld): %s
 %s: could not send reload signal (PID: %ld): %s
 %s: could not send signal %d (PID: %ld): %s
 %s: could not send stop signal (PID: %ld): %s
 %s: could not start server
Examine the log output.
 %s: could not start server due to setsid() failure: %s
 %s: could not start server: %s
 %s: could not start server: error code %lu
 %s: could not start service "%s": error code %lu
 %s: could not unregister service "%s": error code %lu
 %s: could not write log rotation signal file "%s": %s
 %s: could not write promote signal file "%s": %s
 %s: database system initialization failed
 %s: directory "%s" does not exist
 %s: directory "%s" is not a database cluster directory
 %s: invalid data in PID file "%s"
 %s: missing arguments for kill mode
 %s: no database directory specified and environment variable PGDATA unset
 %s: no operation specified
 %s: no server running
 %s: old server process (PID: %ld) seems to be gone
 %s: option file "%s" must have exactly one line
 %s: out of memory
 %s: server did not promote in time
 %s: server did not start in time
 %s: server does not shut down
 %s: server is running (PID: %ld)
 %s: service "%s" already registered
 %s: service "%s" not registered
 %s: single-user server is running (PID: %ld)
 %s: the PID file "%s" is empty
 %s: too many command-line arguments (first is "%s")
 %s: unrecognized operation mode "%s"
 %s: unrecognized shutdown mode "%s"
 %s: unrecognized signal name "%s"
 %s: unrecognized start type "%s"
 HINT: The "-m fast" option immediately disconnects sessions rather than
waiting for session-initiated disconnection.
 If the -D option is omitted, the environment variable PGDATA is used.
 Is server running?
 Please terminate the single-user server and try again.
 Server started and accepting connections
 The program "%s" is needed by %s but was not found in the
same directory as "%s".
Check your installation.
 The program "%s" was found by "%s"
but was not the same version as %s.
Check your installation.
 Timed out waiting for server startup
 Try "%s --help" for more information.
 Usage:
 WARNING: online backup mode is active
Shutdown will not complete until pg_stop_backup() is called.

 Waiting for server startup...
 cannot duplicate null pointer (internal error)
 child process exited with exit code %d child process exited with unrecognized status %d child process was terminated by exception 0x%X child process was terminated by signal %d: %s command not executable command not found could not change directory to "%s": %m could not find a "%s" to execute could not get current working directory: %s
 could not identify current directory: %m could not read binary "%s" could not read symbolic link "%s": %m invalid binary "%s" out of memory out of memory
 pclose failed: %m server promoted
 server promoting
 server shutting down
 server signaled
 server signaled to rotate log file
 server started
 server starting
 server stopped
 starting server anyway
 trying to start server anyway
 waiting for server to promote... waiting for server to shut down... waiting for server to start... Project-Id-Version: PostgreSQL 12
Report-Msgid-Bugs-To: pgsql-bugs@lists.postgresql.org
PO-Revision-Date: 2019-04-29 13:37+0200
Last-Translator: Dennis Björklund <db@zigo.dhs.org>
Language-Team: Swedish <sv@li.org>
Language: sv
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
 
Tillåtna signalnamn för kommando "kill":
 
Gemensamma flaggor:
 
Flaggor för registrering och avregistrering:
 
Flaggor för start eller omstart:
 
Flaggor för stopp eller omstart:
 
Rapportera fel till <pgsql-bugs@lists.postgresql.org>.
 
Stängningsmetoder är:
 
Startmetoder är:
   %s init[db]   [-D DATAKAT] [-s] [-o FLAGGOR]
   %s kill       SIGNALNAMN PID
   %s logrotate  [-D DATAKAT] [-s]
   %s promote    [-D DATAKAT] [-W] [-t SEK] [-s]
   %s register   [-D DATAKAT] [-N TJÄNSTENAMN] [-U ANVÄNDARNAMN] [-P LÖSENORD]
                    [-S STARTTYPE] [-e KÄLLA] [-W] [-t SEK] [-s] [-o FLAGGOR]
   %s reload     [-D DATAKAT] [-s]
   %s restart    [-D DATAKAT] [-m STÄNGNINGSMETOD] [-W] [-t SEK] [-s]
                    [-o FLAGGOR] [-c]
   %s start      [-D DATAKAT] [-l FILNAMN] [-W] [-t SEK] [-s]
                    [-o FLAGGOR] [-p SOKVÄG] [-c]
   %s status     [-D DATAKAT]
   %s stop       [-D DATAKAT] [-m STÄNGNINGSMETOD] [-W] [-t SEK] [-s]
   %s unregister [-N TJÄNSTNAMN]
   -?, --help             visa den här hjälpen, avsluta sedan
   -D, --pgdata=DATAKAT   plats för databasens lagringsarea
   -N TJÄNSTENAMN  tjänstenamn att registrera PostgreSQL-servern med
   -P LÖSENORD     lösenord för konto vid registrering av PostgreSQL-servern
   -S STARTSÄTT    sätt att registrera PostgreSQL-servern vid tjänstestart
   -U NAMN         användarnamn för konto vid registrering av PostgreSQL-servern
   -V, --version          visa versionsinformation, avsluta sedan
   -W, --no-wait          vänta inte på att operationen slutförs
   -c, --core-files       tillåt postgres att skapa core-filer
   -c, --core-files       inte giltig för denna plattform
   -e KÄLLA               händelsekälla för loggning när vi kör som en tjänst
   -l, --log=FILNAMN      skriv, eller tillfoga, server-loggen till FILNAMN
   -m, --mode=METOD       METOD kan vara "smart", "fast" eller "immediate"
   -o, --options=OPTIONS  kommandoradsflaggor som skickas vidare till postgres
                         (PostgreSQL-serverns körbara fil) eller till initdb
   -p SÖKVÄG-TILL-POSTGRES
                         behövs normalt inte
   -s, --silent           skriv bara ut fel, inga informationsmeddelanden
   -t, --timeout=SEK      antal sekunder att vänta när växeln -w används
   -w, --wait             vänta på att operationen slutförs (standard)
   auto       starta tjänsten automatiskt vid systemstart (förval)
   demand     starta tjänsten vid behov
   fast        stäng omedelbart, med en kontrollerad nedstängning (standard)
   immediate   stäng utan kontroller; kommer leda till återställning vid omstart
   smart       stäng när alla klienter har avslutat
  klar
  misslyckades
  avslutade väntan
 %s är ett verktyg för att initiera, starta, stanna och att styra
PostgreSQL-tjänsten.

 %s: flaggan -S stöds inte på denna plattform.
 %s: PID-filen "%s" finns inte
 %s: VARNING: "Restricted Token" stöds inte av plattformen.
 %s: VARNING: kunde inte hitta alla jobb-funktioner system-API:et.
 %s: en annan server verkar köra; försöker starta servern ändå.
 %s: kan inte köras som root
Logga in (t.ex. med "su") som den (opriviligerade) användare
vilken skall äga serverprocessen.
 %s: kan inte befordra servern; servern är inte i beredskapsläge.
 %s: kan inte befordra servern; en-användar-server kör (PID: %ld)
 %s: kan inte ladda om servern; en-användar-server kör (PID: %ld)
 %s: kan inte starta om servern. En-användar-server kör (PID: %ld).
 %s: kan inte rotera loggfil; en-användar-server kör (PID: %ld)
 %s: kan inte sätta storleksgränsning på core-fil; tillåts inte av hård gräns
 %s: Kan inte stanna servern. En-användar-server i drift (PID: %ld).
 %s: kontrollfilen verkar vara trasig
 %s: kunde inte komma åt katalogen "%s": %s
 %s: kunde inte tilldela SID: felkod %lu
 %s: kunde inte skapa loggroteringssignalfil "%s": %s
 %s: kunde inte skapa befordringssignalfil "%s": %s
 %s: kunde inte skapa restriktivt styrmärke (token): felkod %lu
 %s: kunde inte bestämma databaskatalogen från kommandot "%s"
 %s: kunde inte hitta det egna programmets körbara fil
 %s: kunde inte hitta körbar postgres.
 %s: kunde inte hämta LUID:er för rättigheter: felkod %lu
 %s: kunde inte hämta token-information: felkod %lu
 %s: kunde inte öppna PID-fil "%s": %s
 %s: kunde inte öppna process-token: felkod %lu
 %s: kunde inte öppna tjänsten "%s": felkod %lu
 %s: kunde inte öppna tjänstehanteraren
 %s: kunde inte läsa filen "%s"
 %s: kunde inte registrera tjänsten "%s": felkod %lu
 %s: kunde inte ta bort loggroteringssignalfil "%s": %s
 %s: kunde inte ta bort befordringssignalfil "%s": %s
 %s: kunde inte skicka signalen för loggrotering (PID: %ld): %s
 %s: kunde inte skicka befordringssignal (PID: %ld): %s
 %s: kunde inte skicka signalen "reload" (PID: %ld): %s
 %s: kunde inte skicka signal %d (PID: %ld): %s
 %s: kunde inte skicka stopp-signal (PID: %ld): %s
 %s: kunde inte starta servern
Undersök logg-utskriften.
 %s: kunde inte starta servern då setsid() misslyckades: %s
 %s: kunde inte starta servern: %s
 %s: kunde inte starta servern: felkod %lu
 %s: kunde inte starta tjänsten "%s": felkod %lu
 %s: kunde inte avregistrera tjänsten "%s": felkod %lu
 %s: kunde inte skriva loggroteringssignalfil "%s": %s
 %s: kunde inte skriva befordringssignalfil "%s": %s
 %s: skapande av databaskluster misslyckades
 %s: katalogen "%s" existerar inte
 %s: katalogen "%s" innehåller inte något databaskluster.
 %s: ogiltig data i PID-fil "%s"
 %s: saknar argument för "kill"-kommando.
 %s: ingen databaskatalog angiven och omgivningsvariabeln PGDATA är inte satt
 %s: ingen operation angiven
 %s: ingen server kör
 %s: gamla serverprocessen (PID: %ld) verkar vara borta
 %s: inställningsfilen "%s" måste bestå av en enda rad.
 %s: slut på minne
 %s: servern befordrades inte i tid
 %s: servern startade inte i tid
 %s: servern stänger inte ner
 %s: servern kör (PID: %ld)
 %s: tjänsten "%s" är redan registrerad
 %s: tjänsten "%s" är inte registrerad
 %s: en-användar-server kör. (PID: %ld)
 %s: PID-filen "%s" är tom
 %s: för många kommandoradsargument (första är "%s")
 %s: okänd operationsmetod "%s"
 %s: ogiltig stängningsmetod "%s"
 %s: ogiltigt signalnamn "%s"
 %s: ogiltigt startvillkor "%s"
 TIPS: Flaggan "-m fast" avslutar sessioner omedelbart, i stället för att
vänta på deras självvalda avslut.
 Om flaggan -D inte har angivits så används omgivningsvariabeln PGDATA.
 Kör servern?
 Var vänlig att stanna en-användar-servern och försök sedan igen.
 Server startad och accepterar nu anslutningar
 Programmet "%s" behövs av %s men hittades inte i samma
katalog som "%s".
Kontrollera din installation.
 Programmet "%s" hittades av "%s"
men är inte av samma version som %s.
Kontrollera din installation.
 Tidsfristen ute vid väntan på serverstart
 Försök med "%s --help" för mer information.
 Användning:
 VARNING: Läget för backup under drift är i gång.
Nedstängning är inte fullständig förrän pg_stop_backup() har anropats.

 Väntar på serverstart...
 kan inte duplicera null-pekare (internt fel)
 barnprocess avslutade med kod %d barnprocess avslutade med okänd statuskod %d barnprocess terminerades med avbrott 0x%X barnprocess terminerades av signal %d: %s kommandot är inte körbart kommandot kan ej hittas kunde inte byta katalog till "%s": %m kunde inte hitta en "%s" att köra kunde inte fastställa nuvarande arbetskatalog: %s
 kunde inte identifiera aktuell katalog: %m kunde inte läsa binär "%s" kan inte läsa symbolisk länk "%s": %m ogiltig binär "%s" slut på minne slut på minne
 pclose misslyckades: %m servern befordrad
 servern befordras
 servern stänger ner
 servern är signalerad
 servern är signalerad att rotera loggfil
 servern startad
 servern startar
 servern är stoppad
 startar servern ändå
 försöker starta servern ändå
 väntar på att servern skall befordras... väntar på att servern skall stänga ner... väntar på att servern skall starta... 