��    *      l  ;   �      �  E   �  0   �        :   3  E   n  I   �  L   �  s   K  K   �  =     B   I  i   �  G   �  J   >  M   �  M   �  ?   %  G   e  >   �  6   �  <   #	  >   `	  F   �	  P   �	  I   7
  4   �
  2   �
  *   �
       	   .  ,   8  &   e     �  &   �      �  (   �       !         B     V     c  r  u  ^   �  b   G     �  {   �  B   :  J   }  P   �  c     O   }  b   �  k   0  �   �  q   &  L   �  R   �  R   8  c   �  F   �  H   6  S     ^   �  m   2  k   �  �     v   �  3     G   E  U   �  2   �       L   +  Q   x     �  D   �  >   *  J   i  D   �  R   �  /   L     |     �                             %   	      *   )      $           
   "                                      '      &                                                            (         !                    #    
%s provides information about the installed version of PostgreSQL.

 
With no arguments, all known items are shown.

   %s [OPTION]...

   --bindir              show location of user executables
   --cc                  show CC value used when PostgreSQL was built
   --cflags              show CFLAGS value used when PostgreSQL was built
   --cflags_sl           show CFLAGS_SL value used when PostgreSQL was built
   --configure           show options given to "configure" script when
                        PostgreSQL was built
   --cppflags            show CPPFLAGS value used when PostgreSQL was built
   --docdir              show location of documentation files
   --htmldir             show location of HTML documentation files
   --includedir          show location of C header files of the client
                        interfaces
   --includedir-server   show location of C header files for the server
   --ldflags             show LDFLAGS value used when PostgreSQL was built
   --ldflags_ex          show LDFLAGS_EX value used when PostgreSQL was built
   --ldflags_sl          show LDFLAGS_SL value used when PostgreSQL was built
   --libdir              show location of object code libraries
   --libs                show LIBS value used when PostgreSQL was built
   --localedir           show location of locale support files
   --mandir              show location of manual pages
   --pgxs                show location of extension makefile
   --pkgincludedir       show location of other C header files
   --pkglibdir           show location of dynamically loadable modules
   --sharedir            show location of architecture-independent support files
   --sysconfdir          show location of system-wide configuration files
   --version             show the PostgreSQL version
   -?, --help            show this help, then exit
 %s: could not find own program executable
 %s: invalid argument: %s
 Options:
 Report bugs to <pgsql-bugs@postgresql.org>.
 Try "%s --help" for more information.
 Usage:
 could not change directory to "%s": %s could not find a "%s" to execute could not identify current directory: %s could not read binary "%s" could not read symbolic link "%s" invalid binary "%s" not recorded pclose failed: %s Project-Id-Version: postgresql
Report-Msgid-Bugs-To: pgsql-bugs@postgresql.org
PO-Revision-Date: 2019-05-07 12:57
Last-Translator: pasha_golub
Language-Team: Ukrainian
Language: uk_UA
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=4; plural=((n%10==1 && n%100!=11) ? 0 : ((n%10 >= 2 && n%10 <=4 && (n%100 < 12 || n%100 > 14)) ? 1 : ((n%10 == 0 || (n%10 >= 5 && n%10 <=9)) || (n%100 >= 11 && n%100 <= 14)) ? 2 : 3));
X-Generator: crowdin.com
X-Crowdin-Project: postgresql
X-Crowdin-Language: uk
X-Crowdin-File: /REL_11_STABLE/src/bin/pg_config/po/pg_config.pot
 
%s надає інформацію про інстальовану версію PostgreSQL.

 
Без аргументів, всі відображаються відомі елементи.

   %s: [OPTION]...

   --bindir              показує розташування виконуваних файлів користувача
   --cc показує значення CC збірки PostgreSQL
   --cflags показує значення CFLAGS збірки PostgreSQL
   --cflags_sl показує значення CFLAGS_SL збірки PostgreSQL
   --configure показує параметри скрипта "configure" збірки PostgreSQL
   --cppflags показує значення CPPFLAGS збірки PostgreSQL 
   --docdir          показує розташування файлів документації
   --htmldir             показує розташування файлів документації HTML
   -includedir показує розташування заголовків файлів С клієнтських інтерфейсів
   -includedir-server показує розташування заголовків файлів С сервера
   --ldflags показує значення LDFLAGS збірки PostgreSQL
   --ldflags_ex показує значення LDFLAGS_EX збірки PostgreSQL
   --ldflags_sl показує значення LDFLAGS_SL збірки PostgreSQL
   --libdir показує розташування бібліотек об'єктного коду
   --libs показує значення LIBS збірки PostgreSQL
   --localedir показує місце файлів перекладу
   --mandir показує розташування сторінок мануала
   --pgxs показує місцерозташування makefile для розширень
   -pkgincludedir показує розташування інших файлів з заголовками C
   --pkglibdir показує місце динамічно завантажувальних модулів
   --sharedir показує місцерозташування архітектурно незалежних файлів підтримки
   --sysconfdir показує розташування всесистемних файлів конфігурації
   --version показує версію PostgreSQL
   -?, --help показує цю довідку, потім вихід
 %s: не вдалося знайти ехе файл власної програми
 %s: недопустимий аргумент: %s
 Параметри:
 Про помилки повідомляйте <pgsql-bugs@postgresql.org>.
 Спробуйте "%s --help" для додаткової інформації.
 Використання:
 неможливо змінити директорію на "%s": %s неможливо знайти "%s" для виконання не вдалося визначити поточний каталог: %s неможливо прочитати бінарний файл "%s" неможливо прочитати символічне посилання "%s" невірний бінарний файл "%s" не записано помилка pclose: %s 