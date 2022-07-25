import {tableWrapper,tableScroll,text} from './orderTable.module.css'

export default function OrderTable({props}){
        return (
            <div className={tableWrapper}>
            <div className={tableScroll}>
                <table>
                    <thead>
                    <tr>
                        <th><span className={text}>Symbol</span></th>
                        <th><span className={text}>Amount</span></th>
                        <th><span className={text}>Total</span></th>
                    </tr>
                    </thead>
                    <tbody>
                    
                    {props.values?props.values.map(value=>
                        <tr key={value.position_id}>
                        <td >{value.symbol}</td>
                        <td >{value.yield}</td>
                        <td >{value.wallet_value}</td>
                    </tr>):null}
                    </tbody>
                    </table>
            </div>
            </div>
        )
}