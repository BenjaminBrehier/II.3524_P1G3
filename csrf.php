<?php
session_start();

// Afficher l'ID de session pour déboguer
echo "ID de session : " . session_id() . "<br>";

// Simuler une "base de données" en mémoire
$users = [
    'alice' => 'password123',
    'bob' => 'securePass'
];

// Stocker les informations des utilisateurs dans la session (persistantes pour cette session)
if (!isset($_SESSION['users'])) {
    $_SESSION['users'] = $users;
}

// Vérification de connexion
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    // Vérifier si l'utilisateur existe
    if (array_key_exists($username, $_SESSION['users'])) {
        // Modifier le mot de passe de l'utilisateur
        $_SESSION['users'][$username] = $password;
        echo "Le mot de passe de $username a été changé en $password.";
    } else {
        echo "Utilisateur $username introuvable.";
    }
}
?>

<!-- Formulaire vulnérable -->
<form method="POST" action="">
    <input type="text" name="username" placeholder="Nom d'utilisateur">
    <input type="password" name="password" placeholder="Nouveau mot de passe">
    <button type="submit">Soumettre</button>
</form>

<!-- Afficher les utilisateurs stockés dans la session -->
<h3>Utilisateurs enregistrés dans la session :</h3>
<pre><?php print_r($_SESSION['users']); ?></pre>

