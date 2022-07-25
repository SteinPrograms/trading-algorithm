import Head from 'next/head'
import styles from '../styles/Home.module.css'
import useSWR from 'swr'
import Left from '../components/left'
import Right from '../components/right'
import Navbar from '../components/navbar'


var endpoint = String.toString(process.env.API_ENDPOINT)

export default function Home() {
  const fetcher = (...args) => fetch(...args).then((res) => res.json());

  function getServerData(){
    const { data, error } = useSWR(endpoint.concat('/getServerData'), fetcher);
    if (!data || error) return;
    return(data);
  }

  function getTargetData(){
    const { data, error } = useSWR(endpoint.concat('/getTargetData'), fetcher);
    if (!data || error) return {symbol:'ETH'};
    return(data);
  }

  function getPositionsData(){
    const { data, error } = useSWR(endpoint.concat('/getPositionsData'), fetcher);
    if (!data || error) return;
    return(data);
  }

  
  var target = getTargetData();
  var positions = getPositionsData();
  var server = getServerData();

  
  return (
      
      <div className={styles.container}>

      <Head>
        <title>Stein Programs</title>
        <meta name="description" content="Developed by Hugo DEMENEZ" />
        <link rel="icon" href="/favicon.ico" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
      </Head>

      <main className={styles.main}>
        <Navbar />
        <Left props={{target:target}}/>
        <Right props={{server:server,positions:positions,target:target}}/>

      </main>
      <style jsx global>{`
        body {
          margin: 0;
        }
      `}</style>
    </div>

  );
}




