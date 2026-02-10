from django.db import models


class ProjectCategory(models.TextChoices):
    ROUTES = "Routes", "Routes et voiries"
    BATIMENTS = "Bâtiments", "Bâtiments et structures"
    HYDRAULIQUE = "Hydraulique", "Hydraulique et assainissement"
    AMENAGEMENT = "Aménagement", "Aménagements urbains"
    ETUDES = "Études", "Études techniques"


class ProjectStatus(models.TextChoices):
    EN_COURS = "En cours", "En cours"
    TERMINE = "Terminé", "Terminé"
    EN_ATTENTE = "En attente", "En attente"


class ContactStatus(models.TextChoices):
    PENDING = "Pending", "En attente"
    IN_PROGRESS = "In Progress", "En cours"
    RESOLVED = "Resolved", "Résolu"


class AccessLevel(models.TextChoices):
    VIEW = "view", "Lecture"
    COMMENT = "comment", "Commentaire"
    EDIT = "edit", "Édition"


class Department(models.TextChoices):
    DIRECTION = "direction", "Direction Générale"
    RECHERCHE = "recherche", "Recherche, Innovation, Qualité"
    ADMIN = "admin", "Administratif"
    ETUDES = "etudes", "Études, Maîtrise d'Oeuvre, Contrôles Extérieurs"
    LABORATOIRE = "laboratoire", "Laboratoire"


class Division(models.TextChoices):
    RH_COMM = "rh_comm", "Ressource Humaine, Communication, Marketing"
    COMPTABLE = "comptable", "Comptable et Développement"
    BETON = "beton", "Béton"
    ENVIRONNEMENT = "environnement", "Environnement, Hydrogéologie, Pédologie, Bitume"
    GEOTECHNIQUE = "geotechnique", "Géotechnique Routière et Bâtiment"


class TemplateCategory(models.TextChoices):
    QUOTE = "quote_request", "Demande de devis"
    INQUIRY = "project_inquiry", "Demande projet"
    INFO = "general_info", "Information générale"
    CUSTOM = "custom", "Personnalisé"
