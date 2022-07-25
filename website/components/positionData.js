import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

import { position } from './positionData.module.css'


ChartJS.register(ArcElement, Tooltip, Legend);






export default function Position({props}){
    const white = '#FFF'
    const blue = '#8DB9FA'
    const red = '#ED7D73'
    const data = {
        
        datasets: [{
            data: props.wallet,
            borderColor:"black",
            backgroundColor: [        
                blue,
                white,
            ],
            labels:['wallet allocation', 'remaining allocation'],
        },
        {
            data: [],
            labels:[],
        },
        {
            data: props.yield,
            borderColor:"black",
            backgroundColor: [        
                red,
                white,
            ],
            labels:['yield target', 'remaining allocation'],
        }
    ]};
    
    const options = {
        responsive:true,
        maintainAspectRatio: false,
        borderWidth:0,
        spacing:2,
        borderRadius: 15,
    };
    

    return(
        <div className={position}>
            <Doughnut  options={options} data={data}/>
        </div>
    
    )
}