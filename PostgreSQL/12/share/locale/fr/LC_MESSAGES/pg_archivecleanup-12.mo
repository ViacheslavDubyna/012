��          �   %   �      P  �   Q  
   +  �   6  3   �  3   �  +   &  7   R  6   �  L   �  <     6   K  &   �     �  $   �  )   �  (      (   )     R     q     y     �     �  !   �     �  	   �  7    �   >     (	  �   4	  <   �	  B   
  .   H
  .   w
  F   �
  K   �
  @   9  B   z  2   �     �  /   �  :   )  :   d  8   �  -   �  	          #     *   =  @   h  %   �     �                                                                                
                   	                          
For use as archive_cleanup_command in postgresql.conf:
  archive_cleanup_command = 'pg_archivecleanup [OPTION]... ARCHIVELOCATION %%r'
e.g.
  archive_cleanup_command = 'pg_archivecleanup /mnt/server/archiverdir %%r'
 
Options:
 
Or for use as a standalone archive cleaner:
e.g.
  pg_archivecleanup /mnt/server/archiverdir 000000010000000000000010.00000020.backup
 
Report bugs to <pgsql-bugs@lists.postgresql.org>.
   %s [OPTION]... ARCHIVELOCATION OLDESTKEPTWALFILE
   -?, --help     show this help, then exit
   -V, --version  output version information, then exit
   -d             generate debug output (verbose mode)
   -n             dry run, show the names of the files that would be removed
   -x EXT         clean up files if they have this extension
 %s removes older WAL files from PostgreSQL archives.

 Try "%s --help" for more information.
 Usage:
 archive location "%s" does not exist could not close archive location "%s": %m could not open archive location "%s": %m could not read archive location "%s": %m could not remove file "%s": %m error:  fatal:  invalid file name argument must specify archive location must specify oldest kept WAL file too many command-line arguments warning:  Project-Id-Version: pg_archivecleanup (PostgreSQL) 10
Report-Msgid-Bugs-To: pgsql-bugs@lists.postgresql.org
PO-Revision-Date: 2019-05-17 15:55+0200
Last-Translator: 
Language-Team: 
Language: fr
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: Poedit 2.2.1
 
Pour utiliser comme archive_cleanup_command dans postgresql.conf :
  archive_cleanup_command = 'pg_archivecleanup [OPTION]... EMPLACEMENTARCHIVE %%r'
e.g.
  archive_cleanup_command = 'pg_archivecleanup /mnt/serveur/reparchives %%r'
 
Options :
 
Ou pour utiliser comme nettoyeur autonome d'archives :
e.g.
  pg_archivecleanup /mnt/serveur/reparchives 000000010000000000000010.00000020.backup
 
Rapporter les bogues à <pgsql-bugs@lists.postgresql.org>.
   %s [OPTION]... EMPLACEMENTARCHIVE PLUSANCIENFICHIERWALCONSERVÉ
   -?, --help     affiche cette aide et quitte
   -V, --version  affiche la version et quitte
   -d             affiche des informations de débugage (mode verbeux)
   -n             test, affiche le nom des fichiers qui seraient supprimés
   -x EXT         nettoie les fichiers s'ils ont cette extension
 %s supprime les anciens fichiers WAL des archives de PostgreSQL.

 Essayez « %s --help » pour plus d'informations.
 Usage :
 l'emplacement d'archivage « %s » n'existe pas n'a pas pu fermer l'emplacement de l'archive « %s » : %m n'a pas pu ouvrir l'emplacement de l'archive « %s » : %m n'a pas pu lire l'emplacement de l'archive « %s » : %m n'a pas pu supprimer le fichier « %s » : %m erreur :  fatal :  argument du nom de fichier invalide doit spécifier l'emplacement de l'archive doit spécifier le plus ancien journal de transactions conservé trop d'arguments en ligne de commande attention :  