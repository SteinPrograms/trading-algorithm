import styles from '../styles/Home.module.css'
import navbarStyle from './Navbar.module.css'


export default function Navbar() {
    return(
        <div className={styles.navbar}>
            <div>
            <h1 className={navbarStyle.logo}>Stein <b>Programs</b></h1>
            </div>
        </div>
    )
}
