��    X      �     �      �  X   �  
   �     �  3     ?   J  (   �  C   �  -   �  !   %	  ,   G	      t	  4   �	     �	     �	  ,   �	  ,   
  )   8
  )   b
  )   �
  )   �
  )   �
  )   
  )   4  )   ^  )   �  ,   �  )   �  )   	  ,   3  )   `  )   �  )   �  ,   �  )     )   5  ,   _  )   �  )   �  )   �  )   
  )   4  )   ^  )   �  )   �  )   �  )     )   0  )   Z  )   �  )   �  ,   �  )     ,   /  )   \  >  �  )   �  &   �       )     �   H  "       2     B     O     X     o     �     �  )   �  )   �  )   �  )   !     K     N     R  )   U  )     	   �     �     �     �  )   �          &  )   =  )   g     �  |  �  �        �     �  U   �  V   '  8   ~  i   �  Q   !  =   s  V   �  2     a   ;     �     �  Y   �  ]     K   p  )   �  ;   �  P   "  0   s  ?   �  N   �  ,   3  [   `  T   �  /      4   A   Z   v   G   �   G   !  ?   a!  A   �!  F   �!  J   *"  T   u"  B   �"  H   #  I   V#  G   �#  H   �#  W   1$  G   �$  W   �$  A   )%  Q   k%  ?   �%  J   �%  A   H&  l   �&  W   �&  D   O'  L   �'  B   �'  �  $(  @   ,  Q   G,     �,     �,  Z  �,  V   /.    �.     �0     �0  4   �0  &   �0  &   #1     J1  -   d1  0   �1  0   �1  2   �1     '2  	   ,2     62  J   B2  2   �2  !   �2  ;   �2  !   3     @3  4   M3  *   �3  %   �3  ,   �3  +    4     ,4                  2   @          %   F   V   /                                )          X   U                         &   7       	          ?       ,                  #   D   W       A       '   +       
   C   N   $   <   Q   (   T   B   J      8   6      4       1       *   =          -   K   H            :   G           R   3   5   >                 S   P   !       9   I   E          0   O              L          M   ;   "                                          .        
If no data directory (DATADIR) is specified, the environment variable PGDATA
is used.

 
Options:
   %s [OPTION] [DATADIR]
   -?, --help             show this help, then exit
   -V, --version          output version information, then exit
  [-D, --pgdata=]DATADIR  data directory
 %s displays control information of a PostgreSQL database cluster.

 %s: could not open file "%s" for reading: %s
 %s: could not read file "%s": %s
 %s: could not read file "%s": read %d of %d
 %s: no data directory specified
 %s: too many command-line arguments (first is "%s")
 64-bit integers ??? Backup end location:                  %X/%X
 Backup start location:                %X/%X
 Blocks per segment of large relation: %u
 Bytes per WAL segment:                %u
 Catalog version number:               %u
 Data page checksum version:           %u
 Database block size:                  %u
 Database cluster state:               %s
 Database system identifier:           %s
 Date/time type storage:               %s
 End-of-backup record required:        %s
 Fake LSN counter for unlogged rels:   %X/%X
 Float4 argument passing:              %s
 Float8 argument passing:              %s
 Latest checkpoint location:           %X/%X
 Latest checkpoint's NextMultiOffset:  %u
 Latest checkpoint's NextMultiXactId:  %u
 Latest checkpoint's NextOID:          %u
 Latest checkpoint's NextXID:          %u:%u
 Latest checkpoint's PrevTimeLineID:   %u
 Latest checkpoint's REDO WAL file:    %s
 Latest checkpoint's REDO location:    %X/%X
 Latest checkpoint's TimeLineID:       %u
 Latest checkpoint's full_page_writes: %s
 Latest checkpoint's newestCommitTsXid:%u
 Latest checkpoint's oldestActiveXID:  %u
 Latest checkpoint's oldestCommitTsXid:%u
 Latest checkpoint's oldestMulti's DB: %u
 Latest checkpoint's oldestMultiXid:   %u
 Latest checkpoint's oldestXID's DB:   %u
 Latest checkpoint's oldestXID:        %u
 Maximum columns in an index:          %u
 Maximum data alignment:               %u
 Maximum length of identifiers:        %u
 Maximum size of a TOAST chunk:        %u
 Min recovery ending loc's timeline:   %u
 Minimum recovery ending location:     %X/%X
 Mock authentication nonce:            %s
 Report bugs to <pgsql-bugs@postgresql.org>.
 Size of a large-object chunk:         %u
 The WAL segment size stored in the file, %d byte, is not a power of two
between 1 MB and 1 GB.  The file is corrupt and the results below are
untrustworthy.

 The WAL segment size stored in the file, %d bytes, is not a power of two
between 1 MB and 1 GB.  The file is corrupt and the results below are
untrustworthy.

 Time of latest checkpoint:            %s
 Try "%s --help" for more information.
 Usage:
 WAL block size:                       %u
 WARNING: Calculated CRC checksum does not match value stored in file.
Either the file is corrupt, or it has a different layout than this program
is expecting.  The results below are untrustworthy.

 WARNING: invalid WAL segment size
 WARNING: possible byte ordering mismatch
The byte ordering used to store the pg_control file might not match the one
used by this program.  In that case the results below would be incorrect, and
the PostgreSQL installation would be incompatible with this data directory.
 by reference by value byte ordering mismatch in archive recovery in crash recovery in production max_connections setting:              %d
 max_locks_per_xact setting:           %d
 max_prepared_xacts setting:           %d
 max_worker_processes setting:         %d
 no off on pg_control last modified:             %s
 pg_control version number:            %u
 shut down shut down in recovery shutting down starting up track_commit_timestamp setting:       %s
 unrecognized status code unrecognized wal_level wal_level setting:                    %s
 wal_log_hints setting:                %s
 yes Project-Id-Version: postgresql
Report-Msgid-Bugs-To: pgsql-bugs@postgresql.org
PO-Revision-Date: 2019-07-11 16:20
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
X-Crowdin-File: /REL_11_STABLE/src/bin/pg_controldata/po/pg_controldata.pot
 
Якщо каталог даних не вказано (DATADIR), використовується змінна середовища PGDATA.

 
Параметри:
   %s [OPTION] [DATADIR]
   -?, --help              показати цю довідку потім вийти
   -V, --version вивести інформацію про версію і вийти
  [-D, --pgdata=]DATADIR  каталог з даними
 %s відображає контрольну інформацію щодо кластеру PostgreSQL.

 %s: не вдалося відкрити файл "%s" для читання: %s
 %s: не вдалося прочитати файл "%s": %s
 %s: не вдалося прочитати файл "%s": прочитано %d з %d
 %s: каталог даних не вказано
 %s: забагато аргументів у командному рядку (перший "%s")
 64-бітні цілі ??? Кінцеве розташування резервного копіювання: %X/%X
 Початкове розташування резервного копіювання: %X/%X
 Блоків на сегмент великого відношення: %u
 Байтів на сегмент WAL: %u
 Номер версії каталогу:               %u
 Версія контрольних сум сторінок даних:      %u
 Розмір блоку бази даних: %u
 Стан кластеру бази даних:              %s
 Системний ідентифікатор бази даних:         %s
 Дата/час типу сховища: %s
 Вимагається запис кінця резервного копіювання: %s
 Фіктивний LSN для таблиць без журналювання: %X/%X
 Передача аргументу Float4: %s
 Передача аргументу Float8:      %s
 Останнє місце знаходження контрольної точки: %X/%X
 Останній NextMultiOffset контрольної точки: %u
 Останній NextMultiXactId контрольної точки: %u
 Останній NextOID контрольної точки: %u
 Останній NextXID контрольної точки: %u%u
 Останній PrevTimeLineID контрольної точки: %u
 Останній файл контрольної точки REDO WAL:  %s
 Розташування останньої контрольної точки: %X%X
 Останній TimeLineID контрольної точки: %u
 Останній full_page_writes контрольної точки: %s
 Останній newestCommitTsXid контрольної точки: %u
 Останній oldestActiveXID контрольної точки: %u
 Останній oldestCommitTsXid контрольної точки:%u
 Остання DB останньої oldestMulti контрольної точки: %u
 Останній oldestMultiXid контрольної точки: %u 
 Остання DB останнього oldestXID контрольної точки: %u
 Останній oldestXID контрольної точки: %u
 Максимальна кількість стовпців в індексі: %u
 Максимальне вирівнювання даних: %u
 Максимальна довжина ідентифікаторів:  %u
 Максимальний розмір сегменту TOAST: %u
 Мінімальна позиція історії часу завершення відновлення: %u
 Мінімальне розташування кінця відновлення: %X/%X
 Імітувати нонс для аутентифікації: %s
 Про помилки повідомляйте <pgsql-bugs@postgresql.org>.
 Розмір сегменту великих обїєктів: %u
 Розмір WAL сегменту збережений у файлі, %d байт, не є степенем двійки між 1 MB та 1 GB. Файл пошкоджено та результати нижче є недостовірними.

 Розмір WAL сегменту збережений у файлі, %d байтів, не є степенем двійки між 1 MB та 1 GB. Файл пошкоджено та результати нижче є недостовірними.

 Розмір WAL сегменту збережений у файлі, %d байтів, не є степенем двійки між 1 MB та 1 GB. Файл пошкоджено та результати нижче є недостовірними.

 Розмір WAL сегменту збережений у файлі, %d байта, не є степенем двійки між 1 MB та 1 GB. Файл пошкоджено та результати нижче є недостовірними.

 Час останньої контрольної точки: %s
 Спробуйте "%s --help" для додаткової інформації.
 Використання:
 Pозмір блоку WAL: %u
 ПОПЕРЕДЖЕННЯ: Контрольна сума CRC не відповідає збереженому значенню у файлі. Або файл пошкоджено, або він містить іншу структуру, ніж очікує ця програма. Результати нижче є недостовірними.

 ПОПЕРЕДЖЕННЯ: неправильний розмір WAL сегменту 
 УВАГА: можлива помилка у послідовності байтів 
Порядок байтів, що використовують для зберігання файлу pg_control може не відповідати тому, який використовується цією програмою.  У такому випадку результати нижче будуть неправильним, і інсталяція PostgreSQL буде несумісною з цим каталогом даних.
 за посиланням за значенням неправильний порядок байтів відновлення в архіві відновлення при збої у виробництві налаштування max_connections: %d
 налаштування max_locks_per_xact: %d
 налаштування max_prepared_xacts: %d
 налаштування max_worker_processes: %d
 ні вимк. увімк. pg_control був модифікований востаннє:         %s
 pg_control номер версії:            %u
 завершення роботи завершення роботи у відновленні завершення роботи запуск налаштування track_commit_timestamp: %s
 невизнаний код статусу невизнаний wal_рівень налаштування wal_рівня: %s
 налаштування wal_log_hints: %s
 так 