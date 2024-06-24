/* 
This code defines a router responsible for handling POST requests to retrieve 
login data and save it as access requests.
 It imports the necessary modules, including the accessRequestModel, 
 which is used to interact with the database.
*/
const express = require("express");
const router = express.Router();
const accessRequestModel = require("../models/accessRequestModel");

// POST: Retrieve login's Data
router.post("/", async (req, res) => {
  try {
    const { firstname, lastname, emailaddress, subteam } = req.body;

    // Create row (data) from fetched data and save into accessRequest table
    const accessRequest = await accessRequestModel.create({
      firstname: firstname,
      lastname: lastname,
      emailaddress: emailaddress,
      subteam: subteam,
    });

    return res.status(200).json(accessRequest);
  } catch (error) {
    console.error(error.message);
    return res.status(500).json({ error: error.message });
  }
});

module.exports = router;
