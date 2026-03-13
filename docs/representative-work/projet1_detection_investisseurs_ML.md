# Projet 1 : Détection des Investisseurs à Long Terme avec l'Apprentissage Automatique

**Auteur :** SOME Fiarma Landry  
**Date d'achèvement :** Juillet 2024  
**Compétition :** Amdari Data Science Challenge — Entreprise nigériane spécialisée en Data Science & IA  
**Liens :**
- Portfolio : *(TODO : remplacer par le lien exact vers la page du projet dans votre portfolio)*
- Code source (GitHub) : *(TODO : remplacer par le lien exact vers votre dépôt GitHub public)*

---

## 1. Introduction et Contexte

Ce projet a été réalisé en juillet 2024 dans le cadre d'une compétition de Data Science organisée par **Amdari**, une entreprise nigériane spécialisée dans la science des données et l'intelligence artificielle.

Le défi proposé portait sur **EliteBank**, une institution bancaire fictive confrontée à un problème stratégique majeur : sa stratégie marketing s'avérait coûteuse et peu efficace face à un marché en pleine croissance. Afin d'améliorer ses performances commerciales et d'optimiser l'allocation de ses ressources, la direction souhaitait identifier en amont les clients les plus susceptibles de devenir des **déposants et investisseurs à long terme**.

---

## 2. Objectifs du Projet

Les objectifs définis pour ce challenge sont les suivants :

1. **Développer un modèle prédictif** capable d'estimer la probabilité qu'un client devienne un investisseur à long terme.
2. **Sélectionner et concevoir des variables** (*feature selection* et *feature engineering*) pertinentes pour la détection.
3. **Explorer l'interprétabilité des modèles** (*Explainable AI*) afin de démystifier les prédictions.
4. **Maximiser la spécificité** du modèle pour minimiser les faux négatifs coûteux pour la banque.

---

## 3. Données Utilisées

Les données fournies couvrent trois catégories d'informations clients :

| Catégorie | Variables |
|-----------|-----------|
| **Informations démographiques** | Âge, profession, situation matrimoniale, niveau d'éducation |
| **Historique financier** | Solde du compte, historique des dépôts, présence de prêts immobiliers ou personnels, défauts de paiement |
| **Données de campagnes marketing** | Type de contact, durée des appels téléphoniques, nombre de contacts, résultats des campagnes précédentes |
| **Variable cible** | Dépôt effectué ou non (variable binaire) |

---

## 4. Méthodologie

### 4.1 Analyse Exploratoire des Données (EDA)

L'EDA a permis de dresser un portrait détaillé de la clientèle et d'identifier des patterns significatifs :

