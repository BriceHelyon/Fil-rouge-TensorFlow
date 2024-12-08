import Navbar from '../componants/Navbar';
import '../assets/scss/user.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

function User() {
  const users = [
    { id: 1, nom: 'Dupont', prenom: 'Martin', role: 'Admin', email: 'martindupont@example.com', profession: 'Maintenance' },
    { id: 2, nom: 'Durand', prenom: 'Sophie', role: 'Utilisateur', email: 'sophiedurand@example.com', profession: 'Électricienne' },
    { id: 3, nom: '...', prenom: '...', role: '...', email: '...', profession: '...' },
    { id: 4, nom: '...', prenom: '...', role: '...', email: '...', profession: '...' },
    { id: 5, nom: '...', prenom: '...', role: '...', email: '...', profession: '...' },
  ];

  return (
    <div className="user-container app-content">
      {/* Navbar */}
      <Navbar active="user" />

      <div className='card-container'>
        <div className='card-header'>
          <h2>Liste des Utilisateurs</h2>
          <div className="search-container">
            <input type="text" placeholder="Rechercher..." />
            <FontAwesomeIcon icon={faSearch} className="search-icon" />
          </div>
        </div>
        <table className="user-table">
          <thead>
            <tr>
              <th>Nom</th>
              <th>Prénom</th>
              <th>Rôle</th>
              <th>E-mail</th>
              <th>Profession</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id}>
                <td>{user.nom}</td>
                <td>{user.prenom}</td>
                <td>{user.role}</td>
                <td>{user.email}</td>
                <td>{user.profession}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default User;