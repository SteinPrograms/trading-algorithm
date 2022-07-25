export default async function handler(req, res) {
    // Get data submitted in request's body.
    const body = req.body
  
    const {MongoClient} = require('mongodb');
    const uri = "mongodb+srv://hugodemenez:Manonhugo147@test.yqzxd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority";
    const client = new MongoClient(uri);

    try {
        await client.connect();

        const filter = {}

        const options = { upsert: true };

        const updateDoc = {
            $set: body,
        };
        
        await client.db("Trading").collection("Server").updateOne(filter, updateDoc, options);
        res.redirect(307, '/')
    } catch (e) {
        console.error(e);
    }
    finally {
        await client.close();
    }

  }