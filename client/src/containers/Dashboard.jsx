import { useState } from 'react';

import Navbar from '../componants/Navbar';
import Chart, { Title, elements, plugins, scales, defaults } from "chart.js/auto";
import { Line, Bar } from "react-chartjs-2";
import Header from '../componants/Header';
defaults.responsive = true;

function Dashboard() {
  
  const [showMenu, setShowMenu] = useState(false);

  // Affiche du menu en mode responsive
  function handleShowMenu() {
    setShowMenu(!showMenu);
  }
  
  // Graphique des interventions
  const InterventionLabels = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
  const InterventionData = {
    labels: InterventionLabels,
    datasets: [{
      label: 'Nombres d\'intervention',
      data: [65, 59, 80, 81, 56, 55, 40, 84, 65, 59, 80, 81],
      fill: false,
      borderColor: 'rgb(32, 42, 84, 0.8)',  
      tension: 0.2,
      borderWidth: 7,
    }]
  };
  const InterventionOptions = {
    aspectRatio: 4,
    scales: {
      y: {
        beginAtZero: true,
      }
    },
    interaction: {
      intersect: false,
      mode: 'index',
    },
    plugins: {
      legend: {
        display: false,
      }
    },
  };
  // Graphique des dépenses
  const CostLabels = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"];
  const CostData = {
    labels: CostLabels,
    datasets: [{
      label: 'Dépense (€)',
      data: [650, 509, 800, 810, 560, 550, 400, 840, 605, 590, 800, 801],
      borderWidth: 0,
      borderRadius: 10,
      borderSkipped: false,
      backgroundColor: 'rgb(32, 42, 84, 0.8)',
    }]
  };
  const CostOptions = {
    scales: {
      y: {
        beginAtZero: true
      }
    },
    barThickness: 10,
    interaction: {
      intersect: false,
      mode: 'index',
    },
    plugins: {
      legend: {
        display: false,
      }
    }
  };

  const barPattern = {
    id: 'barPattern',
    beforeDatasetsDraw(chart, args, pluginOptions) {
      const { ctx, chartArea: {top, bottom, height}, scales: {x, y}} = chart;

      ctx.save();
      const width = chart.getDatasetMeta(0).data[0].width;

      chart.getDatasetMeta(0).data.forEach((dataPoint, index) => {
        ctx.fillStyle = "#F2F7FF";
        ctx.fillRect(x.getPixelForValue(index) - width / 2, top, width, height - 0.5)
      })
    }
  }
  
  return (
    <div className='app-content'>
      {/* Navbar */}
      <Navbar active="Dashboard" showMenu={showMenu} handleShowMenu={handleShowMenu} />

      {/* Header */}
      <Header showMenu={showMenu} handleShowMenu={handleShowMenu} />

      {/* Graphiques */}
      <main className='main-container'>
        <div className='graph-container'>
          <div className='graph-header'><p>Intervention / mois</p><p>Admin <button></button></p></div>
          <Line data={InterventionData} options={InterventionOptions}></Line>
        </div>
        <div className='graph-half-section'>
          {/* Dépense */}
          <div className='graph-container-half'>
            <div className='graph-header'><p>Dépense (€) / mois</p><p>Admin <button></button></p></div>
            <Bar data={CostData} options={CostOptions} plugins={[barPattern]}></Bar>
          </div>
          {/* Site avec le plus d'intervention */}
          <div className='graph-container-half'>
            <div className='graph-header'><p>Site avec le plus d'intervention</p></div>
            <div className='graph-item'><p>site</p><p>inter</p></div>
            <div className='graph-item'><p>site</p><p>inter</p></div>
            <div className='graph-item'><p>site</p><p>inter</p></div>
            <div className='graph-item'><p>site</p><p>inter</p></div>
            <div className='graph-item'><p>site</p><p>inter</p></div>
            <div className='graph-item'><p>site</p><p>inter</p></div>
            <div className='graph-item'><p>site</p><p>inter</p></div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Dashboard