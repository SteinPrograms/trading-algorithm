export default async function handler(req, res) {
    // Get data submitted in request's body.
    const body = req.body
  
    const {MongoClient} = require('mongodb');
    const uri = "mongodb+srv://hugodemenez:Manonhugo147@test.yqzxd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority";
    const client = new MongoClient(uri);

    try {
        const buyPrice = parseFloat(body.buyPriceTarget.replace(',','.').replace(' ',''))
        const sellPrice = parseFloat(body.sellPriceTarget.replace(',','.').replace(' ',''))

        const yielding = sellPrice/buyPrice

        if (yielding < 1.0014){
            throw 'Yield is too low' 
        }

        await client.connect();

        const filter = {}

        const options = { upsert: true };

        const updateDoc = {
            $set: {
                symbol:body.symbol,
                buyPrice: buyPrice,
                sellPrice:sellPrice,
            },
        };




        
        await client.db("Trading").collection("Target").updateOne(filter, updateDoc, options);
        res.redirect(307, '../')
        

    } catch (e) {
        console.error(e);
    }
    finally {
        await client.close();
    }

  }