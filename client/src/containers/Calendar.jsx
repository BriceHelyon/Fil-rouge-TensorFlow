import React, { useState, useEffect } from "react";
import Fullcalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import frLocale from "@fullcalendar/core/locales/fr"; // Importer la locale française
import Navbar from '../componants/Navbar';
import { useNavigate } from "react-router-dom"; // Importer useNavigate
import AddInterventionForm from '../componants/AddInterventionForm';
import env from '.././environment';

// Fonction pour récupérer le token dans les cookies
const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
};

function Calendar() {
  const navigate = useNavigate();
  const [events, setEvents] = useState([]); // État pour stocker les événements
  const [interventions, setInterventions] = useState([]); // État pour stocker les interventions de la journée sélectionnée
  const [selectedDate, setSelectedDate] = useState(""); // État pour stocker la date sélectionnée
  const [selectedCell, setSelectedCell] = useState(null); // État pour suivre la cellule cliquée

  // Fonction pour obtenir la date d'aujourd'hui au format YYYY-MM-DD
  const getTodayDate = () => {
    const today = new Date();
    return today.toISOString().split("T")[0];
  };

  // Fonction pour récupérer les interventions depuis l'API
  const fetchInterventions = async () => {
    try {
      const token = getCookie("authToken"); // Récupérer le token JWT dans les cookies
      if (!token) {
        navigate("/login");
        console.log("Aucun token trouvé.");
        return;
      }
      
      const response = await fetch(env.REACT_APP_PSQL_HOST+"interventions", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`, // Envoyer le token JWT dans les headers
        },
      });

      if (response.ok) {
        const data = await response.json(); // Les données récupérées depuis l'API
        console.log("Interventions:", data);

        // Transformer les interventions en format d'événements pour FullCalendar
        const formattedEvents = data.map((intervention) => ({
          id: intervention.id,
          title: intervention.name,
          start: intervention.starting_date,
          end: intervention.ending_date,
          description: intervention.description,
        }));

        setEvents(formattedEvents); // Mettre à jour l'état avec les événements formatés

        // Filtrer les interventions pour n'afficher que celles du jour actuel
        const today = getTodayDate();
        const interventionsOfToday = formattedEvents.filter((event) =>
          event.start.startsWith(today)
        );
        setInterventions(interventionsOfToday); // Afficher les interventions du jour par défaut

        // Mettre la date du jour dans l'état
        const todayFormatted = new Date(today).toLocaleDateString("fr-FR", {
          weekday: "long",
          month: "long",
          day: "numeric",
        });
        setSelectedDate(todayFormatted); // Afficher la date du jour actuel
      } else {
        navigate("/login");
        console.log("Erreur lors de la récupération des interventions.");
      }
    } catch (error) {
      navigate("/login");
      console.log("Erreur:", error);
    }
  };

  // Utiliser useEffect pour appeler l'API lorsque le composant est monté
  useEffect(() => {
    fetchInterventions(); // Appeler l'API lors du chargement de la page
  }, []);

  // Fonction pour gérer le clic sur un jour du calendrier
  const handleDateClick = (info) => {
    // Filtrer les interventions en fonction de la date sélectionnée
    const interventionsOfDay = events.filter((event) =>
      event.start.startsWith(info.dateStr)
    );
    setInterventions(interventionsOfDay); // Mettre à jour le tableau avec les interventions du jour

    // Mettre à jour la date sélectionnée dans le bon format
    const selected = new Date(info.dateStr);
    const options = { weekday: "long", month: "long", day: "numeric" }; // Format du jour en français
    const formattedDate = selected.toLocaleDateString("fr-FR", options);
    setSelectedDate(formattedDate); // Mettre à jour l'état avec la date formatée

    // Gérer la classe pour la cellule cliquée
    if (selectedCell) {
      selectedCell.classList.remove("selected-cell"); // Retirer la classe de la cellule précédente
    }
    setSelectedCell(info.dayEl); // Stocker la nouvelle cellule sélectionnée
    info.dayEl.classList.add("selected-cell"); // Ajouter la classe à la nouvelle cellule cliquée
  };

  return (
    <div className="app-content">
      {/* Navbar */}
      <Navbar active="calendar" />

      <div className="calendar-container">
        <Fullcalendar
          plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
          initialView={"dayGridMonth"}
          headerToolbar={{
            start: "prev,next",
            center: "title",
            end: "",
          }}
          height={"auto"}
          events={events}
          firstDay={1}
          locale={frLocale} // Utilisation de la langue française
          dateClick={handleDateClick} // Gestion du clic sur une date
          showNonCurrentDates={false} // Ne pas afficher les jours du mois précédent/suivant
        />
      </div>

      {/* Tableau des interventions du jour sélectionné */}
      <div className="intervention-table-container">
        <h3>
          {selectedDate
            ? `Interventions du ${selectedDate}`
            : "Interventions du jour"}
        </h3>
        <AddInterventionForm></AddInterventionForm>
        <table className="intervention-table">
          <thead>
            <tr>
              <th>Nom</th>
              <th>Description</th>
              <th>Date de début</th>
              <th>Date de fin</th>
            </tr>
          </thead>
          <tbody>
            {interventions.length > 0 ? (
              interventions.map((intervention) => (
                <tr key={intervention.id}>
                  <td>{intervention.title}</td>
                  <td>{intervention.description}</td>
                  <td>{new Date(intervention.start).toLocaleDateString("fr-FR")}</td>
                  <td>{new Date(intervention.end).toLocaleDateString("fr-FR")}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td class='no-intervention' colSpan="4">Aucune intervention pour cette journée.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Calendar;
