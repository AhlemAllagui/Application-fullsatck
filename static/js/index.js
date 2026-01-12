window.addEventListener('DOMContentLoaded', () => {
    console.log("JavaScript chargé !");

    // Sélectionne tous les liens qui contiennent 'delete' dans l'URL
    const deleteLinks = document.querySelectorAll('a[href*="/delete/"]');

    deleteLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            const confirmed = confirm("Êtes-vous sûr de vouloir supprimer cet utilisateur ?");
            if (!confirmed) {
                event.preventDefault(); // annule la navigation
            }
        });
    });
});