from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.accounts.models import User
from apps.projects.models import Project

PROJECTS = [
    # --- ROUTES (16) ---
    ("Routes", "Etude technique et d'impact environnemental/social et elaboration d'un dossier d'appel d'offre pour les travaux de constructions/rehabilitation de 160 km de pistes rurales dans les poles de developpement de Tounfafi et Sabon Guida (Region de Tahoua), Sabon Machi, Djirataoua et Tessaou (Region de Maradi) et Bande (Region de Zinder). Financement ProDaf Maradi"),
    ("Routes", "Etude technique et d'impact environnemental/social et elaboration d'un dossier d'appel d'offre pour les travaux de constructions/rehabilitation de 55 km de pistes rurales dans les poles de developpement de bande et Gayi dans la region de Zinder, financement ProDaf Zinder"),
    ("Routes", "Etude de dimensionnement dans le cadre du projet d'amenagement et de bitumage de la route ILLELA-BAGAROUA-BRETELLE DANDAJIDANGONA"),
    ("Routes", "Etude technique detaillee, etude d'impact environnementale et sociale, elaboration du dossier d'appel d'offre (DAO) pour les travaux d'amenagement et de pavage de certaines rues d'Agadez"),
    ("Routes", "Etudes techniques (faisabilite technique, environnementale et sociale) sur les routes rurales dans les communes d'intervention du PARCA - Realisation de la piste Ayorou-Inates"),
    ("Routes", "Supervision et controle des travaux de construction de la route de contournement du barrage de Kandadji (40.2 km)"),
    ("Routes", "Controle et surveillance des travaux d'entretien des routes, LOT 1"),
    ("Routes", "Etudes APD et elaboration des DAO de 10 km de pistes rurales et 1 point critique - Controle des travaux de construction de 10 km de pistes et 1 point critique dans la region d'Agadez"),
    ("Routes", "Etude technique detaillees de 140 km de pistes rurales dans des collectivites locales des Regions de Louga et Diourbel (Zone 2), Senegal, Financement BAD"),
    ("Routes", "Etudes techniques des ouvrages de franchissement de la Pendjari et de la Mekrou dans le complexe WAP (Parc W et Arly), Burkina Faso, Financement Pnud (Sous-traitant GEFA)"),
    ("Routes", "Etude de faisabilite technique d'une route dans le cadre de viabilisation de Seno dans la ville de Niamey, Financement Pgrudc"),
    ("Routes", "Projet de construction d'une piste de 07km qui reliera Thiare a Senala Keur Abdou pour le compte de la communaute rurale de Thiare, Senegal"),
    ("Routes", "Projet de realisation d'une piste de 02km qui reliera la route Transgambienne au village de Diossong, Senegal"),
    ("Routes", "Projet de realisation d'une piste de 07km qui reliera Guinguineo a Ndiago, Senegal"),
    ("Routes", "Projet d'etude socio economique des routes dans la region de Sedhiou, Senegal"),
    ("Routes", "Etude de 136 km de route en terre"),
    # --- BATIMENTS (21) ---
    ("Bâtiments", "Controle de la construction d'un marche demi gros a Sarkin Haoussa et Moulle"),
    ("Bâtiments", "Etude et controle d'un marche a Iferouane"),
    ("Bâtiments", "Etude et controle d'un marche a Dannet"),
    ("Bâtiments", "Etude et controle d'une Maison de Jeune a Bilma"),
    ("Bâtiments", "Etudes techniques, elaboration de DAO pour la construction de 4 blocs de 2 salles de classe et 10 blocs de latrines scolaires a 2 cabines"),
    ("Bâtiments", "Appui a la preparation des dossiers techniques pour la rehabilitation de 7 salles de classes et leur equipement et la rehabilitation d'un logement d'astreinte pour directeur"),
    ("Bâtiments", "Etudes techniques, elaboration de DAO et controle des travaux de construction de cinq (5) parcs modernes de vaccination en elements metalliques"),
    ("Bâtiments", "Etude et Controle d'un marche a betail a Bilma"),
    ("Bâtiments", "Etude de sol et delimitation de 15 ha sur le site d'accueil des migrants"),
    ("Bâtiments", "Etude technique et controle de construction d'un foyer feminin equipe, etude technique et DAO de l'electrification solaire et controle travaux d'installation electrique et de pose des equipements solaires au foyer feminin a Tabotaki"),
    ("Bâtiments", "Etude et Controle de salle de classe a Tabotaki et Tilkorodji"),
    ("Bâtiments", "Programme d'amelioration de la gestion des defis migratoires au Niger. Projet d'etude de 5 batiments dans la region de Zinder"),
    ("Bâtiments", "Mission de suivi et de controle technique de travaux de reprise de la dalle de la galerie, l'assainissement des fosses septiques et du point d'eau de l'ecole centre 1 de Maradi"),
    ("Bâtiments", "Etude pour la construction d'une terrasse au bord du fleuve"),
    ("Bâtiments", "Etude de dimensionnement dans le cadre du projet d'amenagement et de bitumage de la route ILLELA-BAGAROUA-BRETELLE DANDAJIDANGONA"),
    ("Bâtiments", "Etude technique et d'impact environnemental/social et elaboration d'un dossier d'appel d'offre pour les travaux de constructions/rehabilitation de 55 km de pistes rurales - bande et Gayi region de Zinder"),
    ("Bâtiments", "Etude technique et d'impact environnemental/social - 160 km de pistes rurales Tounfafi, Sabon Guida, Sabon Machi, Djirataoua, Tessaou et Bande"),
    ("Bâtiments", "Etudes techniques des ouvrages de franchissement de la Pendjari et de la Mekrou dans le complexe WAP"),
    ("Bâtiments", "Projet de construction d'une piste de 07km Thiare a Senala Keur Abdou, Senegal"),
    ("Bâtiments", "Mission de suivi et de controle techniques de travaux d'Eau, Hygiene et Assainissement du lot E de la region de Tahoua"),
    ("Bâtiments", "Mission de suivi et de controle techniques de travaux d'Eau, Hygiene et Assainissement du lot A de la region d'Agadez"),
    # --- HYDRAULIQUE (14) ---
    ("Hydraulique", "Etude ouvrages hydrauliques a Tillia"),
    ("Hydraulique", "Etude de faisabilite Infrastructure pour l'amelioration de l'EFTP, des Moyens de Subsistance et de la Cohesion Sociale dans les communes de Makalondi, Diagourou et Tera, Niger"),
    ("Hydraulique", "Etude de faisabilite (Socio economique et technique) et/ou le controle de travaux de 3 nouvelles Mini Adductions d'Eau Potable (Mini-AEP) Multi Villages solaires et 3 nouvelles Mini-AEP Simples Solaires"),
    ("Hydraulique", "Evaluation Rapide Des besoins en WASH et Electrification pour l'amelioration de la qualite des services dans les CSIs et Cases de Sante des Communes de Kornaka et Sabon Machi"),
    ("Hydraulique", "Etudes de faisabilite techniques, environnementale et sociale des infrastructures hydrauliques (mini AEP et poste d'eau) dans les communes d'intervention du PARCA dans les regions de Tahoua et Tillabery"),
    ("Hydraulique", "Suivi et controle des travaux de 17 multi villages dans les regions de Maradi et Zinder par les bureaux d'etudes lot 1 Zinder"),
    ("Hydraulique", "Controle de 10 Mini AEP Multivillage"),
    ("Hydraulique", "Suivi et controle des travaux de rehabilitation de 3 mini AEP dans la commune rurale de Bazaga"),
    ("Hydraulique", "Suivi et controle des travaux de rehabilitation de 4 mini AEP dans la commune de Konni"),
    ("Hydraulique", "Etudes et de Controle pour la fourniture d'une assistance technique aux acteurs WASH intervenant dans la Region de Diffa"),
    ("Hydraulique", "Etudes diagnostiques techniques et sociales pour les infrastructures hydrauliques a realiser/rehabiliter au niveau communautaire, des ecoles et des centres de sante dans les regions d'Agadez, Diffa, Dosso, Maradi, Tahoua, Tillabery et Zinder"),
    ("Hydraulique", "Mission de suivi et de controle techniques de travaux d'Eau, Hygiene et Assainissement du lot E de la region de Tahoua"),
    ("Hydraulique", "Mission de suivi et de controle techniques de travaux d'Eau, Hygiene et Assainissement du lot A de la region d'Agadez"),
    ("Hydraulique", "Etudes techniques des ouvrages de franchissement de la Pendjari et de la Mekrou dans le complexe WAP (Parc W et Arly)"),
    # --- AMENAGEMENT (6) ---
    ("Aménagement", "Etude ouvrages hydrauliques a Tillia"),
    ("Aménagement", "Etude technique en vue de la rehabilitation de la digue de protection de Mombeye Tounga dans la commune rurale de Tanda dans le departement de Gaya"),
    ("Aménagement", "Les etudes de mise en valeur du potentiel agricole autour des 15 seuils realises dans le cadre du projet Badaguichiri et l'identification des besoins d'accompagnement dans la Region de Tahoua"),
    ("Aménagement", "Etude de faisabilite Infrastructure pour l'amelioration de l'EFTP, des Moyens de Subsistance et de la Cohesion Sociale dans les communes de Makalondi, Diagourou et Tera"),
    ("Aménagement", "Surveillance et controle des travaux de construction de cinq (5) seuils d'epandage dans les PDE de Guidan Roumdji et Djirataoua, Region de Maradi"),
    ("Aménagement", "Surveillance et controle des travaux de construction de quatre (4) seuils d'epandage dans les PDE de Guidan Roumdji, Djirataoua et Sabon Machi, Region de Maradi"),
    # --- ETUDES (6) ---
    ("Études", "Etude de faisabilite Infrastructure pour l'amelioration de l'EFTP, des Moyens de Subsistance et de la Cohesion Sociale dans les communes de Makalondi, Diagourou et Tera, Niger"),
    ("Études", "Etudes de mise en valeur du potentiel agricole autour des 15 seuils realises dans le cadre du projet Badaguichiri et l'identification des besoins d'accompagnement dans la region de Tahoua"),
    ("Études", "Etude ouvrages hydrauliques a Tillia"),
    ("Études", "Etude de faisabilite (Socio economique et technique) et/ou le controle de travaux de 3 nouvelles Mini-AEP Multi Villages solaires et 3 nouvelles Mini-AEP Simples Solaires"),
    ("Études", "Etude de dimensionnement dans le cadre du projet d'amenagement et de bitumage de la route ILLELA-BAGAROUA-BRETELLE DANDAJIDANGON"),
    ("Études", "Etudes techniques (faisabilite technique, environnementale et sociale) sur les routes rurales dans les communes d'intervention du PARCA - Realisation de la piste Ayorou-Inates"),
]


