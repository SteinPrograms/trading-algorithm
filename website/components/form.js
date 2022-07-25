import formStyle from './Form.module.css'
import Select from 'react-select'



export default function Form({props}){
    const options = [
        { value: 'BTC', label: 'Bitcoin' },
        { value: 'ETH', label: 'Ethereum' },
      ]
      var symbolIndex = 0;
      options.forEach(value =>  value.value == props.target.symbol?symbolIndex=options.indexOf(value):null);

    return(
        
        <form className={formStyle.form}  action='/api/publishForm' method='post'>
                <Select className={formStyle.symbolSelection} defaultValue={options[symbolIndex]} name ='symbol' options={options}/>
                
                <input required type='number' step="0.01" min='0' minLength="4" maxLength="8" className={formStyle.buyPriceTarget} name="buyPriceTarget"  placeholder={props.target?props.target.buyPrice:'loading'}/>
                <input required type='number' step="0.01" min='0' minLength="4" maxLength="8" className={formStyle.sellPriceTarget} name="sellPriceTarget"  placeholder={props.target?props.target.sellPrice:'loading'}/>
                <button className={formStyle.updateButton}>UPDATE</button>
            </form>
    )
}