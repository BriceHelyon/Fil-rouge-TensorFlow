import React, { useState } from 'react';

const AddInterventionForm = ({ onSubmit }) => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [startingDate, setStartingDate] = useState("");
  const [endingDate, setEndingDate] = useState("");
  const [execution, setExecution] = useState(0); // Valeur par défaut
  const [userId, setUserId] = useState(1); // Valeur factice
  const [equipementId, setEquipementId] = useState(1); // Valeur factice

  // Fonction pour soumettre le formulaire
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Création de l'objet intervention à envoyer
    const newIntervention = {
      name,
      description,
      starting_date: startingDate,
      ending_date: endingDate,
      execution,
      user_id: userId,
      equipement_id: equipementId
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/interventions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${document.cookie.replace(/(?:(?:^|.*;\s*)authToken\s*\=\s*([^;]*).*$)|^.*$/, "$1")}` // Récupérer le token
        },
        body: JSON.stringify(newIntervention)
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Intervention ajoutée:", data);
        onSubmit(data); // Appeler la fonction de rappel avec la nouvelle intervention
      } else {
        const errorData = await response.json();
        console.log("Erreur lors de l'ajout de l'intervention:", errorData);
      }
    } catch (error) {
      console.log("Erreur lors de la soumission:", error);
    }
  };

  return (
    <div className="intervention-form-container">
      <form onSubmit={handleSubmit}>
        <h2>Ajouter une intervention</h2>
        <div>
          <label>Nom</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Date de début</label>
          <input
            type="date"
            value={startingDate}
            onChange={(e) => setStartingDate(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Date de fin</label>
          <input
            type="date"
            value={endingDate}
            onChange={(e) => setEndingDate(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Exécution</label>
          <select value={execution} onChange={(e) => setExecution(parseInt(e.target.value))}>
            <option value={0}>Standard</option>
            <option value={1}>Admin</option>
          </select>
        </div>
        <div>
          <label>ID Utilisateur</label>
          <input
            type="number"
            value={userId}
            onChange={(e) => setUserId(parseInt(e.target.value))}
          />
        </div>
        <div>
          <label>ID Équipement</label>
          <input
            type="number"
            value={equipementId}
            onChange={(e) => setEquipementId(parseInt(e.target.value))}
          />
        </div>
        <button type="submit">Ajouter</button>
      </form>
    </div>
  );
};

export default AddInterventionForm;
