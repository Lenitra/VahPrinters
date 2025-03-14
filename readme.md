# 📌 Projet : Plateforme de Devis & Boutique en Ligne pour Impression 3D

## 🚀 Objectif du Projet
Développer une plateforme où les visiteurs peuvent :
1. **Demander un devis** pour une impression 3D.
2. **Acheter des objets imprimés en 3D** via une boutique en ligne.

Les **printers** (imprimeurs 3D) peuvent consulter les demandes de devis et en prendre en charge une pour contacter directement le client.

---

## 🛠️ Fonctionnalités Clés

### 1️⃣ Demande de Devis
#### ✅ Côté Visiteur :
- **Formulaire de soumission** :
  - Téléversement de fichiers 3D (STL, OBJ…).
  - Sélection des options (matériau, finition, couleur…).
  - Saisie des coordonnées et description du projet.
- **Envoi automatique d’e-mails** :
  - 📩 **Confirmation de soumission** → Accusé de réception au client.
  - 📩 **Notification d’attribution** → Un printer a pris en charge le devis.
  - 📨 **Contact direct** → Le printer contacte ensuite manuellement le client.

#### ✅ Côté Printer :
- **Tableau de bord** listant les devis en attente.
- **Possibilité de réserver un devis** (un seul printer par devis).
- **Historique des devis traités**.
- **Aucune gestion des paiements sur la plateforme** → tout est géré directement entre le printer et le client.

---

### 2️⃣ Boutique en Ligne (Implémenté plus tard)
- **Catalogue de produits imprimés en 3D**.
- **Paiement en ligne sécurisé** (Stripe, PayPal).
- **Gestion des commandes et suivi des expéditions**.
- **Pas de personnalisation de produits** (contrairement aux devis).
