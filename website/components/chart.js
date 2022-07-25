import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';


ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);



export default function Chart({props}) {
  const options = {
    maintainAspectRatio: false,
    responsive: true,
  
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: props.graphTitle,
      },
    },
  };
  
  const labels = props.graphLabels;
  
  
  const data = {
    labels,
    datasets: [
      {
        label: 'Dataset 1',
        data: props.graphData,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      }
    ],
  };

  return <Line options={options} data={data} />;
}
