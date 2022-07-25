import styles from '../styles/Home.module.css'
import Form from './form'
import leftStyles from './Left.module.css'
export default function Left({props}){
    return(
        <div className={styles.left}>
                
                <Form className={leftStyles.form} props={props}>
                    
                </Form>

        </div>
    );
}

