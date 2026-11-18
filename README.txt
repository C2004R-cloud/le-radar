LE RADAR 👑 — VERSION AVEC COLLECTE AUTOMATIQUE QUOTIDIENNE

CE QUI CHANGE
- TECH & IA et FINANCE affichent un flux d'articles collectés chaque jour.
- Le robot utilise des flux RSS de Google Actualités, avec des requêtes en français.
- Collecte quotidienne par GitHub Actions, vers 06:00 UTC (07:00 en France l'hiver, 08:00 l'été).
- Bouton Actualiser = recharge le dernier flux publié ; il ne déclenche pas lui-même une nouvelle recherche.
- Queen To Do reste enregistrée localement sur le navigateur/appareil. Export/import JSON inclus.
- Politique et Féminisme sont encore des rubriques en attente dans cette version.

MISE EN LIGNE GRATUITE (À FAIRE UNE FOIS)
1. Sur ordinateur, crée un compte GitHub si nécessaire : https://github.com
2. Crée un nouveau dépôt public nommé le-radar (Public).
3. Décompresse ce ZIP et envoie TOUS les fichiers du dossier LE_RADAR_UPGRADE dans le dépôt (y compris .github).
4. Dans le dépôt : Settings > Pages > Build and deployment > Source : Deploy from a branch > Branch : main > /(root) > Save.
5. Va dans Actions, ouvre "Daily Radar Feed", puis "Run workflow" une première fois pour lancer la collecte immédiatement.
6. Quand le workflow a fini (vert), ouvre Settings > Pages pour récupérer l'URL du site.
7. Sur iPhone : ouvre cette URL dans Safari > Partager > Sur l'écran d'accueil > Ajouter.

IMPORTANT
- Le dépôt doit rester public pour utiliser GitHub Pages gratuitement sans configuration de facturation. Ne publie pas de données personnelles.
- Les horaires cron sont approximatifs : GitHub peut décaler l'exécution. La collecte peut échouer si une source est temporairement indisponible.
- Google Actualités RSS fournit des titres, liens et parfois des extraits ; ce n'est pas une analyse IA ni un conseil financier. Toujours vérifier les articles originaux.
- Les articles peuvent être incomplets, répétés ou mal classés. Le flux ne garantit pas une couverture exhaustive.
- Les tâches Queen To Do restent dans le stockage local du navigateur, sans synchronisation entre iPhone et ordinateur.
- Cette archive n'est pas encore déployée : elle doit être publiée dans ton compte GitHub pour obtenir ton URL installable.