- **Qualité des données :** aucune valeur manquante ni doublon ; nettoyage des incohérences effectué.
- **Variables catégorielles :** encodage nécessaire pour les variables telles que l'emploi, la situation matrimoniale, l'éducation et le résultat des campagnes précédentes.
- **Corrélations :** faible corrélation entre les variables indépendantes (garantie d'indépendance des caractéristiques) et corrélation modérée avec la variable cible.
- **Démographie :** la majorité des clients est âgée de 25 à 35 ans ; les gestionnaires, ouvriers et techniciens sont les profils les plus représentés.
- **Comportement d'investissement :** les retraités sont statistiquement plus enclins à effectuer des dépôts d'investissement que les jeunes actifs.
- **Analyse des campagnes :** les appels d'une durée d'environ 250 secondes (~4 minutes) corrèlent positivement avec les souscriptions réussies.

### 4.2 Préparation des Données

Sur la base des résultats de l'EDA, les étapes suivantes ont été appliquées :

- **Division des données** en ensembles d'entraînement et de test (stratifiée pour respecter la distribution de la variable cible).
- **Encodage des variables catégorielles** (*Label Encoding* et *One-Hot Encoding*).
- **Normalisation / standardisation** des variables numériques présentant des amplitudes importantes (solde du compte, durée des appels).

### 4.3 Modélisation

Trois algorithmes ont été comparés :

| Modèle | Justification du choix |
|--------|------------------------|
| **Régression Logistique** | Modèle de référence, interprétable, rapide |
| **ExtraTreesClassifier** | Ensemble basé sur les arbres, robuste aux valeurs aberrantes |
| **CatBoostClassifier** | Gradient boosting optimisé pour les variables catégorielles |

Les métriques d'évaluation retenues sont : **Précision**, **Rappel (Recall)**, **F1-Score** et **Exactitude (Accuracy)**.

---

## 5. Résultats

| Modèle | Accuracy | Précision | Rappel | F1-Score |
|--------|----------|-----------|--------|----------|
| Régression Logistique | 83 % | 83 % | 80–85 % | 82–84 % |
| ExtraTreesClassifier | 84 % | 82–85 % | 83–84 % | 83–84 % |
| **CatBoostClassifier** | **94 %** | **92–95 %** | **93–95 %** | **94 %** |

Le **CatBoostClassifier** a obtenu les meilleures performances avec une exactitude de **94 %** et un F1-Score de **94 %**.

Cependant, après une analyse approfondie des compromis (biais-variance, vitesse d'entraînement et explicabilité), la **Régression Logistique** a été recommandée pour un déploiement en production, en raison de :
- Sa meilleure capacité de généralisation (erreur de généralisation plus faible),
- Sa rapidité d'entraînement et d'inférence,
- Son explicabilité supérieure, essentielle dans un contexte bancaire réglementé.

---

## 6. Recommandations

### Basées sur l'EDA

- **Durée des appels :** privilégier des appels d'environ 250 secondes (~4 minutes) pour maximiser le taux de souscription.
- **Timing des campagnes :** contacter les clients dès le lancement d'une nouvelle campagne.
- **Ciblage des retraités :** adapter les offres d'investissement à ce segment, statistiquement plus enclin à investir.
- **Stratégies de prêts immobiliers :** proposer des mécanismes de subdivision et de remboursement facilité pour fidéliser les clients endettés.

### Basées sur la Modélisation

- Explorer des méthodes d'optimisation hyperparamétrique plus avancées : **RandomizedSearchCV** ou **optimisation bayésienne**.
- Tester d'autres algorithmes de boosting tels que **LightGBM** ou des architectures de Deep Learning adaptées aux données tabulaires (**TabNet**).
- Développer une interface utilisateur simple permettant aux équipes de télémarketing de visualiser et prioriser les scores clients.

---

## 7. Outils et Technologies Utilisés

| Outil | Usage |
|-------|-------|
| **Python** | Langage de programmation principal |
| **NumPy** | Calcul numérique |
| **Pandas** | Manipulation et analyse des données |
| **Matplotlib / Seaborn** | Visualisation des données |
| **Scikit-learn** | Régression Logistique, ExtraTreesClassifier, métriques |
| **CatBoost** | CatBoostClassifier |

---

## 8. Conclusion

Ce projet illustre la capacité à mener de bout en bout un projet de Data Science appliqué à la finance : de la compréhension du problème métier à la recommandation actionnable, en passant par l'analyse exploratoire, l'ingénierie des variables et la modélisation comparative. Il démontre l'articulation entre les fondements mathématiques (statistiques, algèbre linéaire, optimisation) et leur mise en œuvre computationnelle dans un contexte réel et compétitif.

---

## Déclaration d'Intégrité

Je certifie que l'intégralité de ce travail est le mien. Ce projet a été réalisé **individuellement** dans le cadre d'une compétition de Data Science organisée par Amdari en juillet 2024, sans collaboration avec d'autres participants.

**SOME Fiarma Landry**

---

## Motivation pour le Travail Représentatif #1 *(proposition pour le formulaire AIMS)*

> *Texte à copier dans le champ "Motivation for representative work #1" du formulaire AIMS :*

---

J'ai choisi ce projet car il représente, à mes yeux, la synthèse la plus complète de mes compétences en mathématiques appliquées et en informatique. Il couvre l'intégralité du pipeline d'un projet de science des données : formulation mathématique du problème, analyse statistique exploratoire, prétraitement des données, comparaison de modèles et interprétation des résultats. À travers la sélection et l'ingénierie des variables, j'ai mobilisé des concepts d'algèbre linéaire, de statistiques inférentielles et d'optimisation que j'ai appris lors de mes études. La comparaison des trois algorithmes — régression logistique, forêts d'arbres extrêmement aléatoires et gradient boosting — m'a permis d'approfondir ma compréhension des compromis biais-variance et de l'importance de l'interprétabilité des modèles dans des applications à fort enjeu comme la finance. Je suis particulièrement fier de ce travail car il a été réalisé dans le cadre d'une compétition internationale organisée par Amdari (Nigeria), ce qui m'a permis de confronter mes capacités à celles d'autres praticiens de la science des données à l'échelle africaine et internationale. Ce projet est entièrement mon travail personnel, réalisé de façon individuelle et autonome.

*(Nombre de mots approximatif : ~180)*
