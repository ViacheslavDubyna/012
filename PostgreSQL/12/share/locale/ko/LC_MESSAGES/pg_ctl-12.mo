Þ          Ì  Ó   |	      È      É     ê  &   ü     #     C  -   b          ¦  -   ¹     ç  /        5      Í  f   î  k   U     Á  B   Ý  !      3   B  ?   v  H   ¶  D   ÿ  C   D  E     ?   Î  ?     >   N  9     L   Ç  B     E   W       0   "  F   S  >     B   Ù  I     %   f  <     O   É  7        Q     X     a  M   s  -   Á  !   ï  >     E   P  C     y   Ú  9   T  D     C   Ó  D     >   \  A     '   Ý  (     ,   .  2   [  6     >   Å  *     /   /  7   _  4     %   Ì  1   ò  0   $  #   U     y  4     2   Ì  1   ÿ  0   1  ,   b  .     3   ¾     ò  +     1   >  6   p  1   §  *   Ù  "     7   '  "   _  $     J   §     ò        3   %   0   Y         #      !   Á      ã   !   !  $   $!      I!  -   j!     !  4   ¸!  %   í!  $   "  "   8"  !   ["  u   }"  F   ó"     :#  7   N#  )   #  k   °#  `   $  %   }$  &   £$     Ê$  d   Ò$     7%  /   V%  &   %  0   ­%  .   Þ%  )   &  )   7&     a&     x&  &   &      ±&  ,   Ò&  (   ÿ&     ('  !   C'     e'     y'     '     '     «'     ½'     Ó'     ä'     ô'     (     (     -(      L(  "   m(     (  v  ¯(  <   &*     c*  '   w*  4   *  4   Ô*  ,   	+     6+     M+  :   d+  "   +  <   Â+  ©   ÿ+  .   ©,  q   Ø,  }   J-  )   È-  N   ò-  %   A.  >   g.  c   ¦.  L   
/  A   W/  M   /  >   ç/  >   &0  H   e0  8   ®0  E   ç0  `   -1  L   1  M   Û1     )2  4   ¾2  Y   ó2  A   M3  J   3  W   Ú3     24  c   N4  b   ²4  N   5     d5     m5     v5  b   5  ?   ó5  $   36  I   X6  N   ¢6  T   ñ6  ã   F7  L   *8  O   w8  l   Ç8  _   49  o   9  K   :  "   P:  5   s:  3   ©:  J   Ý:  =   (;  I   f;  =   °;  @   î;  B   /<  :   r<  *   ­<  =   Ø<  8   =  *   O=  %   z=  >    =  J   ß=  H   *>  9   s>  5   ­>  7   ã>  I   ?  (   e?  6   ?  >   Å?  O   @  F   T@  (   @     Ä@  Z   â@  !   =A  7   _A  U   A  5   íA  #   #B  ?   GB  E   B     ÍB  D   ãB  3   (C  "   \C  '   C  2   §C  1   ÚC  7   D  .   DD  4   sD  &   ¨D  !   ÏD  $   ñD  %   E  ½   <E  J   úE     EF  @   eF  1   ¦F     ØF     vG  6   H  *   BH     mH     yH  2   I  6   6I  8   mI  ?   ¦I  ;   æI  4   "J  =   WJ     J     ´J  =   ÓJ  *   K  1   <K  )   nK  -   K  *   ÆK  "   ñK     L     &L     8L  +   UL     L  +   L     ÅL     ×L     òL  $   M  (   ,M  /   UM  .   M  1   ´M             2           b   y   <           Z   x                 v   8                  
      B       ;   )       @              l       R   %                          ?             6          =   r                  ,          0   J   G   3          a       h   5   p   {   X   [   `       7                     +   t   K         |   S      :   \   !              z   W          i   s          _   (   q   >       V               9   k   e      N   #             A                     c   /                	   ]              "       F              U   }   g               j      D   ~      *   '   d   -   f   ^          H      4   C       m       P   1      L             $   E         Q              w                  O   u      .   T       Y               I   &      M   n      o        
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
Report bugs to <pgsql-bugs@postgresql.org>.
 
Shutdown modes are:
 
Start types are:
   %s init[db] [-D DATADIR] [-s] [-o OPTIONS]
   %s kill     SIGNALNAME PID
   %s promote  [-D DATADIR] [-W] [-t SECS] [-s]
   %s register [-D DATADIR] [-N SERVICENAME] [-U USERNAME] [-P PASSWORD]
                  [-S START-TYPE] [-e SOURCE] [-W] [-t SECS] [-s] [-o OPTIONS]
   %s reload   [-D DATADIR] [-s]
   %s restart  [-D DATADIR] [-m SHUTDOWN-MODE] [-W] [-t SECS] [-s]
                  [-o OPTIONS] [-c]
   %s start    [-D DATADIR] [-l FILENAME] [-W] [-t SECS] [-s]
                  [-o OPTIONS] [-p PATH] [-c]
   %s status   [-D DATADIR]
   %s stop     [-D DATADIR] [-m SHUTDOWN-MODE] [-W] [-t SECS] [-s]
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
 %s: cannot set core file size limit; disallowed by hard limit
 %s: cannot stop server; single-user server is running (PID: %ld)
 %s: control file appears to be corrupt
 %s: could not access directory "%s": %s
 %s: could not allocate SIDs: error code %lu
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
 %s: could not remove promote signal file "%s": %s
 %s: could not send promote signal (PID: %ld): %s
 %s: could not send reload signal (PID: %ld): %s
 %s: could not send signal %d (PID: %ld): %s
 %s: could not send stop signal (PID: %ld): %s
 %s: could not start server
Examine the log output.
 %s: could not start server: %s
 %s: could not start server: error code %lu
 %s: could not start service "%s": error code %lu
 %s: could not unregister service "%s": error code %lu
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
 child process exited with exit code %d child process exited with unrecognized status %d child process was terminated by exception 0x%X child process was terminated by signal %d child process was terminated by signal %s command not executable command not found could not change directory to "%s": %s could not find a "%s" to execute could not get current working directory: %s
 could not identify current directory: %s could not read binary "%s" could not read symbolic link "%s" invalid binary "%s" out of memory
 pclose failed: %s server promoted
 server promoting
 server shutting down
 server signaled
 server started
 server starting
 server stopped
 starting server anyway
 trying to start server anyway
 waiting for server to promote... waiting for server to shut down... waiting for server to start... Project-Id-Version: pg_ctl (PostgreSQL) 11
Report-Msgid-Bugs-To: pgsql-bugs@postgresql.org
PO-Revision-Date: 2018-09-07 15:18+0900
Last-Translator: Ioseph Kim <ioseph@uri.sarang.net>
Language-Team: Korean Team <pgsql-kr@postgresql.kr>
Language: ko
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=1; plural=0;
 
ì¬ì©í  ì ìë ì¤ì§ì©(for kill) ìê·¸ë ì´ë¦:
 
ì¼ë° ìµìë¤:
 
ìë¹ì¤ ë±ë¡/ì ê±°ì© ìµìë¤:
 
start, restart ë ì¬ì©í  ì ìë ìµìë¤:
 
stop, restart ë ì¬ì© í  ì ìë ìµìë¤:
 
ì¤ë¥ë³´ê³ : <pgsql-bugs@postgresql.org>.
 
ì¤ì§ë°©ë² ì¤ëª:
 
ììíí ì¤ëª:
   %s init[db] [-D ë°ì´í°ëë í°ë¦¬] [-s] [-o ìµì]
   %s kill     ìê·¸ëì´ë¦ PID
   %s promote  [-D ë°ì´í°ëë í°ë¦¬] [-W] [-t ì´] [-s]
   %s register [-D ë°ì´í°ëë í°ë¦¬] [-N ìë¹ì¤ì´ë¦] [-U ì¬ì©ìì´ë¦] [-P ìí¸]
                  [-S ììíí] [-e SOURCE] [-w] [-t ì´] [-o ìµì]
   %s reload   [-D ë°ì´í°ëë í°ë¦¬] [-s]
   %s restart  [-D ë°ì´í°ëë í°ë¦¬] [-m ì¤ì§ë°©ë²] [-W] [-t ì´] [-s]
                  [-o ìµì] [-c]
   %s start    [-D ë°ì´í°ëë í°ë¦¬] [-l íì¼ì´ë¦] [-W] [-t ì´] [-s]
                  [-o ìµì] [-p ê²½ë¡] [-c]
   %s status   [-D ë°ì´í°ëë í°ë¦¬]
   %s stop     [-D ë°ì´í°ëë í°ë¦¬] [-m ì¤ì§ë°©ë²] [-W] [-t ì´] [-s]
   %s unregister [-N ìë¹ì¤ì´ë¦]
   -?, --help             ì´ ëìë§ì ë³´ì¬ì£¼ê³  ë§ì¹¨
   -D, --pgdata=ë°ì´í°ëë í°ë¦¬  ë°ì´í°ë² ì´ì¤ ìë£ê° ì ì¥ëì´ìë ëë í°ë¦¬
   -N SERVICENAME  ìë¹ì¤ ëª©ë¡ì ë±ë¡ë  PostgreSQL ìë¹ì¤ ì´ë¦
   -P PASSWORD     ì´ ìë¹ì¤ë¥¼ ì¤íí  ì¬ì©ìì ìí¸
   -S ììíí     ìë¹ì¤ë¡ ë±ë¡ë PostgreSQL ìë² ìì ë°©ë²
   -U USERNAME     ì´ ìë¹ì¤ë¥¼ ì¤íí  ì¬ì©ì ì´ë¦
   -V, --version          ë²ì  ì ë³´ë¥¼ ë³´ì¬ì£¼ê³  ë§ì¹¨
   -W, --no-wait          ììì´ ëë  ëê¹ì§ ê¸°ë¤ë¦¬ì§ ìì
   -c, --core-files       ì½ì´ ë¤í íì¼ì ë§ë¬
   -c, --core-files       ì´ íë«í¼ììë ì¬ì©í  ì ìì
   -e SOURCE              ìë¹ì¤ê° ì¤í ì¤ì¼ë ìì ë¡ê·¸ë¥¼ ìí ì´ë²¤í¸ ìì¤
   -l, --log=ë¡ê·¸íì¼     ìë² ë¡ê·¸ë¥¼ ì´ ë¡ê·¸íì¼ì ê¸°ë¡í¨
   -m, --mode=ëª¨ë        ëª¨ëë "smart", "fast", "immediate" ì¤ íë
   -o, --options=ìµìë¤   PostgreSQL ìë²íë¡ê·¸ë¨ì¸ postgresë initdb
                         ëªë ¹ìì ì¬ì©í  ëªë ¹í ìµìë¤
   -p PATH-TO-POSTGRES    ë³´íµì íìì¹ ìì
   -s, --silent           ì¼ë°ì ì¸ ë©ìì§ë ë³´ì´ì§ ìê³ , ì¤ë¥ë§ ë³´ì¬ì¤
   -t, --timeout=ì´      -w ìµì ì¬ì© ì ëê¸° ìê°(ì´)
   -w, --wait             ììì´ ëë  ëê¹ì§ ê¸°ë¤ë¦¼ (ê¸°ë³¸ê°)
   auto       ìì¤íì´ ììëë©´ ìëì¼ë¡ ìë¹ì¤ê° ììë¨ (ì´ê¸°ê°)
   demand     ìë ìì
   fast        í´ë¼ì´ì¸í¸ì ì°ê²°ì ê°ì ë¡ ëê³  ì ìì ì¼ë¡ ì¤ì§ ë¨ (ê¸°ë³¸ê°)
   immediate   ê·¸ë¥ ë¬´ì¡°ê±´ ì¤ì§í¨; ë¤ì ììí  ë ë³µêµ¬ ììì í  ìë ìì
   smart       ëª¨ë  í´ë¼ì´ì¸í¸ì ì°ê²°ì´ ëê¸°ê² ëë©´ ì¤ì§ ë¨
  ìë£
  ì¤í¨
  ì¤ì§ ê¸°ë¤ë¦¬ë ì¤
 %s íë¡ê·¸ë¨ì PostgreSQL ìë²ë¥¼ ì´ê¸°í, ìì, ì¤ì§, ì ì´íë ëêµ¬ìëë¤.

 %s: -S ìµìì ì´ ì´ìì²´ì ììë ì§ìíì§ ìì
 %s: "%s" PID íì¼ì´ ììµëë¤
 %s: ê²½ê³ : ì´ ì´ìì²´ì ìì restricted tokenì ë§ë¤ ì ìì
 %s: ê²½ê³ : ìì¤í APIìì ëª¨ë  job ê°ì²´ í¨ìë¥¼ ì°¾ì ì ìì
 %s: ë¤ë¥¸ ìë²ê° ê°ë ì¤ì¸ ê² ê°ì; ì´ì§¸ë  ìë² ê°ëì ìëí¨
 %s: rootë¡ ì´ íë¡ê·¸ë¨ì ì¤ííì§ ë§ì­ìì¤
ìì¤íê´ë¦¬ì ê¶íì´ ìë, ìë²íë¡ì¸ì¤ì ìì ì£¼ê° ë  ì¼ë° ì¬ì©ìë¡
ë¡ê·¸ì¸ í´ì("su", "runas" ê°ì ëªë ¹ ì´ì©) ì¤ííì­ìì¤.
 %s: ì´ììë² ì í ì¤í¨; ìë²ê° ëê¸° ëª¨ëë¡ ìíê° ìë
 %s: ì´ììë² ì í ì¤í¨; ë¨ì¼ì¬ì©ì ìë²ê° ì¤í ì¤(PID: %ld)
 %s: ìë² íê²½ì¤ì ì ë¤ì ë¶ë¬ì¬ ì ìì; ë¨ì¼ ì¬ì©ì ìë²ê° ì¤í ì¤ì (PID: %ld)
 %s: ìë²ë¥¼ ë¤ì ìì í  ì ìì; ë¨ì¼ì¬ì©ì ìë²ê° ì¤í ì¤ì (PID: %ld)
 %s: ì½ì´ íì¼ í¬ê¸° íëë¥¼ ì¤ì í  ì ìì, íë ëì¤í¬ ì©ë ì´ê³¼ë¡ íì©ëì§ ìì
 %s: ìë² ì¤ì§ ì¤í¨; ë¨ì¼ ì¬ì©ì ìë²ê° ì¤í ì¤ (PID: %ld)
 %s: ì»¨í¸ë¡¤ íì¼ì´ ê¹¨ì¡ì
 %s: "%s" ëë í°ë¦¬ì ì¡ì¸ì¤í  ì ìì: %s
 %s: SIDë¥¼ í ë¹í  ì ìì: ì¤ë¥ ì½ë %lu
 %s: ì´ìì í ìê·¸ë íì¼ì¸ "%s" íì¼ì ë§ë¤ ì ìì: %s
 %s: restricted tokenì ë§ë¤ ì ìì: ì¤ë¥ ì½ë %lu
 %s: "%s" ëªë ¹ìì ì¬ì©í  ë°ì´í° ëë í°ë¦¬ë¥¼ ì ì ìì
 %s: ì¤í ê°ë¥í íë¡ê·¸ë¨ì ì°¾ì ì ììµëë¤
 %s: ì¤í ê°ë¥í postgres íë¡ê·¸ë¨ì ì°¾ì ì ìì
 %s: ì ê·¼ ê¶íì© LUIDë¥¼ êµ¬í  ì ìì: ì¤ë¥ ì½ë %lu
 %s: í í° ì ë³´ë¥¼ êµ¬í  ì ìì: ì¤ë¥ ì½ë %lu
 %s: "%s" PID íì¼ì ì´ ì ìì: %s
 %s: íë¡ì¸ì¤ í í°ì ì´ ì ìì: ì¤ë¥ ì½ë %lu
 %s: "%s" ìë¹ì¤ë¥¼ ì´ ì ìì: ì¤ë¥ ì½ë %lu
 %s: ìë¹ì¤ ê´ë¦¬ìë¥¼ ì´ ì ìì
 %s: "%s" íì¼ì ì½ì ì ìì
 %s: "%s" ìë¹ì¤ë¥¼ ë±ë¡í  ì ìì: ì¤ë¥ ì½ë %lu
 %s: ì´ìì í ìê·¸ë íì¼ì¸ "%s" íì¼ì ì§ì¸ ì ìì: %s
 %s: ì´ìì í ìê·¸ëì ìë²(PID: %ld)ë¡ ë³´ë¼ ì ìì: %s
 %s: reload ìê·¸ëì ë³´ë¼ ì ìì (PID: %ld): %s
 %s: %d ìê·¸ëì ë³´ë¼ ì ìì (PID: %ld): %s
 %s: stop ìê·¸ëì ë³´ë¼ ì ìì (PID: %ld): %s
 %s: ìë²ë¥¼ ìì í  ì ìì
ë¡ê·¸ ì¶ë ¥ì ì´í´ë³´ì­ìì¤.
 %s: ìë²ë¥¼ ìì í  ì ìì: %s
 %s: ìë²ë¥¼ ììí  ì ìì: ì¤ë¥ ì½ë %lu
 %s: "%s" ìë¹ì¤ë¥¼ ììí  ì ìì: ì¤ë¥ ì½ë %lu
 %s: "%s" ìë¹ì¤ë¥¼ ìë¹ì¤ ëª©ë¡ìì ëº ì ìì: ì¤ë¥ ì½ë %lu
 %s: ì´ìì í ìê·¸ë íì¼ì¸ "%s" íì¼ì ì°ê¸° ì¤í¨: %s
 %s: ë°ì´í°ë² ì´ì¤ ì´ê¸°í ì¤í¨
 %s: "%s" ëë í°ë¦¬ ìì
 %s: ì§ì í "%s" ëë í°ë¦¬ë ë°ì´í°ë² ì´ì¤ í´ë¬ì¤í¸ ëë í°ë¦¬ê° ìë
 %s: "%s" PID íì¼ì´ ë¹ìì
 %s: kill ììì íìí ì¸ìê° ë¹ ì¡ìµëë¤
 %s: -D ìµìë ìê³ , PGDATA íê²½ë³ìê°ë ì§ì ëì´ ìì§ ììµëë¤.
 %s: ìíí  ììì ì§ì íì§ ìììµëë¤
 %s: ê°ë ì¤ì¸ ìë²ê° ìì
 %s: ì´ì  ìë² íë¡ì¸ì¤(PID: %ld)ê° ìì´ì¡ìµëë¤
 %s: "%s" íê²½ì¤ì íì¼ì ë°ëì í ì¤ì ê°ì ¸ì¼íë¤?
 %s: ë©ëª¨ë¦¬ ë¶ì¡±
 %s: ìë²ë¥¼ ì  ìê°ì ì´ì ëª¨ëë¡ ì ííì§ ëª»íì
 %s: ìë²ê° ì  ìê°ì ììëì§ ëª»íì
 %s: ìë²ë¥¼ ë©ì¶ì§ ëª»íì
 %s: ìë²ê° ì¤í ì¤ì (PID: %ld)
 %s: "%s" ìë¹ì¤ê° ì´ë¯¸ ë±ë¡ ëì´ ìì
 %s: "%s" ìë¹ì¤ê° ë±ë¡ëì´ ìì§ ìì
 %s: ë¨ì¼ì¬ì©ì ìë²ê° ì¤í ì¤ì (PID: %ld)
 %s: "%s" PID íì¼ì ë´ì©ì´ ììµëë¤
 %s: ëë¬´ ë§ì ëªë ¹í ì¸ìë¤ (ìì "%s")
 %s: ì ì ìë ìì ëª¨ë "%s"
 %s: ìëª»ë ì¤ì§ ë°©ë² "%s"
 %s: ìëª»ë ìê·¸ë ì´ë¦ "%s"
 %s: ì ì ìë ììíí "%s"
 íí¸: "-m fast" ìµìì ì¬ì©íë©´ ì ìí ì¸ìë¤ì ì¦ì ì ë¦¬í©ëë¤.
ì´ ìµìì ì¬ì©íì§ ìì¼ë©´ ì ìí ì¸ìë¤ ì¤ì¤ë¡ ëì ëê¹ì§ ê¸°ë¤ë¦½ëë¤.
 -D ìµìì ì¬ì©íì§ ìì¼ë©´, PGDATA íê²½ë³ìê°ì ì¬ì©í¨.
 ìë²ê° ì¤í ì¤ìëê¹?
 ë¨ì¼ ì¬ì©ì ìë²ë¥¼ ë©ì¶ê³  ë¤ì ìëíì­ìì¤.
 ìë²ê° ììëìì¼ë©° ì°ê²°ì íì©í¨
 "%s" íë¡ê·¸ë¨ì %s ìì íìë¡ í©ëë¤. ê·¸ë°ë°, ì´ íì¼ì´
"%s" ëë í°ë¦¬ ìì ììµëë¤.
ì¤ì¹ ìíë¥¼ íì¸í´ ì£¼ì­ìì¤.
 "%s" íë¡ê·¸ë¨ì "%s" ìì íìí´ì ì°¾ìì§ë§ ì´ íì¼ì
%s ë²ì ê³¼ ê°ì§ ììµëë¤.
ì¤ì¹ ìíë¥¼ íì¸í´ ì£¼ì­ìì¤.
 ìë² ììì ê¸°ë¤ë¦¬ë ëì ìê° ì´ê³¼ë¨
 ë³´ë¤ ìì¸í ì¬ì©ë²ì "%s --help"
 ì¬ì©ë²:
 ê²½ê³ : ì¨ë¼ì¸ ë°±ì ëª¨ëê° íì± ìíìëë¤.
pg_stop_backup()ì´ í¸ì¶ë  ëê¹ì§ ì¢ë£ê° ìë£ëì§ ììµëë¤.

 ìë²ë¥¼ ììíê¸° ìí´ ê¸°ë¤ë¦¬ë ì¤...
 null í¬ì¸í°ë¥¼ ë³µì í  ì ìì(ë´ë¶ ì¤ë¥)
 íì íë¡ì¸ì¤ê° ì¢ë£ëìì, ì¢ë£ ì½ë %d íì íë¡ì¸ì¤ê° ì¢ë£ëìì, ìì ìë ìí %d 0x%X ìì¸ì²ë¦¬ë¡ íì íë¡ì¸ì¤ê° ì¢ë£ëìì íì íë¡ì¸ì¤ê° ì¢ë£ëìì, ìê·¸ë %d %s ìê·¸ë ê°ì§ë¡ íì íë¡ì¸ì¤ê° ì¢ë£ëìì ëªë ¹ì ì¤íí  ì ìì ëªë ¹ì´ë¥¼ ì°¾ì ì ìì "%s" ì´ë¦ì ëë í°ë¦¬ë¡ ì´ëí  ì ììµëë¤: %s ì¤íí  "%s" íì¼ì ì°¾ì ì ìì íì¬ ìì ëë í°ë¦¬ë¥¼ ì ì ìì: %s
 íì¬ ëë í°ë¦¬ë¥¼ ì ì ìì: %s "%s" ë°ì´ëë¦¬ íì¼ì ì½ì ì ìì "%s" ì¬ë²ë¦­ ë§í¬ë¥¼ ì½ì ì ìì ìëª»ë ë°ì´ëë¦¬ íì¼ "%s" ë©ëª¨ë¦¬ ë¶ì¡±
 pclose ì¤í¨: %s ì´ì ëª¨ë ì í ìë£
 ìë²ë¥¼ ì´ì ëª¨ëë¡ ì íí©ëë¤
 ìë²ë¥¼ ë©ì¶¥ëë¤
 ìë²ê° ìì¤í ìê·¸ëì ë°ìì
 ìë² ììë¨
 ìë²ë¥¼ ììí©ëë¤
 ìë² ë©ì¶ìì
 ì´ì§¸ë  ìë²ë¥¼ ììí©ëë¤
 ì´ì§¸ë  ìë²ë¥¼ ììí´ ë´ëë¤
 ìë²ë¥¼ ì´ì ëª¨ëë¡ ì ííë ì¤ ... ìë²ë¥¼ ë©ì¶ê¸° ìí´ ê¸°ë¤ë¦¬ë ì¤... ìë²ë¥¼ ììíê¸° ìí´ ê¸°ë¤ë¦¬ë ì¤... 