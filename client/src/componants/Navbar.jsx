import { Link } from 'react-router-dom';
import logo from '../assets/img/logo.png';
import userIcon from '../assets/img/user-icon.jpg';
import close from '../assets/img/close.svg';

function Navbar({ active, showMenu, handleShowMenu }) {

  // Fonction handleOut
  // appel la fonction logOut
  function handleOut() {
    // user.logOut();
  }

  return (
    <aside className={showMenu ? "navbar show" : "navbar"}>
      <div className="navbar__container">
        <div className="menu close">
          <div className={showMenu ? "menu__icon" : "menu__icon show"} onClick={handleShowMenu}>
            <img src={close} alt="menu icon" />
          </div>
        </div>
        <div className='toggle'>
          <img src={logo} alt="Logo Dashboard" />
        </div>
        <Link to="/dashboard" className={active == "Dashboard" ? "navbar__container-item active" : "navbar__container-item"}>
          <div className='navbar__container-item-link'>
            <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9.4 25H16.6C22.6 25 25 22.6 25 16.6V9.4C25 3.4 22.6 1 16.6 1H9.4C3.4 1 1 3.4 1 9.4V16.6C1 22.6 3.4 25 9.4 25Z" stroke={active == "Dashboard" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M18.136 14.932C16.78 16.288 14.836 16.708 13.12 16.168L10.012 19.264C9.79598 19.492 9.35198 19.636 9.02798 19.588L7.58798 19.396C7.10798 19.336 6.67598 18.88 6.60398 18.412L6.41198 16.972C6.36398 16.66 6.51998 16.216 6.73598 15.988L9.83198 12.892C9.30398 11.176 9.71198 9.23203 11.068 7.87603C13.012 5.93203 16.18 5.93203 18.136 7.87603C20.08 9.80803 20.08 12.976 18.136 14.932Z" stroke={active == "Dashboard" ? "white" : "#9197B3"} strokeWidth="2" strokeMiterlimit="10" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M11.14 18.136L10.1199 17.104" stroke={active == "Dashboard" ? "white" : "#9197B3"} strokeWidth="2" strokeMiterlimit="10" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M14.6734 11.44H14.684" stroke={active == "Dashboard" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <h3>Dashboard</h3>
          </div>
          <i className='bx bx-chevron-right bx-sm' />
        </Link>

        <Link to="/equipements" className={active == "equipments" ? "navbar__container-item active" : "navbar__container-item"}>
          <div className='navbar__container-item-link'>
            <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9.4 25H16.6C22.6 25 25 22.6 25 16.6V9.4C25 3.4 22.6 1 16.6 1H9.4C3.4 1 1 3.4 1 9.4V16.6C1 22.6 3.4 25 9.4 25Z" stroke={active == "equipments" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M6.63995 9.71201L12.9999 13.396L19.3119 9.73601" stroke={active == "equipments" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M13 19.9241V13.3841" stroke={active == "equipments" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M11.512 6.14799L7.67202 8.28399C6.80802 8.76399 6.08801 9.97599 6.08801 10.972V15.04C6.08801 16.036 6.79602 17.248 7.67202 17.728L11.512 19.864C12.328 20.32 13.672 20.32 14.5 19.864L18.34 17.728C19.204 17.248 19.924 16.036 19.924 15.04V10.96C19.924 9.96399 19.216 8.75199 18.34 8.27199L14.5 6.13599C13.672 5.67999 12.328 5.67999 11.512 6.14799Z" stroke={active == "equipments" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <h3>Équipements</h3>
          </div>
          <i className='bx bx-chevron-right bx-sm' />
        </Link>

        <Link to="/calendrier" className={active == "calendar" ? "navbar__container-item active" : "navbar__container-item"}>
          <div className='navbar__container-item-link'>
            <svg width="24" height="27" viewBox="0 0 24 27" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M14.7692 4.61538C14.7692 5.12518 15.1825 5.53846 15.6923 5.53846C16.2021 5.53846 16.6154 5.12518 16.6154 4.61538H14.7692ZM16.6154 0.923077C16.6154 0.41328 16.2021 0 15.6923 0C15.1825 0 14.7692 0.41328 14.7692 0.923077H16.6154ZM7.38462 4.61538C7.38462 5.12518 7.7979 5.53846 8.30769 5.53846C8.81749 5.53846 9.23077 5.12518 9.23077 4.61538H7.38462ZM9.23077 0.923077C9.23077 0.41328 8.81749 0 8.30769 0C7.7979 0 7.38462 0.41328 7.38462 0.923077H9.23077ZM12 24.6154C9.67188 24.6154 7.99999 24.6142 6.70528 24.4738C5.42785 24.3354 4.62759 24.0706 4.00235 23.6164L2.91721 25.1099C3.90961 25.831 5.07193 26.1538 6.50644 26.3093C7.92367 26.4628 9.71299 26.4615 12 26.4615V24.6154ZM3.34538e-07 14.4615C3.34538e-07 16.7486 -0.00126743 18.5378 0.152283 19.9551C0.307705 21.3897 0.630548 22.5519 1.35157 23.5444L2.84514 22.4592C2.39088 21.834 2.12609 21.0337 1.98769 19.7563C1.84742 18.4615 1.84615 16.7897 1.84615 14.4615H3.34538e-07ZM4.00235 23.6164C3.55829 23.2938 3.16778 22.9033 2.84514 22.4592L1.35157 23.5444C1.78807 24.1451 2.31642 24.6735 2.91721 25.1099L4.00235 23.6164ZM21.1548 22.4592C20.8322 22.9033 20.4417 23.2938 19.9977 23.6164L21.0828 25.1099C21.6836 24.6735 22.2119 24.1451 22.6484 23.5444L21.1548 22.4592ZM24 14.4615C24 12.1745 24.0012 10.3852 23.8478 8.96798C23.6923 7.53346 23.3695 6.37115 22.6484 5.37875L21.1548 6.46389C21.6091 7.08913 21.8738 7.88939 22.0123 9.16682C22.1526 10.4615 22.1538 12.1334 22.1538 14.4615H24ZM19.9977 5.30668C20.4417 5.62932 20.8322 6.01983 21.1548 6.46389L22.6484 5.37875C22.2119 4.77796 21.6836 4.24961 21.0828 3.81311L19.9977 5.30668ZM1.84615 14.4615C1.84615 12.1334 1.84742 10.4615 1.98769 9.16682C2.12609 7.88939 2.39088 7.08913 2.84514 6.46389L1.35157 5.37875C0.630548 6.37115 0.307705 7.53346 0.152283 8.96798C-0.00126743 10.3852 3.34538e-07 12.1745 3.34538e-07 14.4615H1.84615ZM2.91721 3.81311C2.31642 4.24961 1.78807 4.77796 1.35157 5.37875L2.84514 6.46389C3.16778 6.01983 3.55829 5.62932 4.00235 5.30668L2.91721 3.81311ZM20.7391 17.3179C17.7109 17.7975 15.336 20.1724 14.8564 23.2006L16.6798 23.4895C17.0343 21.2512 18.7897 19.4959 21.0279 19.1413L20.7391 17.3179ZM9.23077 4.61538V3.42022H7.38462V4.61538H9.23077ZM9.23077 3.42022V0.923077H7.38462V3.42022H9.23077ZM12 2.46154C10.5664 2.46154 9.33445 2.46143 8.27609 2.49769L8.3393 4.34276C9.35932 4.3078 10.5562 4.30769 12 4.30769V2.46154ZM8.27609 2.49769C5.9703 2.57669 4.27557 2.82622 2.91721 3.81311L4.00235 5.30668C4.87072 4.67578 6.05631 4.42097 8.3393 4.34276L8.27609 2.49769ZM16.6154 4.61538V3.42022H14.7692V4.61538H16.6154ZM16.6154 3.42022V0.923077H14.7692V3.42022H16.6154ZM12 4.30769C13.4438 4.30769 14.6407 4.3078 15.6607 4.34276L15.7239 2.49769C14.6656 2.46143 13.4336 2.46154 12 2.46154V4.30769ZM15.6607 4.34276C17.9436 4.42097 19.1292 4.67578 19.9977 5.30668L21.0828 3.81311C19.7244 2.82622 18.0297 2.57669 15.7239 2.49769L15.6607 4.34276ZM23.0414 17.2308C21.9554 17.2308 21.302 17.2288 20.7391 17.3179L21.0279 19.1413C21.4117 19.0805 21.8878 19.0769 23.0414 19.0769V17.2308ZM22.1538 14.4615C22.1538 15.9054 22.1537 17.1023 22.1188 18.1222L23.9638 18.1855C24.0001 17.1271 24 15.8951 24 14.4615H22.1538ZM22.1188 18.1222C22.0406 20.4052 21.7857 21.5908 21.1548 22.4592L22.6484 23.5444C23.6353 22.186 23.8848 20.4912 23.9638 18.1855L22.1188 18.1222ZM16.6154 25.5029C16.6154 24.3493 16.619 23.8732 16.6798 23.4895L14.8564 23.2006C14.7673 23.7636 14.7692 24.417 14.7692 25.5029H16.6154ZM12 26.4615C13.4336 26.4615 14.6656 26.4617 15.7239 26.4254L15.6607 24.5803C14.6407 24.6153 13.4438 24.6154 12 24.6154V26.4615ZM15.7239 26.4254C18.0297 26.3463 19.7244 26.0969 21.0828 25.1099L19.9977 23.6164C19.1292 24.2473 17.9436 24.5022 15.6607 24.5803L15.7239 26.4254Z" fill={active == "calendar" ? "white" : "#9197B3"} />
              <path d="M7.07689 9.53851C7.07689 10.2182 6.52585 10.7693 5.84613 10.7693C5.1664 10.7693 4.61536 10.2182 4.61536 9.53851C4.61536 8.85878 5.1664 8.30774 5.84613 8.30774C6.52585 8.30774 7.07689 8.85878 7.07689 9.53851Z" fill={active == "calendar" ? "white" : "#9197B3"} />
              <path d="M7.07689 14.4615C7.07689 15.1413 6.52585 15.6923 5.84613 15.6923C5.1664 15.6923 4.61536 15.1413 4.61536 14.4615C4.61536 13.7818 5.1664 13.2308 5.84613 13.2308C6.52585 13.2308 7.07689 13.7818 7.07689 14.4615Z" fill={active == "calendar" ? "white" : "#9197B3"} />
              <path d="M13.2308 9.53851C13.2308 10.2182 12.6797 10.7693 12 10.7693C11.3202 10.7693 10.7692 10.2182 10.7692 9.53851C10.7692 8.85878 11.3202 8.30774 12 8.30774C12.6797 8.30774 13.2308 8.85878 13.2308 9.53851Z" fill={active == "calendar" ? "white" : "#9197B3"} />
              <path d="M13.2308 14.4615C13.2308 15.1413 12.6797 15.6923 12 15.6923C11.3202 15.6923 10.7692 15.1413 10.7692 14.4615C10.7692 13.7818 11.3202 13.2308 12 13.2308C12.6797 13.2308 13.2308 13.7818 13.2308 14.4615Z" fill={active == "calendar" ? "white" : "#9197B3"} />
              <path d="M13.2308 19.3846C13.2308 20.0644 12.6797 20.6154 12 20.6154C11.3202 20.6154 10.7692 20.0644 10.7692 19.3846C10.7692 18.7049 11.3202 18.1538 12 18.1538C12.6797 18.1538 13.2308 18.7049 13.2308 19.3846Z" fill={active == "calendar" ? "white" : "#9197B3"} />
              <path d="M19.3846 9.53851C19.3846 10.2182 18.8336 10.7693 18.1539 10.7693C17.4741 10.7693 16.9231 10.2182 16.9231 9.53851C16.9231 8.85878 17.4741 8.30774 18.1539 8.30774C18.8336 8.30774 19.3846 8.85878 19.3846 9.53851Z" fill={active == "calendar" ? "white" : "#9197B3"} />
              <path d="M19.3846 14.4615C19.3846 15.1413 18.8336 15.6923 18.1539 15.6923C17.4741 15.6923 16.9231 15.1413 16.9231 14.4615C16.9231 13.7818 17.4741 13.2308 18.1539 13.2308C18.8336 13.2308 19.3846 13.7818 19.3846 14.4615Z" fill={active == "calendar" ? "white" : "#9197B3"} />
              <path d="M7.07689 19.3846C7.07689 20.0644 6.52585 20.6154 5.84613 20.6154C5.1664 20.6154 4.61536 20.0644 4.61536 19.3846C4.61536 18.7049 5.1664 18.1538 5.84613 18.1538C6.52585 18.1538 7.07689 18.7049 7.07689 19.3846Z" fill={active == "calendar" ? "white" : "#9197B3"} />
            </svg>
            <h3>Calendrier</h3>
          </div>
          <i className='bx bx-chevron-right bx-sm' />
        </Link>


        <Link to="/utilisateurs" className={active == "user" ? "navbar__container-item active" : "navbar__container-item"}>
          <div className='navbar__container-item-link'>
            <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20.368 24.544C19.312 24.856 18.064 25 16.6 25H9.39995C7.93595 25 6.68796 24.856 5.63196 24.544C5.89596 21.424 9.09995 18.964 13 18.964C16.9 18.964 20.104 21.424 20.368 24.544Z" stroke={active == "user" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M16.6 1H9.4C3.4 1 1 3.4 1 9.4V16.6C1 21.136 2.368 23.62 5.632 24.544C5.896 21.424 9.1 18.964 13 18.964C16.9 18.964 20.104 21.424 20.368 24.544C23.632 23.62 25 21.136 25 16.6V9.4C25 3.4 22.6 1 16.6 1ZM13 15.604C10.624 15.604 8.704 13.672 8.704 11.296C8.704 8.92002 10.624 7 13 7C15.376 7 17.296 8.92002 17.296 11.296C17.296 13.672 15.376 15.604 13 15.604Z" stroke={active == "user" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M17.296 11.296C17.296 13.672 15.376 15.604 13 15.604C10.624 15.604 8.70404 13.672 8.70404 11.296C8.70404 8.92002 10.624 7 13 7C15.376 7 17.296 8.92002 17.296 11.296Z" stroke={active == "user" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <h3>Utilisateurs</h3>
          </div>
          <i className='bx bx-chevron-right bx-sm' />
        </Link>

        <Link to="/pieces" className={active == "pieces" ? "navbar__container-item active" : "navbar__container-item"}>
          <div className='navbar__container-item-link'>
            <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20.368 24.544C19.312 24.856 18.064 25 16.6 25H9.39995C7.93595 25 6.68796 24.856 5.63196 24.544C5.89596 21.424 9.09995 18.964 13 18.964C16.9 18.964 20.104 21.424 20.368 24.544Z" stroke={active == "pieces" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M16.6 1H9.4C3.4 1 1 3.4 1 9.4V16.6C1 21.136 2.368 23.62 5.632 24.544C5.896 21.424 9.1 18.964 13 18.964C16.9 18.964 20.104 21.424 20.368 24.544C23.632 23.62 25 21.136 25 16.6V9.4C25 3.4 22.6 1 16.6 1ZM13 15.604C10.624 15.604 8.704 13.672 8.704 11.296C8.704 8.92002 10.624 7 13 7C15.376 7 17.296 8.92002 17.296 11.296C17.296 13.672 15.376 15.604 13 15.604Z" stroke={active == "pieces" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M17.296 11.296C17.296 13.672 15.376 15.604 13 15.604C10.624 15.604 8.70404 13.672 8.70404 11.296C8.70404 8.92002 10.624 7 13 7C15.376 7 17.296 8.92002 17.296 11.296Z" stroke={active == "pieces" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <h3>Pièces</h3>
          </div>
          <i className='bx bx-chevron-right bx-sm' />
        </Link>

        <Link to="/infrastructures" className={active == "infrastructures" ? "navbar__container-item active" : "navbar__container-item"}>
          <div className='navbar__container-item-link'>
            <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20.368 24.544C19.312 24.856 18.064 25 16.6 25H9.39995C7.93595 25 6.68796 24.856 5.63196 24.544C5.89596 21.424 9.09995 18.964 13 18.964C16.9 18.964 20.104 21.424 20.368 24.544Z" stroke={active == "infrastructures" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M16.6 1H9.4C3.4 1 1 3.4 1 9.4V16.6C1 21.136 2.368 23.62 5.632 24.544C5.896 21.424 9.1 18.964 13 18.964C16.9 18.964 20.104 21.424 20.368 24.544C23.632 23.62 25 21.136 25 16.6V9.4C25 3.4 22.6 1 16.6 1ZM13 15.604C10.624 15.604 8.704 13.672 8.704 11.296C8.704 8.92002 10.624 7 13 7C15.376 7 17.296 8.92002 17.296 11.296C17.296 13.672 15.376 15.604 13 15.604Z" stroke={active == "infrastructures" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M17.296 11.296C17.296 13.672 15.376 15.604 13 15.604C10.624 15.604 8.70404 13.672 8.70404 11.296C8.70404 8.92002 10.624 7 13 7C15.376 7 17.296 8.92002 17.296 11.296Z" stroke={active == "infrastructures" ? "white" : "#9197B3"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <h3>Infrastructures</h3>
          </div>
          <i className='bx bx-chevron-right bx-sm' />
        </Link>
      </div>

      
      <div className={showMenu ? "navbar__container show" : "navbar__container"}>
        <div className="navbar__container-list">
         
          
          
          
          
        </div>

        <div className="navbar__container-account">
          <div className="navbar__container-account_picture">
            <img src={userIcon} alt="Account" />
          </div>
          <div className="navbar__container-account_name">
            <p>
              Project Manager
            </p>
          </div>
          <button className="navbar__container-account_more" aria-label="Voir plus">
            <i className='bx bx-chevron-down bx-sm' />
          </button>
        </div>
        <Link to="/login" onClick={handleOut} className='navbar__container-logout'>
          <i className='bx bx-log-out'></i>
          <p>
            Se déconnecter
          </p>
        </Link>
      </div>
    </aside >
  )
}

export default Navbar