def _detect_location(title):
    title_lower = title.lower()
    if "senegal" in title_lower or "sénégal" in title_lower:
        return "Sénégal"
    if "burkina" in title_lower:
        return "Burkina Faso"
    return "Niger"


class Command(BaseCommand):
    help = "Seed 63 projects across 5 categories from old site content"

    def handle(self, *args, **options):
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            self.stderr.write(self.style.ERROR("No superuser found. Create one first."))
            return

        counts = {}
        seen_slugs = set()

        for category, title in PROJECTS:
            base_slug = slugify(title)[:255]
            slug = base_slug
            suffix = 1
            while slug in seen_slugs or Project.objects.filter(slug=slug).exclude(category=category).exists():
                slug = f"{base_slug[:250]}-{suffix}"
                suffix += 1
            seen_slugs.add(slug)

            _, created = Project.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": title[:255],
                    "description": title if len(title) > 255 else "",
                    "category": category,
                    "location": _detect_location(title),
                    "published": True,
                    "created_by": superuser,
                },
            )

            if created:
                counts[category] = counts.get(category, 0) + 1

        total = sum(counts.values())
        for cat, count in sorted(counts.items()):
            self.stdout.write(f"  {cat}: {count}")
        self.stdout.write(self.style.SUCCESS(f"Total created: {total}"))
