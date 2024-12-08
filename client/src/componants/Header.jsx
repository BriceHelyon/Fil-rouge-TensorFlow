import menu from '../assets/img/menu.png';

function Header({ showMenu, handleShowMenu }) {
  return (
    <header>
      <div className="menu">
        <div className={showMenu ? "menu__icon" : "menu__icon show"} onClick={handleShowMenu}>
          <img src={menu} alt="menu icon" />
        </div>
      </div>
      <div className='account'>
        <h1>
          Hey Charlotte 👋🏿👋👋🏾👋🏼
        </h1>
      </div>
    </header>
  )
}

export default Header