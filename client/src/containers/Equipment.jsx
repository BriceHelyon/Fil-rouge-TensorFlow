import Navbar from '../componants/Navbar';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

function Equipment() {
  const equipments = [
    { id: 1, code_mat: '001454', organisation: 'Stade Océance', materiel: 'Surpresseur', nature_intervention: 'Maintenance préventive', code_marque: 'ELBAC_CABLE', status: 'Active' },
    { id: 2, code_mat: '002563', organisation: 'Laverie', materiel: 'Hotte laverie', nature_intervention: 'Maintenance corrective', code_marque: 'FRANCE_AIR', status: 'Inactive' },
    { id: 3, code_mat: '...', organisation: '...', materiel: '...', nature_intervention: '...', code_marque: '...', status: '...' },
    { id: 4, code_mat: '...', organisation: '...', materiel: '...', nature_intervention: '...', code_marque: '...', status: '...' },
    { id: 5, code_mat: '...', organisation: '...', materiel: '...', nature_intervention: '...', code_marque: '...', status: '...' },
  ];
  return (
    <div className="user-container app-content">
      {/* Navbar */}
      <Navbar active="equipments" />

      <div className='card-container'>
        <div className='card-header'>
          <h2>Liste des équipements</h2>
          <div className="search-container">
            <input type="text" placeholder="Rechercher..." />
            <FontAwesomeIcon icon={faSearch} className="search-icon" />
          </div>
        </div>
        <table className="user-table">
          <thead>
            <tr>
              <th>Code matériel</th>
              <th>Organisation</th>
              <th>Matériel</th>
              <th>Nature d'intervention</th>
              <th>Code marque</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {equipments.map(equipment => (
              <tr key={equipment.id}>
                <td>{equipment.code_mat}</td>
                <td>{equipment.organisation}</td>
                <td>{equipment.materiel}</td>
                <td>{equipment.nature_intervention}</td>
                <td>{equipment.code_marque}</td>
                <td className={equipment.status === 'Active' ? 'active-row' : 'inactive-row'}>
                    {equipment.status}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Equipment