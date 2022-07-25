import styles from '../styles/Home.module.css'
import rightStyle from './Right.module.css'
import Position from './positionData'
import OrderTable from './orderTable'
import Chart from './chart'

export default function Right({props}){

    function serverDataMapping(json_data){
        var result = "";
        for (var key in json_data) {
            if (json_data.hasOwnProperty(key)) {
                result += key +" : "+ json_data[key]+"\n"
            }
        }
        return result
    }
    if (props.server){
        var result = props.server.map(json_data => serverDataMapping(json_data))[0];
    }

    return(
        <div className={styles.right}>
            <h1 className={rightStyle.header}>Dashboard</h1>
            <div className={rightStyle.doughnut}>                
                <Position props={{
                    wallet:[props.positions?props.positions.length?props.positions[0].walletValue:0:0,
                        100000,
                        
                ],
                    yield:[
                        parseFloat(props.server?props.server.position_yield:0)>0?parseFloat(props.server?props.server.position_yield:0):0,
                        (parseFloat(props.server?props.server.expected_yield:0)-1)*100-parseFloat(props.server?props.server.position_yield:0)]}}
                        />
                
                        
            </div>
            <div className={rightStyle.orders}>
                <h2 className={rightStyle.orderTitle}>Orders</h2>
                
                <OrderTable props={{values:
                    props.positions
                    }}/>
            </div>
            <div className={rightStyle.chart}>
                <Chart props={{graphTitle:'ETH price',graphData:[1340,1240,1400,1349,1653,1309],graphLabels:['Mon','Tue','Wed','Thu','Fri','Sat']}}></Chart>
            </div>
            <div className={rightStyle.console}>
                {result?<p>{result}</p>:null}
            </div>
        </div>
    );
}
